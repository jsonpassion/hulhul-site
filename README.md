# 훌훌 (Hulhul) — 소개 사이트

> 떠나보낸 사람이 아직 사진첩에 남아 있나요.
> 얼굴 하나면 그 사람이 담긴 사진을 모두 찾아, 찾고 고르고 **훌훌** 털어 보내요.

iOS 앱 **훌훌**의 랜딩 사이트입니다. 정적 HTML/CSS 한 벌로, 별도 빌드 없이 GitHub Pages로 배포됩니다.

**🔗 https://jsonpassion.github.io/hulhul-site/**

## 훌훌은 어떤 앱인가요

이별한 뒤 사진첩에 남은 그 사람의 사진을, 얼굴 한 장으로 모두 찾아 한 번에 정리하도록 돕는 iOS 앱입니다.

- **모두 찾기** — 얼굴 1~3장을 등록하면 사진첩 전체에서 그 사람이 담긴 사진을 확신도별로 찾아줍니다. 자동 삭제는 없고, 마지막 결정은 언제나 사용자의 몫입니다.
- **훌훌 털기 / 봉인하기** — 고른 사진을 한 번에 지우거나(‘최근 삭제’ 30일 복구 가능), 아직 지울 자신이 없으면 사진 앱의 ‘가려진 앨범’으로 봉인합니다.
- **100% 온디바이스** — 서버도 계정도 없고, 얼굴 인식은 전부 아이폰 안에서 처리됩니다. 어떤 사진도 밖으로 나가지 않습니다.

## 구성

| 파일 | 내용 |
|---|---|
| `index.html` | 랜딩 (히어로+필름 · 사용법 4단계 · 기능 · 디테일 · 가격 · FAQ) |
| `privacy.html` | 개인정보 처리방침 |
| `terms.html` | 이용약관 |
| `assets/video/hero-feather.mp4` | 히어로 시네마틱 루프, 무음 (+ `.jpg` 포스터) |
| `assets/video/hulhul-film.mp4` | 12초 광고 필름 — 히어로 우측 폰 카드에서 음소거 자동재생, 🔊 버튼으로 소리 (+ `.jpg` 포스터) |
| `assets/video/closing-light.mp4` | 클로징 앰비언트 배경 (무자막 페이오프 컷, 무음 루프) (+ `.jpg` 포스터) |
| `assets/lottie/*.json` | 자체 제작 Lottie 애니메이션 10종 |
| `tools/make-lottie.py` | Lottie 생성 스크립트 (아래 참고) |

의존성은 애니메이션 재생용 [bodymovin(lottie-web)](https://github.com/airbnb/lottie-web) CDN 하나뿐입니다.

## 브랜딩

- **컨셉**: “훌훌 털기” — 지운 뒤의 가벼움. 깃털과 먼지가 바람에 날아가는 밝고 회복적인 톤.
- **마크**: 브랜드 블루 타일 위의 흰 깃털 + 위로 날아오르는 입자. 앱 아이콘 · 나비 로고 · 파비콘 · 히어로 Lottie가 같은 지오메트리를 공유합니다.
- **컬러**: 산들바람 `#3D95C7` (라이트) / `#6FBBE6` (다크 계열 보조), 배경 솜구름 `#F7FAFC`, 본문 먹빛 `#22303B`.

## Lottie 재생성

애니메이션은 프로그램으로 생성합니다. 손으로 JSON을 고치지 말고 스크립트를 수정하세요.

```bash
python3 tools/make-lottie.py   # assets/lottie/*.json 재생성
```

10종: `how-register/scan/review/sweep`(사용법 4단계) · `feature-seal/privacy/shared`(기능) · `feature-multiface/period/live`(디테일 3종).
히어로는 Lottie 대신 시네마틱 영상 루프(`assets/video/hero-feather.mp4`)가 맡습니다 — 무음·자동재생·루프,
화면 밖에선 정지하고 `prefers-reduced-motion`에선 포스터만 보여줍니다.

## 로컬 미리보기

```bash
python3 -m http.server 8000    # http://localhost:8000
```

## 배포

`main` 브랜치 루트를 GitHub Pages가 그대로 서빙합니다. `main`에 push하면 자동 배포됩니다.

## 만든 곳

**ForgeLab** · 대표 Jason Lee
문의는 사이트 푸터의 **✉️ 문의하기** 버튼으로 받습니다.

© 2026 ForgeLab
