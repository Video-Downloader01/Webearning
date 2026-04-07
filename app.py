from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Save Pro | HD Video Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { margin: 0; padding: 0; color: white; text-align: center; background: #05010a; background-image: radial-gradient(circle at 15% 50%, rgba(254, 9, 121, 0.1), transparent 25%), radial-gradient(circle at 85% 30%, rgba(0, 242, 254, 0.1), transparent 25%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }
        .main-card { max-width: 440px; width: 92%; padding: 40px 25px; border-radius: 25px; background: rgba(15, 10, 25, 0.8); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9); margin-top: 60px; position: relative; }
        h1 { margin: 0; font-size: 42px; font-weight: 900; background: linear-gradient(to right, #fe0979, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -2px; }
        .subtitle { color: #00f2fe; font-size: 11px; letter-spacing: 3px; font-weight: 600; text-transform: uppercase; margin-bottom: 30px; }
        .input-box { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.5); color: #fff; font-size: 15px; outline: none; margin-bottom: 15px; }
        .main-btn { background: linear-gradient(90deg, #fe0979, #ff77a9); color: white; border: none; padding: 18px; border-radius: 12px; width: 100%; font-weight: 800; cursor: pointer; font-size: 16px; text-transform: uppercase; box-shadow: 0 10px 25px rgba(254, 9, 121, 0.4); }
        #fullLoader { display: none; margin-top: 20px; flex-direction: column; align-items: center; }
        .dot { width: 12px; height: 12px; background: #fe0979; border-radius: 50%; display: inline-block; animation: bounce 0.5s infinite alternate; margin: 0 4px; }
        @keyframes bounce { to { transform: translateY(-10px); } }
        #result { margin-top: 30px; display: none; text-align: left; }
        .dl-btn { text-decoration: none; display: block; padding: 18px; border-radius: 12px; font-weight: 800; font-size: 15px; text-align: center; margin-top: 15px; text-transform: uppercase; background: #00f2fe; color: #000; }
        .shayari-box { margin-top: 30px; padding: 15px; background: rgba(254, 9, 121, 0.05); border-radius: 15px; font-style: italic; font-size: 13px; border-left: 4px solid #fe0979; }
        .live-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; border: 1px solid #00f2fe; color: #00f2fe; font-size: 11px; margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="main-card">
        <h1>Save Pro</h1>
        <p class="subtitle">Ultimate Downloader</p>
        <input type="text" id="videoUrl" class="input-box" placeholder="Paste link here...">
        <button id="mainBtn" class="main-btn" onclick="startProcess()">DOWNLOAD HD</button>
        
        <div id="fullLoader">
            <div class="dot"></div><div class="dot" style="animation-delay:0.1s"></div><div class="dot" style="animation-delay:0.2s"></div>
            <p style="color:#00f2fe; font-size:12px; margin-top:10px;">CONNECTING TO GLOBAL NODES...</p>
        </div>

        <div id="result">
            <div id="mediaWrap"></div>
            <a id="downloadBtn" class="dl-btn" href="#" target="_blank" download>📥 CLICK TO SAVE FILE</a>
        </div>

        <div class="shayari-box">"Rakh hausla wo manzar bhi aayega, Pyaase ke paas chalkar samundar bhi aayega."</div>
        <div class="live-badge">🟢 LIVE: <span id="vCount">524</span> USERS</div>
    </div>

<script>
    setInterval(() => {
        let v = parseInt(document.getElementById('vCount').innerText);
        document.getElementById('vCount').innerText = v + (Math.random() > 0.5 ? 1 : -1);
    }, 3000);

    async function startProcess() {
        const url = document.getElementById("videoUrl").value;
        if(!url) return alert("Bhai link dalo!");
        
        document.getElementById("mainBtn").style.display = "none";
        document.getElementById("fullLoader").style.display = "flex";
        document.getElementById("result").style.display = "none";

        // --- NEW BYPASS STRATEGY ---
        // Hum kisi ek server par depend nahi rahenge.
        try {
            const response = await fetch('https://co.wuk.sh/api/json', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({ url: url, vQuality: '720' })
            });
            const data = await response.json();

            document.getElementById("fullLoader").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";

            if (data.url || (data.picker && data.picker[0].url)) {
                const finalUrl = data.url || data.picker[0].url;
                confetti({ particleCount: 150, spread: 70 });
                
                let wrap = document.getElementById("mediaWrap");
                if (url.includes("/p/") || url.includes("/tv/")) {
                    wrap.innerHTML = `<img src="${finalUrl}" style="width:100%; border-radius:15px; margin-bottom:10px;">`;
                } else {
                    wrap.innerHTML = `<video src="${finalUrl}" controls style="width:100%; border-radius:15px; margin-bottom:10px;"></video>`;
                }
                
                document.getElementById("downloadBtn").href = finalUrl;
                document.getElementById("result").style.display = "block";
            } else {
                // AGAR ENGINE 1 FAIL HUA TO ENGINE 2 (Backup)
                window.open("https://snapinsta.app/php/download.php?url=" + encodeURIComponent(url), "_blank");
                alert("Bhai Link ready hai! New tab check karo.");
                location.reload();
            }
        } catch (e) {
            // ENGINE 3 (Force Download)
            window.open("https://savefrom.net/?url=" + encodeURIComponent(url), "_blank");
            alert("Bhai server busy tha, backup server se download link open ho gaya hai!");
            location.reload();
        }
    }
</script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_PAGE)

if __name__ == '__main__': app.run()

