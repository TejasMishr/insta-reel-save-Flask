from flask import Flask, render_template, request, Response, jsonify
import os
from main import get_shortcode_from_url, download_reel
import requests
from instaloader import Instaloader, Post
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form.get('insta_url')
        if not url:
            return render_template('index.html', error="Please enter a valid Instagram URL")
        
        shortcode = get_shortcode_from_url(url)
        
        # Get video URL using instaloader
        L = Instaloader()
        post = Post.from_shortcode(L.context, shortcode)
        video_url = post.video_url
        
        return render_template('index.html', 
                             video_url=video_url,
                             source_url=url)
                             
    except ValueError as e:
        return render_template('index.html', error=str(e))
    except Exception as e:
        return render_template('index.html', error=f"An unexpected error occurred: {str(e)}")

@app.route('/stream')
def stream():
    video_url = request.args.get('video_url')
    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400
    
    def generate():
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                yield chunk
    
    return Response(
        generate(),
        mimetype='video/mp4',
        headers={
            'Content-Disposition': 'attachment; filename=instagram_video.mp4'
        }
    )

# Remove the if __name__ == '__main__' block and add this for Vercel
app = app 