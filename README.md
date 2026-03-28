# 🇺🇸 US Market Intelligence Dashboard (Project Manual)

본 문서는 Lee님과 AI(Antigravity)가 공동으로 기획 및 제작한 **"미국 주식 시장 전문가용 대시보드 자동화 프로젝트"**의 전체 설계도 및 운영 매뉴얼입니다. 대화 내용을 따로 저장할 필요 없이, 이 문서 하나로 전체 시스템을 파악하고 유지보수할 수 있습니다.

---

## 🔗 핵심 링크
* **실제 라이브 웹사이트:** [https://us-monitor-daily.github.io/us-market-daily/](https://us-monitor-daily.github.io/us-market-daily/)
* **GitHub 원격 저장소:** [https://github.com/us-monitor-daily/us-market-daily](https://github.com/us-monitor-daily/us-market-daily)
* **로컬 원본 코드 소스 폴더 (Mac):** `/Users/jaewoonglee/.gemini/antigravity/scratch/`

## ⚙️ 작동 원리 및 시스템 아키텍처

이 대시보드는 **매일 오후 4시 30분(EST 기준)** 정규장이 마감된 직후, 수동 개입 없이 자동으로 데이터를 수집하고 웹사이트를 배포하는 "Full-Auto 시스템"입니다.

### 1. 백룸(Back-room) 데이터 수집 로직
1. Mac OS의 `cron` 스케줄러가 매일 지정된 시간에 **`update_dashboard.py`** 파일을 백그라운드에서 실행합니다.
2. 해당 스크립트 내부에서 **`extract_tradingview_movers.py`**가 트리거되어 트레이딩뷰 비공식 API로 [오늘 미국장 주도주 Top 20]의 티커, 시가총액, 등락률, 섹터 맵핑 데이터를 스크래핑합니다.
3. 파이썬 `urllib` 라이브러리가 각 티커별로 **야후 파이낸스(Yahoo Finance) RSS**에 접속하여 기관용 최신 영문 헤드라인 뉴스를 긁어옵니다. (ex: `BRK.B` ➡️ `BRK-B`로 자동 치환 처리)
4. AI 기반 알고리즘이 매일 수집된 상승/하락률을 분석하여, **"거시 경제 브리핑"**과 **"종목별 딥다이브 리포트"** 텍스트를 고도화된 한국어 증권가 문체로 자동 생성합니다.

### 2. 프론트엔드 렌더링 및 배포
1. 수집된 모든 데이터가 하나의 **`index.html`** 파일(다크 모드, Pitch Black 블룸버그 스타일)로 즉시 찍혀나갑니다.
2. 파이썬 스크립트의 마지막 줄에서 `git commit` & `git push` 명령어 라인이 연속 실행됩니다.
3. 완성된 HTML 파일이 GitHub 원격 저장소로 강제 푸시(Push)되며, 약 1~3분 뒤 GitHub Pages의 글로벌 CDN 서버를 통해 전 세계에 실시간 송출(Deploy)됩니다.

## 📊 프론트엔드 핵심 위젯

트레이딩뷰의 외부 서드파티 사이트 실시간 데이터 전송 제한(Popup Error)을 완벽하게 우회하기 위해 설계된 전용 로직입니다.

* **3대 지수 실시간 흐름 (Custom Tabs):**
  * S&P 500, Nasdaq 100, Dow Jones 탭을 직접 CSS/JS로 짰습니다.
  * 트레이딩뷰 차트 에러를 막기 위해 내부적으로는 1:1 완벽 동기화되는 초거대 ETF인 `AMEX:SPY`, `NASDAQ:QQQ`, `AMEX:DIA` 데이터를 수신하여 캔들을 뿌립니다.
  * 1D, 1M, 3M, 1Y 타임프레임 연동이 완전 구축되어 있습니다.
* **자본 흐름 히트맵 (Heatmap):** S&P 500 기반 실시간 섹터별 시가총액 지배력 모니터링
* **투자 심리 지수 (Sentiment):** 테크니컬 어낼리시스 모멘텀 스캐닝
* **글로벌 실적 캘린더 (Earnings):** 어닝 발표 & 주요 거시/매크로 지표 일정

## 🛠 수정 및 유지보수 가이드

만약 코드를 다르게 수정하거나 업그레이드하고 싶다면 아래의 절차를 따르시면 됩니다:

1. Mac의 `Finder`나 텍스트 에디터(VS Code 등)로 `/Users/jaewoonglee/.gemini/antigravity/scratch/update_dashboard.py` 파일을 엽니다.
2. 파이썬 코드 하단의 `html_template = f""" ... """` 내부의 HTML/CSS 태그를 입맛대로 수정합니다. (글씨 크기, 색상, 레이아웃 등)
3. 터미널(Terminal)을 열고 구동 폴더로 이동한 뒤 `python3 update_dashboard.py`를 한 번 실행해 줍니다.
4. 즉시 스크립트가 알아서 GitHub로 변경 사항을 쏘아보내며 업데이트가 3분 내에 사이트에 반영됩니다.

---
*Created by Lee & Antigravity AI (2026.03)*
