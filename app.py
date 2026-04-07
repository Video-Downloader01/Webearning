from flask import Flask, request, jsonify, render_template_string
import requests
import instaloader
import re

app = Flask(__name__)

# Loader instance for Instagram
L = instaloader.Instaloader()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Save Pro | Ultimate Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { margin: 0; padding: 0; color: white; text-align: center; background: #05010a; background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.15), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.15), transparent 25%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }
        .ambient-glow { position: fixed; width: 400px; height: 400px; background: #fe0979; border-radius: 50%; filter: blur(150px); opacity: 0.1; z-index: -1; }
        .main-card { max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; background: rgba(15, 10, 25, 0.7); backdrop-filter: blur(25px); border-top: 2px solid rgba(254, 9, 121, 0.5); border-bottom: 2px solid rgba(0, 242, 254, 0.5); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8); margin-top: 50px; position: relative; }
        h1 { margin: 0; font-size: 42px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; text-transform: uppercase;}
        p.subtitle { color: #00f2fe; font-size: 13px; margin-bottom: 30px; font-weight: 500; letter-spacing: 2px; }
        .input-wrapper { position: relative; width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 15px; background: rgba(0,0,0,0.6); color: #fff; outline: none; }
        button#mainBtn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 800; box-shadow: 0 10px 20px rgba(254, 9, 121, 0.4); }
        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dot { width: 12px; height: 12px; background: #fe0979; border-radius: 50%; display: inline-block; animation: bounce 0.5s infinite alternate; margin: 0 4px; }
        @keyframes bounce { to { transform: translateY(-10px); } }
        #result { margin-top: 30px; display: none; width: 100%; text-align: left; }
        .media-preview { width: 100%; max-height: 400px; border-radius: 12px; margin-bottom: 20px; border: 2px solid rgba(0, 242, 254, 0.3); background: #000; }
        .dl-btn { text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 16px; color: #000; border-radius: 12px; font-weight: 800; font-size: 15px; background: #00f2fe; text-transform: uppercase;}
        .live-count { margin-top: 20px; color: #00f2fe; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="ambient-glow"></div>
    <div class="main-card">
        <h1>Save Pro</h1>
        <p class="subtitle">Next-Gen Media Engine</p>
        <div class="input-wrapper">
            <input type="text" id="videoUrl" placeholder="Paste link here...">
        </div>
        <button id="mainBtn" onclick="startProcess()">DOWNLOAD</button>
        
        <div id="fullLoader">
            <div class="dot"></div><div class="dot" style="animation-delay:0.1s"></div><div class="dot" style="animation-delay:0.2s"></div>
            <p style="color:#00f2fe; font-size:12px; margin-top:10px;">SCRAPING FROM INSTAGRAM...</p>
        </div>

        <div id="result">
            <div id="mediaContainer"></div>
            <a id="downloadBtn" class="dl-btn" href="#" target="_blank">📥 SAVE TO GALLERY</a>
        </div>
        <div class="live-count">🟢 LIVE VISITORS: <span id="vCount">457</span></div>
    </div>

<script>
    setInterval(() => {
        document.getElementById('vCount').innerText = parseInt(document.getElementById('vCount').innerText) + (Math.random() > 0.5 ? 1 : -1);
    }, 3000);

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
                confetti({particleCount: 100, spread: 70});
                let cont = document.getElementById("mediaContainer");
                if(data.type === "image") {
                    cont.innerHTML = `<img src="${data.url}" class="media-preview">`;
                } else {
                    cont.innerHTML = `<video src="${data.url}" controls class="media-preview"></video>`;
                }
                document.getElementById("downloadBtn").href = data.url;
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
    
    # Instagram Logic (No API Required)
    if "instagram.com" in url:
        try:
            # Extract shortcode
            shortcode = re.search(r'/(?:reels|reel|p|tv)/([A-Za-z0-9_-]+)', url).group(1)
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            
            if post.is_video:
                return jsonify({"success": True, "url": post.video_url, "type": "video"})
            else:
                return jsonify({"success": True, "url": post.url, "type": "image"})
        except Exception as e:
            # Fallback to a super backup API if scraping fails
            try:
                headers = {"X-RapidAPI-Key": "703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be", "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com"}
                r = requests.post("https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink", json={"url": url}, headers=headers, timeout=10).json()
                media = r.get('hd') or r.get('video') or r.get('url')
                if media: return jsonify({"success": True, "url": media, "type": "video"})
            except: pass
            return jsonify({"success": False, "message": "Instagram Blocked this request. Try again in 1 min."})

    return jsonify({"success": False, "message": "Link not supported yet!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
