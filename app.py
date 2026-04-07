from flask import Flask, request, jsonify, render_template_string
import requests

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
    
    <title>Save Pro | Free Instagram, YouTube & Facebook Video Downloader</title>
    <meta name="description" content="Download Instagram Reels, YouTube Videos and Facebook videos in HD instantly with Save Pro.">
    
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { margin: 0; padding: 0; color: white; text-align: center; background: #05010a; background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.15), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.15), transparent 25%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }
        
        .ambient-glow { position: fixed; width: 400px; height: 400px; background: #fe0979; border-radius: 50%; filter: blur(150px); opacity: 0.1; z-index: -1; }
        
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 2px #00f2fe; animation: drift 5s ease-in-out infinite alternate; }
        @keyframes drift { 0% { transform: translate(0,0); opacity: 0.2; } 100% { transform: translate(30px, -50px); opacity: 0.8; } }
        
        .promo-banner { background: rgba(0, 242, 254, 0.1); padding: 12px 30px; border-radius: 50px; margin-top: 25px; margin-bottom: 20px; font-weight: 700; text-decoration: none; color: #00f2fe; font-size: 14px; border: 1px solid #00f2fe; display: inline-block; }
        
        .main-card { max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; background: rgba(15, 10, 25, 0.7); backdrop-filter: blur(25px); border-top: 2px solid rgba(254, 9, 121, 0.5); border-bottom: 2px solid rgba(0, 242, 254, 0.5); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8); margin-top: 10px; margin-bottom: 20px; position: relative; }
        
        h1 { margin: 0; font-size: 42px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; text-transform: uppercase;}
        p.subtitle { color: #00f2fe; font-size: 13px; margin-bottom: 30px; font-weight: 500; letter-spacing: 2px; }
        
        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 90px 18px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 15px; background: rgba(0,0,0,0.6); color: #fff; outline: none; }
        .paste-btn { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: transparent; color: #fe0979; border: 1px solid #fe0979; border-radius: 8px; padding: 10px 18px; font-weight: 700; font-size: 12px; cursor: pointer; }
        
        button#mainBtn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 800; text-transform: uppercase; box-shadow: 0 10px 20px rgba(254, 9, 121, 0.4); }

        .game-ad-box { margin-top: 15px; background: rgba(245, 175, 25, 0.1); border: 1px dashed #f5af19; padding: 15px; border-radius: 15px; }
        .game-link { color: #f5af19; text-decoration: none; font-weight: 700; font-size: 14px; display: block; animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.03); } 100% { transform: scale(1); } }
        
        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dot { width: 12px; height: 12px; background: #fe0979; border-radius: 50%; display: inline-block; animation: bounce 0.5s infinite alternate; margin: 0 4px; }
        @keyframes bounce { to { transform: translateY(-10px); } }

        #result { margin-top: 30px; display: none; width: 100%; text-align: left; }
        .media-preview { width: 100%; max-height: 400px; border-radius: 12px; margin-bottom: 20px; border: 2px solid #00f2fe; background: #000; object-fit: contain; }
        
        .dl-group { display: flex; flex-direction: column; gap: 15px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 16px; color: #000; border-radius: 12px; font-weight: 800; font-size: 15px; text-transform: uppercase;}
        .btn-main { background: #00f2fe; box-shadow: 0 5px 15px rgba(0, 242, 254, 0.3); } 
        .btn-whatsapp { background: #25D366; color: white; margin-top: 10px;} 
        .btn-earning { background: linear-gradient(90deg, #f5af19, #f12711); color: white; margin-top: 10px;}

        .shayari-corner { margin-top: 40px; padding: 20px; background: rgba(254, 9, 121, 0.05); border-left: 5px solid #fe0979; border-radius: 15px; text-align: center; }
        .shayari-corner p { font-style: italic; color: #fff; font-size: 14px; margin: 0; line-height: 1.5; }
        
        .live-count-badge { display: inline-block; background: rgba(0, 242, 254, 0.1); padding: 5px 15px; border-radius: 20px; border: 1px solid #00f2fe; color: #00f2fe; font-size: 12px; font-weight: 700; margin-top: 20px; }
        .social-links { display: flex; justify-content: center; gap: 20px; margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); width: 100%; }
        .social-links a { color: #aaa; text-decoration: none; font-size: 13px; font-weight: 600; }
        
        #toast { visibility: hidden; min-width: 250px; background: #fe0979; color: #fff; text-align: center; border-radius: 10px; padding: 15px; position: fixed; z-index: 1000; left: 50%; bottom: 30px; transform: translateX(-50%); font-weight: 700; }
        #toast.show { visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }
    </style>
</head>
<body>

<div class="ambient-glow"></div>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">🔥 Join Telegram For Movies: @CineTrixaHub</a>

<div class="main-card">
    <h1>Save Pro</h1>
    <p class="subtitle">Next-Gen Media Engine</p>
    
    <div class="input-wrapper">
        <input type="text" id="videoUrl" placeholder="Paste link here...">
        <button class="paste-btn" onclick="pasteFromClipboard()">PASTE</button>
    </div>

    <button id="mainBtn" onclick="startProcess()">DOWNLOAD</button>

    <div class="game-ad-box">
        <a href="{{ game_link }}" target="_blank" class="game-link">🎮 JAI CLUB: Play & Win ₹500 Daily!</a>
    </div>
    
    <div id="fullLoader">
        <div class="dot"></div><div class="dot" style="animation-delay:0.1s"></div><div class="dot" style="animation-delay:0.2s"></div>
        <p style="color:#00f2fe; font-size:12px; margin-top:10px; font-weight:bold;">FETCHING HD MEDIA...</p>
    </div>

    <div id="result">
        <div id="mediaContainer"></div>
        <div class="dl-group">
            <a id="downloadBtn" class="dl-btn btn-main" href="#" target="_blank">📥 SAVE TO GALLERY</a>
            <a class="dl-btn btn-whatsapp" href="whatsapp://send?text=Bhai%20best%20site%20reels%20download%20karne%20ke%20liye!%20Ye%20dekh:%20https://webearning.vercel.app" target="_blank">📲 SHARE ON WHATSAPP</a>
            <a class="dl-btn btn-earning" href="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js" target="_blank">💰 CLAIM BONUS</a>
        </div>
    </div>

    <div class="shayari-corner">
        <p id="randomShayari">"Rakh hausla wo manzar bhi aayega,<br>Pyaase ke paas chalkar samundar bhi aayega."</p>
    </div>
    
    <div class="live-count-badge">🟢 LIVE VISITORS: <span id="vCount">457</span></div>

    <div class="social-links">
        <a href="https://t.me/CineTrixaHub" target="_blank">📢 Telegram</a>
        <a href="https://instagram.com/innocent._.foji._.shayar" target="_blank">📸 Instagram</a>
    </div>
</div>

<div id="toast">Message here</div>

<script>
    const fb = document.createElement('div'); fb.className = 'fireflies';
    for(let i=0; i<20; i++){ let f=document.createElement('div'); f.className='firefly'; f.style.left=Math.random()*100+'vw'; f.style.top=Math.random()*100+'vh'; fb.appendChild(f); }
    document.body.appendChild(fb);

    setInterval(() => {
        let v = document.getElementById('vCount');
        let current = parseInt(v.innerText);
        v.innerText = current + (Math.random() > 0.5 ? 1 : -1);
    }, 3000);

    function showToast(msg) { let x = document.getElementById("toast"); x.innerText = msg; x.className = "show"; setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000); }
    async function pasteFromClipboard() { try { const text = await navigator.clipboard.readText(); document.getElementById("videoUrl").value = text; showToast("✅ Link Pasted!"); } catch (err) { showToast("⚠️ Paste manually."); } }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return showToast("⚠️ Paste link first!");
        
        document.getElementById("mainBtn").style.display = "none";
        document.getElementById("fullLoader").style.display = "flex";
        document.getElementById("result").style.display = "none";

        fetch("/api/download", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({url: url}) })
        .then(res => res.json())
        .then(data => {
            document.getElementById("fullLoader").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            if(data.success) {
                confetti({particleCount: 100, spread: 70});
                let cont = document.getElementById("mediaContainer");
                if(data.media_type === "image") {
                    cont.innerHTML = `<img src="${data.media_url}" class="media-preview">`;
                } else {
                    cont.innerHTML = `<video src="${data.media_url}" poster="${data.thumbnail}" controls playsinline class="media-preview"></video>`;
                }
                document.getElementById("downloadBtn").href = data.media_url;
                document.getElementById("result").style.display = "block";
                showToast("✅ Ready!");
            } else {
                showToast("❌ Media Not Found!");
            }
        }).catch(() => {
            document.getElementById("fullLoader").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            showToast("⚠️ Network Error!");
        });
    }
</script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path): return render_template_string(HTML_PAGE, game_link=GAME_LINK)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    # Simple clean url logic
    clean_url = url.split('?')[0] if "instagram.com" in url else url
    headers = { "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    try:
        # Direct API Call
        res = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", json={"url": clean_url}, headers=headers, timeout=15).json()
        
        # Priority 1: Check for HD/Video link directly
        media_url = res.get('hd') or res.get('video') or res.get('url')
        media_type = "video"
        
        # Priority 2: Scan medias list if direct link is not video
        if not media_url or not any(x in str(media_url) for x in ['.mp4', '.m3u8']):
            for m in res.get('medias', []):
                m_type = str(m.get('type', '')).lower()
                if m_type == 'video' or 'mp4' in str(m.get('url')):
                    media_url = m.get('url')
                    media_type = "video"
                    break
                if m_type == 'image' and not media_url:
                    media_url = m.get('url')
                    media_type = "image"
        
        if media_url:
            return jsonify({
                "success": True, 
                "media_url": media_url, 
                "media_type": media_type, 
                "thumbnail": res.get('thumbnail', "")
            })
        return jsonify({"success": False})
    except:
        return jsonify({"success": False})

if __name__ == '__main__':
    app.run()

