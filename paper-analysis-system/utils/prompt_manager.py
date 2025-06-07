# paper-analysis-system/utils/prompt_manager.py

# This module is intended to centralize the management of prompts used for
# interacting with Large Language Models (LLMs) like GPT-4 or Claude.
# This helps in keeping prompts organized, versioned, and easily updatable.

# Currently, the prompts are defined directly within the `PaperAnalyzer` and `PaperVisualizer` classes.
# For a more complex system, or if prompts become very long or need A/B testing,
# moving them here would be beneficial.

from typing import Dict, List

def get_paper_analysis_prompt(paper_data: Dict) -> str:
    """
    Generates the prompt for the 5-stage paper analysis (for GPT-4).
    This is a centralized version of the prompt currently in PaperAnalyzer._create_analysis_prompt.
    """
    print(f"prompt_manager.py: Generating paper analysis prompt for '{paper_data.get('title', 'N/A')}'...")

    results_formatted = _format_results_for_prompt(paper_data.get('results', []))

    title = paper_data.get('title', '제목 없음')
    authors = paper_data.get('authors', '저자 정보 없음')
    abstract = paper_data.get('abstract', '초록 없음')
    introduction = paper_data.get('introduction', '서론 없음')
    discussion = paper_data.get('discussion', '토론 없음')

    # This is the same detailed prompt structure as defined in PaperAnalyzer
    prompt = f"""
## 🎯 Mission: 5개 영역 정밀 분석

다음 논문을 분석하여 한국어로 작성해주세요:

**제목**: {title}
**저자**: {authors}
**초록**: {abstract}
**서론**: {introduction}
**결과**:
{results_formatted}
**토론**: {discussion}

### 1. Abstract 정량 분석
- **연구 배경** (3문장): 연구 맥락과 필요성
- **새로운 발견** (3-6문장): 기존 연구에서 밝혀지지 않은 새로운 사실
- **참신성/확장성**: 각각 2문장씩 독창성과 응용 가능성
- **핵심 키워드** (10개): 전문용어는 영어 원문 + 한국어 설명 (예: Mitochondria - 미토콘드리아, 세포 호흡 중추)

### 2. Introduction 키워드 중심 분석
- **5개 핵심 키워드** 선정 (Abstract와 Introduction에서 3회 이상 등장하는 중요 단어)
- 각 키워드마다: 연구 배경, Unmet Needs (미충족 수요), 본 연구의 차별점

### 3. Results 소제목별 정밀 분석 ⭐ 중요 ⭐
- **모든 소제목 추출** - 절대 누락 금지. 각 소제목은 `### 소제목명` 형식으로 명시.
- 각 소제목마다 다음 항목을 상세히 분석:
  - **새로운 과학적 발견** (5문장 내외): 이 결과가 보여주는 핵심적인 새로운 과학적 사실.
  - **정량적 실험 결과** (5문장 내외): 구체적인 데이터, 통계치, 측정값 등을 포함.
  - **혁신적 결과물/방법론**: 이 결과가 제시하는 혁신적인 제품, 기술, 방법론 (해당하는 경우).
  - **논문 전체 기여도**: 이 특정 결과가 논문 전체의 목표 달성에 어떻게 기여하는지.

### 4. Discussion 전략적 분석
- **연구의 제한점**: 연구에서 해결하지 못한 문제, 한계점 및 그 원인 분석.
- **향후 연구 방향**: 본 연구 결과를 바탕으로 제안할 수 있는 구체적인 후속 연구 아이디어.
- **새로운 메커니즘/접근법 제안**: 연구가 제시하는 새로운 과학적 메커니즘이나 문제 해결 접근법, 그리고 이것이 다른 분야에 적용될 가능성.

### 5. Strategic Insight (정량 평가)
- **참신성** (1-5점): 기존 연구 대비 얼마나 새로운가? (구체적 차별점 2-3개 명시)
- **확장성** (1-5점): 다른 분야로의 응용 가능성 및 파급력은? (구체적 예시 포함)
- **핵심 통찰** (한 문장 요약): 이 논문이 주는 가장 중요한 메시지 또는 통찰.

위 형식에 맞춰 정확하고 상세하게 분석해주세요. 모든 섹션은 한국어로 작성되어야 합니다.
"""
    return prompt

