import os
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from pathlib import Path

# Ensure the download directory exists
download_dir = Path("D:/Videos/Downloads")
os.makedirs(download_dir, exist_ok=True)

def get_meta_video_url(page_url):
    # Send a GET request to the page
    response = requests.get(page_url)
    response.raise_for_status()  # Raise an exception if the request is not successful

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <meta> tag with the specified property
    meta_tag = soup.find("meta", property="og:video")
    
    if not meta_tag:
        raise ValueError("No <meta property='og:video'> tag found.")
    
    # Get the video URL from the content attribute of the <meta> tag
    video_url = meta_tag.get("content")
    
    if not video_url:
        raise ValueError("The <meta> tag does not contain a 'content' attribute with the video URL.")
    
    return video_url

def download_video(video_url, download_folder):
    # Get the file name
    file_name = os.path.basename(video_url)
    destination_file_path = download_folder / file_name

    # Stream the video content
    with requests.get(video_url, stream=True) as response:
        response.raise_for_status()

        # Get total length of the file
        file_size = int(response.headers.get("Content-Length", 0))
        chunk_size = 1024  # 1KB chunks

        # Show a progress bar
        progress = tqdm(response.iter_content(chunk_size), f"Downloading {file_name}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
        
        # Write content to file
        with open(destination_file_path, 'wb') as video_file:
            for chunk in progress:
                if chunk:  # filter out keep-alive chunks
                    video_file.write(chunk)
                    progress.update(len(chunk))
    return destination_file_path

while True:
    # Use the get_meta_video_url function if you're scraping a meta tag for a video URL
    page_url = input("Enter the page URL where the video is located: ")
    try:
        video_url = get_meta_video_url(page_url)
        downloaded_video_path = download_video(video_url, download_dir)
        print(f"Video successfully downloaded to {downloaded_video_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
