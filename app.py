from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'
RENDER_MIXER_URL = "https://sultan-mixer.onrender.com/mix"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sultan Pro | Final Masterpiece</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; margin: 0; padding: 0; color: white; text-align: center; background: #0f0c29; overflow-x: hidden; min-height: 100vh; display: flex; flex-direction: column; align-items: center; }
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 3px #ff77a9; animation: drift 6s infinite alternate; }
        @keyframes drift { 0% { transform: translate(0,0); opacity: 0.3; } 100% { transform: translate(50px,-80px); opacity: 1; } }
        .main-card { max-width: 460px; width: 92%; padding: 35px 25px; border-radius: 25px; background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7); margin: 30px 0; z-index: 10; }
        h1 { margin: 0; font-size: 32px; color: #ff77a9; }
        .input-wrapper { position: relative; width: 100%; margin: 20px 0; }
        .input-wrapper input { width: 100%; padding: 16px 85px 16px 15px; border: none; border-radius: 12px; font-size: 15px; background: white; color: #000; outline: none; }
        .paste-btn { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: #ff77a9; color: white; border: none; border-radius: 8px; padding: 8px 12px; font-weight: bold; cursor: pointer; }
        button#mainBtn { background: linear-gradient(90deg, #ff416c, #ff4b2b); color: white; border: none; padding: 16px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 600; box-shadow: 0 8px 20px rgba(255, 65, 108, 0.4); }
        #fullLoader { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 9999; display: none; flex-direction: column; justify-content: center; align-items: center; }
        .spinner { border: 5px solid rgba(255,255,255,0.1); border-top: 5px solid #ff77a9; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        #result { margin-top: 25px; display: none; width: 100%; }
        video, img { width: 100%; border-radius: 15px; margin-bottom: 15px; }
        .dl-group { display: flex; flex-direction: column; gap: 10px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 14px; color: white; border-radius: 10px; font-weight: 600; font-size: 15px; }
        .btn-mp4 { background: #28a745; }
        .btn-mp3 { background: #007bff; }
        .btn-mix { background: linear-gradient(90deg, #8E2DE2, #4A00E0); }
    </style>
</head>
<body>

<div id="fullLoader">
    <div class="spinner"></div>
    <div style="margin-top:15px; font-weight:bold; color:#ff77a9;">🚀 Sultan's Engine is Working...</div>
</div>

<div class="main-card">
    <h1>Sultan Pro</h1>
    <p style="color:#aaa; font-size:14px;">Photo + Music Downloader (Final Version)</p>
    
    <div class="input-wrapper">
        <input type="text" id="videoUrl" placeholder="Paste Instagram Link...">
        <button class="paste-btn" onclick="pasteFromClipboard()">Paste</button>
    </div>

    <button id="mainBtn" onclick="startProcess()">Unlock Magic</button>
    
    <div id="result">
        <img id="imgPlayer" style="display:none;" />
        <video id="vidPlayer" controls style="display:none;"></video>
        <audio id="audioPlayer" controls style="display:none; width:100%; margin-bottom:10px;"></audio>
        
        <div class="dl-group">
            <a id="downloadBtn" class="dl-btn btn-mp4" href="#" target="_blank">📥 Save HD File</a>
            <button id="mixBtn" class="dl-btn btn-mix" style="display: none;" onclick="startMixing()">✨ Download Photo + Music (MP4 Video)</button>
            <a id="audioBtn" class="dl-btn btn-mp3" href="#" target="_blank" style="display: none;">🎵 Save Audio (MP3)</a>
        </div>
    </div>
</div>

<script>
    // Magical Fireflies
    for(let i=0; i<25; i++){
        let f = document.createElement('div'); f.className = 'firefly';
        f.style.left = Math.random() * 100 + 'vw'; f.style.top = Math.random() * 100 + 'vh';
        f.style.width = f.style.height = (Math.random()*3+2)+'px';
        document.body.appendChild(f);
    }

    let globalImgUrl = ""; let globalAudioUrl = "";

    async function pasteFromClipboard() {
        const text = await navigator.clipboard.readText();
        document.getElementById("videoUrl").value = text;
    }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return alert("Paste Link First!");
        
        document.getElementById("fullLoader").style.display = "flex";
        document.getElementById("result").style.display = "none";
        
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
                if(data.media_type === "image") {
                    document.getElementById("imgPlayer").src = data.media_url;
                    document.getElementById("imgPlayer").style.display = "block";
                    document.getElementById("vidPlayer").style.display = "none";
                    globalImgUrl = data.media_url;
                } else {
                    document.getElementById("vidPlayer").src = data.media_url;
                    document.getElementById("vidPlayer").style.display = "block";
                    document.getElementById("imgPlayer").style.display = "none";
                }
                
                document.getElementById("downloadBtn").href = data.media_url;

                if(data.audio_url) {
                    globalAudioUrl = data.audio_url;
                    document.getElementById("audioPlayer").src = data.audio_url;
                    document.getElementById("audioPlayer").style.display = "block";
                    document.getElementById("audioBtn").href = data.audio_url;
                    document.getElementById("audioBtn").style.display = "flex";
                    if(data.media_type === "image") document.getElementById("mixBtn").style.display = "flex";
                }
                document.getElementById("result").style.display = "block";
            } else {
                alert("Error: " + data.message);
            }
        });
    }

    function startMixing() {
        document.getElementById("fullLoader").style.display = "flex";
        document.getElementById("fullLoader").querySelector("div:last-child").innerText = "⏳ Factory is Mixing... Wait 15s";
        
        fetch("{{ mixer_url }}", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_url: globalImgUrl, audio_url: globalAudioUrl })
        })
        .then(res => res.blob())
        .then(blob => {
            document.getElementById("fullLoader").style.display = "none";
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a'); a.href = url; a.download = 'Sultan_Mixed_Post.mp4';
            a.click();
        })
        .catch(() => {
            document.getElementById("fullLoader").style.display = "none";
            alert("Mixing Factory is waking up. Try again in 20 seconds!");
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
    # Deep Audio Scanner Engine
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com"}
    
    try:
        # Puraani API ko aggressive mode mein run karna
        res = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", 
                            json={"url": url}, headers=headers).json()
        
        media_url = None; audio_url = None; media_type = "video"
        
        # AGGRESSIVE SCANNER: Chhupe huye music ko dhoondhna
        if 'medias' in res:
            for m in res['medias']:
                if m.get('type') == 'audio' or 'mp3' in str(m.get('url')):
                    audio_url = m.get('url')
                if m.get('type') == 'video':
                    media_url = m.get('url'); media_type = "video"
                if m.get('type') == 'image' and not media_url:
                    media_url = m.get('url'); media_type = "image"
        
        if not audio_url:
            # Check music/audio keys directly
            audio_url = res.get('audio') or res.get('music_url') or res.get('music')

        if not media_url:
            media_url = res.get('url') or res.get('image')

        if media_url:
            return jsonify({"success": True, "media_url": media_url, "media_type": media_type, "audio_url": audio_url})
        return jsonify({"success": False, "message": "API couldn't find the media."})
    except:
        return jsonify({"success": False, "message": "Server Timeout."})

if __name__ == '__main__':
    app.run()

