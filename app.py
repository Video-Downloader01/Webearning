from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# --- AAPKI SECURE KEYS ---
RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sultan Pro | Serene Video Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        /* LIVE VIDEO BACKGROUND & RESET */
        * { box-sizing: border-box; }
        body { 
            font-family: 'Poppins', sans-serif; 
            margin: 0; padding: 0; 
            color: white; text-align: center;
            overflow-x: hidden;
            min-height: 100vh;
            display: flex; flex-direction: column; align-items: center; justify-content: start;
        }

        /* Video Background Container */
        .video-background {
            position: fixed; right: 0; bottom: 0;
            min-width: 100%; min-height: 100%;
            z-width: -100;
        }
        
        /* Dark Overlay over video for text readability */
        .overlay {
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.4); /* subtle dark overlay */
            z-index: -99;
        }

        /* Top Header Banner */
        .promo-banner { 
            background: rgba(255, 255, 255, 0.1); 
            padding: 10px 20px; border-radius: 50px; margin-top: 20px; margin-bottom: 20px; 
            font-weight: 600; text-decoration: none; color: #fff; 
            font-size: 14px;
            display: inline-block; backdrop-filter: blur(5px); 
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: 0.3s;
            z-index: 10;
        }
        .promo-banner:hover { transform: scale(1.03); background: rgba(255, 255, 255, 0.2); }
        
        /* ULTRA SLIM CLEAN CARD */
        .main-card { 
            max-width: 440px; width: 90%; padding: 40px 25px; 
            border-radius: 25px; background: rgba(0, 0, 0, 0.75); 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7);
            margin-bottom: 30px;
            position: relative; z-index: 10;
        }

        h1 { margin: 0; font-size: 32px; font-weight: 700; color: #ffffff; text-shadow: 0 2px 10px rgba(0, 205, 172, 0.5); }
        p.subtitle { color: #ccc; font-size: 14px; margin-bottom: 30px; font-weight: 400; }
        
        input[type="text"] { 
            width: 100%; padding: 16px; margin-bottom: 20px; 
            border: none; border-radius: 12px; font-size: 16px; 
            background: rgba(255, 255, 255, 1); color: #000; 
            outline: none; transition: 0.3s;
            font-family: inherit;
        }
        input[type="text"]:focus { box-shadow: 0 0 15px #02aab0; }
        
        button#mainBtn { 
            background: linear-gradient(90deg, #02aab0, #00cdac); 
            color: white; border: none; padding: 16px; font-size: 18px; 
            border-radius: 12px; cursor: pointer; width: 100%; font-weight: 600; 
            transition: 0.3s; font-family: inherit;
        }
        button#mainBtn:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(2, 170, 176, 0.6); }
        
        .limit-text { margin-top: 20px; font-size: 13px; color: #ffcc00; font-weight: 600; }
        
        /* 10-SECOND SMART AD (NEW DESIGN) */
        .smart-ad-box { 
            display: none; background: rgba(0,0,0,0.8); padding: 25px; 
            border-radius: 20px; margin-top: 25px; border: 2px dashed #ffcc00; 
        }
        .timer-text { font-size: 26px; font-weight: 700; color: #ffcc00; margin-bottom: 15px; }
        .game-ad { 
            display: block; background: linear-gradient(90deg, #ff416c, #ff4b2b); color: white; padding: 15px; 
            border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 18px; 
            margin-top: 15px; animation: pulse 1.5s infinite; transition: 0.3s;
        }
        .game-ad:hover { transform: scale(1.03); }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
        
        #loading { display: none; margin-top: 25px; font-size: 16px; color: #00ffcc; font-weight: 600; }
        #result { margin-top: 30px; display: none; text-align: left; }
        video { width: 100%; border-radius: 15px; border: 2px solid rgba(255,255,255,0.1); margin-bottom: 15px; background: #000; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        
        /* Caption Box */
        .caption-box { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 20px; font-size: 13px; color: #eee; border-left: 3px solid #00ffcc; max-height: 100px; overflow-y: auto;}

        /* DOWNLOAD BUTTONS GROUP */
        .dl-group { display: flex; flex-direction: column; gap: 10px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 15px; color: white; border-radius: 10px; font-weight: 600; font-size: 16px; transition: 0.3s;}
        .dl-btn:hover { transform: scale(1.02); }
        
        /* NEW STEP: MP3 BUTTON DESIGN */
        .btn-mp4 { background: #28a745; }
        .btn-mp3 { background: #007bff; }
        
        /* SHAYARI CORNER (Minimal) */
        .shayari-corner { 
            margin-top: 35px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); color: #fff; font-style: italic; font-size: 14px;
        }
        .shayari-corner h3 { margin: 0 0 12px 0; font-size: 16px; color: #00ffcc; font-weight: 600; }
        .ig-link { color: #ff416c; font-weight: bold; text-decoration: none; }
    </style>
</head>
<body>

<div class="overlay"></div>
<video autoplay loop muted playsinline class="video-background">
  <source src="https://assets.mixkit.co/videos/preview/mixkit-forest-stream-in-the-sunlight-529-large.mp4" type="video/mp4">
</video>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">
    ✨ Join Telegram For Movies: @CineTrixaHub🍿
</a>

<div class="main-card">
    <h1>Sultan Pro</h1>
    <p class="subtitle">Social Video & Audio Downloader</p>
    
    <input type="text" id="videoUrl" placeholder="Paste link (Insta, YT Shorts, FB, Twitter)...">
    <button id="mainBtn" onclick="startProcess()">Process Link</button>
    
    <div id="limitMsg" class="limit-text">🎁 3 Free downloads left today.</div>

    <div class="smart-ad-box" id="smartAd">
        <div class="timer-text">🔓 Unlocking in <span id="timerCount">10</span>s</div>
        <p style="font-size: 13px; color: #ccc;">Support us by checking out our sponsor below:</p>
        <a href="{{ game_link }}" target="_blank" class="game-ad">🎮 Play & Win ₹500 Cash!</a>
        <br>
        <button id="unlockBtn" style="display: none; background: #00ffcc; color: black; padding: 12px; border-radius:8px; border:none; font-weight:600; cursor:pointer;" onclick="fetchVideoAPI()">🚀 Continue Download</button>
    </div>

    <div id="loading">🌊 Searching video on high-speed servers...</div>

    <div id="result">
        <div id="vidTitle" class="caption-box"></div>
        <video id="vidPlayer" controls></video>
        
        <div class="dl-group">
            <a id="downloadBtn" class="dl-btn btn-mp4" href="#" target="_blank">📥 Save Video (MP4 HD)</a>
            <a id="audioBtn" class="dl-btn btn-mp3" href="#" target="_blank" style="display: none;">🎵 Save Audio (MP3)</a>
        </div>
    </div>

    <div class="shayari-corner">
        <h3>✨ Sultan's Creative Corner</h3>
        <p>"Rakh hausla wo manzar bhi aayega, pyaase ke paas chalkar samundar bhi aayega..."</p>
        <p style="font-size: 11px; margin-top: 15px;">Follow for amazing Shayari:<br><a href="https://instagram.com/innocent._.foji._.shayar" target="_blank" class="ig-link">@innocent._.foji._.shayar</a></p>
    </div>
</div>

<script>
    let today = new Date().toDateString();
    if(localStorage.getItem('dl_date') !== today) {
        localStorage.setItem('dl_count', 0);
        localStorage.setItem('dl_date', today);
    }
    
    let count = parseInt(localStorage.getItem('dl_count')) || 0;
    let pendingUrl = "";
    updateLimitText();

    function updateLimitText() {
        let left = 3 - count;
        if(left > 0) {
            document.getElementById('limitMsg').innerText = "🎁 " + left + " Free instant downloads left today.";
        } else {
            document.getElementById('limitMsg').innerHTML = "⚡ <span style='color:#ff416c'>Limit reached! Short ad required.</span>";
        }
    }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) { alert("Please paste a link first!"); return; }
        
        document.getElementById("result").style.display = "none";
        document.getElementById("vidTitle").style.display = "none";
        document.getElementById("audioBtn").style.display = "none"; // Hide MP3 initially
        pendingUrl = url;

        if(count >= 3) {
            document.getElementById("mainBtn").style.display = "none";
            document.getElementById("limitMsg").style.display = "none";
            document.getElementById("smartAd").style.display = "block";
            
            let timeLeft = 10;
            document.getElementById("timerCount").innerText = timeLeft;
            let timer = setInterval(function() {
                timeLeft--;
                document.getElementById("timerCount").innerText = timeLeft;
                if(timeLeft <= 0) {
                    clearInterval(timer);
                    document.getElementById("timerCount").parentNode.innerHTML = "Unlocked!";
                    document.getElementById("unlockBtn").style.display = "block";
                }
            }, 1000);
        } else {
            document.getElementById("mainBtn").style.display = "none";
            document.getElementById("loading").style.display = "block";
            fetchVideoAPI();
        }
    }

    function fetchVideoAPI() {
        document.getElementById("smartAd").style.display = "none";
        document.getElementById("loading").style.display = "block";
        document.getElementById("unlockBtn").style.display = "none";

        fetch("/api/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: pendingUrl })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            if(data.success) {
                count++;
                localStorage.setItem('dl_count', count);
                updateLimitText();
                if(count >= 3) { document.getElementById("limitMsg").style.display = "block"; }

                if(data.title) {
                    document.getElementById("vidTitle").innerText = data.title;
                    document.getElementById("vidTitle").style.display = "block";
                }

                document.getElementById("vidPlayer").src = data.video_url;
                document.getElementById("downloadBtn").href = data.video_url;
                
                // NEW STEP: Handle MP3 if available from API
                if(data.audio_url) {
                    document.getElementById("audioBtn").href = data.audio_url;
                    document.getElementById("audioBtn").style.display = "flex";
                } else {
                    document.getElementById("audioBtn").style.display = "none";
                }

                document.getElementById("result").style.display = "block";
            } else {
                alert("❌ Error: " + data.message);
            }
        })
        .catch(err => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            alert("⚠️ Something went wrong. Video might be too large.");
        });
    }
</script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template_string(HTML_PAGE, game_link=GAME_LINK)

@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.json
    raw_url = data.get('url', '')

    # Smart Link Cleaner
    clean_url = raw_url
    if "instagram.com" in raw_url or "twitter.com" in raw_url or "x.com" in raw_url:
        clean_url = raw_url.split('?')[0]

    api_url = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com"
    }

    try:
        response = requests.post(api_url, json={"url": clean_url}, headers=headers).json()
        video_url = None
        audio_url = None # NEW STEP: Audio URL
        video_title = None
        
        if 'title' in response:
            video_title = response['title']

        # Handling different API response structures for Video and Audio
        medias = response.get('medias', [])
        if medias and isinstance(medias, list):
            # Check for Video
            video_media = next((m for m in medias if m.get('type') == 'video' or (not m.get('type') and 'mp4' in m.get('url',''))), None)
            if video_media:
                video_url = video_media.get('url')
            
            # Check for Audio (New Step)
            audio_media = next((m for m in medias if m.get('type') == 'audio' or 'mp3' in m.get('url','')), None)
            if audio_media:
                audio_url = audio_media.get('url')
        
        # Fallback to general URL if video not found in medias
        if not video_url:
            if 'url' in response: video_url = response['url']
            elif 'video' in response: video_url = response['video']
            elif 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0: video_url = response['data'][0].get('url')

        if video_url:
            # Send both video and audio back to frontend
            return jsonify({"success": True, "video_url": video_url, "audio_url": audio_url, "title": video_title})
        else:
            return jsonify({"success": False, "message": "Video/Audio not found. Link might be private or invalid."})
    except Exception as e:
        return jsonify({"success": False, "message": "Server Timeout. Please try again."})

if __name__ == '__main__':
    app.run()

