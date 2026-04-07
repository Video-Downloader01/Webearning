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
    <title>Sultan Pro | Water Theme Downloader</title>
    <style>
        /* DEEP OCEAN WATER BACKGROUND */
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 20px; color: white; text-align: center;
            background: linear-gradient(-45deg, #000428, #004e92, #02aab0, #00cdac);
            background-size: 400% 400%;
            animation: waterWave 12s ease infinite;
            min-height: 100vh;
        }
        @keyframes waterWave {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .promo-banner { 
            background: rgba(0, 0, 0, 0.4); 
            padding: 12px 20px; border-radius: 30px; margin-bottom: 25px; 
            font-weight: bold; text-decoration: none; color: #00ffcc; 
            display: inline-block; border: 1px solid #00ffcc;
            transition: 0.3s;
        }
        .promo-banner:hover { background: #00ffcc; color: black; }
        
        /* CLEAN DARK WATER CARD */
        .main-card { 
            max-width: 480px; width: 90%; margin: auto; padding: 35px 25px; 
            border-radius: 20px; background: rgba(0, 0, 0, 0.6); 
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            border-top: 2px solid rgba(255, 255, 255, 0.2);
        }

        h1 { margin: 0; font-size: 32px; color: #ffffff; text-shadow: 0 2px 10px rgba(0, 205, 172, 0.8); }
        p.subtitle { color: #b3e5fc; font-size: 14px; margin-bottom: 25px; }
        
        input[type="text"] { 
            width: 88%; padding: 15px; margin-bottom: 20px; 
            border: none; border-radius: 10px; font-size: 16px; 
            background: rgba(255, 255, 255, 0.9); color: #000; 
            outline: none; transition: 0.3s;
        }
        input[type="text"]:focus { box-shadow: 0 0 15px #02aab0; }
        
        button { 
            background: linear-gradient(90deg, #02aab0, #00cdac); 
            color: white; border: none; padding: 15px; font-size: 18px; 
            border-radius: 10px; cursor: pointer; width: 100%; font-weight: bold; 
            transition: 0.3s; text-transform: uppercase; letter-spacing: 1px;
        }
        button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(2, 170, 176, 0.6); }
        
        .limit-text { margin-top: 15px; font-size: 14px; color: #00ffcc; font-weight: bold; }
        
        /* 10-SECOND SMART AD */
        .smart-ad-box { 
            display: none; background: rgba(0,0,0,0.8); padding: 25px; 
            border-radius: 15px; margin-top: 20px; border: 2px dashed #ffcc00; 
        }
        .timer-text { font-size: 24px; font-weight: bold; color: #ffcc00; margin-bottom: 10px; }
        .game-ad { 
            display: block; background: #ff416c; color: white; padding: 12px; 
            border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 18px; 
            margin-top: 15px; animation: pulse 1.5s infinite;
        }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
        
        #loading { display: none; margin-top: 20px; font-size: 16px; color: #00ffcc; }
        #result { margin-top: 25px; display: none; }
        video { width: 100%; border-radius: 10px; border: 2px solid #00cdac; margin-bottom: 15px; background: #000; }
        
        /* NEW FEATURE: CAPTION BOX */
        .caption-box { background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; margin-bottom: 15px; font-size: 14px; color: #e0f7fa; text-align: left; border-left: 3px solid #00ffcc; display: none; }

        .dl-btn { background: #007bff; text-decoration: none; display: block; padding: 14px; color: white; border-radius: 8px; font-weight: bold; font-size: 18px; }
        
        /* NEW FEATURE: SHAYARI CORNER */
        .shayari-corner { 
            margin-top: 30px; padding: 20px; background: rgba(0,0,0,0.5); 
            border-radius: 15px; color: #fff; font-style: italic; border-top: 3px solid #00cdac;
        }
        .shayari-corner h3 { margin: 0 0 10px 0; font-size: 18px; color: #00ffcc; }
        .ig-link { color: #ff416c; font-weight: bold; text-decoration: none; }
    </style>
</head>
<body>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">
    🚀 Join Telegram: @CineTrixaHub
</a>

<div class="main-card">
    <h1>Sultan Pro</h1>
    <p class="subtitle">High-Speed Video Downloader</p>
    
    <input type="text" id="videoUrl" placeholder="Paste Video Link Here...">
    <button id="mainBtn" onclick="startProcess()">Download Video</button>
    
    <div id="limitMsg" class="limit-text">🎁 3 Free downloads left today.</div>

    <div class="smart-ad-box" id="smartAd">
        <div class="timer-text">Unlocking in <span id="timerCount">10</span>s</div>
        <a href="{{ game_link }}" target="_blank" class="game-ad">🎮 Play Game & Win ₹500 Cash!</a>
        <br>
        <button id="unlockBtn" style="display: none; background: #00ffcc; color: black;" onclick="fetchVideoAPI()">🔓 Continue Download</button>
    </div>

    <div id="loading">🌊 Diving into servers to fetch video...</div>

    <div id="result">
        <div id="vidTitle" class="caption-box"></div>
        <video id="vidPlayer" controls></video>
        <a id="downloadBtn" class="dl-btn" href="#" target="_blank">📥 Save to Gallery</a>
    </div>

    <div class="shayari-corner">
        <h3>✨ Sultan's Creative Corner</h3>
        <p>"Aag lagi hai dil mein, par dhuan nahi uthta...<br>Ishq ka ye kaisa asar hai, jo ruka nahi rukta."</p>
        <p style="font-size: 12px; margin-top: 15px;">Follow for more amazing Shayari:<br><a href="https://instagram.com/innocent._.foji._.shayar" target="_blank" class="ig-link">@innocent._.foji._.shayar</a></p>
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
            document.getElementById('limitMsg').innerText = "🎁 " + left + " Free downloads left today.";
        } else {
            document.getElementById('limitMsg').innerHTML = "⚡ <span style='color:#ff416c'>Instant limit reached!</span>";
        }
    }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) { alert("Please paste a link first!"); return; }
        
        document.getElementById("result").style.display = "none";
        document.getElementById("vidTitle").style.display = "none";
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
                document.getElementById("result").style.display = "block";
            } else {
                alert("❌ Error: " + data.message);
            }
        })
        .catch(err => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            alert("⚠️ Something went wrong. Try again!");
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
        video_title = None
        
        if 'title' in response:
            video_title = response['title']

        if 'medias' in response and isinstance(response['medias'], list) and len(response['medias']) > 0:
            video_url = response['medias'][0].get('url')
        elif 'url' in response:
            video_url = response['url']
        elif 'video' in response:
            video_url = response['video']
        elif 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0:
            video_url = response['data'][0].get('url')

        if video_url:
            return jsonify({"success": True, "video_url": video_url, "title": video_title})
        else:
            return jsonify({"success": False, "message": "Video link not found or account is private."})
    except Exception as e:
        return jsonify({"success": False, "message": "Server Error. Please try again."})

if __name__ == '__main__':
    app.run()
