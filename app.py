from flask import Flask, request, jsonify, render_template_string
import requests
import re
import json

app = Flask(__name__)

RAPID_API_KEY = '703d7948b0msh9c8856f5920ec9ep1e27ddjsna9a8686438be'

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sultan Pro | Hacker Mode</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Poppins', sans-serif; background: #0b0e14; color: white; text-align: center; padding: 20px;}
        .input-box { width: 90%; max-width: 400px; padding: 15px; border-radius: 10px; margin: 20px 0; font-size: 15px; outline: none; }
        button { background: #ff416c; color: white; border: none; padding: 15px; border-radius: 10px; width: 90%; max-width: 400px; font-weight: bold; cursor: pointer; font-size: 16px; }
        #debugScreen { background: #1a1a1a; border: 2px solid #00ffcc; color: #00ffcc; padding: 15px; margin-top: 20px; text-align: left; font-family: monospace; font-size: 12px; height: 300px; overflow-y: auto; display: none; border-radius: 10px; width: 90%; max-width: 600px; margin-left: auto; margin-right: auto;}
    </style>
</head>
<body>

    <h1>Sultan Pro - Hacker Mode 🕵️‍♂️</h1>
    <p style="color: #ffcc00;">Check what the API is actually sending us!</p>
    
    <input type="text" id="videoUrl" class="input-box" placeholder="Paste IG Link Here...">
    <button onclick="startHack()">Scan API Data</button>
    
    <p id="loading" style="display:none; color: #ff77a9;">Scanning Instagram Servers...</p>
    
    <div id="debugScreen"></div>

<script>
    function startHack() {
        let url = document.getElementById("videoUrl").value;
        if(!url) return alert("Please paste a link!");
        
        document.getElementById("loading").style.display = "block";
        document.getElementById("debugScreen").style.display = "none";

        fetch("/api/hack", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("loading").style.display = "none";
            let debugBox = document.getElementById("debugScreen");
            debugBox.style.display = "block";
            // Print raw JSON data beautifully
            debugBox.innerText = JSON.stringify(data.raw_data, null, 4);
        })
        .catch(e => {
            document.getElementById("loading").style.display = "none";
            alert("Error running hack.");
        });
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/api/hack', methods=['POST'])
def hack_api():
    url = request.json.get('url', '')
    clean_url = url.split('?')[0] if "instagram" in url else url
    
    try:
        # Nayi Advanced API
        shortcode_match = re.search(r'instagram\.com/(?:p|reel|tv)/([^/?#&]+)', clean_url)
        if shortcode_match:
            shortcode = shortcode_match.group(1)
            adv_url = f"https://instagram-scraper-api-advanced.p.rapidapi.com/api/download/reel/{shortcode}"
            headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "instagram-scraper-api-advanced.p.rapidapi.com"}
            res = requests.get(adv_url, headers=headers, timeout=10).json()
            return jsonify({"raw_data": res})
    except Exception as e:
        return jsonify({"raw_data": {"error": "API Request failed completely."}})

if __name__ == '__main__':
    app.run()

