from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# --- AAPKI SECURE KEYS ---
RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'
GAME_LINK = 'https://www.jaiclub36.com/#/register?invitationCode=46857835121'

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sultan Pro | Ultra-Glass Downloader</title>
    <style>
        /* ANIMATED DARK GRADIENT BACKGROUND */
        body { 
            font-family: 'Poppins', sans-serif; 
            margin: 0; padding: 20px; color: white; text-align: center;
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #000000);
            background-size: 400% 400%;
            animation: gradientBG 10s ease infinite;
            min-height: 100vh;
            display: flex; flex-direction: column; align-items: center;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .promo-banner { 
            background: rgba(255, 255, 255, 0.1); 
            padding: 12px 25px; border-radius: 50px; margin-bottom: 25px; 
            font-weight: bold; text-decoration: none; color: #00d2ff; 
            display: inline-block; backdrop-filter: blur(10px); 
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            transition: 0.3s;
        }
        .promo-banner:hover { transform: scale(1.05); background: rgba(255, 255, 255, 0.2); }
        
        /* ULTRA GLASSMORPHISM CONTAINER */
        .glass-container { 
            max-width: 450px; width: 90%; padding: 40px 25px; border-radius: 30px; 
            background: rgba(255, 255, 255, 0.08); /* Semi-transparent white */
            backdrop-filter: blur(25px); /* Strong Blur for Glass Effect */
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.18); /* White border for edges */
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
            margin-top: 10px;
        }

        h1 { margin: 0; font-size: 35px; letter-spacing: 1px;
             background: linear-gradient(to right, #00d2ff, #92fe9d);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

        p.subtitle { color: #aaa; font-size: 14px; margin-bottom: 30px; letter-spacing: 0.5px; }
        
        input[type="text"] { 
            width: 88%; padding: 16px; margin-bottom: 20px; 
            border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; 
            font-size: 16px; background: rgba(255, 255, 255, 0.05); color: white; 
            outline: none; transition: 0.3s;
        }
        input[type="text"]:focus { background: rgba(255, 255, 255, 0.1); border-color: #00d2ff; }
        
        button { 
            background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%); 
            color: white; border: none; padding: 16px; font-size: 18px; 
            border-radius: 15px; cursor: pointer; width: 100%; font-weight: bold; 
            box-shadow: 0 10px 20px rgba(0, 210, 255, 0.3); transition: 0.3s; 
        }
        button:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(0, 210, 255, 0.5); }
        
        .limit-text { margin-top: 20px; font-size: 14px; color: #92fe9d; font-weight: bold; }
        
        /* 10-SECOND SMART AD (MODERN LOOK) */
        .smart-ad-box { 
            display: none; background: rgba(0,0,0,0.4); padding: 25px; 
            border-radius: 20px; margin-top: 25px; border: 1px dashed #ffcc00; 
        }
        .timer-text { font-size: 26px; font-weight: bold; color: #ffcc00; margin-bottom: 10px; }
        .game-ad { 
            display: block; background: linear-gradient(90deg, #f80759, #bc4e9c); 
            color: white; padding: 15px; border-radius: 12px; text-decoration: none; 
            font-weight: bold; font-size: 18px; margin-top: 15px; box-shadow: 0 5px 15px rgba(248, 7, 89, 0.4);
        }
        
        #loading { display: none; margin-top: 25px; font-size: 16px; color: #00d2ff; font-style: italic; }
        #result { margin-top: 30px; display: none; }
        video { width: 100%; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 20px; }
        .dl-btn { 
            background: #28a745; text-decoration: none; display: block; 
            padding: 16px; color: white; border-radius: 15px; font-weight: bold; font-size: 18px; 
        }
    </style>
</head>
<body>

<a href="https://t.me/CineTrixaHub" target="_blank" class="promo-banner">
    ✨ Join Telegram: @CineTrixaHub 🍿
</a>

<div class="glass-container">
    <h1>Sultan Pro</h1>
    <p class="subtitle">Premium Social Media Downloader</p>
    
    <input type="text" id="videoUrl" placeholder="Paste link here (Insta, YT, FB)...">
    <button id="mainBtn" onclick="startProcess()">Get Video</button>
    
    <div id="limitMsg" class="limit-text">🎁 3 Free instant downloads left today.</div>

    <div class="smart-ad-box" id="smartAd">
        <div class="timer-text">Unlocking in <span id="timerCount">10</span>s</div>
        <a href="{{ game_link }}" target="_blank" class="game-ad">🎮 Play & Win ₹500 Cash!</a>
        <br>
        <button id="unlockBtn" style="display: none; background: #92fe9d; color: black;" onclick="fetchVideoAPI()">🔓 Download Now</button>
    </div>

    <div id="loading">🚀 Searching video on high-speed servers...</div>

    <div id="result">
        <video id="vidPlayer" controls></video>
        <a id="downloadBtn" class="dl-btn" href="#" target="_blank">📥 Save Video</a>
    </div>
</div>

<script>
    let today = new Date().toDateString();
    if(localStorage.getItem('dl_date') !== today) {
        localStorage.setItem('dl_count', 0);
        localStorage.setItem('dl_date', today);
    }
    
    let count = parseInt(localStorage.getItem('dl_count')) || 0;
    let pendingUrl = "";
    updateLimitText();

    function updateLimitText() {
        let left = 3 - count;
        if(left > 0) {
            document.getElementById('limitMsg').innerText = "🎁 " + left + " Free instant downloads left today.";
        } else {
            document.getElementById('limitMsg').innerHTML = "⚡ <span style='color:#ff4b2b'>Instant limit reached!</span>";
        }
    }

    function startProcess() {
        let url = document.getElementById("videoUrl").value;
        if(!url) { alert("Please paste a link first!"); return; }
        
        document.getElementById("result").style.display = "none";
        pendingUrl = url;

        if(count >= 3) {
            document.getElementById("mainBtn").style.display = "none";
            document.getElementById("limitMsg").style.display = "none";
            document.getElementById("smartAd").style.display = "block";
            
            let timeLeft = 10;
            let timer = setInterval(function() {
                timeLeft--;
                document.getElementById("timerCount").innerText = timeLeft;
                if(timeLeft <= 0) {
                    clearInterval(timer);
                    document.getElementById("timerCount").parentNode.innerHTML = "Link Unlocked!";
                    document.getElementById("unlockBtn").style.display = "block";
                }
            }, 1000);
        } else {
            document.getElementById("mainBtn").style.display = "none";
            document.getElementById("loading").style.display = "block";
            fetchVideoAPI();
        }
    }

    function fetchVideoAPI() {
        document.getElementById("smartAd").style.display = "none";
        document.getElementById("loading").style.display = "block";
        document.getElementById("unlockBtn").style.display = "none";

        fetch("/api/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: pendingUrl })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("mainBtn").style.display = "block";
            if(data.success) {
                count++;
                localStorage.setItem('dl_count', count);
                updateLimitText();
                if(count >= 3) { document.getElementById("limitMsg").style.display = "block"; }

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
            alert("⚠️ Something went wrong. Try again!");
        });
    }
</script>
</body>
</html>
