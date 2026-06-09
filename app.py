@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json() or {}
    video_url = data.get('url')
    if not video_url:
        return jsonify({'success': False, 'error': 'No URL provided'}), 400
        
    # ওঅথ২ কনফিগারেশন (সঠিক স্পেসিং বা মার্জিনসহ)
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'username': 'oauth2',
        'password': ''
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'Video')
            formats_list = []
            if 'formats' in info:
                valid_formats = [f for f in info['formats'] if f.get('acodec') != 'none' and f.get('vcodec') != 'none' and f.get('url')]
                if not valid_formats:
                    formats_list.append({'quality': 'Standard Quality', 'ext': info.get('ext', 'mp4'), 'url': info.get('url')})
                else:
                    for f in valid_formats[-3:]:
                        formats_list.append({'quality': f.get('format_note', 'HD') or f.get('resolution', 'Default'), 'ext': f.get('ext', 'mp4'), 'url': f['url']})
            else:
                formats_list.append({'quality': 'Direct Link', 'ext': info.get('ext', 'mp4'), 'url': info.get('url')})
            return jsonify({'success': True, 'title': title, 'formats': formats_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
