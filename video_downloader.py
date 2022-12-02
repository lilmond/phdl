from urllib import parse
import requests
import re

def get_video_url(cookie, token, viewkey):
    cookies = {
        'ss': cookie,
        'platform': 'tv',
        'quality': '99999',
    }

    params = {
        'viewkey': viewkey,
        'token': token,
    }

    response = requests.get('https://www.pornhub.com/video/tv_media', params=params, cookies=cookies).json()

    if not response:
        print("Error: Unable to get video URL. Try again!")
        return

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
    video_link = input("Video URL: ").strip()

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
        print("Error: Invalid video URL. Unable to get videokey.")
        return

    try:
        cookie, token = get_cookientoken()
    except Exception:
        print("Error: Unable to get cookie and token.")
        return
    
    try:
        video_url = get_video_url(cookie, token, video_key)
    except Exception:
        print("Error: Unable to get video source.")
        return

    print(f"Video Source: {video_url}")

if __name__ == "__main__":
    main()
