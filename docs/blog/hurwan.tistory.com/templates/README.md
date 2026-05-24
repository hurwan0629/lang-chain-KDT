# Blog Templates

이 폴더는 티스토리 업로드용 HTML을 만들기 전 디자인과 구조를 확인하는 공간이다.

## Files

- `style.css`: 공통 스타일 원본이다. 디자인을 바꿀 때는 이 파일을 먼저 수정한다.
- `preview.html`: 스타일 확인용 샘플 페이지다. 실제 업로드 글이 아니다.
- `post_template.html`: 새 글 HTML을 만들 때 사용하는 최소 골격이다.

## Usage

1. `preview.html`을 브라우저로 열어 현재 디자인을 확인한다.
2. 새 글을 만들 때는 `post_template.html`의 구조를 기준으로 본문을 채운다.
3. 최종 티스토리 업로드 파일은 단일 HTML이어야 하므로, `style.css` 내용을 `<style>` 태그 안에 인라인으로 넣는다.
4. 사용자가 쓴 원문 문장은 바꾸지 않고, HTML 태그와 스타일만 적용한다.
