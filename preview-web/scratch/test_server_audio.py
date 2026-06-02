import urllib.request
import urllib.error

url = "http://localhost:8080/waiting_music.mp3"

try:
    print(f"Requesting head headers for {url}...")
    req = urllib.request.Request(url, method='HEAD')
    with urllib.request.urlopen(req) as resp:
        print("Response Code:", resp.status)
        print("Headers:")
        for k, v in resp.getheaders():
            print(f"  {k}: {v}")
except urllib.error.URLError as e:
    print("URL Error:", e)
except Exception as e:
    print("General Error:", e)
