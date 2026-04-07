from flask import Flask, render_template_string

app = Flask(__name__)

# --- WAHI ASLI PREMIUM DESIGN (FINAL VERSION) ---
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
        .main-card { max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; background: rgba(15, 10, 25, 0.7); backdrop-filter: blur(25px); border-top: 2px solid rgba(254, 9, 121, 0.5); border-bottom: 2px solid rgba(0, 242, 254, 0.5); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8); margin-top: 60px; position: relative; }
        h1 { margin: 0; font-size: 42px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; text-transform: uppercase;}
        .subtitle { color: #00f2fe; font-size: 13px; margin-bottom: 30px; font-weight: 500; letter-spacing: 2px; }
        .input-wrapper { width: 100%; margin-bottom: 20px; }
        .input-wrapper input { width: 100%; padding: 18px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; font-size: 15px; background: rgba(0,0,0,0.6); color: #fff; outline: none; }
        button#mainBtn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; font-size: 18px; border-radius: 12px; cursor: pointer; width: 100%; font-weight: 800; text-transform: uppercase; box-shadow: 0 10px 20px rgba(254, 9, 121, 0.4); }
        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dot { width: 12px; height: 12px; background: #fe0979; border-radius: 50%; display: inline-block; animation: bounce 0.5s infinite alternate; margin: 0 4px; }
        @keyframes bounce { to { transform: translateY(-10px); } }
        #result { margin-top: 30px; display: none; width: 100%; text-align: left; }
        .media-preview { width: 100%; border-radius: 12px; border: 2px solid #00f2fe; background: #000; margin-bottom: 15px; }
        .dl-btn { text-decoration: none; display: block; padding: 16px; color: #000; border-radius: 12px; font-weight: 800; font-size: 15px; background: #00f2fe; text-align: center; text-transform: uppercase; }
        .shayari-corner { margin-top: 40px; padding: 20px; background: rgba(254, 9, 121, 0.05); border-radius: 15px; text-align: center; border-left: 4px solid #fe0979; }
        .live-count { margin-top: 20px; color: #00f2fe; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div id="firefliesBox" class="fireflies"></div>
    <div class="main-card">
        <h1>Save Pro</h1>
        <p class="subtitle">Next-Gen Media Engine</p>
        <div class="input-wrapper">
            <input type="text" id="videoUrl" placeholder="Paste Instagram / YouTube link...">
        </div>
        <button id="mainBtn" onclick="startProcess()">DOWNLOAD</button>
        <div id="fullLoader">
            <div class="dot"></div><div class="dot" style="animation-delay:0.1s"></div><div class="dot" style="animation-delay:0.2s"></div>
            <p style="color:#00f2fe; font-size:12px; margin-top:10px;">CONNECTING TO BYPASS SERVER...</p>
        </div>
        <div id="result">
            <div id="mediaContainer"></div>
            <a id="downloadBtn" class="dl-btn" href="#" target="_blank">📥 SAVE TO GALLERY</a>
        </div>
        <div class="live-count">🟢 LIVE VISITORS: <span id="vCount">457</span></div>
    </div>
    <div class="shayari-corner">
        <p style="font-style: italic;">"Rakh hausla wo manzar bhi aayega, Pyaase ke paas chalkar samundar bhi aayega."</p>
    </div>
<script>
    const fb = document.getElementById('firefliesBox');
    for(let i=0; i<20; i++){ let f=document.createElement('div'); f.className='firefly'; f.style.left=Math.random()*100+'vw'; f.style.top=Math.random()*100+'vh'; fb.appendChild(f); }
    setInterval(() => { document.getElementById('vCount').innerText = parseInt(document.getElementById('vCount').innerText) + (Math.random() > 0.5 ? 1 : -1); }, 3000);

    async function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return alert("Bhai link toh daalo!");
        document.getElementById("mainBtn").style.display = "none";
        document.getElementById("fullLoader").style.display = "flex";
        document.getElementById("result").style.display = "none";

        try {
            // Cobalt API Bypass (Client Side)
            const response = await fetch("https://api.cobalt.tools/api/json", {
                method: "POST",
                headers: { "Content-Type": "application/json", "Accept": "application/json" },
                body: JSON.stringify({ url: url })
            });
            const data = await response.json();
            document.getElementById("fullLoader").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";

            if (data.url) {
                confetti({ particleCount: 100, spread: 70 });
                let cont = document.getElementById("mediaContainer");
                if (data.url.includes(".jpg") || data.url.includes(".png") || url.includes("/p/")) {
                    cont.innerHTML = `<img src="${data.url}" class="media-preview">`;
                } else {
                    cont.innerHTML = `<video src="${data.url}" controls playsinline class="media-preview"></video>`;
                }
                document.getElementById("downloadBtn").href = data.url;
                document.getElementById("result").style.display = "block";
            } else { alert("Server Busy! Ek baar page refresh karke dobara link daalo."); }
        } catch (e) {
            document.getElementById("fullLoader").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            alert("Network Error! Try again.");
        }
    }
</script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run()
