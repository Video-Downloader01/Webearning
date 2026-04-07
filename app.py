from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# CONFIGURATION (Tumhare Links)
RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
AD_DIRECT_LINK = "https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js"
GAME_LINK = "https://www.jaiclub36.com/#/register?invitationCode=46857835121"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Save Pro | Free HD Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { margin: 0; padding: 0; color: white; text-align: center; background: #05010a; background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.15), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.15), transparent 25%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }
        
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 2px #00f2fe; animation: drift 5s infinite alternate; }
        @keyframes drift { 0% { transform: translate(0,0); opacity: 0.2; } 100% { transform: translate(30px, -50px); opacity: 0.8; } }

        .main-card { max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; background: rgba(15, 10, 25, 0.7); backdrop-filter: blur(25px); border-top: 2px solid rgba(254, 9, 121, 0.5); border-bottom: 2px solid rgba(0, 242, 254, 0.5); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8); margin-top: 30px; position: relative; }
        
        h1 { margin: 0; font-size: 42px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; }
        .subtitle { color: #00f2fe; font-size: 13px; margin-bottom: 30px; font-weight: 500; letter-spacing: 2px; }

        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; background: rgba(0,0,0,0.6); color: #fff; outline: none; }
        
        #mainBtn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 800; box-shadow: 0 10px 20px rgba(254, 9, 121, 0.4); }

        /* TIMER & AD STYLING */
        #adTimerBox { display: none; margin-top: 20px; border: 1px dashed #f5af19; padding: 15px; border-radius: 15px; background: rgba(245, 175, 25, 0.1); }
        .timer-val { font-size: 24px; font-weight: 900; color: #f5af19; }
        .ad-link-btn { display: block; margin-top: 10px; color: #00f2fe; font-weight: 700; text-decoration: none; font-size: 13px; border: 1px solid #00f2fe; padding: 8px; border-radius: 8px; }

        /* POPUP */
        #adPopup { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 1000; display: none; flex-direction: column; justify-content: center; align-items: center; }
        .popup-box { background: #1a1a2e; padding: 30px; border-radius: 20px; border: 2px solid #fe0979; text-align: center; max-width: 320px; }

        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dot { width: 12px; height: 12px; background: #fe0979; border-radius: 50%; display: inline-block; animation: bounce 0.5s infinite alternate; margin: 0 4px; }
        @keyframes bounce { to { transform: translateY(-10px); } }

        #result { margin-top: 30px; display: none; width: 100%; }
        .media-preview { width: 100%; border-radius: 12px; border: 2px solid #00f2fe; margin-bottom: 20px; }
        .dl-btn { text-decoration: none; display: block; padding: 16px; border-radius: 12px; font-weight: 800; text-align: center; margin-top: 10px; }
        .btn-main { background: #00f2fe; color: #000; }

        .shayari-corner { margin-top: 30px; padding: 15px; background: rgba(254, 9, 121, 0.05); border-left: 4px solid #fe0979; font-style: italic; font-size: 13px; }
    </style>
</head>
<body>

<div id="adPopup">
    <div class="popup-box">
        <h3 style="color:#fff;">Video Ready! 🚀</h3>
        <p style="color:#ccc; font-size:14px;">Your download will start <b>after clicking</b> this short ad.</p>
        <a href="{{ ad_link }}" target="_blank" onclick="finalDownload()" style="background:#fe0979; color:#fff; padding:12px 25px; border-radius:10px; text-decoration:none; font-weight:800; display:inline-block;">GET VIDEO NOW</a>
    </div>
</div>

<div class="main-card">
    <h1>Save Pro</h1>
    <p class="subtitle">PREMIUM DOWNLOADER</p>
    
    <div class="input-wrapper">
        <input type="text" id="videoUrl" placeholder="Paste link here...">
    </div>

    <button id="mainBtn" onclick="startProcess()">UNLOCK HD VIDEO</button>

    <div id="adTimerBox">
        <div class="timer-val" id="timer">10</div>
        <p style="font-size:12px; color:#fff;">Bypassing Security... Please Wait</p>
        <a href="{{ game_link }}" target="_blank" class="ad-link-btn">🔥 PLAY & EARN ₹500 (Bonus Ad)</a>
    </div>
    
    <div id="fullLoader">
        <div class="dot"></div><div class="dot" style="animation-delay:0.1s"></div><div class="dot" style="animation-delay:0.2s"></div>
        <p style="color:#00f2fe; font-size:12px; margin-top:10px;">GENERATING SECURE LINK...</p>
    </div>

    <div id="result">
        <div id="mediaContainer"></div>
        <a id="downloadBtn" class="dl-btn btn-main" href="#" onclick="openAdPopup(event)">📥 SAVE TO GALLERY</a>
    </div>

    <div class="shayari-corner" id="shayari">"Rakh hausla wo manzar bhi aayega..."</div>
</div>

<script>
    // Fireflies effect
    const fb = document.createElement('div'); fb.className = 'fireflies';
    for(let i=0; i<20; i++){ let f=document.createElement('div'); f.className='firefly'; f.style.left=Math.random()*100+'vw'; f.style.top=Math.random()*100+'vh'; fb.appendChild(f); }
    document.body.appendChild(fb);

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return alert("Please paste a link!");

        document.getElementById("mainBtn").style.display = "none";
        document.getElementById("adTimerBox").style.display = "block";
        
        let sec = 10;
        let t = setInterval(() => {
            sec--;
            document.getElementById("timer").innerText = sec;
            if(sec <= 0) {
                clearInterval(t);
                document.getElementById("adTimerBox").style.display = "none";
                fetchMedia(url);
            }
        }, 1000);
    }

    function fetchMedia(url) {
        document.getElementById("fullLoader").style.display = "flex";
        fetch("/api/download", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({url: url}) })
        .then(res => res.json())
        .then(data => {
            document.getElementById("fullLoader").style.display = "none";
            if(data.success) {
                let cont = document.getElementById("mediaContainer");
                if(data.media_type === "image") {
                    cont.innerHTML = `<img src="${data.media_url}" class="media-preview">`;
                } else {
                    cont.innerHTML = `<video src="${data.media_url}" poster="${data.thumbnail}" controls class="media-preview"></video>`;
                }
                document.getElementById("downloadBtn").href = data.media_url;
                document.getElementById("result").style.display = "block";
                confetti({particleCount: 100, spread: 70});
            } else {
                alert("Error! Link not supported.");
                document.getElementById("mainBtn").style.display = "block";
            }
        });
    }

    function openAdPopup(e) {
        e.preventDefault();
        document.getElementById("adPopup").style.display = "flex";
    }

    function finalDownload() {
        document.getElementById("adPopup").style.display = "none";
        let link = document.getElementById("downloadBtn").href;
        window.open(link, '_blank');
    }
</script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path): return render_template_string(HTML_PAGE, ad_link=AD_DIRECT_LINK, game_link=GAME_LINK)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    headers = { "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    try:
        res = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", json={"url": url}, headers=headers, timeout=15).json()
        media_url = res.get('hd') or res.get('video') or res.get('url')
        m_type = "video"
        for m in res.get('medias', []):
            if m.get('type') == 'image' and not media_url: media_url = m.get('url'); m_type = "image"
        
        if media_url: return jsonify({"success": True, "media_url": media_url, "media_type": m_type, "thumbnail": res.get('thumbnail', "")})
        return jsonify({"success": False})
    except: return jsonify({"success": False})

if __name__ == '__main__': app.run()

