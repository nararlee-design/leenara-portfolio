# Lee Nara Portfolio

정적 사이트입니다. 빌드 과정 없이 `index.html`을 그대로 배포합니다.

- `index.html` — 사이트 전체 (HTML · CSS · JS)
- `fonts/` — Pretendard Variable
- `img/` — 썸네일 · 케이스 이미지 (파일명 = 프로젝트 id)

## 이미지 교체
`img/` 안의 같은 파일명으로 덮어쓰고 커밋하면 자동 배포됩니다.

## 공개 전 체크
- `index.html`의 `<meta name="robots" content="noindex, nofollow">` 삭제
- `robots.txt`의 `Disallow: /` → `Allow: /`
- 기획 주석 버튼 · 자리표시 제거
