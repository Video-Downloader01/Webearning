from flask import Flask, request, jsonify, render_template_string
import requests
import random

app = Flask(__name__)

RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'
AD_DIRECT_LINK = "https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>Save Pro | Best Free Instagram Reels & YouTube HD Video Downloader</title>
    <meta name="description" content="Save Pro is the world's fastest free media downloader. Download Instagram Reels with music, YouTube Shorts, and Facebook videos in Ultra HD quality. No login required.">
    <meta name="keywords" content="Save Pro, Instagram downloader, YouTube video downloader HD, FB video saver, Reel download with music, SaveInsta, Download YouTube Shorts, Social Media Tool">
    <meta name="robots" content="index, follow">
    
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { margin: 0; padding: 0; color: white; text-align: center; background: #05010a; background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.1), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.1), transparent 25%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }
        
        .ambient-glow { position: fixed; width: 450px; height: 450px; background: #fe0979; border-radius: 50%; filter: blur(160px); opacity: 0.08; animation: float 10s infinite alternate; z-index: -1; }
        @keyframes float { 0% { transform: translateY(0px); } 100% { transform: translateY(-60px); } }
        
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 2px #fe0979; animation: drift 5s infinite alternate; }
        @keyframes drift { 0% { transform: translate(0,0); opacity: 0.2; } 100% { transform: translate(40px, -100px); opacity: 0.8; } }

        .top-nav { background: rgba(0, 242, 254, 0.1); padding: 12px 25px; border-radius: 50px; margin: 25px 0; border: 1px solid #00f2fe; box-shadow: 0 0 20px rgba(0, 242, 254, 0.2); font-weight: 700; color: #00f2fe; text-decoration: none; font-size: 14px; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.03); } 100% { transform: scale(1); } }

        .main-card { max-width: 450px; width: 92%; padding: 45px 25px; border-radius: 30px; background: rgba(15, 10, 25, 0.75); backdrop-filter: blur(30px); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9); position: relative; margin-bottom: 30px;}
        
        h1 { margin: 0; font-size: 45px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -2px; }
        .subtitle { color: #00f2fe; font-size: 12px; letter-spacing: 3px; font-weight: 600; text-transform: uppercase; margin-bottom: 35px; }

        .input-box { width: 100%; padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.6); color: #fff; font-size: 15px; outline: none; margin-bottom: 20px; transition: 0.3s; }
        .input-box:focus { border-color: #fe0979; box-shadow: 0 0 20px rgba(254, 9, 121, 0.3); }

        .main-btn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 20px; border-radius: 15px; width: 100%; font-weight: 800; cursor: pointer; font-size: 18px; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 10px 30px rgba(254, 9, 121, 0.4); transition: 0.3s; }
        .main-btn:hover { transform: translateY(-4px); box-shadow: 0 15px 40px rgba(254, 9, 121, 0.6); }

        /* EARNING BOOSTER: SPECIAL GIFT BUTTON */
        .gift-btn { background: linear-gradient(90deg, #f5af19, #f12711); color: white; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 13px; display: block; margin: 20px 0; border: 2px dashed #fff; animation: shake 4s infinite; }
        @keyframes shake { 0%, 100% {transform: rotate(0deg);} 10% {transform: rotate(2deg);} 20% {transform: rotate(-2deg);} }

        #result { margin-top: 35px; display: none; text-align: left; }
        .media-preview { width: 100%; border-radius: 15px; border: 2px solid #00f2fe; background: #000; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }

        .dl-group { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
        .dl-btn { text-decoration: none; padding: 18px; border-radius: 15px; font-weight: 800; font-size: 15px; text-align: center; transition: 0.3s; text-transform: uppercase; }
        .btn-hd { background: #00f2fe; color: #000; box-shadow: 0 5px 20px rgba(0, 242, 254, 0.3); }
        .btn-wa { background: #25D366; color: #fff; }

        .shayari-box { margin-top: 40px; padding: 20px; background: rgba(254, 9, 121, 0.05); border-radius: 20px; border: 1px solid rgba(254, 9, 121, 0.2); position: relative; }
        .shayari-box i { color: #fe0979; font-size: 12px; display: block; margin-bottom: 10px; }
        .shayari-text { font-style: italic; font-size: 14px; line-height: 1.6; color: #eee; }

        /* SEO & VISITOR COUNTER SECTION */
        .footer-info { max-width: 450px; width: 92%; text-align: left; margin-bottom: 50px; }
        .visitor-count { display: inline-block; background: rgba(0, 242, 254, 0.1); padding: 5px 15px; border-radius: 20px; border: 1px solid #00f2fe; color: #00f2fe; font-size: 11px; font-weight: 700; margin-bottom: 20px; }
        .seo-content h2 { font-size: 18px; color: #f5af19; margin-bottom: 10px; }
        .seo-content p { font-size: 12px; color: #888; line-height: 1.6; }

        .floating-wa { position: fixed; bottom: 20px; right: 20px; background: #25D366; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; box-shadow: 0 10px 25px rgba(37,211,102,0.5); z-index: 1000; text-decoration: none; }
        
        #toast { visibility: hidden; min-width: 200px; background: #fe0979; color: #fff; text-align: center; border-radius: 10px; padding: 15px; position: fixed; z-index: 1001; left: 50%; bottom: 30px; transform: translateX(-50%); font-weight: 700; }
        #toast.show { visibility: visible; animation: fade 3s; }
        @keyframes fade { from {opacity: 0;} to {opacity: 1;} }
    </style>
</head>
<body>

<div class="ambient-glow"></div>

<a href="https://t.me/CineTrixaHub" class="top-nav">🚀 JOIN VIP MOVIE CHANNEL</a>

<div class="main-card">
    <h1>Save Pro</h1>
    <p class="subtitle">Premium Multi-Downloader</p>
    
    <input type="text" id="videoUrl" class="input-box" placeholder="Paste link (Instagram, YouTube, FB)...">
    <button class="main-btn" onclick="startProcess()">Unlock HD Media</button>
    
    <div id="fullLoader" style="display:none; margin-top:20px;">
        <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
        <p style="color:#00f2fe; font-size:12px; font-weight:bold;">BYPASSING SERVERS...</p>
    </div>

    <a href="{{ ad_link }}" target="_blank" class="gift-btn">🎁 CLAIM YOUR DAILY SURPRISE GIFT!</a>

    <div id="result">
        <div id="mediaWrap"></div>
        <div class="dl-group">
            <a id="dlLink" class="dl-btn btn-hd" href="#" target="_blank">📥 DOWNLOAD HD NOW</a>
            <a class="dl-btn btn-wa" href="whatsapp://send?text=Bhai%20Insta/YT%20ki%20reels%20download%20karne%20ka%20best%20tarika!%20Ye%20dekh:%20https://webearning.vercel.app" target="_blank">📲 SHARE ON WHATSAPP</a>
        </div>
    </div>

    <div class="shayari-box">
        <i>--- Random Shayari ---</i>
        <p class="shayari-text" id="shayariDisplay">Loading inspiration...</p>
        <p style="font-size:10px; color:#fe0979; margin-top:10px;">@innocent._.foji._.shayar</p>
    </div>
</div>

<div class="footer-info">
    <div class="visitor-count">🟢 LIVE VISITORS: <span id="vCount">482</span></div>
    
    <div class="seo-content">
        <h2>About Save Pro Downloader</h2>
        <p>Save Pro is the world's leading <b>free Instagram reel downloader</b> and <b>YouTube video downloader</b>. Our engine extracts the highest quality MP4 files with original music. Whether you want to save a Facebook video, a YouTube short, or an Instagram post with music, Save Pro delivers lightning-fast results without any annoying login. 100% Secure & HD.</p>
    </div>
</div>

<div class="adsterra-box">
    <script async="async" data-cfasync="false" src="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js"></script>
    <div id="container-c05ed5afc6630ec65fedf5ff06fe1b31"></div>
</div>

<a href="whatsapp://send?text=Bhai%20Insta/YT%20reels%20download%20karne%20ke%20liye%20best%20site!%20Ye%20lo:%20https://webearning.vercel.app" class="floating-wa">💬</a>

<div id="toast">Message</div>

<script>
    // MAGICAL PARTICLES
    const fBox = document.createElement('div'); fBox.className = 'fireflies';
    for(let i=0; i<30; i++){ let f=document.createElement('div'); f.className='firefly'; f.style.left=Math.random()*100+'vw'; f.style.top=Math.random()*100+'vh'; fBox.appendChild(f); }
    document.body.appendChild(fBox);

    // LIVE VISITOR SIMULATOR (For trust)
    setInterval(() => {
        let current = parseInt(document.getElementById('vCount').innerText);
        document.getElementById('vCount').innerText = current + (Math.random() > 0.5 ? 1 : -1);
    }, 3000);

    const shayaris = [
        "Rakh hausla wo manzar bhi aayega, Pyaase ke paas chalkar samundar bhi aayega.",
        "Aag lagi hai dil mein, par dhuan nahi uthta... Ishq ka ye kaisa asar hai, jo ruka nahi rukta.",
        "Waqt ko apna waqt banane mein waqt lagta hai... Khamoshi se mehnat kar, safalta shor machayegi.",
        "Manzil mile na mile ye toh muqaddar ki baat hai, Hum koshish bhi na karein, ye toh galat baat hai.",
        "Hawaon ke bharose mat ud, chattanein toofano ka rukh mod deti hain."
    ];
    document.getElementById('shayariDisplay').innerText = shayaris[Math.floor(Math.random()*shayaris.length)];

    function showToast(m) { let t=document.getElementById('toast'); t.innerText=m; t.className='show'; setTimeout(()=>t.className='', 3000); }

    function startProcess() {
        let url = document.getElementById('videoUrl').value;
        if(!url) return showToast("❌ Paste Link First!");
        
        document.getElementById('fullLoader').style.display = 'flex';
        document.getElementById('result').style.display = 'none';

        fetch("/api/download", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({url: url}) })
        .then(res => res.json())
        .then(data => {
            document.getElementById('fullLoader').style.display = 'none';
            if(data.success) {
                confetti({particleCount: 150, spread: 70, origin: {y: 0.6}});
                let wrap = document.getElementById('mediaWrap');
                if(data.media_type === "image") {
                    wrap.innerHTML = `<img src="${data.media_url}" class="media-preview">`;
                } else {
                    wrap.innerHTML = `<video src="${data.media_url}" poster="${data.thumbnail}" controls playsinline class="media-preview"></video>`;
                }
                document.getElementById('dlLink').href = data.media_url;
                document.getElementById('result').style.display = 'block';
                showToast("✅ Ready to Save!");
            } else {
                showToast("❌ Error: Protected Link");
            }
        });
    }
</script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path): return render_template_string(HTML_PAGE, ad_link=AD_DIRECT_LINK)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    clean_url = url.split('?')[0] if "instagram.com" in url or "twitter.com" in url else url
    headers = { "content-type": "application/json", "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    try:
        res = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", json={"url": clean_url}, headers=headers, timeout=15).json()
        media_url = None; media_type = "video"; title = res.get('title')
        thumbnail = res.get('thumbnail') or res.get('image') or ""

        is_yt = 'youtube.com' in clean_url or 'youtu.be' in clean_url
        
        if is_yt:
            media_url = res.get('hd') or res.get('video') or res.get('url')
        else:
            for m in res.get('medias', []):
                t = str(m.get('type', '')).lower()
                if t == 'video' or 'mp4' in str(m.get('url')):
                    media_url = m.get('url'); break
                if t == 'image' and not media_url:
                    media_url = m.get('url'); media_type = "image"
        
        if media_url: return jsonify({"success": True, "media_url": media_url, "media_type": media_type, "thumbnail": thumbnail, "title": title})
        return jsonify({"success": False})
    except: return jsonify({"success": False})

if __name__ == '__main__': app.run()

