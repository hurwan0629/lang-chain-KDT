import requests

from bs4 import BeautifulSoup
import pandas as pd

def bugs_artist_tracks(artist_id):
    url = f"https://music.bugs.co.kr/artist/{artist_id}/tracks"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://music.bugs.co.kr/"
    }

    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("table.list.trackList tbody tr")

    data = []

    for row in rows:
        title_tag = row.select_one("p.title a")
        artist_tag = row.select_one("p.artist a")
        album_tag = row.select_one("a.album")

        if not title_tag:
            continue
    
        title = title_tag.get_text(strip=True)
        artist = artist_tag.get_text(strip=True) if artist_tag else ""
        album = album_tag.get_text(strip=True) if album_tag else ""

        data.append({
            "title": title,
            "artist": artist,
            "album": album,
        })
    
    df = pd.DataFrame(data)
    df.index = df.index + 1

    file_name = f"bugs_artist_{artist_id}_tracks.csv"
    df.to_csv(file_name, encoding="utf-8-sig")

    return df

df = bugs_artist_tracks("20260859")
print(df)