# Paper Analysis System (논문 분석 시스템)

본 프로젝트는 웹 기반의 논문 분석 시스템입니다. 사용자가 논문 URL을 입력하면 해당 논문의 내용을 스크래핑하고, AI를 활용하여 분석 결과를 제공하며, 다양한 형식의 보고서를 생성합니다.

## 주요 기능

- **논문 데이터 스크래핑**: 제공된 URL로부터 논문의 제목, 저자, 초록 등의 기본 정보를 추출합니다.
- **AI 기반 내용 분석**: OpenAI 또는 Anthropic과 같은 LLM을 활용하여 논문의 주요 내용, 주제, 핵심 키워드, 강점 및 약점 등을 심층적으로 분석합니다.
- **분석 결과 시각화**: 분석된 데이터를 바탕으로 이해하기 쉬운 시각 자료를 생성합니다 (구체적인 시각화 내용은 `visualizer.py`에 따라 다를 수 있음).
- **보고서 생성 및 다운로드**: 분석 결과를 Markdown 및 DOCX 파일 형식으로 정리하여 사용자가 다운로드할 수 있도록 제공합니다.

## 사용 기술 및 라이브러리

- **백엔드**: Flask
- **웹 스크래핑**: Selenium, BeautifulSoup, requests, aiohttp
- **AI 및 NLP**: OpenAI API, Anthropic API (LLM 활용)
- **데이터 처리 및 시각화**: Pillow (이미지 처리 관련, 구체적인 시각화 라이브러리는 `visualizer.py` 확인 필요)
- **문서 생성**: python-docx (DOCX), Markdown
- **기타**: python-dotenv (환경 변수 관리), asyncio (비동기 처리)

주요 의존성 패키지 목록은 `requirements.txt` 파일에서 확인할 수 있습니다.

## 로컬 환경 설정 및 실행 방법

아래 단계를 따라 로컬 환경에서 논문 분석 시스템을 설정하고 실행할 수 있습니다.

1.  **프로젝트 저장소 복제 (Clone)**:
    ```bash
    git clone <repository_url>
    cd paper-analysis-system
    ```
    *`<repository_url>`을 실제 Git 저장소 URL로 변경해주세요.*

2.  **가상 환경 생성 및 활성화**:
    Python 가상 환경을 생성하고 활성화합니다. 이는 프로젝트별 의존성을 관리하는 데 도움이 됩니다.
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **의존성 패키지 설치**:
    `requirements.txt` 파일에 명시된 모든 필수 라이브러리를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

4.  **환경 변수 설정**:
    `.env` 파일을 프로젝트 루트 디렉토리(`paper-analysis-system/`)에 생성하고 필요한 환경 변수를 설정합니다. `.env.example` 파일이 있다면 해당 파일을 복사하여 `.env` 파일을 만드세요. (만약 `.env.example` 파일이 없다면 아래 내용을 참고하여 직접 생성합니다.)

    최소한 다음 환경 변수가 필요할 수 있습니다:
    ```env
    FLASK_SECRET_KEY='your_very_secret_flask_key_here'
    # OPENAI_API_KEY='your_openai_api_key_if_using_openai'
    # ANTHROPIC_API_KEY='your_anthropic_api_key_if_using_anthropic'
    # 기타 필요한 API 키 또는 설정
    ```
    *`FLASK_SECRET_KEY`는 Flask 세션 관리를 위해 필수적입니다. 복잡하고 예측 불가능한 문자열로 설정하세요.*
    *AI 서비스(OpenAI, Anthropic 등)를 사용한다면 해당 서비스의 API 키를 위와 같이 설정해야 합니다.*

