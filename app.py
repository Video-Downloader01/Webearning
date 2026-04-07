from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# --- AAPKI SECURE KEYS (Server ke piche chhupi hui) ---
RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'
GPLINKS_UNLOCK = 'https://gplinks.co/RZ2LLpr'

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sultan Pro Downloader</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: white; text-align: center; margin: 0; padding: 20px; }
        .promo-banner { background: linear-gradient(90deg, #ff8a00, #e52e71); padding: 15px; border-radius: 10px; margin-bottom: 20px; font-weight: bold; text-decoration: none; color: white; display: block; }
        .container { max-width: 550px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 15px; box-shadow: 0px 8px 20px rgba(0,0,0,0.5); }
        h1 { color: #00d2ff; font-size: 28px; }
        p { color: #aaa; font-size: 15px; }
        input[type="text"] { width: 90%; padding: 15px; margin: 20px 0; border: none; border-radius: 8px; font-size: 16px; background: #2d2d2d; color: white; outline: none; }
        button { background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: white; border: none; padding: 15px 20px; font-size: 18px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; transition: 0.3s; }
        button:hover { transform: scale(1.02); }
        .ad-popup { display: none; background: #ffcc00; color: black; padding: 20px; border-radius: 10px; margin-top: 15px; font-weight: bold; animation: pop 0.5s ease; }
        @keyframes pop { 0% { transform: scale(0.8); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        .gplink-box { display: none; background: #e52e71; padding: 20px; border-radius: 10px; margin-top: 20px; }
        .gplink-box a { color: white; text-decoration: none; font-size: 18px; font-weight: bold; }
        #result { margin-top: 25px; display: none; }
        video { width: 100%; border-radius: 10px; border: 2px solid #3a7bd5; margin-bottom: 15px; }
        .dl-btn { background-color: #28a745; text-decoration: none; display: block; padding: 15px; color: white; border-radius: 8px; font-weight: bold; font-size: 18px; }
        #loading { display: none; color: #00d2ff; font-weight: bold; margin-top: 15px; font-size: 18px; }
        .limit-text { color: #ff4d4d; margin-top: 10px; font-size: 14px; }
    </style>
</head>
<body>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">
    🚀 Join @CineTrixaHub For Free HD Movies & Series! Click Here
</a>

<div class="container">
    <h1>🎬 Sultan Pro Downloader</h1>
    <p>Paste Instagram, YouTube, Facebook, or Twitter Link</p>
    
    <input type="text" id="videoUrl" placeholder="Paste your link here...">
    <button id="mainBtn" onclick="processDownload()">Download Video</button>
    
    <div id="limitMsg" class="limit-text">You have 3 free downloads left today.</div>

    <div class="gplink-box" id="lockBox">
        <h3>🔒 Daily Free Limit Reached!</h3>
        <p>To continue downloading unlimited videos for the next 24 hours, please click the button below and verify.</p>
        <br>
        <a href="{{ gplinks_unlock }}" target="_blank" style="background: white; color: #e52e71; padding: 10px 20px; border-radius: 5px;">🔓 Unlock Unlimited Downloads</a>
    </div>

    <div class="ad-popup" id="adPopup">
        ⏳ Generating Video...<br><br>
        <a href="{{ game_link }}" target="_blank" style="background: black; color: white; padding: 10px; text-decoration: none; border-radius: 5px; display: inline-block;">🎮 Play Game & Win ₹500 Cash!</a>
    </div>

    <div id="loading">⏳ Server is fetching the video in HD... Please wait!</div>

    <div id="result">
        <video id="vidPlayer" controls></video>
        <a id="downloadBtn" class="dl-btn" href="#" target="_blank">📥 Direct Download Video</a>
    </div>
</div>

<script>
    // 24 Hour Logic & 3 Limits
    let today = new Date().toDateString();
    if(localStorage.getItem('dl_date') !== today) {
        localStorage.setItem('dl_count', 0);
        localStorage.setItem('dl_date', today);
    }
    
    let count = parseInt(localStorage.getItem('dl_count')) || 0;
    updateLimitText();

    function updateLimitText() {
        let left = 3 - count;
        if(left > 0) {
            document.getElementById('limitMsg').innerText = "🎁 You have " + left + " free downloads left today.";
        } else {
            document.getElementById('mainBtn').style.display = "none";
            document.getElementById('limitMsg').style.display = "none";
            document.getElementById('lockBox').style.display = "block";
        }
    }

    function processDownload() {
        let url = document.getElementById("videoUrl").value;
        if(!url) { alert("Please paste a valid video link!"); return; }

        if(count >= 3) { updateLimitText(); return; }

        // Show Game Ad Pop-up for 4 seconds
        document.getElementById("adPopup").style.display = "block";
        document.getElementById("mainBtn").style.display = "none";
        document.getElementById("result").style.display = "none";

        setTimeout(() => {
            document.getElementById("adPopup").style.display = "none";
            document.getElementById("loading").style.display = "block";
            fetchVideoAPI(url);
        }, 4000);
    }

    function fetchVideoAPI(url) {
        fetch("/api/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            
            if(data.success) {
                // Increase Count
                count++;
                localStorage.setItem('dl_count', count);
                updateLimitText();

                document.getElementById("vidPlayer").src = data.video_url;
                document.getElementById("downloadBtn").href = data.video_url;
                document.getElementById("result").style.display = "block";
            } else {
                alert("❌ Error: " + data.message);
            }
        })
        .catch(err => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            alert("⚠️ Server Timeout! Please try again.");
        });
    }
</script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template_string(HTML_PAGE, game_link=GAME_LINK, gplinks_unlock=GPLINKS_UNLOCK)

@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.json
    raw_url = data.get('url', '')

    clean_url = raw_url
    if "instagram.com" in raw_url or "twitter.com" in raw_url or "x.com" in raw_url:
        clean_url = raw_url.split('?')[0]

    api_url = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "social-download-all-in-one.p.rapidapi.com"
    }

    try:
        response = requests.post(api_url, json={"url": clean_url}, headers=headers).json()
        video_url = None
        
        if 'medias' in response and isinstance(response['medias'], list) and len(response['medias']) > 0:
            video_url = response['medias'][0].get('url')
        elif 'url' in response:
            video_url = response['url']
        elif 'video' in response:
            video_url = response['video']
        elif 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0:
            video_url = response['data'][0].get('url')

        if video_url:
            return jsonify({"success": True, "video_url": video_url})
        else:
            return jsonify({"success": False, "message": "Video link not found or account is private."})
    except Exception as e:
        return jsonify({"success": False, "message": "Server Timeout. Video is too large or link is invalid."})

if __name__ == '__main__':
    app.run()
