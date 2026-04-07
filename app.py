from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Save Pro | Premium Media Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { 
            margin: 0; padding: 0; color: white; text-align: center; 
            background: #05010a; 
            background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.15), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.15), transparent 25%); 
            min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; 
        }

        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 2px #00f2fe; animation: drift 5s ease-in-out infinite alternate; }
        @keyframes drift { 0% { transform: translate(0,0); opacity: 0.2; } 100% { transform: translate(30px, -50px); opacity: 0.8; } }

        .promo-banner { background: rgba(0, 242, 254, 0.1); padding: 12px 30px; border-radius: 50px; margin-top: 25px; margin-bottom: 20px; font-weight: 700; text-decoration: none; color: #00f2fe; font-size: 14px; border: 1px solid #00f2fe; box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); transition: 0.3s; z-index: 10; letter-spacing: 1px; }
        .promo-banner:hover { transform: scale(1.05); background: #00f2fe; color: #000; }

        .main-card { max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; background: rgba(15, 10, 25, 0.7); backdrop-filter: blur(25px); border-top: 2px solid rgba(254, 9, 121, 0.5); border-bottom: 2px solid rgba(0, 242, 254, 0.5); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8); margin-top: 10px; margin-bottom: 20px; position: relative; }
        
        h1 { margin: 0; font-size: 40px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; text-transform: uppercase;}
        p.subtitle { color: #00f2fe; font-size: 13px; margin-bottom: 30px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase;}

        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 15px; background: rgba(0,0,0,0.6); color: #fff; outline: none; }
        
        button#mainBtn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; transition: 0.3s; box-shadow: 0 10px 20px rgba(254, 9, 121, 0.4); }
        button#mainBtn:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(254, 9, 121, 0.6); }

        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dot { width: 12px; height: 12px; background: #fe0979; border-radius: 50%; display: inline-block; animation: bounce 0.5s infinite alternate; margin: 0 4px; }
        @keyframes bounce { to { transform: translateY(-10px); } }

        #result { margin-top: 30px; display: none; width: 100%; text-align: left; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        
        .media-preview { width: 100%; max-height: 400px; border-radius: 12px; margin-bottom: 20px; border: 2px solid rgba(0, 242, 254, 0.3); background: #000; object-fit: contain; }
        
        .dl-group { display: flex; flex-direction: column; gap: 15px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 16px; color: #000; border-radius: 12px; font-weight: 800; font-size: 15px; transition: 0.3s; text-transform: uppercase;}
        .btn-main { background: #00f2fe; box-shadow: 0 5px 15px rgba(0, 242, 254, 0.3); } 

        .shayari-corner { margin-top: 40px; padding: 20px; background: rgba(254, 9, 121, 0.05); border-left: 5px solid #fe0979; border-radius: 15px; text-align: center; }
        .shayari-corner p { font-style: italic; color: #fff; font-size: 14px; margin: 0; line-height: 1.5; }
        
        .social-links { display: flex; justify-content: center; gap: 20px; margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); width: 100%; max-width: 440px; }
        .social-links a { color: #aaa; text-decoration: none; font-size: 13px; font-weight: 600; }
    </style>
</head>
<body>

<div class="fireflies" id="firefliesBox"></div>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">🔥 Join Telegram For Movies: @CineTrixaHub</a>

<div class="main-card">
    <h1>Save Pro</h1>
    <p class="subtitle">Next-Gen Media Engine</p>
    
    <div class="input-wrapper">
        <input type="text" id="videoUrl" placeholder="Paste link here...">
    </div>

    <button id="mainBtn" onclick="startProcess()">UNLOCK HD MEDIA</button>
    
    <div id="fullLoader">
        <div class="dot"></div><div class="dot" style="animation-delay:0.1s"></div><div class="dot" style="animation-delay:0.2s"></div>
        <p style="color:#00f2fe; font-size:12px; margin-top:10px;">GENERATING SECURE LINK...</p>
    </div>

    <div id="result">
        <div id="mediaContainer"></div>
        <div class="dl-group">
            <a id="downloadBtn" class="dl-btn btn-main" href="#" target="_blank">📥 SAVE TO GALLERY</a>
        </div>
    </div>

    <div class="shayari-corner">
        <p>"Rakh hausla wo manzar bhi aayega,<br>Pyaase ke paas chalkar samundar bhi aayega."</p>
        <p style="color:#fe0979; font-size:11px; margin-top:10px; font-weight:bold;">@innocent._.foji._.shayar</p>
    </div>

    <div class="social-links">
        <a href="https://t.me/CineTrixaHub" target="_blank">📢 Telegram Channel</a>
        <a href="https://t.me/SultanBot" target="_blank">🤖 Download Bot</a>
    </div>
</div>

<script>
    // Simple Fireflies
    const fb = document.getElementById('firefliesBox');
    for(let i=0; i<20; i++){ 
        let f=document.createElement('div'); f.className='firefly'; 
        f.style.left=Math.random()*100+'vw'; f.style.top=Math.random()*100+'vh'; 
        fb.appendChild(f); 
    }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return alert("Please paste a link!");

        document.getElementById("mainBtn").style.display = "none";
        document.getElementById("fullLoader").style.display = "flex";
        document.getElementById("result").style.display = "none";

        fetch("/api/download", { 
            method: "POST", 
            headers: {"Content-Type":"application/json"}, 
            body: JSON.stringify({url: url}) 
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("fullLoader").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            
            if(data.success) {
                confetti({particleCount: 100, spread: 70, origin: {y: 0.6}});
                let cont = document.getElementById("mediaContainer");
                if(data.media_type === "image") {
                    cont.innerHTML = `<img src="${data.media_url}" class="media-preview">`;
                } else {
                    cont.innerHTML = `<video src="${data.media_url}" poster="${data.thumbnail}" controls playsinline class="media-preview"></video>`;
                }
                document.getElementById("downloadBtn").href = data.media_url;
                document.getElementById("result").style.display = "block";
                document.getElementById("videoUrl").value = "";
            } else {
                alert("Error! Link not supported.");
            }
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
    headers = { "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    try:
        res = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", json={"url": clean_url}, headers=headers, timeout=15).json()
        media_url = res.get('hd') or res.get('video') or res.get('url')
        m_type = "video"
        for m in res.get('medias', []):
            if m.get('type') == 'image' and not media_url: media_url = m.get('url'); m_type = "image"
        if media_url: return jsonify({"success": True, "media_url": media_url, "media_type": m_type, "thumbnail": res.get('thumbnail', "")})
        return jsonify({"success": False})
    except: return jsonify({"success": False})

if __name__ == '__main__': app.run()
