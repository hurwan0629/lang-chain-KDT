import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def extract_current_page(driver, wait):
    data = []

    try:
        song_table = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="frm_defaultList"]/div/table')
            )
        )
    except TimeoutException:
        return []

    rows = song_table.find_elements(By.CSS_SELECTOR, "tbody tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) < 5:
            continue

        title_lines = [
            line.strip()
            for line in cols[2].text.split("\n")
            if line.strip()
        ]

        title = ""

        for line in title_lines:
            if line.startswith("Title "):
                title = line.replace("Title ", "").strip()
                break

        if not title:
            for line in title_lines:
                if (
                    "재생" not in line
                    and "담기" not in line
                    and "상세정보" not in line
                    and not line.startswith("Title")
                ):
                    title = line
                    break

        artist_lines = [
            line.strip()
            for line in cols[3].text.split("\n")
            if line.strip()
        ]
        artist = artist_lines[0] if artist_lines else ""

        album_lines = [
            line.strip()
            for line in cols[4].text.split("\n")
            if line.strip()
        ]
        album = album_lines[0] if album_lines else ""

        try:
            like = row.find_element(
                By.CSS_SELECTOR,
                "button.like span.cnt"
            ).text.strip()
        except:
            like = ""

        if title:
            data.append({
                "곡명": title,
                "아티스트": artist,
                "앨범": album,
                "좋아요수": like
            })

    return data


def melon_search_all_pages(keyword, max_page=30):
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    all_data = []

    try:
        driver.get("https://www.melon.com/")
        time.sleep(2)

        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "top_search"))
        )

        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)

        time.sleep(3)

        song_tab = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="divCollection"]/ul/li[3]/a/span')
            )
        )

        song_tab.click()
        time.sleep(3)

        for page in range(1, max_page + 1):
            page_data = extract_current_page(driver, wait)

            if not page_data:
                print(f"{page}페이지 데이터가 없어 종료합니다.")
                break

            all_data.extend(page_data)
            print(f"{page}페이지 크롤링 완료: {len(page_data)}곡")

            next_start_index = page * 50 + 1

            try:
                driver.execute_script(
                    f"pageObj.sendPage('{next_start_index}');"
                )
                time.sleep(3)

            except Exception as e:
                print("다음 페이지 이동 실패:", e)
                break

        df = pd.DataFrame(all_data)

        if not df.empty:
            df = df.drop_duplicates(
                subset=["곡명", "아티스트", "앨범"]
            )
            df.index = df.index + 1

        file_name = f"melon_{keyword}_all_songs.csv"

        df.to_csv(
            file_name,
            encoding="utf-8-sig"
        )

        print(f"CSV 저장 완료: {file_name}")
        print(f"총 {len(df)}곡 수집 완료")

        return df

    finally:
        driver.quit()



melon_search_all_pages("조용필", 4)