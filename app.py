from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Video Downloader</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #0f172a; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; }
        .container { width: 100%; max-width: 600px; background-color: #1e293b; padding: 35px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); border: 1px solid #334155; margin: auto; }
        h1 { text-align: center; font-size: 28px; font-weight: 800; margin-bottom: 8px; background: linear-gradient(to right, #38bdf8, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        p.subtitle { text-align: center; color: #94a3b8; font-size: 14px; margin-bottom: 30px; }
        .input-group { display: flex; flex-direction: column; gap: 15px; }
        input { width: 100%; padding: 14px 16px; background-color: #334155; border: 1px solid #475569; border-radius: 8px; color: #fff; font-size: 15px; transition: all 0.3s; outline: none; }
        input:focus { border-color: #38bdf8; box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2); }
        button { width: 100%; background: linear-gradient(to right, #3b82f6, #8b5cf6); border: none; color: white; padding: 14px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: opacity 0.2s; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
        button:hover { opacity: 0.9; }
        button:disabled { opacity: 0.6; cursor: not-allowed; }
        #loading { display: none; text-align: center; margin-top: 25px; color: #94a3b8; font-size: 14px; }
        .spinner { border: 4px solid rgba(255,255,255,0.1); width: 36px; height: 36px; border-radius: 50%; border-left-color: #38bdf8; animation: spin 1s linear infinite; margin: 0 auto 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        #result { display: none; margin-top: 30px; padding: 20px; background-color: rgba(51, 65, 85, 0.5); border-radius: 12px; border: 1px solid #475569; }
        #videoTitle { font-size: 16px; font-weight: 600; margin-bottom: 15px; color: #e2e8f0; line-height: 1.4; }
        .download-links { display: flex; flex-direction: column; gap: 10px; }
        .dl-btn { display: flex; justify-content: space-between; align-items: center; background-color: #10b981; text-decoration: none; color: white; padding: 12px 16px; border-radius: 8px; font-weight: 500; font-size: 14px; transition: background 0.2s; }
        .dl-btn:hover { background-color: #059669; }
        .badge { background-color: rgba(0,0,0,0.2); padding: 2px 8px; border-radius: 4px; font-size: 11px; text-transform: uppercase; }
    </style>
</head>
<body>
    <div class="container">
        <h1>All-in-One Video Downloader</h1>
        <p class="subtitle">Paste Facebook, YouTube, Instagram, TikTok links to download</p>
        <div class="input-group">
            <input type="text" id="videoUrl" placeholder="Paste your video link here...">
            <button onclick="extractVideo()" id="btnText">Fetch Video</button>
        </div>
        <div id="loading">
            <div class="spinner"></div>
            <p>Extracting video links, please wait...</p>
        </div>
        <div id="result">
            <h3 id="videoTitle">Select Format to Download</h3>
            <div id="downloadLinks" class="download-links"></div>
        </div>
    </div>
    <script>
        async function extractVideo() {
            const urlInput = document.getElementById('videoUrl').value.trim();
            const btnText = document.getElementById('btnText');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const downloadLinks = document.getElementById('downloadLinks');
            if (!urlInput) { alert('Please paste a valid URL!'); return; }
            
            result.style.display = 'none';
            loading.style.display = 'block';
            btnText.disabled = true;
            downloadLinks.innerHTML = '';
            
            try {
                // সরাসরি ক্লায়েন্ট সাইড থেকে ফ্রি কোবাল্ট এপিআই রিকোয়েস্ট
                const response = await fetch("https://cobalt.tools", {
                    method: "POST",
                    headers: {
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ url: urlInput, vQuality: "720" })
                });
                
                const data = await response.json();
                
                if (response.ok && data.status === 'stream') {
                    const btn = document.createElement('a');
                    btn.href = data.url;
                    btn.target = '_blank';
                    btn.className = 'dl-btn';
                    btn.innerHTML = `<span>Download Video (Best Quality)</span> <span class="badge">MP4</span>`;
                    downloadLinks.appendChild(btn);
                    result.style.display = 'block';
                } else if (data.status === 'picker') {
                    data.picker.forEach(item => {
                        const btn = document.createElement('a');
                        btn.href = item.url;
                        btn.target = '_blank';
                        btn.className = 'dl-btn';
                        btn.innerHTML = `<span>Download ${item.type || 'Media'} (${item.quality || 'Default'})</span> <span class="badge">Link</span>`;
                        downloadLinks.appendChild(btn);
                    });
                    result.style.display = 'block';
                } else {
                    alert('Error: ' + (data.text || 'Could not parse video link'));
                }
            } catch (err) {
                alert('Something went wrong. Please try again.');
            } finally {
                loading.style.display = 'none';
                btnText.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/download', methods=['POST'])
def download():
    # ব্যাকএন্ড এখন একদম খালি ও পারফেক্ট থাকবে
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
