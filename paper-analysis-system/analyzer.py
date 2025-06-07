import os
import asyncio
# import openai # OpenAI API call is simulated
from typing import Dict, List

class PaperAnalyzer:
    """논문 AI 분석 엔진 (현재 시뮬레이션 모드)"""

    def __init__(self):
        # In a live environment, you would set the API key:
        # openai.api_key = os.getenv('OPENAI_API_KEY')
        # if not openai.api_key:
        #     print("Warning: OPENAI_API_KEY environment variable not set.")
        print("PaperAnalyzer Initialized (Simulated Mode - OpenAI API not called).")

    async def analyze(self, paper_data: Dict) -> Dict:
        """5단계 정밀 분석 수행 (시뮬레이션)"""
        print(f"PaperAnalyzer: Starting simulated analysis for paper titled '{paper_data.get('title', 'N/A')}'...")

        # Create the detailed prompt that would be sent to GPT-4
        prompt = self._create_analysis_prompt(paper_data)
        # print(f"Generated analysis prompt for GPT-4 (simulated):
{prompt}") # For debugging, can be verbose

        # Simulate GPT-4 API call delay
        await asyncio.sleep(0.3) # Simulate processing time

        # Simulate a response from GPT-4. This response should match the structure
        # expected by _parse_analysis_result and the 5-stage analysis format.
        simulated_gpt4_response = self._generate_simulated_gpt4_response(paper_data)

        print("PaperAnalyzer: Simulated analysis complete. Parsing results...")
        return self._parse_analysis_result(simulated_gpt4_response, paper_data) # Pass paper_data for context if needed

    def _create_analysis_prompt(self, paper_data: Dict) -> str:
        """실제 GPT-4에 전달될 분석 프롬프트를 생성합니다."""
        results_formatted = self._format_results_for_prompt(paper_data.get('results', []))

        # Ensure all keys exist in paper_data, provide defaults if not
        title = paper_data.get('title', '제목 없음')
        authors = paper_data.get('authors', '저자 정보 없음')
        abstract = paper_data.get('abstract', '초록 없음')
        introduction = paper_data.get('introduction', '서론 없음')
        discussion = paper_data.get('discussion', '토론 없음')

        return f"""
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

    def _format_results_for_prompt(self, results: List[Dict]) -> str:
        """Results 섹션을 프롬프트에 포함하기 좋게 포맷팅합니다."""
        if not results:
            return "결과 섹션 내용 없음."

        formatted_parts = []
        for i, result_item in enumerate(results, 1):
            subtitle = result_item.get('subtitle', f'결과 {i}')
            content = result_item.get('content', '내용 없음')
            formatted_parts.append(f"#### {i}. {subtitle}\n{content}")
        return "\n\n".join(formatted_parts) # Ensure newlines are escaped for the f-string

    def _generate_simulated_gpt4_response(self, paper_data: Dict) -> str:
        """GPT-4의 응답을 시뮬레이션합니다. paper_data를 기반으로 내용을 채웁니다."""
        title = paper_data.get('title', 'N/A')
        results_list = paper_data.get('results', [])

        sim_results_analysis = []
        if results_list:
            for res in results_list:
                sim_results_analysis.append(
                    f"### {res.get('subtitle', '알 수 없는 소제목')}\n"
                    f"- **새로운 과학적 발견**: 이 '{res.get('subtitle', '결과')}'는 시뮬레이션된 환경에서 중요한 가상적 발견을 제시합니다.\n"
                    f"- **정량적 실험 결과**: 데이터에 따르면, 시뮬레이션된 값은 평균 X이고 표준편차는 Y입니다.\n"
                    f"- **혁신적 결과물/방법론**: 해당 없음 (시뮬레이션된 기본 결과).\n"
                    f"- **논문 전체 기여도**: 이 가상 결과는 논문의 시뮬레이션된 목표에 크게 기여합니다."
                )
        else:
            sim_results_analysis.append("### 결과 없음\n분석할 결과 데이터가 제공되지 않았습니다.")

        sim_results_section_str = "\n\n".join(sim_results_analysis)

        return f"""
### 1. Abstract 정량 분석
- **연구 배경**: 이 시뮬레이션된 논문 '{title}'은 가상의 연구 분야에서 중요한 문제를 다룹니다. 기존의 시뮬레이션된 연구들은 특정 한계를 보여왔습니다.
- **새로운 발견**: 본 시뮬레이션 연구는 해당 분야에서 몇 가지 가상의 새로운 발견을 제시합니다. 예를 들어, X라는 가상 조건에서 Y라는 현상이 관찰되었습니다.
- **참신성/확장성**: 참신성: 이 연구는 기존에 시도되지 않은 가상의 접근법을 사용합니다. 확장성: 이 가상 결과는 다른 시뮬레이션 분야에도 적용될 수 있습니다.
- **핵심 키워드**: 시뮬레이션 (Simulation - 가상 환경 실험), AI 분석 (AI Analysis - 인공지능 기반 분석), {paper_data.get('authors', '저자 불명').split(',')[0].strip()} (연구 방법론 관련 키워드)

