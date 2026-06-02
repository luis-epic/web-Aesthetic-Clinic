import urllib.request
import os

url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Gymnopedie%20No%201.mp3"
dest_path = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\waiting_music.mp3"

print(f"Downloading from {url}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
    print(f"Successfully downloaded to: {dest_path}")
    print(f"File size: {os.path.getsize(dest_path)} bytes")
except Exception as e:
    print(f"Error downloading: {e}")
    exit(1)
