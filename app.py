from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# --- CONFIGURATION ---
RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Save Pro | HD Media Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { margin: 0; padding: 0; color: white; text-align: center; background: #05010a; background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.15), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.15), transparent 25%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }
        .ambient-glow { position: fixed; width: 400px; height: 400px; background: #fe0979; border-radius: 50%; filter: blur(150px); opacity: 0.1; animation: float 10s infinite alternate; z-index: -1; }
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 2px #00f2fe; animation: drift 5s ease-in-out infinite alternate; }
        @keyframes drift { 0% { transform: translateY(0) translateX(0) scale(1); opacity: 0.2; } 100% { transform: translateY(-80px) translateX(30px) scale(1.2); opacity: 0.8; } }
        .promo-banner { background: rgba(0, 242, 254, 0.1); padding: 12px 30px; border-radius: 50px; margin-top: 25px; margin-bottom: 20px; font-weight: 700; text-decoration: none; color: #00f2fe; font-size: 14px; border: 1px solid #00f2fe; box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); transition: 0.3s; z-index: 10; letter-spacing: 1px; }
        .main-card { max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; background: rgba(15, 10, 25, 0.7); backdrop-filter: blur(25px); border-top: 2px solid rgba(254, 9, 121, 0.5); border-bottom: 2px solid rgba(0, 242, 254, 0.5); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8); margin-top: 10px; margin-bottom: 20px; position: relative; }
        h1 { margin: 0; font-size: 42px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; text-transform: uppercase;}
        p.subtitle { color: #00f2fe; font-size: 13px; margin-bottom: 30px; font-weight: 500; letter-spacing: 2px; }
        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 90px 18px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 15px; background: rgba(0,0,0,0.6); color: #fff; outline: none; transition: 0.3s; }
        .paste-btn { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: transparent; color: #fe0979; border: 1px solid #fe0979; border-radius: 8px; padding: 10px 18px; font-weight: 700; font-size: 12px; cursor: pointer; transition: 0.3s; }
        button#mainBtn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; transition: 0.3s; box-shadow: 0 10px 20px rgba(254, 9, 121, 0.4); }
        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dots { display: flex; gap: 8px; margin-bottom: 15px; }
        .dot { width: 14px; height: 14px; background: #fe0979; border-radius: 50%; animation: bounce 0.5s infinite alternate; }
        @keyframes bounce { to { transform: translateY(-12px); } }
        #result { margin-top: 30px; display: none; width: 100%; text-align: left; }
        .media-preview { width: 100%; max-height: 400px; border-radius: 12px; margin-bottom: 20px; border: 2px solid rgba(0, 242, 254, 0.3); background: #000; object-fit: contain; }
        .dl-group { display: flex; flex-direction: column; gap: 15px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 16px; color: #000; border-radius: 12px; font-weight: 800; font-size: 15px; transition: 0.3s; text-transform: uppercase; }
        .btn-main { background: #00f2fe; box-shadow: 0 5px 15px rgba(0, 242, 254, 0.3); } 
        .btn-earning { background: linear-gradient(90deg, #f5af19, #f12711); color: white; margin-top: 10px; animation: gentleShake 3s infinite;}
        @keyframes gentleShake { 0%, 100% {transform: rotate(0deg);} 10%, 30%, 50% {transform: rotate(-1deg);} 20%, 40%, 60% {transform: rotate(1deg);} }
        .live-count { margin-top: 20px; color: #00f2fe; font-weight: 700; font-size: 12px; }
    </style>
</head>
<body>
    <a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">🔥 JOIN VIP MOVIE CHANNEL</a>
    <div class="main-card">
        <h1>Save Pro</h1>
        <p class="subtitle">Next-Gen Media Engine</p>
        <div class="input-wrapper">
            <input type="text" id="videoUrl" placeholder="Paste link here...">
            <button class="paste-btn" onclick="pasteFromClipboard()">PASTE</button>
        </div>
        <button id="mainBtn" onclick="startProcess()">DOWNLOAD MEDIA</button>
        <div id="fullLoader">
            <div class="dots"><div class="dot"></div><div class="dot" style="animation-delay:0.1s"></div><div class="dot" style="animation-delay:0.2s"></div></div>
            <div style="color:#00f2fe; font-size:12px; font-weight:600;">BYPASSING PROTECTED SERVERS...</div>
        </div>
        <div id="result">
            <div id="mediaContainer"></div>
            <div class="dl-group">
                <a id="downloadBtn" class="dl-btn btn-main" href="#" target="_blank">📥 SAVE HD MEDIA</a>
                <a class="dl-btn btn-earning" href="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js" target="_blank">💰 CLAIM BONUS</a>
            </div>
        </div>
        <div class="live-count">🟢 LIVE VISITORS: <span id="vCount">457</span></div>
    </div>

<script>
    setInterval(() => {
        let v = document.getElementById('vCount');
        let current = parseInt(v.innerText);
        v.innerText = current + (Math.random() > 0.5 ? 1 : -1);
    }, 3000);

    async function pasteFromClipboard() {
        const text = await navigator.clipboard.readText();
        document.getElementById("videoUrl").value = text;
    }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return alert("Paste link first!");
        document.getElementById("result").style.display = "none";
        document.getElementById("mainBtn").style.display = "none";
        document.getElementById("fullLoader").style.display = "flex";

        fetch("/api/download", { 
            method: "POST", 
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify({ url: url }) 
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("fullLoader").style.display = "none"; 
            document.getElementById("mainBtn").style.display = "block";
            if(data.success) {
                confetti({ particleCount: 100, spread: 70 });
                let container = document.getElementById("mediaContainer");
                if(data.media_type === "image") {
                    container.innerHTML = `<img src="${data.media_url}" class="media-preview">`;
                } else {
                    container.innerHTML = `<video src="${data.media_url}" poster="${data.thumbnail}" controls playsinline class="media-preview"></video>`;
                }
                document.getElementById("downloadBtn").href = data.media_url;
                document.getElementById("result").style.display = "block";
            } else { alert("Error: " + data.message); }
        });
    }
</script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path): return render_template_string(HTML_PAGE)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    # Engine logic switch to bypass Replit blocks
    headers = { "X-RapidAPI-Key": RAPID_API_KEY }
    
    # Engine 1: Heavy Scraper
    try:
        api_url = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"
        res = requests.post(api_url, json={"url": url}, headers={**headers, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com"}, timeout=12).json()
        
        media_url = res.get('hd') or res.get('video') or res.get('url')
        if media_url and 'http' in media_url and not "youtube.com" in media_url:
            return jsonify({"success": True, "media_url": media_url, "media_type": "video", "thumbnail": res.get('thumbnail', '')})
        
        # Scan medias array if direct fail
        for m in res.get('medias', []):
            if m.get('type') == 'video':
                return jsonify({"success": True, "media_url": m.get('url'), "media_type": "video", "thumbnail": res.get('thumbnail', '')})
    except:
        pass

    # Engine 2: Fallback for Instagram (Scraper API)
    if "instagram.com" in url:
        try:
            shortcode = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
            ig_api = f"https://instagram-scraper-api2.p.rapidapi.com/api/v1/post_info?shortcode={shortcode}"
            res_ig = requests.get(ig_api, headers={**headers, "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com"}, timeout=10).json()
            video_url = res_ig['data']['video_url']
            return jsonify({"success": True, "media_url": video_url, "media_type": "video"})
        except:
            pass

    return jsonify({"success": False, "message": "All engines busy. Try another link!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