### 2. Introduction 키워드 중심 분석
- **5개 핵심 키워드**: 시뮬레이션, AI 분석, 가상 모델링, 데이터 해석, 연구 방법론
- **시뮬레이션**:
  - 연구 배경: 복잡한 시스템을 이해하기 위한 핵심 도구.
  - Unmet Needs: 실제 실험이 어렵거나 비용이 많이 드는 경우의 대안 필요.
  - 차별점: 본 연구는 고도화된 가상 환경을 제공.
- **AI 분석**: (나머지 키워드에 대해서도 유사한 분석이 시뮬레이션될 수 있음)

### 3. Results 소제목별 정밀 분석
{sim_results_section_str}

### 4. Discussion 전략적 분석
- **연구의 제한점**: 이 시뮬레이션은 실제 세계의 모든 변수를 반영하지 못했습니다. 또한, 사용된 가상 데이터셋의 크기가 제한적이었습니다.
- **향후 연구 방향**: 더 복잡한 시뮬레이션 모델을 개발하고, 다양한 가상 시나리오에서 테스트할 필요가 있습니다.
- **새로운 메커니즘/접근법 제안**: 본 연구의 시뮬레이션 방법론은 다른 복잡계 문제 해결에 적용될 수 있는 새로운 프레임워크를 제시합니다.

