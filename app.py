from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sultan Pro | Cyberpunk Media Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        
        /* EXCLUSIVE CYBERPUNK AURORA BACKGROUND */
        body { 
            margin: 0; padding: 0; color: white; text-align: center; 
            background: #05010a; /* Deepest space black */
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.15), transparent 25%);
            min-height: 100vh; display: flex; flex-direction: column; align-items: center; 
            overflow-x: hidden;
        }

        /* Glowing Orbs */
        .ambient-glow { position: fixed; width: 400px; height: 400px; background: #fe0979; border-radius: 50%; filter: blur(150px); opacity: 0.1; animation: float 10s infinite alternate; z-index: -1; }
        .ambient-glow:nth-child(2) { background: #00f2fe; right: -100px; bottom: -100px; animation-duration: 15s; opacity: 0.1; }
        @keyframes float { 0% { transform: translateY(0px) scale(1); } 100% { transform: translateY(-50px) scale(1.1); } }

        /* MAGICAL FIREFLIES */
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 2px #00f2fe; animation: drift 5s ease-in-out infinite alternate; }
        @keyframes drift { 0% { transform: translateY(0) translateX(0) scale(1); opacity: 0.2; } 100% { transform: translateY(-80px) translateX(30px) scale(1.2); opacity: 0.8; } }

        /* VIP TOP BANNER */
        .promo-banner { 
            background: rgba(0, 242, 254, 0.1); 
            padding: 12px 30px; border-radius: 50px; margin-top: 25px; margin-bottom: 20px; 
            font-weight: 700; text-decoration: none; color: #00f2fe; font-size: 14px; 
            border: 1px solid #00f2fe; box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); 
            transition: 0.3s; z-index: 10; letter-spacing: 1px;
        }
        .promo-banner:hover { transform: scale(1.05); background: #00f2fe; color: #000; }

        /* MAIN NEON CARD */
        .main-card { 
            max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; 
            background: rgba(15, 10, 25, 0.7); backdrop-filter: blur(25px); 
            border-top: 2px solid rgba(254, 9, 121, 0.5);
            border-bottom: 2px solid rgba(0, 242, 254, 0.5);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8); 
            margin-top: 10px; margin-bottom: 20px; position: relative; 
        }

        h1 { margin: 0; font-size: 40px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; text-transform: uppercase;}
        p.subtitle { color: #00f2fe; font-size: 13px; margin-bottom: 30px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase;}

        /* INPUT BOX */
        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 90px 18px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 15px; background: rgba(0,0,0,0.6); color: #fff; outline: none; transition: 0.3s; }
        .input-wrapper input:focus { border-color: #fe0979; background: rgba(0,0,0,0.9); box-shadow: 0 0 15px rgba(254, 9, 121, 0.4); }
        .paste-btn { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: transparent; color: #fe0979; border: 1px solid #fe0979; border-radius: 8px; padding: 10px 18px; font-weight: 700; font-size: 12px; cursor: pointer; transition: 0.3s; }
        .paste-btn:hover { background: #fe0979; color: white; box-shadow: 0 0 10px #fe0979;}

        /* MAIN ACTION BUTTON */
        button#mainBtn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; transition: 0.3s; box-shadow: 0 10px 20px rgba(254, 9, 121, 0.4); }
        button#mainBtn:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(254, 9, 121, 0.6); }

        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dots { display: flex; gap: 8px; margin-bottom: 15px; }
        .dot { width: 14px; height: 14px; background: #fe0979; border-radius: 50%; animation: bounce 0.5s infinite alternate; }
        .dot:nth-child(2) { animation-delay: 0.1s; background: #f5af19; }
        .dot:nth-child(3) { animation-delay: 0.2s; background: #00f2fe; }
        @keyframes bounce { to { transform: translateY(-12px); } }
        #loaderText { font-size: 14px; color: #00f2fe; font-weight: 600; letter-spacing: 1px;}

        .limit-text { margin-top: 15px; font-size: 12px; color: #00f2fe; font-weight: 600; }
        
        #result { margin-top: 30px; display: none; width: 100%; text-align: left; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        
        /* PLAYER FIXED CSS */
        .media-preview { width: 100%; max-height: 400px; border-radius: 12px; margin-bottom: 20px; border: 2px solid rgba(0, 242, 254, 0.3); box-shadow: 0 10px 20px rgba(0,0,0,0.6); background: #000; object-fit: contain; }
        audio { width: 100%; height: 45px; margin-bottom: 20px; border-radius: 12px; }

        .caption-box { background: rgba(0,0,0,0.5); padding: 15px; border-radius: 10px; margin-bottom: 20px; font-size: 13px; color: #eee; border-left: 4px solid #f5af19; max-height: 90px; overflow-y: auto; position: relative;}
        .copy-btn { position: absolute; right: 10px; top: 10px; background: #f5af19; color: #000; border: none; border-radius: 6px; padding: 5px 12px; font-size: 10px; cursor: pointer; font-weight: 800;}

        /* DISTINCT BUTTON COLORS */
        .dl-group { display: flex; flex-direction: column; gap: 15px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 16px; color: #000; border-radius: 12px; font-weight: 800; font-size: 15px; transition: 0.3s; text-transform: uppercase; letter-spacing: 0.5px;}
        .dl-btn:hover { transform: scale(1.03); }
        
        .btn-main { background: #00f2fe; box-shadow: 0 5px 15px rgba(0, 242, 254, 0.3); } /* Cyan for Video/Image */
        .btn-audio { background: #b100ff; color: white; box-shadow: 0 5px 15px rgba(177, 0, 255, 0.3); } /* Purple for Audio */
        .btn-whatsapp { background: #25D366; color: white; box-shadow: 0 5px 15px rgba(37, 211, 102, 0.3);} /* Green for WhatsApp */
        .btn-earning { background: linear-gradient(90deg, #f5af19, #f12711); color: white; box-shadow: 0 5px 15px rgba(241, 39, 17, 0.4); border: 2px solid #ffcc00;} /* Yellow/Red for Earning */

        /* ATTRACTIVE SHAYARI CORNER */
        .shayari-corner { 
            margin-top: 40px; padding: 20px; 
            background: rgba(254, 9, 121, 0.05); 
            border: 1px solid rgba(254, 9, 121, 0.3);
            border-left: 5px solid #fe0979;
            border-right: 5px solid #00f2fe;
            border-radius: 15px; text-align: center;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
        }
        .shayari-corner h3 { color: #00f2fe; margin: 0 0 10px 0; font-size: 16px; text-transform: uppercase; letter-spacing: 1px;}
        .shayari-corner p { font-style: italic; color: #fff; font-size: 14px; margin: 0 0 12px 0; font-weight: 400; line-height: 1.5;}
        .shayari-corner a { color: #fe0979; font-weight: 800; font-size: 13px; text-decoration: none; padding: 5px 15px; border: 1px solid #fe0979; border-radius: 20px; display: inline-block; transition: 0.3s;}
        .shayari-corner a:hover { background: #fe0979; color: #fff; box-shadow: 0 0 10px #fe0979;}

        /* SULTAN SERVICES BANNER */
        .services-banner { margin-top: 30px; padding: 20px; background: rgba(0, 0, 0, 0.5); border: 1px dashed #00f2fe; border-radius: 15px; font-size: 13px; line-height: 1.6;}
        .services-banner b { color: #00f2fe; font-size: 15px;}
        .services-banner a { display: inline-block; margin-top: 10px; background: transparent; border: 1px solid #00f2fe; color: #00f2fe; padding: 8px 20px; border-radius: 8px; font-weight: bold; text-decoration: none; transition: 0.3s;}
        .services-banner a:hover { background: #00f2fe; color: #000; box-shadow: 0 0 15px #00f2fe; }

        .footer-area { margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); }
        .social-links { display: flex; justify-content: center; gap: 20px; margin-bottom: 15px; }
        .social-links a { color: #aaa; text-decoration: none; font-size: 13px; font-weight: 600; transition: 0.3s; }
        .social-links a:hover { color: #00f2fe; }

        #toast { visibility: hidden; min-width: 250px; background: #fe0979; color: #fff; text-align: center; border-radius: 10px; padding: 15px; position: fixed; z-index: 1000; left: 50%; bottom: 30px; font-size: 14px; font-weight: 700; transform: translateX(-50%); box-shadow: 0 10px 30px rgba(0,0,0,0.8);}
        #toast.show { visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }
        
        .adsterra-box { width: 100%; max-width: 440px; margin: 0 auto 20px auto; min-height: 50px; display: flex; justify-content: center; align-items: center; overflow: hidden; border-radius: 12px;}
    </style>
</head>
<body>

<div class="ambient-glow"></div>
<div class="ambient-glow"></div>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">🔥 Join Telegram For Movies: @CineTrixaHub</a>

<div class="main-card">
    <h1>Sultan Pro</h1>
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

    <div id="limitMsg" class="limit-text">🎁 Unlimited Downloads Active!</div>

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
            
            <a class="dl-btn btn-earning" href="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js" target="_blank">🎁 CLAIM TODAY's BONUS</a>
        </div>
    </div>

    <div class="shayari-corner">
        <h3>✨ Sultan's Creative Corner</h3>
        <p>"Rakh hausla wo manzar bhi aayega,<br>Pyaase ke paas chalkar samundar bhi aayega."</p>
        <a href="https://instagram.com/innocent._.foji._.shayar" target="_blank">@innocent._.foji._.shayar</a>
    </div>

    <div class="services-banner">
        💻 <b>Bot ya Website banwani hai?</b><br>
        <span style="color: #aaa; font-size: 11px;">Affordable price mein premium features ke sath!</span><br>
        <a href="https://instagram.com/innocent._.foji._.shayar" target="_blank">🚀 DM on Instagram</a>
    </div>

    <div class="footer-area">
        <div class="social-links">
            <a href="https://t.me/CineTrixaHub" target="_blank">📢 Telegram Channel</a>
            <a href="https://t.me/SultanBot" target="_blank">🤖 Download Bot</a>
        </div>
        <p style="color: #555; font-size: 11px; margin: 0;">© 2026 Sultan Pro. Made with ❤️</p>
    </div>
</div>

<div class="adsterra-box">
    <script async="async" data-cfasync="false" src="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js"></script>
    <div id="container-c05ed5afc6630ec65fedf5ff06fe1b31"></div>
</div>

<div id="toast">Message here</div>

<script>
    const fContainer = document.createElement('div'); fContainer.className = 'fireflies';
    for(let i=0; i<25; i++){ 
        let f = document.createElement('div'); f.className = 'firefly'; 
        f.style.left = Math.random() * 100 + 'vw'; f.style.top = Math.random() * 100 + 'vh'; 
        let size = Math.random() * 3 + 2; f.style.width = size + 'px'; f.style.height = size + 'px'; 
        f.style.animationDuration = (Math.random() * 6 + 4) + 's'; f.style.animationDelay = (Math.random() * 5) + 's'; 
        fContainer.appendChild(f); 
    } 
    document.body.appendChild(fContainer);

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
                
                if(data.title) { document.getElementById("vidTitle").innerText = data.title; document.getElementById("captionWrap").style.display = "block"; } else { document.getElementById("captionWrap").style.display = "none"; }

                let container = document.getElementById("mediaContainer"); container.innerHTML = "";
                let thumb = data.thumbnail || "";
                
                if(data.media_type === "image") {
                    container.innerHTML = `<img src="${data.media_url}" class="media-preview">`;
                    document.getElementById("downloadBtn").innerText = "📥 SAVE IMAGE (HD)";
                    
                    if(data.audio_url) {
                        document.getElementById("audioPlayer").src = data.audio_url; 
                        document.getElementById("audioPlayer").style.display = "block";
                        document.getElementById("audioBtn").href = data.audio_url; 
                        document.getElementById("audioBtn").style.display = "flex";
                    } else {
                        document.getElementById("audioPlayer").style.display = "none"; document.getElementById("audioBtn").style.display = "none";
                    }
                } else {
                    let thumbAttr = thumb ? `poster="${thumb}"` : '';
                    container.innerHTML = `<video src="${data.media_url}" ${thumbAttr} class="media-preview" controls playsinline preload="metadata"></video>`;
                    document.getElementById("downloadBtn").innerText = "📥 SAVE VIDEO (MP4)";
                    document.getElementById("audioPlayer").style.display = "none"; document.getElementById("audioBtn").style.display = "none";
                }
                
                document.getElementById("downloadBtn").href = data.media_url;
                document.getElementById("result").style.display = "block"; 
                document.getElementById("videoUrl").value = ""; 
                showToast("✅ Ready!");
            } else { showToast("❌ Error: " + data.message); }
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
def home(path): return render_template_string(HTML_PAGE, game_link=GAME_LINK)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    clean_url = url.split('?')[0] if "instagram.com" in url or "twitter.com" in url else url
    
    api_url = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    headers = { "content-type": "application/json", "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    
    try:
        res = requests.post(api_url, json={"url": clean_url}, headers=headers, timeout=15).json()
        media_url = None; audio_url = None; media_type = "video"; title = res.get('title')
        thumbnail = res.get('thumbnail') or res.get('image') or res.get('picture') or ""

        # YOUTUBE STRICT FILTER: Prevents loading webpage links as video
        is_youtube = 'youtube.com' in clean_url or 'youtu.be' in clean_url
        
        medias = res.get('medias', [])
        
        for m in medias:
            t = str(m.get('type', '')).lower()
            url_str = str(m.get('url', ''))
            
            # YouTube specific safeguard: Do not accept original youtube link as media_url
            if is_youtube and ('youtube.com/watch' in url_str or 'youtu.be' in url_str):
                continue
                
            if t == 'video' or 'mp4' in url_str:
                if not media_url: 
                    media_url = url_str; media_type = "video"
                if not thumbnail and m.get('thumbnail'): thumbnail = m.get('thumbnail')
            elif t in ['image', 'photo']:
                if not media_url: media_url = url_str; media_type = "image"
            elif t == 'audio' or 'mp3' in url_str:
                if not audio_url: audio_url = url_str

        # General Fallback
        if not media_url and not is_youtube: 
            media_url = res.get('url') or res.get('video') or res.get('image')
            if media_url and ('youtube.com' in media_url): media_url = None # Reject fake URL

        if not audio_url: audio_url = res.get('audio') or res.get('music')

        if media_url:
            return jsonify({"success": True, "media_url": media_url, "media_type": media_type, "audio_url": audio_url, "title": title, "thumbnail": thumbnail})
        return jsonify({"success": False, "message": "Video protected or not found."})
    except Exception as e:
        return jsonify({"success": False, "message": "Server Timeout."})

if __name__ == '__main__': app.run()
