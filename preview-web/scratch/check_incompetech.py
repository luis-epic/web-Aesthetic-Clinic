import urllib.request

urls = [
    "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Gymnopedie%20No%201.mp3",
    "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Healing.mp3"
]

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            print(f"URL: {url}")
            print(f"Status Code: {response.getcode()}")
            print(f"Content Type: {response.info().get_content_type()}")
            print("="*40)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        print("="*40)
