from flask import Flask, request, jsonify, render_template_string
import requests
import random

app = Flask(__name__)

# CONFIGURATION
RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'
AD_DIRECT_LINK = "https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Save Pro | HD Media Downloader & Saver</title>
    
    <meta name="description" content="Save Pro is the fastest free Instagram and YouTube downloader. Save reels, videos, and photos in HD instantly.">
    <meta name="keywords" content="Save Pro, Instagram downloader, YouTube video download, HD reel saver">
    
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { margin: 0; padding: 0; color: white; text-align: center; background: #05010a; background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.1), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.1), transparent 25%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }
        
        .main-card { max-width: 450px; width: 92%; padding: 40px 25px; border-radius: 30px; background: rgba(15, 10, 25, 0.8); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9); margin-top: 20px; position: relative; z-index: 5; }
        h1 { margin: 0; font-size: 42px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -2px; }
        .subtitle { color: #00f2fe; font-size: 11px; letter-spacing: 3px; font-weight: 600; text-transform: uppercase; margin-bottom: 30px; }

        .input-box { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.5); color: #fff; font-size: 15px; outline: none; margin-bottom: 15px; }
        .main-btn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; border-radius: 12px; width: 100%; font-weight: 800; cursor: pointer; font-size: 16px; text-transform: uppercase; box-shadow: 0 10px 25px rgba(254, 9, 121, 0.4); }

        /* AD TIMER SYSTEM */
        #adSection { display: none; margin-top: 20px; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px; border: 1px dashed #f5af19; }
        .timer-circle { width: 60px; height: 60px; border: 4px solid #f5af19; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 20px; font-weight: 900; color: #f5af19; }
        .trending-ad-btn { display: block; background: #00f2fe; color: #000; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: 800; font-size: 14px; margin-top: 10px; animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.05);} 100% {transform: scale(1);} }

        /* POPUP STYLING */
        #adPopup { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 9999; display: none; flex-direction: column; justify-content: center; align-items: center; padding: 30px; }
        .popup-content { background: #1a1a2e; padding: 30px; border-radius: 20px; border: 2px solid #fe0979; max-width: 350px; text-align: center; box-shadow: 0 0 30px #fe0979; }

        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dot-loader { display: flex; gap: 8px; margin-bottom: 10px; }
        .dot { width: 12px; height: 12px; background: #fe0979; border-radius: 50%; animation: bounce 0.5s infinite alternate; }
        @keyframes bounce { to { transform: translateY(-10px); } }

        #result { margin-top: 30px; display: none; text-align: left; }
        .media-preview { width: 100%; border-radius: 15px; border: 2px solid #00f2fe; background: #000; }
        .dl-btn { text-decoration: none; display: block; padding: 18px; border-radius: 12px; font-weight: 800; font-size: 15px; text-align: center; margin-top: 15px; text-transform: uppercase; }
        .btn-hd { background: #00f2fe; color: #000; }

        .shayari-box { margin-top: 30px; padding: 15px; background: rgba(254, 9, 121, 0.05); border-radius: 15px; border-left: 4px solid #fe0979; font-style: italic; font-size: 13px; }
        
        .footer-info { max-width: 450px; width: 92%; text-align: left; margin: 30px 0; font-size: 12px; color: #777; }
        .visitor-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; border: 1px solid #00f2fe; color: #00f2fe; font-weight: 700; margin-bottom: 10px; }
    </style>
</head>
<body>

<div id="adPopup">
    <div class="popup-content">
        <h2 style="color:#fff; margin-bottom:10px;">🚀 Fast Server Active</h2>
        <p style="color:#aaa; font-size:14px; margin-bottom:20px;">Your video will start downloading immediately <b>after this short ad!</b></p>
        <a href="{{ ad_link }}" target="_blank" onclick="closePopupAndShow()" style="background:#fe0979; color:#fff; padding:15px 30px; border-radius:10px; text-decoration:none; font-weight:800; display:inline-block;">WATCH AD & DOWNLOAD</a>
    </div>
</div>

<div class="main-card">
    <h1>Save Pro</h1>
    <p class="subtitle">Next-Gen Media Saver</p>
    
    <input type="text" id="videoUrl" class="input-box" placeholder="Paste link here...">
    <button id="mainBtn" class="main-btn" onclick="startTimer()">Extract Media</button>
    
    <div id="adSection">
        <div class="timer-circle" id="timer">10</div>
        <p style="color:#fff; font-size:12px;">Unlocking High-Speed Link...</p>
        <a href="{{ game_link }}" target="_blank" class="trending-ad-btn">🔥 PLAY TRENDING GAME (Earn ₹500)</a>
    </div>

    <div id="fullLoader">
        <div class="dot-loader"><div class="dot"></div><div class="dot" style="animation-delay:0.1s"></div><div class="dot" style="animation-delay:0.2s"></div></div>
        <p style="color:#00f2fe; font-size:11px; font-weight:bold;">PROCESSING ON SECURE SERVER...</p>
    </div>

    <div id="result">
        <div id="mediaWrap"></div>
        <a id="dlLink" class="dl-btn btn-hd" href="#" target="_blank" onclick="showFinalPopup(event)">📥 SAVE HD VIDEO</a>
    </div>

    <div class="shayari-box" id="shayariDisplay">Loading shayari...</div>
</div>

<div class="footer-info">
    <div class="visitor-badge">🟢 LIVE: <span id="vCount">524</span> USERS</div>
    <p><b>Save Pro</b> is a professional tool for downloading Instagram Reels, YouTube HD videos, and Facebook clips. Get the best <b>Instagram downloader</b> experience with original music extraction.</p>
</div>

<script>
    const shayaris = [
        "Waqt ko apna waqt banane mein waqt lagta hai...",
        "Rakh hausla wo manzar bhi aayega, Pyaase ke paas chalkar samundar bhi aayega.",
        "Manzil mile na mile ye toh muqaddar ki baat hai, Hum koshish bhi na karein ye galat baat hai."
    ];
    document.getElementById('shayariDisplay').innerText = shayaris[Math.floor(Math.random()*shayaris.length)];

    setInterval(() => {
        let v = parseInt(document.getElementById('vCount').innerText);
        document.getElementById('vCount').innerText = v + (Math.random() > 0.5 ? 1 : -1);
    }, 3000);

    function startTimer() {
        let url = document.getElementById('videoUrl').value;
        if(!url) return alert("Paste link first!");
        
        document.getElementById('mainBtn').style.display = 'none';
        document.getElementById('adSection').style.display = 'block';
        
        let timeLeft = 10;
        let t = setInterval(() => {
            timeLeft--;
            document.getElementById('timer').innerText = timeLeft;
            if(timeLeft <= 0) {
                clearInterval(t);
                document.getElementById('adSection').style.display = 'none';
                fetchData(url);
            }
        }, 1000);
    }

    function fetchData(url) {
        document.getElementById('fullLoader').style.display = 'flex';
        fetch("/api/download", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({url: url}) })
        .then(res => res.json())
        .then(data => {
            document.getElementById('fullLoader').style.display = 'none';
            if(data.success) {
                let wrap = document.getElementById('mediaWrap');
                if(data.media_type === "image") {
                    wrap.innerHTML = `<img src="${data.media_url}" class="media-preview">`;
                } else {
                    wrap.innerHTML = `<video src="${data.media_url}" poster="${data.thumbnail}" controls playsinline class="media-preview"></video>`;
                }
                document.getElementById('dlLink').href = data.media_url;
                document.getElementById('result').style.display = 'block';
                confetti({particleCount: 100, spread: 70});
            } else {
                alert("Error: Link not supported!");
                document.getElementById('mainBtn').style.display = 'block';
            }
        });
    }

    function showFinalPopup(e) {
        e.preventDefault();
        document.getElementById('adPopup').style.display = 'flex';
    }

    function closePopupAndShow() {
        document.getElementById('adPopup').style.display = 'none';
        let link = document.getElementById('dlLink').href;
        window.open(link, '_blank');
    }
</script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path): return render_template_string(HTML_PAGE, game_link=GAME_LINK, ad_link=AD_DIRECT_LINK)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    headers = { "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    try:
        res = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", json={"url": url}, headers=headers).json()
        media_url = res.get('hd') or res.get('video') or res.get('url')
        m_type = "video"
        for m in res.get('medias', []):
            if m.get('type') == 'image' and not media_url: media_url = m.get('url'); m_type = "image"
        
        if media_url: return jsonify({"success": True, "media_url": media_url, "media_type": m_type, "thumbnail": res.get('thumbnail', "")})
        return jsonify({"success": False})
    except: return jsonify({"success": False})

if __name__ == '__main__': app.run()
