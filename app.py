from flask import Flask, request, jsonify, render_template_string
import requests

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
    <meta name="keywords" content="Instagram reel downloader, YouTube video download free, FB video downloader, save insta, download yt video, Photo with music download instagram, Save Pro, social media downloader">
    <meta name="author" content="Save Pro">
    <meta name="robots" content="index, follow">
    
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { margin: 0; padding: 0; color: white; text-align: center; background: #05010a; background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.15), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.15), transparent 25%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }
        .ambient-glow { position: fixed; width: 400px; height: 400px; background: #fe0979; border-radius: 50%; filter: blur(150px); opacity: 0.1; animation: float 10s infinite alternate; z-index: -1; }
        .ambient-glow:nth-child(2) { background: #00f2fe; right: -100px; bottom: -100px; animation-duration: 15s; opacity: 0.1; }
        @keyframes float { 0% { transform: translateY(0px) scale(1); } 100% { transform: translateY(-50px) scale(1.1); } }
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 2px #00f2fe; animation: drift 5s ease-in-out infinite alternate; }
        @keyframes drift { 0% { transform: translate(0,0); opacity: 0.2; } 100% { transform: translate(30px, -50px); opacity: 0.8; } }
        .promo-banner { background: rgba(0, 242, 254, 0.1); padding: 12px 30px; border-radius: 50px; margin-top: 25px; margin-bottom: 20px; font-weight: 700; text-decoration: none; color: #00f2fe; font-size: 14px; border: 1px solid #00f2fe; box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); transition: 0.3s; z-index: 10; letter-spacing: 1px; }
        .promo-banner:hover { transform: scale(1.05); background: #00f2fe; color: #000; }
        .main-card { max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; background: rgba(15, 10, 25, 0.7); backdrop-filter: blur(25px); border-top: 2px solid rgba(254, 9, 121, 0.5); border-bottom: 2px solid rgba(0, 242, 254, 0.5); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8); margin-top: 10px; margin-bottom: 20px; position: relative; }
        h1 { margin: 0; font-size: 42px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; text-transform: uppercase;}
        p.subtitle { color: #00f2fe; font-size: 13px; margin-bottom: 30px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase;}
        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 90px 18px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 15px; background: rgba(0,0,0,0.6); color: #fff; outline: none; transition: 0.3s; }
        .input-wrapper input:focus { border-color: #fe0979; background: rgba(0,0,0,0.9); box-shadow: 0 0 15px rgba(254, 9, 121, 0.4); }
        .paste-btn { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: transparent; color: #fe0979; border: 1px solid #fe0979; border-radius: 8px; padding: 10px 18px; font-weight: 700; font-size: 12px; cursor: pointer; transition: 0.3s; }
        .paste-btn:hover { background: #fe0979; color: white; box-shadow: 0 0 10px #fe0979;}
        button#mainBtn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; transition: 0.3s; box-shadow: 0 10px 20px rgba(254, 9, 121, 0.4); }
        button#mainBtn:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(254, 9, 121, 0.6); }
        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dots { display: flex; gap: 8px; margin-bottom: 15px; }
        .dot { width: 14px; height: 14px; background: #fe0979; border-radius: 50%; animation: bounce 0.5s infinite alternate; }
        .dot:nth-child(2) { animation-delay: 0.1s; background: #f5af19; }
        .dot:nth-child(3) { animation-delay: 0.2s; background: #00f2fe; }
        @keyframes bounce { to { transform: translateY(-12px); } }
        #loaderText { font-size: 14px; color: #00f2fe; font-weight: 600; letter-spacing: 1px;}
        #result { margin-top: 30px; display: none; width: 100%; text-align: left; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        .media-preview { width: 100%; max-height: 400px; border-radius: 12px; margin-bottom: 20px; border: 2px solid rgba(0, 242, 254, 0.3); box-shadow: 0 10px 20px rgba(0,0,0,0.6); background: #000; object-fit: contain; }
        audio { width: 100%; height: 45px; margin-bottom: 20px; border-radius: 12px; }
        .caption-box { background: rgba(0,0,0,0.5); padding: 15px; border-radius: 10px; margin-bottom: 20px; font-size: 13px; color: #eee; border-left: 4px solid #f5af19; max-height: 90px; overflow-y: auto; position: relative;}
        .copy-btn { position: absolute; right: 10px; top: 10px; background: #f5af19; color: #000; border: none; border-radius: 6px; padding: 5px 12px; font-size: 10px; cursor: pointer; font-weight: 800;}
        .dl-group { display: flex; flex-direction: column; gap: 15px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 16px; color: #000; border-radius: 12px; font-weight: 800; font-size: 15px; transition: 0.3s; text-transform: uppercase; letter-spacing: 0.5px;}
        .dl-btn:hover { transform: scale(1.03); }
        .btn-main { background: #00f2fe; box-shadow: 0 5px 15px rgba(0, 242, 254, 0.3); } 
        .btn-audio { background: #b100ff; color: white; box-shadow: 0 5px 15px rgba(177, 0, 255, 0.3); } 
        .btn-whatsapp { background: #25D366; color: white; box-shadow: 0 5px 15px rgba(37, 211, 102, 0.3);} 
        .btn-earning { background: linear-gradient(90deg, #f5af19, #f12711); color: white; box-shadow: 0 5px 15px rgba(241, 39, 17, 0.4); border: 2px solid #ffcc00; animation: gentleShake 3s infinite;}
        @keyframes gentleShake { 0%, 100% {transform: rotate(0deg);} 10%, 30%, 50% {transform: rotate(-1deg);} 20%, 40%, 60% {transform: rotate(1deg);} 70% {transform: rotate(0deg);} }
        .shayari-corner { margin-top: 40px; padding: 20px; background: rgba(254, 9, 121, 0.05); border: 1px solid rgba(254, 9, 121, 0.3); border-left: 5px solid #fe0979; border-right: 5px solid #00f2fe; border-radius: 15px; text-align: center; box-shadow: inset 0 0 20px rgba(0,0,0,0.5); }
        .shayari-corner h3 { color: #00f2fe; margin: 0 0 10px 0; font-size: 16px; text-transform: uppercase; letter-spacing: 1px;}
        .shayari-corner p { font-style: italic; color: #fff; font-size: 14px; margin: 0 0 12px 0; font-weight: 400; line-height: 1.5; min-height: 45px;}
        .shayari-corner a { color: #fe0979; font-weight: 800; font-size: 13px; text-decoration: none; padding: 5px 15px; border: 1px solid #fe0979; border-radius: 20px; display: inline-block; transition: 0.3s;}
        .shayari-corner a:hover { background: #fe0979; color: #fff; box-shadow: 0 0 10px #fe0979;}
        .services-banner { margin-top: 30px; padding: 20px; background: rgba(0, 0, 0, 0.5); border: 1px dashed #00f2fe; border-radius: 15px; font-size: 13px; line-height: 1.6;}
        .services-banner b { color: #00f2fe; font-size: 15px;}
        .services-banner a { display: inline-block; margin-top: 10px; background: transparent; border: 1px solid #00f2fe; color: #00f2fe; padding: 8px 20px; border-radius: 8px; font-weight: bold; text-decoration: none; transition: 0.3s;}
        .services-banner a:hover { background: #00f2fe; color: #000; box-shadow: 0 0 15px #00f2fe; }
        .seo-section { max-width: 440px; width: 92%; padding: 30px 25px; border-radius: 20px; background: rgba(15, 10, 25, 0.8); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6); margin-bottom: 30px; text-align: left; }
        .seo-section h2 { color: #f5af19; font-size: 18px; margin-top: 0; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid rgba(245, 175, 25, 0.3); padding-bottom: 10px;}
        .faq-item { margin-bottom: 15px; }
        .faq-item h3 { color: #00f2fe; font-size: 14px; margin: 0 0 8px 0; font-weight: 700; }
        .faq-item p { color: #bbb; font-size: 12px; margin: 0; line-height: 1.6; font-weight: 300; }
        .footer-area { margin-top: 10px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); width: 100%; max-width: 440px; }
        .social-links { display: flex; justify-content: center; gap: 20px; margin-bottom: 15px; }
        .social-links a { color: #aaa; text-decoration: none; font-size: 13px; font-weight: 600; transition: 0.3s; }
        .social-links a:hover { color: #00f2fe; }
        .live-count-badge { display: inline-block; background: rgba(0, 242, 254, 0.1); padding: 5px 15px; border-radius: 20px; border: 1px solid #00f2fe; color: #00f2fe; font-size: 12px; font-weight: 700; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;}
        .pulse-dot { height: 8px; width: 8px; background-color: #00f2fe; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 10px #00f2fe; animation: live-pulse 1.5s infinite;}
        @keyframes live-pulse { 0% { transform: scale(0.95); opacity: 1; } 70% { transform: scale(1.5); opacity: 0; } 100% { transform: scale(0.95); opacity: 0; } }
        #toast { visibility: hidden; min-width: 250px; background: #fe0979; color: #fff; text-align: center; border-radius: 10px; padding: 15px; position: fixed; z-index: 1000; left: 50%; bottom: 30px; font-size: 14px; font-weight: 700; transform: translateX(-50%); box-shadow: 0 10px 30px rgba(0,0,0,0.8);}
        #toast.show { visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }
        .adsterra-box { width: 100%; max-width: 440px; margin: 0 auto 20px auto; min-height: 50px; display: flex; justify-content: center; align-items: center; overflow: hidden; border-radius: 12px;}
        .floating-wa { position: fixed; bottom: 25px; right: 25px; background: #25D366; color: white; border-radius: 50%; width: 55px; height: 55px; display: flex; align-items: center; justify-content: center; font-size: 28px; box-shadow: 0 0 20px rgba(37,211,102,0.6); text-decoration: none; z-index: 1000; transition: 0.3s; border: 2px solid rgba(255,255,255,0.2); }
        .floating-wa:hover { transform: scale(1.1) rotate(10deg); }
    </style>
</head>
<body>

<div class="ambient-glow"></div>
<div class="ambient-glow"></div>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">🔥 Join Telegram For Movies: @CineTrixaHub</a>

<div class="main-card">
    <h1>Save Pro</h1>
    <p class="subtitle">Next-Gen Media Engine</p>
    
    <div class="input-wrapper">
        <input type="text" id="videoUrl" placeholder="Paste IG, YT, FB link here...">
        <button class="paste-btn" onclick="pasteFromClipboard()">PASTE</button>
    </div>

    <button id="mainBtn" onclick="startProcess()">UNLOCK MEDIA</button>
    
    <div id="fullLoader">
        <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
        <div id="loaderText">Fetching High Quality File...</div>
    </div>

    <div id="limitMsg" style="margin-top:15px; font-size:12px; color:#00f2fe; font-weight:600;">🎁 Unlimited Downloads Active!</div>

    <div id="result">
        <div class="caption-box" id="captionWrap" style="display:none;">
            <span id="vidTitle"></span>
            <button class="copy-btn" onclick="copyCaption()">COPY</button>
        </div>
        
        <div id="mediaContainer"></div>
        <audio id="audioPlayer" controls style="display:none;"></audio>
        
        <div class="dl-group">
            <a id="downloadBtn" class="dl-btn btn-main" href="#" target="_blank">📥 SAVE HD MEDIA</a>
            <a id="audioBtn" class="dl-btn btn-audio" href="#" target="_blank" style="display: none;">🎵 SAVE AUDIO (MP3)</a>
            <a class="dl-btn btn-whatsapp" href="whatsapp://send?text=Bhai%20ye%20website%20dekh,%20Insta/YT%20ki%20koi%20bhi%20video%20ek%20click%20me%20download%20hoti%20hai!%20Link:%20https://webearning.vercel.app" target="_blank">📲 SHARE ON WHATSAPP</a>
            <a class="dl-btn btn-earning" href="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js" target="_blank">💰 CLAIM TODAY'S BONUS!</a>
        </div>
    </div>

    <div class="shayari-corner">
        <h3>✨ Creator's Corner</h3>
        <p id="randomShayari">"Rakh hausla wo manzar bhi aayega,<br>Pyaase ke paas chalkar samundar bhi aayega."</p>
        <a href="https://instagram.com/innocent._.foji._.shayar" target="_blank">@innocent._.foji._.shayar</a>
    </div>

    <div class="services-banner">
        💻 <b>Bot ya Website banwani hai?</b><br>
        <span style="color: #aaa; font-size: 11px;">Affordable price mein premium features ke sath!</span><br>
        <a href="https://instagram.com/innocent._.foji._.shayar" target="_blank">🚀 DM on Instagram</a>
    </div>
</div>

<div class="adsterra-box">
    <script async="async" data-cfasync="false" src="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js"></script>
    <div id="container-c05ed5afc6630ec65fedf5ff06fe1b31"></div>
</div>

<div class="seo-section">
    <h2>⚡ How Save Pro Works</h2>
    <div class="faq-item">
        <h3>How to download Instagram Reels?</h3>
        <p>Save Pro is the ultimate Instagram reel downloader. Just paste the reel link, hit unlock, and save the HD MP4 file directly to your gallery.</p>
    </div>
    <div class="faq-item">
        <h3>Is this YouTube Video Downloader Free?</h3>
        <p>Yes! Our YouTube video download free tool lets you save YT shorts and full-length videos in High Definition.</p>
    </div>
</div>

<div class="footer-area">
    <div class="live-count-badge">
        <span class="pulse-dot"></span> 🟢 LIVE VISITORS: <span id="vCount">457</span>
    </div>
    <div class="social-links">
        <a href="https://t.me/CineTrixaHub" target="_blank">📢 Telegram Channel</a>
        <a href="https://t.me/SultanBot" target="_blank">🤖 Download Bot</a>
    </div>
    <p style="color: #555; font-size: 11px; margin: 0 0 20px 0;">© 2026 Save Pro. All Rights Reserved.</p>
</div>

<a href="whatsapp://send?text=Bhai%20ye%20website%20dekh,%20Insta/YT%20ki%20koi%20bhi%20video%20ek%20click%20me%20download%20hoti%20hai!%20Link:%20https://webearning.vercel.app" class="floating-wa" target="_blank">💬</a>

<div id="toast">Message here</div>

<script>
    const fContainer = document.createElement('div'); fContainer.className = 'fireflies';
    for(let i=0; i<25; i++){ 
        let f = document.createElement('div'); f.className = 'firefly'; 
        f.style.left = Math.random() * 100 + 'vw'; f.style.top = Math.random() * 100 + 'vh'; 
        f.style.width = f.style.height = (Math.random() * 3 + 2) + 'px';
        f.style.animationDuration = (Math.random() * 6 + 4) + 's'; f.style.animationDelay = (Math.random() * 5) + 's'; 
        fContainer.appendChild(f); 
    } 
    document.body.appendChild(fContainer);

    setInterval(() => {
        let v = document.getElementById('vCount');
        let current = parseInt(v.innerText);
        let change = Math.floor(Math.random() * 5) + 1;
        if(Math.random() > 0.5) current += change;
        else current -= change;
        v.innerText = current;
    }, 3000);

    const shayaris = [
        '"Rakh hausla wo manzar bhi aayega,<br>Pyaase ke paas chalkar samundar bhi aayega."',
        '"Aag lagi hai dil mein, par dhuan nahi uthta...<br>Ishq ka ye kaisa asar hai, jo ruka nahi rukta."',
        '"Waqt ko apna waqt banane mein waqt lagta hai..."'
    ];
    document.getElementById("randomShayari").innerHTML = shayaris[Math.floor(Math.random() * shayaris.length)];

    function showToast(msg) { let x = document.getElementById("toast"); x.innerText = msg; x.className = "show"; setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000); }
    async function pasteFromClipboard() { try { const text = await navigator.clipboard.readText(); document.getElementById("videoUrl").value = text; showToast("✅ Link Pasted!"); } catch (err) { showToast("⚠️ Long press to paste."); } }
    function copyCaption() { navigator.clipboard.writeText(document.getElementById("vidTitle").innerText); showToast("✅ Caption Copied!"); }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return showToast("⚠️ Paste a link first!");
        
        document.getElementById("result").style.display = "none";
        document.getElementById("mainBtn").style.display = "none";
        document.getElementById("fullLoader").style.display = "flex";

        fetch("/api/download", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ url: url }) })
        .then(res => res.json())
        .then(data => {
            document.getElementById("fullLoader").style.display = "none"; 
            document.getElementById("mainBtn").style.display = "block";
            if(data.success) {
                confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 }});
                if(data.title) { document.getElementById("vidTitle").innerText = data.title; document.getElementById("captionWrap").style.display = "block"; }
                let container = document.getElementById("mediaContainer"); container.innerHTML = "";
                if(data.media_type === "image") {
                    container.innerHTML = `<img src="${data.media_url}" class="media-preview">`;
                } else {
                    container.innerHTML = `<video src="${data.media_url}" poster="${data.thumbnail}" controls playsinline class="media-preview"></video>`;
                }
                document.getElementById("downloadBtn").href = data.media_url;
                if(data.audio_url) {
                    document.getElementById("audioPlayer").src = data.audio_url; 
                    document.getElementById("audioBtn").href = data.audio_url; 
                    document.getElementById("audioBtn").style.display = "flex";
                }
                document.getElementById("result").style.display = "block";
                showToast("✅ Ready!");
            } else { showToast("❌ Error: Media not found."); }
        }).catch(() => { 
            document.getElementById("fullLoader").style.display = "none"; document.getElementById("mainBtn").style.display = "block"; showToast("⚠️ Network Error."); 
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
    # Logic to fix YouTube/Instagram parsing
    clean_url = url.split('?')[0] if "instagram.com" in url or "twitter.com" in url else url
    headers = { "content-type": "application/json", "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    try:
        res = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", json={"url": clean_url}, headers=headers, timeout=15).json()
        media_url = None; audio_url = None; media_type = "video"
        title = res.get('title')
        thumbnail = res.get('thumbnail') or res.get('image') or ""

        # Youtube Smart Extractor
        if 'youtube.com' in clean_url or 'youtu.be' in clean_url:
            media_url = res.get('hd') or res.get('video') or res.get('url')
        else:
            # Standard medias array scanner
            medias = res.get('medias', [])
            for m in medias:
                t = str(m.get('type', '')).lower()
                u = m.get('url')
                if t == 'video' or 'mp4' in str(u):
                    media_url = u; break
                if t == 'image' and not media_url:
                    media_url = u; media_type = "image"
                if t == 'audio': audio_url = u

        if not media_url:
            media_url = res.get('url') or res.get('video') or res.get('image')
        
        if media_url:
            return jsonify({"success": True, "media_url": media_url, "media_type": media_type, "audio_url": audio_url, "thumbnail": thumbnail, "title": title})
        return jsonify({"success": False})
    except: return jsonify({"success": False})

if __name__ == '__main__': app.run()

