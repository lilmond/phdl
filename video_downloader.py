from urllib import parse
import requests
import re

def get_video_url(cookie, token, viewkey, quality):
    cookies = {
        "ss": cookie,
        "platform": "tv",
        "quality": str(quality),
    }

    response = requests.get(f"https://www.pornhub.com/video/tv_media?viewkey={viewkey}&token={token}", cookies=cookies, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"}).json()

    if not "videoUrl" in response:
        print("Error: Unable to get videoUrl. Try again!")
        return
    
    return response["videoUrl"]

def get_cookientoken():
    http = requests.get("https://www.pornhub.com/")
    html = http.text
    tokens = re.findall(r'token="(.+?)"', html)
    
    return (http.cookies.get_dict()["ss"], tokens[0])

def main():
    try:
        while True:
            video_link = input("Video URL: ").strip()
            try:
                quality = int(input("Quality: ").strip())
            except ValueError:
                print("Error: Invalid quality. Must be integer. Setting to max...")
                quality = 99999

            video_key = None
            queries = parse.urlsplit(video_link).query.split("&")
            for query in queries:
                try:
                    query_key, query_value = query.split("=", 1)
                except Exception:
                    continue
                if query_key.lower() == "viewkey":
                    video_key = query_value
            
            if not video_key:
                print("Error: Invalid video URL. Unable to get videokey.\n")
                continue

            try:
                cookie, token = get_cookientoken()
            except Exception:
                print("Warning: Unable to get cookie and token.\n")
                continue
            
            try:
                video_url = get_video_url(cookie, token, video_key, quality)
            except Exception:
                print("Error: Unable to get video source.\n")
                continue

            print(f"Video Source: {video_url}\n")

    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
