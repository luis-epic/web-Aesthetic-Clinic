import urllib.request

url = "https://upload.wikimedia.org/wikipedia/commons/b/b3/Gymnop%C3%A9die_No._1_%28Erik_Satie%29_by_Kavin_MacLeod.mp3"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        print(f"Content Type: {response.info().get_content_type()}")
except Exception as e:
    print(f"Error fetching URL: {e}")
