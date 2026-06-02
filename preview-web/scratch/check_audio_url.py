import urllib.request

url = "https://assets.mixkit.co/music/preview/mixkit-relaxing-in-the-spa-2194.mp3"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        print(f"Content Type: {response.info().get_content_type()}")
except Exception as e:
    print(f"Error fetching URL: {e}")
