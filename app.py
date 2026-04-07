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
    <title>Sultan Pro | Premium All-in-One Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; margin: 0; padding: 0; color: white; text-align: center; background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e); overflow-x: hidden; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: start; }
        .fireflies { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; }
        .firefly { position: absolute; background: #fff; border-radius: 50%; box-shadow: 0 0 10px 3px #ff77a9; animation: drift ease-in-out infinite alternate; }
        @keyframes drift { 0% { transform: translateY(0) translateX(0) scale(1); opacity: 0.3; } 100% { transform: translateY(-80px) translateX(50px) scale(1.5); opacity: 1; } }
        .promo-banner { background: rgba(255, 255, 255, 0.1); padding: 10px 20px; border-radius: 50px; margin-top: 20px; margin-bottom: 20px; font-weight: 600; text-decoration: none; color: #ff77a9; font-size: 14px; display: inline-block; backdrop-filter: blur(5px); border: 1px solid rgba(255, 119, 169, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3); transition: 0.3s; z-index: 10; }
        .main-card { max-width: 460px; width: 90%; padding: 35px 25px; border-radius: 25px; background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7); margin-bottom: 20px; position: relative; z-index: 10; }
        h1 { margin: 0; font-size: 34px; font-weight: 700; color: #ffffff; text-shadow: 0 2px 10px rgba(255, 119, 169, 0.5); }
        p.subtitle { color: #ccc; font-size: 14px; margin-bottom: 25px; font-weight: 400; }
        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 16px 85px 16px 15px; border: none; border-radius: 12px; font-size: 15px; background: rgba(255, 255, 255, 0.95); color: #000; outline: none; font-family: inherit; transition: 0.3s; }
        .paste-btn { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: #ff77a9; color: white; border: none; border-radius: 8px; padding: 8px 15px; font-weight: 600; font-size: 13px; cursor: pointer; transition: 0.3s; }
        button#mainBtn { background: linear-gradient(90deg, #ff416c, #ff4b2b); color: white; border: none; padding: 16px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 600; transition: 0.3s; font-family: inherit; box-shadow: 0 8px 20px rgba(255, 65, 108, 0.4); }
        .limit-text { margin-top: 15px; font-size: 13px; color: #ffcc00; font-weight: 600; }
        .progress-container { width: 100%; background-color: rgba(255,255,255,0.1); border-radius: 10px; margin-top: 15px; display: none; overflow: hidden;}
        .progress-bar { width: 0%; height: 6px; background: linear-gradient(90deg, #00cdac, #02aab0); border-radius: 10px; transition: width 0.4s ease; }
        #loadingText { display: none; margin-top: 10px; font-size: 14px; color: #ff77a9; font-weight: 600; }
        .smart-ad-box { display: none; background: rgba(0,0,0,0.8); padding: 25px; border-radius: 20px; margin-top: 25px; border: 2px dashed #ffcc00; }
        .timer-text { font-size: 26px; font-weight: 700; color: #ffcc00; margin-bottom: 15px; }
        .game-ad { display: block; background: linear-gradient(90deg, #02aab0, #00cdac); color: white; padding: 15px; border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 18px; margin-top: 15px; animation: pulse 1.5s infinite; transition: 0.3s; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
        #result { margin-top: 25px; display: none; text-align: left; }
        video, img#imgPlayer { width: 100%; border-radius: 15px; border: 2px solid rgba(255,255,255,0.1); margin-bottom: 10px; background: #000; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
        audio { width: 100%; height: 40px; margin-bottom: 15px; border-radius: 10px; outline: none; }
        .caption-wrapper { position: relative; margin-bottom: 15px; }
        .caption-box { background: rgba(255,255,255,0.05); padding: 12px 40px 12px 12px; border-radius: 10px; font-size: 13px; color: #eee; border-left: 3px solid #ff77a9; max-height: 80px; overflow-y: auto; word-wrap: break-word; }
        .copy-btn { position: absolute; right: 5px; top: 5px; background: #ff77a9; color: white; border: none; border-radius: 5px; padding: 5px 10px; font-size: 11px; cursor: pointer; font-weight: bold;}
        .dl-group { display: flex; flex-direction: column; gap: 10px; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 14px; color: white; border-radius: 10px; font-weight: 600; font-size: 15px; transition: 0.3s; cursor: pointer;}
        .btn-mp4 { background: #28a745; }
        .btn-mp3 { background: #007bff; }
        .btn-mix { background: linear-gradient(90deg, #8E2DE2, #4A00E0); border: none; }
        .btn-whatsapp { background: #25D366; margin-top: 5px; }
        .footer { width: 100%; max-width: 460px; padding: 20px; background: rgba(0,0,0,0.4); border-radius: 20px 20px 0 0; text-align: center; font-size: 12px; color: #aaa; margin-top: auto; }
        .footer-links { display: flex; justify-content: center; gap: 15px; margin-bottom: 10px; flex-wrap: wrap; }
        .footer-links a { color: #ff77a9; text-decoration: none; font-weight: 600; }
        #toast { visibility: hidden; min-width: 250px; background-color: #333; color: #fff; text-align: center; border-radius: 10px; padding: 16px; position: fixed; z-index: 1000; left: 50%; bottom: 30px; font-size: 14px; font-weight: 600; transform: translateX(-50%); box-shadow: 0 4px 15px rgba(0,0,0,0.5); border-bottom: 3px solid #ff416c; }
        #toast.show { visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }
        @keyframes fadein { from {bottom: 0; opacity: 0;} to {bottom: 30px; opacity: 1;} }
        @keyframes fadeout { from {bottom: 30px; opacity: 1;} to {bottom: 0; opacity: 0;} }
    </style>
</head>
<body>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">✨ Join Telegram For Movies: @CineTrixaHub</a>

<div class="main-card">
    <h1>Sultan Pro</h1>
    <p class="subtitle">Video, Image & Audio Downloader</p>
    
    <div class="input-wrapper">
        <input type="text" id="videoUrl" placeholder="Paste link (Insta, YT, FB)...">
        <button class="paste-btn" onclick="pasteFromClipboard()">Paste</button>
    </div>

    <button id="mainBtn" onclick="startProcess()">Download Now</button>
    
    <div class="progress-container" id="progContainer"><div class="progress-bar" id="progBar"></div></div>
    <div id="loadingText">✨ Analyzing magical link...</div>
    <div id="limitMsg" class="limit-text">🎁 3 Free downloads left today.</div>

    <div class="smart-ad-box" id="smartAd">
        <div class="timer-text">🔓 Unlocking in <span id="timerCount">10</span>s</div>
        <a href="{{ game_link }}" target="_blank" class="game-ad">🎮 Play & Win ₹500 Cash!</a><br>
        <button id="unlockBtn" style="display: none; background: #ff77a9; color: white; padding: 12px; border-radius:8px; border:none; font-weight:600; cursor:pointer;" onclick="fetchVideoAPI()">🚀 Continue Download</button>
    </div>

    <div id="result">
        <div class="caption-wrapper" id="captionWrap" style="display:none;">
            <div id="vidTitle" class="caption-box"></div>
            <button class="copy-btn" onclick="copyCaption()">Copy</button>
        </div>
        
        <video id="vidPlayer" controls style="display:none;"></video>
        <img id="imgPlayer" style="display:none;" />
        <audio id="audioPlayer" controls style="display:none;"></audio>
        
        <div class="dl-group">
            <a id="downloadBtn" class="dl-btn btn-mp4" href="#" target="_blank">📥 Save File (HD)</a>
            <button id="mixBtn" class="dl-btn btn-mix" style="display: none;" onclick="startMixing()">✨ Download Photo + Music (MP4 Video)</button>
            <a id="audioBtn" class="dl-btn btn-mp3" href="#" target="_blank" style="display: none;">🎵 Download Only Music (MP3)</a>
            <a class="dl-btn btn-whatsapp" href="whatsapp://send?text=Bhai%20ye%20website%20dekh,%20Insta/YT%20ki%20koi%20bhi%20video/photo%201%20click%20me%20download%20hoti%20hai!%20Link:%20https://webearning.vercel.app" data-action="share/whatsapp/share" target="_blank">📲 Share on WhatsApp</a>
        </div>
    </div>
</div>

<div class="footer">
    <div class="footer-links">
        <a href="https://t.me/CineTrixaHub" target="_blank">Telegram</a> • 
        <a href="https://t.me/SultanBot" target="_blank">Download Bot</a> • 
        <a href="https://instagram.com/innocent._.foji._.shayar" target="_blank">Instagram</a>
    </div>
    <p>© 2026 Sultan Pro Downloader.</p>
</div>

<div id="toast">Message here</div>

<script>
    const fContainer = document.createElement('div'); fContainer.className = 'fireflies';
    for(let i=0; i<30; i++){ let f = document.createElement('div'); f.className = 'firefly'; f.style.left = Math.random() * 100 + 'vw'; f.style.top = Math.random() * 100 + 'vh'; let size = Math.random() * 3 + 2; f.style.width = size + 'px'; f.style.height = size + 'px'; f.style.animationDuration = (Math.random() * 6 + 4) + 's'; f.style.animationDelay = (Math.random() * 5) + 's'; fContainer.appendChild(f); } document.body.appendChild(fContainer);

    function showToast(msg) { let x = document.getElementById("toast"); x.innerText = msg; x.className = "show"; setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000); }
    async function pasteFromClipboard() { try { const text = await navigator.clipboard.readText(); document.getElementById("videoUrl").value = text; showToast("✅ Link Pasted!"); } catch (err) { showToast("⚠️ Cannot read clipboard."); } }
    function copyCaption() { navigator.clipboard.writeText(document.getElementById("vidTitle").innerText); showToast("✅ Caption Copied!"); }
    function fireConfetti() { confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 }, colors: ['#ff77a9', '#00cdac', '#ffcc00'] }); }

    let count = parseInt(localStorage.getItem('dl_count')) || 0; let pendingUrl = "";
    let globalImgUrl = ""; let globalAudioUrl = "";

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) { showToast("⚠️ Please paste a valid link first!"); return; }
        document.getElementById("result").style.display = "none"; document.getElementById("captionWrap").style.display = "none"; document.getElementById("audioBtn").style.display = "none"; document.getElementById("audioPlayer").style.display = "none"; document.getElementById("mixBtn").style.display = "none"; pendingUrl = url;
        if(count >= 3) {
            document.getElementById("mainBtn").style.display = "none"; document.getElementById("limitMsg").style.display = "none"; document.getElementById("smartAd").style.display = "block";
            let timeLeft = 10; document.getElementById("timerCount").innerText = timeLeft;
            let timer = setInterval(function() { timeLeft--; document.getElementById("timerCount").innerText = timeLeft; if(timeLeft <= 0) { clearInterval(timer); document.getElementById("timerCount").parentNode.innerHTML = "Unlocked!"; document.getElementById("unlockBtn").style.display = "block"; } }, 1000);
        } else { document.getElementById("mainBtn").style.display = "none"; startLoadingAnim(); fetchVideoAPI(); }
    }

    function startLoadingAnim() {
        document.getElementById("smartAd").style.display = "none"; document.getElementById("progContainer").style.display = "block"; document.getElementById("loadingText").style.display = "block"; document.getElementById("loadingText").innerText = "✨ Analyzing magical link...";
        let bar = document.getElementById("progBar"); let width = 10; bar.style.width = width + "%";
        let int = setInterval(() => { if(width >= 85) { clearInterval(int); } else { width += 5; bar.style.width = width + "%"; } }, 300);
    }

    function fetchVideoAPI() {
        fetch("/api/download", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ url: pendingUrl }) })
        .then(response => response.json())
        .then(data => {
            document.getElementById("progContainer").style.display = "none"; document.getElementById("loadingText").style.display = "none"; document.getElementById("mainBtn").style.display = "block";
            if(data.success) {
                fireConfetti(); count++; localStorage.setItem('dl_count', count);
                if(data.title) { document.getElementById("vidTitle").innerText = data.title; document.getElementById("captionWrap").style.display = "block"; }

                if(data.media_type === "image") {
                    document.getElementById("imgPlayer").src = data.media_url; document.getElementById("imgPlayer").style.display = "block"; document.getElementById("vidPlayer").style.display = "none"; document.getElementById("downloadBtn").innerText = "📥 Save Image (HD)";
                    globalImgUrl = data.media_url;
                } else {
                    document.getElementById("vidPlayer").src = data.media_url; document.getElementById("vidPlayer").style.display = "block"; document.getElementById("imgPlayer").style.display = "none"; document.getElementById("downloadBtn").innerText = "📥 Save Video (MP4 HD)";
                }
                document.getElementById("downloadBtn").href = data.media_url;
                
                if(data.audio_url) {
                    globalAudioUrl = data.audio_url;
                    document.getElementById("audioPlayer").src = data.audio_url; document.getElementById("audioPlayer").style.display = "block"; document.getElementById("audioBtn").href = data.audio_url; document.getElementById("audioBtn").style.display = "flex";
                    
                    if(data.media_type === "image") { document.getElementById("mixBtn").style.display = "flex"; }
                }

                document.getElementById("result").style.display = "block"; document.getElementById("videoUrl").value = ""; showToast("✅ File Ready!");
            } else { showToast("❌ Error: Link is invalid or private."); }
        }).catch(err => { document.getElementById("progContainer").style.display = "none"; document.getElementById("loadingText").style.display = "none"; document.getElementById("mainBtn").style.display = "block"; showToast("⚠️ Network Error. Try again!"); });
    }

    // THE UPDATED BULLETPROOF MIX FUNCTION
    function startMixing() {
        let renderAPI = "https://sultan-mixer.onrender.com/mix"; 
        
        showToast("⏳ Mixing Magic Started! Please wait 10-15s...");
        let btn = document.getElementById("mixBtn");
        btn.innerText = "⏳ Loading... Do not close";
        btn.style.opacity = "0.7"; btn.disabled = true;

        fetch(renderAPI, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_url: globalImgUrl, audio_url: globalAudioUrl })
        })
        .then(async res => {
            const contentType = res.headers.get("content-type");
            // Agar Error Aaya toh JSON check karega
            if (contentType && contentType.indexOf("application/json") !== -1) {
                const errorData = await res.json();
                throw new Error(errorData.error || "Server Error");
            }
            if(!res.ok) { throw new Error("Render server sleeping/busy"); }
            return res.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a'); a.style.display = 'none'; a.href = url; a.download = 'Sultan_Mixed_Post.mp4';
            document.body.appendChild(a); a.click(); window.URL.revokeObjectURL(url);
            showToast("✅ Post Mix Downloaded!"); fireConfetti();
            btn.innerText = "✨ Download Photo + Music (MP4 Video)";
            btn.style.opacity = "1"; btn.disabled = false;
        })
        .catch(err => { 
            // Ab real error screen par dikhega!
            showToast("⚠️ " + err.message); 
            btn.innerText = "✨ Download Photo + Music (MP4 Video)"; 
            btn.style.opacity = "1"; btn.disabled = false;
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
def download_video():
    data = request.json; raw_url = data.get('url', ''); clean_url = raw_url
    if "instagram.com" in raw_url or "twitter.com" in raw_url or "x.com" in raw_url: clean_url = raw_url.split('?')[0]
    api_url = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    headers = { "content-type": "application/json", "X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com" }
    try:
        response = requests.post(api_url, json={"url": clean_url}, headers=headers).json()
        media_url = None; media_type = "video"; audio_url = None; video_title = None
        if 'title' in response: video_title = response['title']
        medias = response.get('medias', [])
        if medias and isinstance(medias, list):
            video_media = next((m for m in medias if m.get('type') == 'video' or 'mp4' in m.get('url','')), None)
            image_media = next((m for m in medias if m.get('type') == 'image' or 'jpg' in m.get('url','') or 'webp' in m.get('url','')), None)
            audio_media = next((m for m in medias if m.get('type') == 'audio' or 'mp3' in m.get('url','')), None)
            if video_media: media_url = video_media.get('url'); media_type = "video"
            elif image_media: media_url = image_media.get('url'); media_type = "image"
            if audio_media: audio_url = audio_media.get('url')
        if not media_url:
            if 'url' in response: media_url = response['url']
            elif 'video' in response: media_url = response['video']
            elif 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0: media_url = response['data'][0].get('url')
        if media_url: return jsonify({"success": True, "media_url": media_url, "media_type": media_type, "audio_url": audio_url, "title": video_title})
        else: return jsonify({"success": False, "message": "Media not found."})
    except Exception as e: return jsonify({"success": False, "message": "Server Error."})

if __name__ == '__main__': app.run()

