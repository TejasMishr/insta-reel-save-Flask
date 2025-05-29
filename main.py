#!/usr/bin/env python3
"""
download_reel.py

Download an Instagram Reel (with sound) to a local MP4 file.

Usage:
    python download_reel.py

Prerequisites:
    pip install instaloader requests
"""
import re
import sys
import os

import instaloader
from instaloader import Post
import requests

def get_shortcode_from_url(url: str) -> str:
    """
    Extract the shortcode from an Instagram Reel URL.
    """
    m = re.search(r"instagram\.com/(?:reel|p|tv)/([^/?]+)", url)
    if not m:
        raise ValueError(f"Invalid Instagram Reel URL: {url!r}")
    return m.group(1)

def download_reel(shortcode: str, output_path: str = "video.mp4") -> None:
    """
    Fetch the video_url via Instaloader and stream it into a file.
    """
    try:
        L = instaloader.Instaloader()
        # If you need to download a private reel, uncomment and fill in:
        # L.login("your_username", "your_password")

        post = Post.from_shortcode(L.context, shortcode)
        video_url = post.video_url  # public CDN link including audio 

        print(f"Starting download from {video_url}")
        resp = requests.get(video_url, stream=True)
        resp.raise_for_status()
        
        # Create downloads directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Successfully saved reel to {output_path}")
    except Exception as e:
        print(f"Error downloading reel: {str(e)}")
        sys.exit(1)

def main():
    print("Instagram Reel Downloader")
    print("------------------------")
    
    while True:
        url = input("\nEnter Instagram Reel URL (or 'q' to quit): ").strip()
        
        if url.lower() == 'q':
            print("Goodbye!")
            break
            
        if not url:
            print("Please enter a valid URL")
            continue
            
        try:
            shortcode = get_shortcode_from_url(url)
            output_name = f"reel_{shortcode}.mp4"
            download_reel(shortcode, output_name)
            
            # Another download?
            if input("\nDownload another reel? (y/n): ").lower() != 'y':
                print("Goodbye!")
                break
                
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