### 5. Strategic Insight (정량 평가)
- **참신성** (4/5점): 가상 문제에 대한 새로운 시뮬레이션 접근법을 제시했습니다. (차별점: 알고리즘 A와 B의 결합)
- **확장성** (5/5점): 이 시뮬레이션 프레임워크는 다양한 산업의 가상 테스트에 응용될 수 있습니다. (예: 가상 제조 공정 최적화)
- **핵심 통찰** (한 문장 요약): 시뮬레이션을 통한 AI 분석은 현실 문제 해결에 대한 비용 효율적이고 강력한 통찰을 제공할 수 있습니다.
"""

    async def _call_gpt4_live(self, prompt: str) -> str:
        """실제 GPT-4 API를 호출합니다. (현재는 사용되지 않음)"""
        # This is where the actual OpenAI API call would be made.
        # Ensure openai library is imported and API key is set.
        # response = await openai.ChatCompletion.acreate( # Use acreate for async
        #     model="gpt-4-turbo", # Or your preferred model
        #     messages=[
        #         {"role": "system", "content": "You are a world-class research analyst tasked with meticulous and accurate paper analysis."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.1, # Low temperature for factual, consistent output
        #     max_tokens=4000  # Adjust as needed, ensure it's enough for comprehensive analysis
        # )
        # return response.choices[0].message.content
        raise NotImplementedError("Live GPT-4 call is not enabled in this simulation.")

    def _parse_analysis_result(self, gpt_response_text: str, paper_data: Dict) -> Dict:
        """GPT 응답 텍스트를 구조화된 Dict로 파싱합니다."""
        # This is a simplified parser. A more robust parser would use regex or
        # structured parsing if GPT-4 can be prompted to return JSON.
        # For now, we'll extract sections based on "### " headers.

        sections = {}
        current_section_title = None
        current_section_content = []

        for line in gpt_response_text.split('\n'): # Assuming response uses escaped newlines
            if line.startswith("### "):
                if current_section_title: # Save previous section
                    sections[self._normalize_section_title(current_section_title)] = "\n".join(current_section_content).strip()
                current_section_title = line.replace("### ", "").strip()
                current_section_content = []
            elif current_section_title:
                current_section_content.append(line)

        if current_section_title: # Save the last section
            sections[self._normalize_section_title(current_section_title)] = "\n".join(current_section_content).strip()

        # Fallback for section keys expected by result.html template
        # These keys are based on the tab names in result.html
        # (abstract, introduction, results, discussion, insight)
        # The _normalize_section_title should try to match these.

        return {
            'raw_analysis': gpt_response_text,
            'sections': { # Ensure keys match what result.html expects for tabs
                'abstract': sections.get('abstract정량분석', sections.get('abstract', 'Abstract 분석 내용 없음')),
                'introduction': sections.get('introduction키워드중심분석', sections.get('introduction', 'Introduction 분석 내용 없음')),
                'results': sections.get('results소제목별정밀분석', sections.get('results', 'Results 분석 내용 없음')),
                'discussion': sections.get('discussion전략적분석', sections.get('discussion', 'Discussion 분석 내용 없음')),
                'insight': sections.get('strategicinsight정량평가', sections.get('insight', 'Strategic Insight 내용 없음'))
            },
            'keywords': self._extract_keywords_from_text(gpt_response_text),
            'insights': self._extract_insights_from_text(gpt_response_text, sections)
        }

    def _normalize_section_title(self, title: str) -> str:
        # Normalize titles like "1. Abstract 정량 분석" to "abstract" for dict keys
        title_lower = title.lower()
        if "abstract" in title_lower: return "abstract"
        if "introduction" in title_lower: return "introduction"
        if "results" in title_lower: return "results"
        if "discussion" in title_lower: return "discussion"
        if "strategic insight" in title_lower or "정량 평가" in title_lower : return "insight"
        # Fallback, try to remove numbers and spaces
        normalized = re.sub(r'^\d+\.\s*', '', title_lower) # Remove "1. "
        normalized = re.sub(r'\s+', '', normalized) # Remove spaces
        return normalized if normalized else "unknown_section"


    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """응답 텍스트에서 키워드를 추출합니다. (시뮬레이션용)"""
        # Example: Look for a line like "핵심 키워드: Keyword1, Keyword2"
        keywords = []
        for line in text.split('\n'):
            if "핵심 키워드:" in line:
                # Crude extraction, assumes "핵심 키워드: A (Desc A), B (Desc B)"
                parts = line.split(":", 1)[1].split(',')
                for part in parts:
                    keyword_match = re.match(r'\s*([^(]+)', part) # Get text before parenthesis
                    if keyword_match:
                        keywords.append(keyword_match.group(1).strip())
                if keywords: break # Found keyword line
        if not keywords: # Fallback
            keywords.extend(["시뮬레이션 키워드 A", "AI 생성 콘텐츠", "논문 분석"])
        return list(set(keywords))[:10] # Return unique keywords, max 10

    def _extract_insights_from_text(self, text: str, sections: Dict) -> Dict:
        """응답 텍스트나 파싱된 섹션에서 Strategic Insight 점수 및 요약을 추출합니다. (시뮬레이션용)"""
        insights = {
            '참신성': "평가 없음",
            '확장성': "평가 없음",
            '핵심 통찰': "핵심 통찰 요약 없음"
        }

        insight_text = sections.get('insight', '')
        if not insight_text: # Try to find it in raw text if not in parsed sections
            for line in text.split('\n'):
                if "Strategic Insight" in line or "참신성" in line or "확장성" in line:
                    insight_text += line + "\n"

        # Crude extraction from insight_text
        novelty_match = re.search(r'참신성\s*\((\d+/\d+점?)\):\s*(.*)', insight_text)
        if novelty_match:
            insights['참신성'] = f"{novelty_match.group(1)} - {novelty_match.group(2).strip()}"
        else: # Fallback if specific format not found
            novelty_match_simple = re.search(r'참신성\s*\(?(\d+/\d+점?)\)?', insight_text)
            if novelty_match_simple: insights['참신성'] = novelty_match_simple.group(1)


        scalability_match = re.search(r'확장성\s*\((\d+/\d+점?)\):\s*(.*)', insight_text)
        if scalability_match:
            insights['확장성'] = f"{scalability_match.group(1)} - {scalability_match.group(2).strip()}"
        else:
            scalability_match_simple = re.search(r'확장성\s*\(?(\d+/\d+점?)\)?', insight_text)
            if scalability_match_simple: insights['확장성'] = scalability_match_simple.group(1)


        summary_match = re.search(r'핵심 통찰\s*\(한 문장 요약\):\s*(.*)', insight_text)
        if summary_match:
            insights['핵심 통찰'] = summary_match.group(1).strip()
        elif not insights['핵심 통찰'] or insights['핵심 통찰'] == "핵심 통찰 요약 없음": # Fallback for summary
            summary_match_simple = re.search(r'핵심 통찰:\s*(.*)', insight_text)
            if summary_match_simple: insights['핵심 통찰'] = summary_match_simple.group(1).strip()


        # Fallbacks if regex fails
        if insights['참신성'] == "평가 없음": insights['참신성'] = "3/5점 (시뮬레이션)"
        if insights['확장성'] == "평가 없음": insights['확장성'] = "4/5점 (시뮬레이션)"
        if insights['핵심 통찰'] == "핵심 통찰 요약 없음": insights['핵심 통찰'] = "시뮬레이션된 AI 분석은 유용합니다."

        return insights

print("paper-analysis-system/analyzer.py created with simulated analysis logic.")