def get_visualization_prompt(analysis_result: Dict) -> str:
    """
    Generates the prompt for creating the HTML infographic (for Claude).
    This is a centralized version of the prompt currently in PaperVisualizer._create_visualization_prompt.
    """
    print(f"prompt_manager.py: Generating visualization prompt for analysis of '{analysis_result.get('paper_data', {}).get('title', 'N/A')}'...")

    raw_analysis_summary = analysis_result.get('raw_analysis', '분석 내용 없음.')[:1000] # Use a summary

    # This is the same detailed prompt structure as defined in PaperVisualizer
    prompt = f"""
## 🎯 Mission: 그래픽 레코딩 스타일 HTML 인포그래픽 생성

다음 논문 분석 내용을 기반으로, 파란색 계열을 주로 사용하는 그래픽 레코딩 스타일의 HTML 인포그래픽을 생성해주세요.

**분석 내용 요약**:
{raw_analysis_summary}...
(전체 분석 내용은 제공되었으나 간결성을 위해 여기서는 요약만 표시)

**주요 요구사항**:
1.  **레이아웃**: 3단 컬럼 레이아웃을 사용해주세요.
    *   왼쪽 컬럼: Abstract 및 Introduction 핵심 내용 요약.
    *   중간 컬럼: Results의 주요 발견 및 데이터 시각화 (간단한 막대 차트나 아이콘 형태로 표현 가능).
    *   오른쪽 컬럼: Discussion의 주요 논점 및 Strategic Insights (참신성, 확장성 점수 포함).
2.  **스타일**:
    *   전체적으로 손글씨 느낌의 폰트 (웹 안전 폰트 사용)와 손으로 그린 듯한 도형 및 아이콘을 활용해주세요.
    *   색상 팔레트: 주조색은 파란색 계열 (#0A1F44 진한 파랑 ~ #80D8FF 밝은 하늘색 그라데이션 또는 유사 색상). 강조색으로 노란색 또는 주황색 계열 약간 사용 가능.
    *   컴포넌트: 각 정보 단위는 카드 스타일(둥근 모서리, 그림자 효과)로 표현해주세요.
3.  **콘텐츠**:
    *   핵심 키워드를 시각적으로 강조 (예: 다른 배경색, 굵은 글씨).
    *   이모지나 간단한 아이콘을 활용하여 정보를 더 쉽게 이해할 수 있도록 해주세요. (예: 💡, 🔬, 🎯)
    *   Strategic Insights의 점수는 별점(⭐)이나 게이지 형태로 표현하면 좋습니다.
4.  **출력 형식**: CSS가 포함된 완전한 단일 HTML 문서를 생성해주세요. 외부 파일 링크 없이 모든 스타일은 `<style>` 태그 안에 포함되어야 합니다.

**분석 데이터에서 활용할 주요 항목**:
-   Abstract 요약: `{analysis_result.get('sections', {}).get('abstract', 'N/A')[:100]}...`
-   Introduction 키워드: `{', '.join(analysis_result.get('keywords', ['키워드 없음'])[:3])}`
-   Results 하이라이트: (Results 섹션 내용에서 주요 발견 1-2개 요약)
-   Discussion 포인트: `{analysis_result.get('sections', {}).get('discussion', 'N/A')[:100]}...`
-   참신성 점수: `{analysis_result.get('insights', {}).get('참신성', 'N/A')}`
-   확장성 점수: `{analysis_result.get('insights', {}).get('확장성', 'N/A')}`

위 요구사항을 충실히 반영하여, 정보 전달력이 높고 시각적으로 매력적인 HTML 인포그래픽을 만들어주세요.
"""
    return prompt

def _format_results_for_prompt(results: List[Dict]) -> str:
    """
    Helper function to format the 'results' section of paper_data for inclusion in a prompt.
    (Copied from PaperAnalyzer for consistency, ideally would be a shared utility if not here)
    """
    if not results:
        return "결과 섹션 내용 없음."

    formatted_parts = []
    for i, result_item in enumerate(results, 1):
        subtitle = result_item.get('subtitle', f'결과 {i}')
        content = result_item.get('content', '내용 없음')
        # Ensure content is properly escaped if it might contain problematic characters for f-strings,
        # though for simple text it's usually fine.
        formatted_parts.append(f"#### {i}. {subtitle}\n{content}") # Using escaped newline for f-string
    return "\n\n".join(formatted_parts)


# Example of how these functions might be used (not called by current system directly):
if __name__ == '__main__':
    sample_paper_data = {
        'title': '샘플 논문 제목',
        'authors': '홍길동, 김철수',
        'abstract': '이것은 샘플 논문의 초록입니다...',
        'introduction': '이것은 샘플 논문의 서론입니다...',
        'results': [{'subtitle': '결과 1', 'content': '첫 번째 결과 내용...'}],
        'discussion': '이것은 샘플 논문의 토론입니다...'
    }

    analysis_prompt = get_paper_analysis_prompt(sample_paper_data)
    print(f"--- Generated Analysis Prompt (first 300 chars): ---\n{analysis_prompt[:300]}...\n")

    sample_analysis_result = {
        'paper_data': sample_paper_data,
        'raw_analysis': '이것은 AI가 생성한 샘플 분석 결과입니다...',
        'sections': {'abstract': '초록 요약...', 'introduction': '서론 요약...'},
        'keywords': ['샘플', 'AI', '논문'],
        'insights': {'참신성': '4/5점', '확장성': '5/5점'}
    }
    visualization_prompt = get_visualization_prompt(sample_analysis_result)
    print(f"--- Generated Visualization Prompt (first 300 chars): ---\n{visualization_prompt[:300]}...\n")

print("paper-analysis-system/utils/prompt_manager.py created with example prompt generation functions.")
