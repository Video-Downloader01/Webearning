from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sultan Pro | Premium Media Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        
        /* 5. ROMANTIC LIVE LOVE BACKGROUND */
        body { 
            margin: 0; padding: 0; color: white; text-align: center; 
            background: radial-gradient(circle at top, #3a0d1d, #1a0b1c, #0b0e14); 
            min-height: 100vh; display: flex; flex-direction: column; align-items: center; 
            overflow-x: hidden;
        }

        .ambient-glow { position: fixed; width: 350px; height: 350px; background: #ff0844; border-radius: 50%; filter: blur(120px); opacity: 0.15; animation: float 8s infinite alternate; z-index: -1; }
        .ambient-glow:nth-child(2) { background: #ffb199; right: -50px; bottom: -50px; animation-duration: 12s; opacity: 0.1; }
        @keyframes float { 0% { transform: translateY(0px) scale(1); } 100% { transform: translateY(-40px) scale(1.1); } }

        /* MAGICAL FIREFLIES / LOVE PARTICLES */
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 3px #ff77a9; animation: drift 6s ease-in-out infinite alternate; }
        @keyframes drift { 0% { transform: translateY(0) translateX(0) scale(1); opacity: 0.2; } 100% { transform: translateY(-100px) translateX(40px) scale(1.5); opacity: 0.8; } }

        /* 4. ATTRACTIVE VIP TOP BANNER */
        .promo-banner { 
            background: linear-gradient(90deg, #ff0844 0%, #ffb199 100%); 
            padding: 12px 30px; border-radius: 50px; margin-top: 25px; margin-bottom: 20px; 
            font-weight: 700; text-decoration: none; color: #fff; font-size: 15px; 
            box-shadow: 0 0 20px rgba(255, 8, 68, 0.6); 
            animation: glowingPulse 2s infinite; transition: 0.3s; z-index: 10;
            text-transform: uppercase; letter-spacing: 1px;
        }
        .promo-banner:hover { transform: scale(1.05); }
        @keyframes glowingPulse { 0% { box-shadow: 0 0 15px rgba(255,8,68,0.4); } 50% { box-shadow: 0 0 30px rgba(255,8,68,0.8); } 100% { box-shadow: 0 0 15px rgba(255,8,68,0.4); } }

        /* MAIN CARD */
        .main-card { 
            max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 30px; 
            background: rgba(20, 15, 25, 0.6); backdrop-filter: blur(20px); 
            border: 1px solid rgba(255, 119, 169, 0.15); 
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5); 
            margin-top: 20px; margin-bottom: 20px; position: relative; 
        }

        h1 { margin: 0; font-size: 38px; font-weight: 900; background: linear-gradient(to right, #ff77a9, #ffb347); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px;}
        p.subtitle { color: #aaa; font-size: 13px; margin-bottom: 30px; font-weight: 400; letter-spacing: 1px; text-transform: uppercase;}

        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 90px 18px 20px; border: 1px solid rgba(255,119,169,0.3); border-radius: 16px; font-size: 15px; background: rgba(0,0,0,0.5); color: #fff; outline: none; transition: 0.3s; }
        .input-wrapper input:focus { border-color: #ff0844; background: rgba(0,0,0,0.8); box-shadow: 0 0 20px rgba(255, 8, 68, 0.3); }
        .paste-btn { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: #ff0844; color: white; border: none; border-radius: 10px; padding: 10px 18px; font-weight: 600; font-size: 12px; cursor: pointer; transition: 0.3s; }
        .paste-btn:hover { background: #ffb199; color: black; }

        button#mainBtn { background: linear-gradient(135deg, #ff0844, #ffb199); color: white; border: none; padding: 18px; font-size: 16px; border-radius: 16px; cursor: pointer; width: 100%; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; transition: 0.3s; box-shadow: 0 10px 25px rgba(255, 8, 68, 0.4); }
        button#mainBtn:hover { transform: translateY(-3px); box-shadow: 0 15px 30px rgba(255, 8, 68, 0.6); }

        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dots { display: flex; gap: 8px; margin-bottom: 15px; }
        .dot { width: 12px; height: 12px; background: #ff77a9; border-radius: 50%; animation: bounce 0.5s infinite alternate; }
        .dot:nth-child(2) { animation-delay: 0.1s; background: #ffb347; }
        .dot:nth-child(3) { animation-delay: 0.2s; background: #00cdac; }
        @keyframes bounce { to { transform: translateY(-10px); } }
        #loaderText { font-size: 13px; color: #ff77a9; font-weight: 600; }

        .limit-text { margin-top: 15px; font-size: 12px; color: #ffcc00; font-weight: 500; }
        
        #result { margin-top: 30px; display: none; width: 100%; text-align: left; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        /* 1. THUMBNAIL FIXED CSS */
        .media-preview { width: 100%; max-height: 400px; border-radius: 16px; margin-bottom: 20px; border: 2px solid rgba(255,119,169,0.2); box-shadow: 0 10px 20px rgba(0,0,0,0.5); background: #000; object-fit: contain; }
        audio { width: 100%; height: 45px; margin-bottom: 20px; border-radius: 12px; }

        .caption-box { background: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px; margin-bottom: 20px; font-size: 12px; color: #ddd; border-left: 3px solid #ff77a9; max-height: 80px; overflow-y: auto; position: relative;}
        .copy-btn { position: absolute; right: 10px; top: 10px; background: rgba(255, 119, 169, 0.2); color: #ff77a9; border: none; border-radius: 6px; padding: 4px 10px; font-size: 10px; cursor: pointer; font-weight: bold;}

        .dl-group { display: flex; flex-direction: column; gap: 12px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 16px; color: white; border-radius: 14px; font-weight: 700; font-size: 15px; transition: 0.3s; text-transform: uppercase;}
        .dl-btn:hover { transform: scale(1.02); }
        .btn-main { background: #28a745; box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3); }
        .btn-audio { background: #007bff; box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3); }
        .btn-whatsapp { background: #25D366; color: white; }

        /* 6. NEW EARNING IDEA: DIRECT LINK BUTTON */
        .btn-earning { background: linear-gradient(90deg, #f12711, #f5af19); color: white; box-shadow: 0 5px 15px rgba(245, 175, 25, 0.4); animation: shake 3s infinite;}
        @keyframes shake { 0%, 100% {transform: translateX(0);} 10%, 30%, 50%, 70%, 90% {transform: translateX(-2px);} 20%, 40%, 60%, 80% {transform: translateX(2px);} }

        .services-banner { margin-top: 35px; padding: 18px; background: rgba(255, 8, 68, 0.1); border: 1px solid rgba(255, 8, 68, 0.3); border-radius: 16px; font-size: 13px; line-height: 1.6;}
        .services-banner b { color: #ffb199; font-size: 14px;}
        .services-banner a { display: inline-block; margin-top: 8px; background: #ff0844; color: #fff; padding: 8px 15px; border-radius: 8px; font-weight: bold; text-decoration: none; transition: 0.3s;}
        .services-banner a:hover { transform: scale(1.05); }

        .footer-area { margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); }
        .social-links { display: flex; justify-content: center; gap: 20px; margin-bottom: 15px; }
        .social-links a { color: #aaa; text-decoration: none; font-size: 12px; font-weight: 500; transition: 0.3s; }
        .social-links a:hover { color: #ff77a9; }

        #toast { visibility: hidden; min-width: 250px; background: #fff; color: #000; text-align: center; border-radius: 12px; padding: 15px; position: fixed; z-index: 1000; left: 50%; bottom: 30px; font-size: 14px; font-weight: 700; transform: translateX(-50%); box-shadow: 0 10px 30px rgba(0,0,0,0.5);}
        #toast.show { visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }
        
        .adsterra-box { width: 100%; max-width: 440px; margin: 0 auto 20px auto; min-height: 50px; display: flex; justify-content: center; align-items: center; overflow: hidden; border-radius: 12px;}
    </style>
</head>
<body>

<div class="ambient-glow"></div>
<div class="ambient-glow"></div>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">🌟 Join Telegram For Movies: @CineTrixaHub</a>

<div class="main-card">
    <h1>Sultan Pro</h1>
    <p class="subtitle">Ultimate Media Downloader</p>
    
    <div class="input-wrapper">
        <input type="text" id="videoUrl" placeholder="Paste IG, YT, FB link here...">
        <button class="paste-btn" onclick="pasteFromClipboard()">Paste</button>
    </div>

    <button id="mainBtn" onclick="startProcess()">Unlock Media</button>
    
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
            <a id="downloadBtn" class="dl-btn btn-main" href="#" target="_blank">📥 Save HD Media</a>
            <a id="audioBtn" class="dl-btn btn-audio" href="#" target="_blank" style="display: none;">🎵 Save Audio (MP3)</a>
            <a class="dl-btn btn-whatsapp" href="whatsapp://send?text=Bhai%20ye%20website%20dekh,%20Insta/YT%20ki%20koi%20bhi%20video%20ek%20click%20me%20download%20hoti%20hai!%20Link:%20https://webearning.vercel.app" target="_blank">📲 Share on WhatsApp</a>
            
            <a class="dl-btn btn-earning" href="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js" target="_blank">🎁 Claim Today's Bonus</a>
        </div>
    </div>

    <div class="services-banner">
        💻 <b>Bot ya Website banwani hai?</b><br>
        <span style="color: #ffb199; font-size: 11px;">Affordable price mein premium features ke sath!</span><br>
        <a href="https://instagram.com/innocent._.foji._.shayar" target="_blank">🚀 DM on Instagram</a>
    </div>

    <div class="footer-area">
        <div class="social-links">
            <a href="https://t.me/CineTrixaHub" target="_blank">📢 Telegram Channel</a>
            <a href="https://t.me/SultanBot" target="_blank">🤖 Download Bot</a>
        </div>
        <p style="color: #666; font-size: 11px; margin: 0;">© 2026 Sultan Pro. Made with ❤️</p>
    </div>
</div>

<div class="adsterra-box">
    <script async="async" data-cfasync="false" src="https://pl29084580.profitablecpmratenetwork.com/c05ed5afc6630ec65fedf5ff06fe1b31/invoke.js"></script>
    <div id="container-c05ed5afc6630ec65fedf5ff06fe1b31"></div>
</div>

<div id="toast">Message here</div>

<script>
    // MAGICAL FIREFLIES CREATION
    const fContainer = document.createElement('div'); fContainer.className = 'fireflies';
    for(let i=0; i<35; i++){ 
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
                    document.getElementById("downloadBtn").innerText = "📥 Save Image (HD)";
                    
                    if(data.audio_url) {
                        document.getElementById("audioPlayer").src = data.audio_url; 
                        document.getElementById("audioPlayer").style.display = "block";
                        document.getElementById("audioBtn").href = data.audio_url; 
                        document.getElementById("audioBtn").style.display = "flex";
                    } else {
                        document.getElementById("audioPlayer").style.display = "none"; document.getElementById("audioBtn").style.display = "none";
                    }
                } else {
                    // 1. THUMBNAIL FIX: 'poster' tag added to show thumbnail before playing
                    let thumbAttr = thumb ? `poster="${thumb}"` : '';
                    container.innerHTML = `<video src="${data.media_url}" ${thumbAttr} class="media-preview" controls playsinline preload="metadata"></video>`;
                    document.getElementById("downloadBtn").innerText = "📥 Save Video (MP4)";
                    
                    document.getElementById("audioPlayer").style.display = "none"; document.getElementById("audioBtn").style.display = "none";
                }
                
                document.getElementById("downloadBtn").href = data.media_url;
                document.getElementById("result").style.display = "block"; 
                document.getElementById("videoUrl").value = ""; 
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
def home(path): return render_template_string(HTML_PAGE, game_link=GAME_LINK)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    clean_url = url.split('?')[0] if "instagram.com" in url or "twitter.com" in url else url
    
    api_url = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    headers = { "content-type": "application/json", "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    
    try:
        res = requests.post(api_url, json={"url": clean_url}, headers=headers, timeout=12).json()
        media_url = None; audio_url = None; media_type = "video"; title = res.get('title')
        thumbnail = res.get('thumbnail') or res.get('image') or res.get('picture') or ""

        # 2. YOUTUBE SMART FILTER (Quality & Audio Fix)
        is_youtube = 'youtube.com' in clean_url or 'youtu.be' in clean_url
        
        if is_youtube:
            # YouTube ke liye direct main URL uthana hai (isme audio + video HD dono hote hain)
            media_url = res.get('hd') or res.get('video') or res.get('url')
            media_type = "video"
            if not thumbnail: thumbnail = res.get('thumbnail')
        else:
            # Instagram/Facebook ke liye normal filter
            medias = res.get('medias', [])
            for m in medias:
                t = str(m.get('type', '')).lower()
                url_str = str(m.get('url', ''))
                
                if t == 'video':
                    media_url = url_str; media_type = "video"
                    if not thumbnail and m.get('thumbnail'): thumbnail = m.get('thumbnail')
                elif t in ['image', 'photo']:
                    if not media_url: media_url = url_str; media_type = "image"
                elif t == 'audio':
                    audio_url = url_str

            # Fallback for hidden links
            if not media_url:
                for m in medias:
                    url_str = str(m.get('url', ''))
                    if 'mp4' in url_str and 'audio' not in url_str:
                        media_url = url_str; media_type = "video"
                        break

            if not media_url: media_url = res.get('url') or res.get('video') or res.get('image')
            if not audio_url: audio_url = res.get('audio') or res.get('music')

        if media_url:
            return jsonify({"success": True, "media_url": media_url, "media_type": media_type, "audio_url": audio_url, "title": title, "thumbnail": thumbnail})
        return jsonify({"success": False, "message": "Link private or not found."})
    except Exception as e:
        return jsonify({"success": False, "message": "Server Timeout."})

if __name__ == '__main__': app.run()

