from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# --- CONFIGURATION ---
RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>Save Pro | Free Instagram, YouTube & Facebook Video Downloader</title>
    <meta name="description" content="Save Pro is the best free all-in-one media downloader. Download Instagram Reels, Photos with Music, YouTube Videos in HD, and Facebook videos instantly.">
    
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { margin: 0; padding: 0; color: white; text-align: center; background: #05010a; background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.15), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.15), transparent 25%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }
        
        .ambient-glow { position: fixed; width: 400px; height: 400px; background: #fe0979; border-radius: 50%; filter: blur(150px); opacity: 0.1; animation: float 10s infinite alternate; z-index: -1; }
        @keyframes float { 0% { transform: translateY(0px) scale(1); } 100% { transform: translateY(-50px) scale(1.1); } }
        
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 2px #00f2fe; animation: drift 5s ease-in-out infinite alternate; }
        @keyframes drift { 0% { transform: translateY(0) translateX(0) scale(1); opacity: 0.2; } 100% { transform: translateY(-80px) translateX(30px) scale(1.2); opacity: 0.8; } }
        
        .promo-banner { background: rgba(0, 242, 254, 0.1); padding: 12px 30px; border-radius: 50px; margin-top: 25px; margin-bottom: 20px; font-weight: 700; text-decoration: none; color: #00f2fe; font-size: 14px; border: 1px solid #00f2fe; box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); transition: 0.3s; z-index: 10; letter-spacing: 1px; }
        .promo-banner:hover { transform: scale(1.05); background: #00f2fe; color: #000; }
        
        .main-card { max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; background: rgba(15, 10, 25, 0.7); backdrop-filter: blur(25px); border-top: 2px solid rgba(254, 9, 121, 0.5); border-bottom: 2px solid rgba(0, 242, 254, 0.5); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8); margin-top: 10px; margin-bottom: 20px; position: relative; }
        
        h1 { margin: 0; font-size: 42px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; text-transform: uppercase;}
        p.subtitle { color: #00f2fe; font-size: 13px; margin-bottom: 30px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase;}
        
        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 90px 18px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 15px; background: rgba(0,0,0,0.6); color: #fff; outline: none; transition: 0.3s; }
        .input-wrapper input:focus { border-color: #fe0979; background: rgba(0,0,0,0.9); box-shadow: 0 0 15px rgba(254, 9, 121, 0.4); }
        .paste-btn { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: transparent; color: #fe0979; border: 1px solid #fe0979; border-radius: 8px; padding: 10px 18px; font-weight: 700; font-size: 12px; cursor: pointer; transition: 0.3s; }
        
        button#mainBtn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; transition: 0.3s; box-shadow: 0 10px 20px rgba(254, 9, 121, 0.4); }
        button#mainBtn:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(254, 9, 121, 0.6); }
        
        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dots { display: flex; gap: 8px; margin-bottom: 15px; }
        .dot { width: 14px; height: 14px; background: #fe0979; border-radius: 50%; animation: bounce 0.5s infinite alternate; }
        .dot:nth-child(2) { animation-delay: 0.1s; background: #f5af19; }
        .dot:nth-child(3) { animation-delay: 0.2s; background: #00f2fe; }
        @keyframes bounce { to { transform: translateY(-12px); } }
        
        #result { margin-top: 30px; display: none; width: 100%; text-align: left; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        
        .media-preview { width: 100%; max-height: 400px; border-radius: 12px; margin-bottom: 20px; border: 2px solid rgba(0, 242, 254, 0.3); background: #000; object-fit: contain; }
        
        .dl-group { display: flex; flex-direction: column; gap: 15px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 16px; color: #000; border-radius: 12px; font-weight: 800; font-size: 15px; transition: 0.3s; text-transform: uppercase; }
        .btn-main { background: #00f2fe; box-shadow: 0 5px 15px rgba(0, 242, 254, 0.3); } 
        .btn-whatsapp { background: #25D366; color: white; } 
        .btn-earning { background: linear-gradient(90deg, #f5af19, #f12711); color: white; }
        
        .shayari-corner { margin-top: 40px; padding: 20px; background: rgba(254, 9, 121, 0.05); border: 1px solid rgba(254, 9, 121, 0.3); border-left: 5px solid #fe0979; border-right: 5px solid #00f2fe; border-radius: 15px; text-align: center; }
        .shayari-corner p { font-style: italic; color: #fff; font-size: 14px; margin: 0 0 12px 0; }
        
        .live-count-badge { display: inline-block; background: rgba(0, 242, 254, 0.1); padding: 5px 15px; border-radius: 20px; border: 1px solid #00f2fe; color: #00f2fe; font-size: 12px; font-weight: 700; margin-top: 20px; }
        
        .footer-area { margin-top: 10px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); width: 100%; max-width: 440px; }
        .social-links { display: flex; justify-content: center; gap: 20px; margin-bottom: 15px; }
        .social-links a { color: #aaa; text-decoration: none; font-size: 13px; font-weight: 600; }
    </style>
</head>
<body>

<div class="ambient-glow"></div>
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
        <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
        <div style="color:#00f2fe; font-size:12px; font-weight:600;">BYPASSING ENGINES...</div>
    </div>

    <div id="result">
        <div id="mediaContainer"></div>
        <div class="dl-group">
            <a id="downloadBtn" class="dl-btn btn-main" href="#" target="_blank">📥 SAVE TO GALLERY</a>
            <a class="dl-btn btn-whatsapp" href="whatsapp://send?text=Bhai%20ye%20site%20best%20hai%20video%20download%20karne%20ke%20liye!%20Ye%20dekh:%20https://webearning.vercel.app" target="_blank">📲 SHARE ON WHATSAPP</a>
            <a class="dl-btn btn-earning" href="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js" target="_blank">💰 CLAIM BONUS</a>
        </div>
    </div>

    <div class="shayari-corner">
        <p id="randomShayari">"Rakh hausla wo manzar bhi aayega,<br>Pyaase ke paas chalkar samundar bhi aayega."</p>
        <a href="https://instagram.com/innocent._.foji._.shayar" target="_blank" style="color:#fe0979; text-decoration:none; font-size:12px; font-weight:bold;">@innocent._.foji._.shayar</a>
    </div>

    <div class="footer-area">
        <div class="live-count-badge">🟢 LIVE VISITORS: <span id="vCount">457</span></div>
        <div class="social-links">
            <a href="https://t.me/CineTrixaHub" target="_blank">📢 Telegram</a>
            <a href="https://instagram.com/innocent._.foji._.shayar" target="_blank">📸 Instagram</a>
        </div>
        <p style="color: #555; font-size: 11px; margin: 0 0 20px 0;">© 2026 Save Pro. All Rights Reserved.</p>
    </div>
</div>

<script>
    setInterval(() => {
        let v = document.getElementById('vCount');
        let current = parseInt(v.innerText);
        v.innerText = current + (Math.random() > 0.5 ? 1 : -1);
    }, 3000);

    async function pasteFromClipboard() {
        try {
            const text = await navigator.clipboard.readText();
            document.getElementById("videoUrl").value = text;
        } catch (err) {}
    }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return alert("Please paste a link!");
        
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
            } else { alert("Error: Engine Busy! Please try again with a different link."); }
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
    clean_url = url.split('?')[0] if "instagram.com" in url else url
    
    # Engine 1: RapidAPI
    headers = { "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    try:
        res = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", json={"url": clean_url}, headers=headers, timeout=10).json()
        media_url = None; thumbnail = res.get('thumbnail') or ""
        
        for m in res.get('medias', []):
            if m.get('type') == 'video' or 'mp4' in str(m.get('url')):
                media_url = m.get('url'); break
        
        if not media_url:
            media_url = res.get('hd') or res.get('video') or res.get('url')
            
        if media_url and "youtube.com" not in str(media_url):
            return jsonify({"success": True, "media_url": media_url, "media_type": "video", "thumbnail": thumbnail})
    except:
        pass

    # Engine 2: Bypass Engine (Stable)
    try:
        bypass_headers = { "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "all-video-downloader-all-in-one.p.rapidapi.com" }
        res2 = requests.get(f"https://all-video-downloader-all-in-one.p.rapidapi.com/download?url={clean_url}", headers=bypass_headers, timeout=10).json()
        links = res2.get('links', [])
        if links:
            return jsonify({"success": True, "media_url": links[0].get('link'), "media_type": "video", "thumbnail": res2.get('picture', '')})
    except:
        pass

    return jsonify({"success": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
