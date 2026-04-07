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
    <title>Sultan Pro | Premium Downloader</title>
    <style>
        /* GLASSMORPHISM & ANIMATED BACKGROUND */
        body { 
            font-family: 'Segoe UI', sans-serif; 
            margin: 0; padding: 20px; color: white; text-align: center;
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            min-height: 100vh;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .promo-banner { background: rgba(255, 65, 108, 0.8); padding: 12px; border-radius: 10px; margin-bottom: 25px; font-weight: bold; text-decoration: none; color: white; display: block; backdrop-filter: blur(5px); box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4); transition: 0.3s;}
        .promo-banner:hover { transform: translateY(-3px); }
        
        /* PREMIUM GLASS BOX */
        .glass-container { 
            max-width: 500px; margin: auto; padding: 40px 30px; border-radius: 20px; 
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        h1 { margin-top:0; font-size: 32px; background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        p.subtitle { color: #ccc; font-size: 15px; margin-bottom: 25px;}
        
        input[type="text"] { width: 85%; padding: 16px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 16px; background: rgba(0,0,0,0.2); color: white; outline: none; transition: 0.3s; }
        input[type="text"]:focus { border-color: #00d2ff; box-shadow: 0 0 10px rgba(0, 210, 255, 0.5); }
        
        button { background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: white; border: none; padding: 16px 20px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: bold; transition: 0.3s; box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3); }
        button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 210, 255, 0.5); }
        
        .limit-text { margin-top: 15px; font-size: 14px; color: #00d2ff; font-weight: bold; }
        
        /* THE 10-SECOND SMART AD BOX */
        .smart-ad-box { display: none; background: rgba(0,0,0,0.6); padding: 25px; border-radius: 15px; margin-top: 20px; border: 1px solid #ffcc00; }
        .timer-text { font-size: 24px; font-weight: bold; color: #ffcc00; margin-bottom: 15px; }
        .game-ad { display: block; background: #ff416c; color: white; padding: 15px; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 18px; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
        
        #loading { display: none; margin-top: 20px; font-size: 16px; color: #00d2ff; }
        #result { margin-top: 25px; display: none; }
        video { width: 100%; border-radius: 12px; border: 2px solid rgba(255,255,255,0.1); margin-bottom: 15px; }
        .dl-btn { background: #28a745; text-decoration: none; display: block; padding: 15px; color: white; border-radius: 10px; font-weight: bold; font-size: 18px; transition: 0.3s; }
        .dl-btn:hover { background: #218838; }
    </style>
</head>
<body>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">
    ✨ Join @CineTrixaHub For Free HD Movies & Web Series! 🍿
</a>

<div class="glass-container">
    <h1>Sultan Pro</h1>
    <p class="subtitle">Insta, YouTube, FB & Twitter Video Downloader</p>
    
    <input type="text" id="videoUrl" placeholder="Paste video link here...">
    <button id="mainBtn" onclick="startProcess()">Download Now</button>
    
    <div id="limitMsg" class="limit-text">✅ 3 Free instant downloads left today.</div>

    <div class="smart-ad-box" id="smartAd">
        <div class="timer-text">Wait <span id="timerCount">10</span>s to Unlock</div>
        <p style="font-size: 13px; color: #aaa;">Support us by checking out our sponsor below:</p>
        <a href="{{ game_link }}" target="_blank" class="game-ad">🎮 Play Game & Win ₹500 Cash!</a>
        <br><br>
        <button id="unlockBtn" style="display: none; background: #ffcc00; color: black;" onclick="fetchVideoAPI()">🔓 Continue to Video</button>
    </div>

    <div id="loading">⏳ Fetching video from secure servers...</div>

    <div id="result">
        <video id="vidPlayer" controls></video>
        <a id="downloadBtn" class="dl-btn" href="#" target="_blank">📥 Save to Gallery</a>
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
            document.getElementById('limitMsg').innerText = "✅ " + left + " Free instant downloads left today.";
        } else {
            document.getElementById('limitMsg').innerText = "⚡ Instant limit reached. Short ad required.";
        }
    }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) { alert("Please paste a link first!"); return; }
        
        document.getElementById("result").style.display = "none";
        pendingUrl = url;

        if(count >= 3) {
            // Show 10-Second Ad logic
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
            // Direct download for first 3
            document.getElementById("mainBtn").style.display = "none";
            document.getElementById("loading").style.display = "block";
            fetchVideoAPI();
        }
    }

    function fetchVideoAPI() {
        document.getElementById("smartAd").style.display = "none";
        document.getElementById("loading").style.display = "block";
        document.getElementById("unlockBtn").style.display = "none"; // Hide if it was used

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
                if(count >= 3) { document.getElementById("limitMsg").style.display = "block"; } // Re-show text

                document.getElementById("vidPlayer").src = data.video_url;
                document.getElementById("downloadBtn").href = data.video_url;
                document.getElementById("result").style.display = "block";
            } else {
                alert("❌ Error: " + data.message);
            }
        })
        .catch(err => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            alert("⚠️ Server Timeout! Please try again.");
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
        
        if 'medias' in response and isinstance(response['medias'], list) and len(response['medias']) > 0:
            video_url = response['medias'][0].get('url')
        elif 'url' in response:
            video_url = response['url']
        elif 'video' in response:
            video_url = response['video']
        elif 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0:
            video_url = response['data'][0].get('url')

        if video_url:
            return jsonify({"success": True, "video_url": video_url})
        else:
            return jsonify({"success": False, "message": "Video link not found or account is private."})
    except Exception as e:
        return jsonify({"success": False, "message": "Server Error. Please try again."})

if __name__ == '__main__':
    app.run()
