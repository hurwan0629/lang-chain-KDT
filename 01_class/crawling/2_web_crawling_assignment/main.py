from client.request import get_html_as_bs
from pathlib import Path

if __name__ == "__main__":
  BASE_PATH = Path(__file__) / ".."

  html = get_html_as_bs("https://basicenglishspeaking.com/daily-english-conversation-topics/")

  # print(html)
  # url 전부 꺼내기
  res = html.select(".thrv_wrapper.thrv_text_element > p > a")

  size = len(res)

  print(f"총 크기: {size}개")

  print("\n --- 작업 시작 --- \n")

  for index, r in enumerate(res):

    # 저장 폴더 만들어주기
    save_folder = BASE_PATH / "files"
    save_folder.mkdir(parents=True, exist_ok=True)

    # print(r)

    # 파일 이름 예쁘게 만들어주기
    file_name = f"{index+1:2d}_" + r.text.replace("/", "_and_").replace("\\", "_and_").replace(" ", "_") + ".html"

    # src 뽑아주기
    src = r["href"]

    # 파일 저장해주기
    with open(save_folder / file_name, "w") as f:
      f.write(str(get_html_as_bs(src)))
    print(f"{index+1}. {file_name} 작업 완료 ({index+1}/{size})")

    # print(src)
  # print(res)