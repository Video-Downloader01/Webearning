from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# --- CONFIGURATION ---
RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'
RENDER_MIXER_URL = "https://sultan-mixer.onrender.com/mix"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sultan Pro | All-in-One Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; margin: 0; padding: 0; color: white; text-align: center; background: #0b0e14; min-height: 100vh; display: flex; flex-direction: column; align-items: center; }
        .main-card { max-width: 450px; width: 92%; padding: 30px 20px; border-radius: 20px; background: #1a1f26; border: 1px solid #333; margin: 40px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.5); position: relative; z-index: 5; }
        h1 { color: #ff77a9; margin: 0; font-size: 28px; }
        .input-box { width: 100%; padding: 15px; border-radius: 10px; border: none; margin: 20px 0; background: #fff; color: #000; font-size: 15px; outline: none; }
        button#mainBtn { background: #ff416c; color: white; border: none; padding: 15px; border-radius: 10px; width: 100%; font-weight: bold; cursor: pointer; font-size: 16px; }
        #fullLoader { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 9999; display: none; flex-direction: column; justify-content: center; align-items: center; }
        .spinner { border: 4px solid #333; border-top: 4px solid #ff77a9; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        #result { display: none; margin-top: 25px; width: 100%; text-align: left; }
        img, video { width: 100%; border-radius: 12px; margin-bottom: 15px; border: 1px solid #444; }
        .dl-group { display: flex; flex-direction: column; gap: 10px; }
        .btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 12px; border-radius: 8px; font-weight: bold; color: white; font-size: 14px; cursor: pointer; }
        .btn-green { background: #28a745; }
        .btn-blue { background: #007bff; }
        .btn-purple { background: #6f42c1; }
    </style>
</head>
<body>

<div id="fullLoader">
    <div class="spinner"></div>
    <p id="loaderText" style="color: #ff77a9; margin-top: 15px; font-weight: bold;">🔍 Analyzing Link...</p>
</div>

<div class="main-card">
    <h1>Sultan Pro</h1>
    <p style="font-size: 12px; color: #aaa;">Instagram Photo + Music Fixed Engine</p>
    
    <input type="text" id="videoUrl" class="input-box" placeholder="Paste Instagram Link Here...">
    <button id="mainBtn" onclick="startProcess()">Unlock Media</button>
    
    <div id="result">
        <div id="mediaContainer"></div>
        <div class="dl-group">
            <a id="saveMedia" class="btn btn-green" href="#" target="_blank">📥 Save HD File</a>
            <button id="mixBtn" class="btn btn-purple" style="display:none;" onclick="startMixing()">✨ Save Photo + Music (MP4 Video)</button>
            <a id="saveAudio" class="btn btn-blue" style="display:none;" href="#" target="_blank">🎵 Save Only Music (MP3)</a>
        </div>
    </div>
</div>

<script>
    let globalImg = ""; let globalAudio = "";

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return alert("Please paste a link!");
        
        document.getElementById("fullLoader").style.display = "flex";
        document.getElementById("result").style.display = "none";
        document.getElementById("mixBtn").style.display = "none";
        document.getElementById("saveAudio").style.display = "none";

        fetch("/api/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("fullLoader").style.display = "none";
            if(data.success) {
                confetti();
                let container = document.getElementById("mediaContainer");
                container.innerHTML = "";
                
                if(data.media_type === "image") {
                    let img = document.createElement("img"); img.src = data.media_url;
                    container.appendChild(img);
                    globalImg = data.media_url;
                    document.getElementById("saveMedia").innerText = "📥 Save Image (HD)";
                } else {
                    let vid = document.createElement("video"); vid.src = data.media_url; vid.controls = true;
                    container.appendChild(vid);
                    document.getElementById("saveMedia").innerText = "📥 Save Video (MP4)";
                }
                
                document.getElementById("saveMedia").href = data.media_url;

                if(data.audio_url) {
                    globalAudio = data.audio_url;
                    document.getElementById("saveAudio").href = data.audio_url;
                    document.getElementById("saveAudio").style.display = "flex";
                    if(data.media_type === "image") {
                        document.getElementById("mixBtn").style.display = "flex";
                    }
                }
                document.getElementById("result").style.display = "block";
            } else {
                alert("API Error: " + data.message);
            }
        })
        .catch(e => {
            document.getElementById("fullLoader").style.display = "none";
            alert("Connection error!");
        });
    }

    function startMixing() {
        document.getElementById("fullLoader").style.display = "flex";
        document.getElementById("loaderText").innerText = "⏳ Mixing Photo & Music (15s)...";
        
        fetch("{{ mixer_url }}", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_url: globalImg, audio_url: globalAudio })
        })
        .then(res => res.blob())
        .then(blob => {
            document.getElementById("fullLoader").style.display = "none";
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a'); a.href = url; a.download = 'Sultan_Mixed_Post.mp4';
            document.body.appendChild(a); a.click();
            showToast("✅ Download Started!");
        })
        .catch(() => {
            document.getElementById("fullLoader").style.display = "none";
            alert("Mixing failed. Try again in 30 seconds.");
        });
    }
</script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template_string(HTML_PAGE, mixer_url=RENDER_MIXER_URL)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    
    # 1. PEHLE NAYI ADVANCED API TRY KAREIN (Specifically for IG Photo Music)
    try:
        shortcode_match = re.search(r'instagram\.com/(?:p|reel|tv)/([^/?#&]+)', url)
        if shortcode_match:
            shortcode = shortcode_match.group(1)
            adv_url = f"https://instagram-scraper-api-advanced.p.rapidapi.com/api/download/reel/{shortcode}"
            headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "instagram-scraper-api-advanced.p.rapidapi.com"}
            res_adv = requests.get(adv_url, headers=headers, timeout=10).json()
            
            # AGGRESSIVE DATA MINING
            data = res_adv.get('data', {})
            media_url = data.get('video_url') or data.get('thumbnail_url')
            audio_url = data.get('audio_url') or (data.get('music_info', {}).get('music_url') if data.get('music_info') else None)
            media_type = "video" if data.get('video_url') else "image"
            
            if media_url:
                return jsonify({"success": True, "media_url": media_url, "audio_url": audio_url, "media_type": media_type})
    except:
        pass # Agar ye fail hui toh engine 2 kaam karega

    # 2. FALLBACK: PURANI API (Deep Scanning Mode)
    try:
        headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com"}
        res = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", 
                            json={"url": url}, headers=headers, timeout=10).json()
        
        media_url = None; audio_url = None; media_type = "image"
        
        # Deep Search in medias array
        medias = res.get('medias', [])
        for m in medias:
            if m.get('type') == 'video': 
                media_url = m.get('url'); media_type = "video"
            if (m.get('type') == 'image' or m.get('type') == 'photo') and not media_url: 
                media_url = m.get('url'); media_type = "image"
            if m.get('type') == 'audio' or 'mp3' in str(m.get('url')): 
                audio_url = m.get('url')
        
        # Last attempt for hidden links
        if not media_url: media_url = res.get('url') or res.get('thumbnail')
        if not audio_url: audio_url = res.get('music') or res.get('audio')

        if media_url:
            return jsonify({"success": True, "media_url": media_url, "audio_url": audio_url, "media_type": media_type})
        
        return jsonify({"success": False, "message": "Could not find media link."})
    except Exception as e:
        return jsonify({"success": False, "message": "Server error. Try again later."})

if __name__ == '__main__':
    app.run()