5.  **웹 드라이버 설정 (Selenium 사용 시)**:
    Selenium이 웹 브라우저를 제어하기 위해서는 해당 브라우저의 웹 드라이버가 필요합니다. `webdriver-manager`가 대부분 자동으로 처리해주지만, 문제가 발생할 경우 수동으로 설치 및 경로 설정이 필요할 수 있습니다.
    - Chrome: [ChromeDriver](https://chromedriver.chromium.org/downloads)
    - Firefox: [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
    - Edge: [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

    다운로드한 웹 드라이버가 시스템 PATH에 등록되어 있거나, 애플리케이션 코드 내에서 직접 경로를 지정해야 할 수 있습니다.

6.  **Flask 개발 서버 실행**:
    모든 설정이 완료되면 Flask 개발 서버를 시작합니다.
    ```bash
    python app.py
    ```
    또는 (만약 `Procfile`이나 다른 실행 스크립트가 있다면 해당 방법을 따르세요):
    ```bash
    flask run
    ```
    서버가 성공적으로 시작되면, 터미널에 표시된 URL (기본적으로 `http://127.0.0.1:5001` 또는 `http://localhost:5001`)을 웹 브라우저에서 열어 애플리케이션에 접속할 수 있습니다. `app.py`에서 포트 번호가 다르게 설정되어 있을 수 있으니 실행 시 터미널 출력을 확인하세요.

## 프로젝트 구조

주요 파일 및 디렉토리 구성은 다음과 같습니다:

```
paper-analysis-system/
├── .env                   # 환경 변수 파일 (주의: Git에 커밋하지 마세요)
├── app.py                 # Flask 애플리케이션의 메인 파일, 라우팅 및 핵심 로직 처리
├── scraper.py             # 웹 스크래핑 로직 담당
├── analyzer.py            # AI를 이용한 논문 분석 로직 담당
├── visualizer.py          # 분석 결과 시각화 로직 담당
├── requirements.txt       # Python 의존성 패키지 목록
├── static/                # CSS, JavaScript, 이미지 등 정적 파일
│   ├── css/
│   │   └── style.css      # 기본 스타일시트
│   └── js/
│       └── app.js         # 프론트엔드 JavaScript 로직
├── templates/             # HTML 템플릿 파일
│   ├── index.html         # 메인 페이지
│   ├── loading.html       # 분석 진행 중 로딩 페이지
│   └── result.html        # 분석 결과 표시 페이지
└── utils/                 # 유틸리티 모듈
    ├── doc_generator.py   # Markdown, DOCX 등 문서 생성 로직
    ├── paper_parser.py    # 스크래핑된 데이터 파싱 로직 (있을 경우)
    └── prompt_manager.py  # AI 프롬프트 관리 로직 (있을 경우)
```

- **`app.py`**: Flask 애플리케이션의 진입점입니다. HTTP 요청을 처리하고, 각 모듈(스크래퍼, 분석기 등)을 호출하며, 사용자에게 HTML 페이지를 렌더링합니다.
- **`scraper.py`**: 특정 URL에서 논문 정보를 가져오는 코드를 포함합니다.
- **`analyzer.py`**: 가져온 논문 데이터를 AI 모델(예: GPT, Claude)에 전달하고 분석 결과를 받는 역할을 합니다.
- **`visualizer.py`**: 분석된 데이터를 기반으로 차트나 그래프 등의 시각적 표현을 생성합니다.
- **`utils/`**: 프로젝트 전반에서 사용되는 보조 함수나 클래스들을 모아둔 디렉토리입니다.
    - `doc_generator.py`: 분석 내용을 바탕으로 다운로드 가능한 문서 파일을 생성합니다.
- **`static/`**: CSS, JavaScript 파일과 같이 브라우저에서 직접 사용되는 정적 파일들을 저장합니다.
- **`templates/`**: Flask가 사용자에게 보여줄 HTML 페이지들의 템플릿을 담고 있습니다.
- **`requirements.txt`**: 프로젝트 실행에 필요한 모든 Python 라이브러리들의 목록과 버전 정보가 기록되어 있습니다.
- **`.env`**: API 키, 개발 환경 설정 등 민감하거나 환경에 따라 달라지는 변수들을 저장합니다. **이 파일은 `.gitignore`에 추가하여 Git 저장소에 올라가지 않도록 주의해야 합니다.**

## 기여 및 향후 개선 방향

본 프로젝트는 지속적인 개선과 기능 추가를 환영합니다. 기여하고 싶으시거나 아이디어가 있다면 다음 영역들을 참고해주세요:

### 기여 방법

1.  본 저장소를 Fork합니다.
2.  새로운 기능이나 버그 수정을 위한 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature` 또는 `git checkout -b fix/BugFix`).
3.  변경 사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`).
4.  Fork한 저장소의 브랜치로 Push합니다 (`git push origin feature/AmazingFeature`).
5.  Pull Request를 생성하여 변경 사항을 제안합니다.

### 향후 개선 아이디어

-   **다양한 논문 출처 지원**: 현재 지원하는 웹사이트 외 다른 학술 데이터베이스(예: IEEE Xplore, ACM Digital Library, PubMed Central 등) 지원 확대.
-   **분석 모델 선택 기능**: 사용자가 분석에 사용할 AI 모델(GPT 버전, Claude 버전 등)을 선택할 수 있도록 옵션 제공.
-   **분석 결과 상세화**: 논문의 각 섹션별 요약, 인용 분석, 관련 연구 추천 등 더욱 상세한 분석 정보 제공.
-   **사용자 계정 시스템**: 사용자가 자신의 분석 히스토리를 저장하고 관리할 수 있는 기능.
-   **UI/UX 개선**: 더욱 직관적이고 사용자 친화적인 인터페이스로 개선.
-   **다국어 지원**: 한국어 외 다른 언어로도 서비스 제공.
-   **테스트 코드 강화**: 안정적인 서비스 운영을 위한 단위 테스트 및 통합 테스트 코드 추가.

궁금한 점이나 제안 사항이 있다면 언제든지 이슈를 생성해주세요.
