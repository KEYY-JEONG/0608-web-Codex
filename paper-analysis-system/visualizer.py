import os
import uuid
import asyncio
# import anthropic # Anthropic API call is simulated
from typing import Dict

class PaperVisualizer:
    """논문 시각화 생성기 (현재 시뮬레이션 모드)"""

    def __init__(self):
        # In a live environment, you would set the API key:
        # self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        # if not os.getenv('ANTHROPIC_API_KEY'):
        #     print("Warning: ANTHROPIC_API_KEY environment variable not set.")
        print("PaperVisualizer Initialized (Simulated Mode - Anthropic API not called).")

    async def create(self, analysis_result: Dict) -> str: # Returns HTML string
        """그래픽 레코딩 스타일 시각화 생성 (시뮬레이션)"""
        # analysis_result is the dictionary from PaperAnalyzer.analyze()
        # It contains 'raw_analysis', 'sections', 'keywords', 'insights'.

        print(f"PaperVisualizer: Starting simulated visualization for analysis of '{analysis_result.get('paper_data', {}).get('title', 'N/A')}'...")

        prompt = self._create_visualization_prompt(analysis_result)
        # print(f"Generated visualization prompt for Claude (simulated):
{prompt}") # For debugging

        # Simulate Claude API call delay
        await asyncio.sleep(0.2) # Simulate processing time

        # Generate a simulated HTML response based on the analysis_result
        simulated_html_content = self._generate_simulated_claude_response(analysis_result)

        print("PaperVisualizer: Simulated visualization complete.")
        # The original plan mentioned _save_visualization, but app.py expects HTML content directly.
        # If saving to a file and returning a path was intended, app.py and result.html would need adjustment.
        return simulated_html_content

    def _create_visualization_prompt(self, analysis: Dict) -> str:
        """실제 Claude에 전달될 시각화 프롬프트를 생성합니다."""
        # analysis is the dict from PaperAnalyzer, containing 'raw_analysis', 'sections', etc.
        raw_analysis_summary = analysis.get('raw_analysis', '분석 내용 없음.')[:1000] # Use a summary

        return f"""
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
-   Abstract 요약: `{analysis.get('sections', {}).get('abstract', 'N/A')[:100]}...`
-   Introduction 키워드: `{', '.join(analysis.get('keywords', ['키워드 없음'])[:3])}`
-   Results 하이라이트: (Results 섹션 내용에서 주요 발견 1-2개 요약)
-   Discussion 포인트: `{analysis.get('sections', {}).get('discussion', 'N/A')[:100]}...`
-   참신성 점수: `{analysis.get('insights', {}).get('참신성', 'N/A')}`
-   확장성 점수: `{analysis.get('insights', {}).get('확장성', 'N/A')}`

위 요구사항을 충실히 반영하여, 정보 전달력이 높고 시각적으로 매력적인 HTML 인포그래픽을 만들어주세요.
"""

    def _generate_simulated_claude_response(self, analysis: Dict) -> str:
        """Claude의 HTML 응답을 시뮬레이션합니다."""

        # Extract data from analysis_result for the infographic
        title = analysis.get('paper_data', {}).get('title', '논문 제목 없음')
        sections = analysis.get('sections', {})
        keywords = analysis.get('keywords', [])
        insights = analysis.get('insights', {})

        abstract_summary = sections.get('abstract', '초록 분석 내용이 없습니다.')[:300] + "..."
        intro_summary = sections.get('introduction', '서론 분석 내용이 없습니다.')[:250] + "..."
        results_summary = sections.get('results', '결과 분석 내용이 없습니다.')[:400] + "..."
        discussion_summary = sections.get('discussion', '토론 분석 내용이 없습니다.')[:300] + "..."

        keywords_html = "".join([f"<span class='keyword-tag'>{kw}</span>" for kw in keywords[:5]])

        novelty_score_text = insights.get('참신성', '3/5점')
        scalability_score_text = insights.get('확장성', '4/5점')

        # Simple star rating simulation
        def get_stars(score_text):
            try:
                score = int(score_text.split('/')[0])
                return '⭐' * score + '☆' * (5 - score)
            except:
                return score_text # fallback

        novelty_stars = get_stars(novelty_score_text)
        scalability_stars = get_stars(scalability_score_text)
        insight_summary = insights.get('핵심 통찰', '핵심 통찰 요약이 없습니다.')

        # HTML Structure
        html_template = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>논문 분석 인포그래픽: {title}</title>
    <style>
        body {{
            font-family: 'Comic Sans MS', 'Nanum Pen Script', 'Kalam', cursive, sans-serif; /* 손글씨 느낌 폰트 */
            background: linear-gradient(135deg, #e0f7fa, #b3e5fc); /* 파란색 계열 그라데이션 */
            color: #0A1F44; /* 진한 파랑 텍스트 */
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: auto;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }}
        h1, h2, h3 {{
            color: #005A9C; /* 포인트 파란색 */
            text-align: center;
        }}
        h1 {{ font-size: 2em; margin-bottom: 10px; }}
        h2 {{ font-size: 1.5em; margin-bottom: 20px; border-bottom: 2px dashed #80D8FF; padding-bottom: 10px; }}
        h3 {{ font-size: 1.2em; margin-bottom: 10px; text-align:left; color: #1e3a8a; }}

        .columns {{
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-top: 20px;
        }}
        .column {{
            flex: 1;
            background-color: #ffffff;
            border: 1px solid #80D8FF;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .column:hover {{
            transform: translateY(-5px);
        }}
        .card-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #0A1F44;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid #80D8FF;
        }}
        .keyword-tag {{
            display: inline-block;
            background-color: #ffe082; /* 노란색 계열 강조 */
            color: #0A1F44;
            padding: 5px 10px;
            border-radius: 20px;
            margin: 3px;
            font-size: 0.9em;
        }}
        .icon {{
            font-size: 1.5em;
            margin-right: 8px;
        }}
        .insight-item {{
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f0f9ff;
            border-left: 4px solid #0077cc;
            border-radius: 4px;
        }}
        .insight-item strong {{ color: #005A9C; }}
        .stars {{ color: #ffc107; font-size: 1.2em; }} /* 별점 색상 */
    </style>
</head>
<body>
    <div class="container">
        <h1><span class="icon">🔬</span>논문 분석 인포그래픽 (시뮬레이션)<span class="icon">💡</span></h1>
        <h2>{title}</h2>

        <div class="columns">
            <!-- Left Column: Abstract & Introduction -->
            <div class="column">
                <h3 class="card-title"><span class="icon">📜</span>Abstract & Intro 요약</h3>
                <h4>Abstract</h4>
                <p>{abstract_summary}</p>
                <h4>Introduction</h4>
                <p>{intro_summary}</p>
                <h4><span class="icon">🔑</span>주요 키워드:</h4>
                <div>{keywords_html if keywords_html else "키워드 없음"}</div>
            </div>

            <!-- Middle Column: Results -->
            <div class="column">
                <h3 class="card-title"><span class="icon">📊</span>Results 하이라이트</h3>
                <p>{results_summary}</p>
                <!-- Simple simulated bar chart -->
                <div style="margin-top: 20px; text-align: center;">
                    <h4>가상 데이터 시각화 (예시)</h4>
                    <svg width="100%" height="100" viewBox="0 0 200 100">
                        <rect x="20" y="30" width="30" height="70" fill="#80D8FF" rx="3"><title>데이터 A: 70%</title></rect>
                        <rect x="60" y="50" width="30" height="50" fill="#4fc3f7" rx="3"><title>데이터 B: 50%</title></rect>
                        <rect x="100" y="20" width="30" height="80" fill="#29b6f6" rx="3"><title>데이터 C: 80%</title></rect>
                        <rect x="140" y="60" width="30" height="40" fill="#03a9f4" rx="3"><title>데이터 D: 40%</title></rect>
                        <line x1="10" y1="100" x2="190" y2="100" stroke="#0A1F44" stroke-width="2"/>
                    </svg>
                </div>
            </div>

            <!-- Right Column: Discussion & Insights -->
            <div class="column">
                <h3 class="card-title"><span class="icon">💭</span>Discussion & Strategic Insights</h3>
                <h4>Discussion 요점</h4>
                <p>{discussion_summary}</p>
                <h4 style="margin-top:20px;">Strategic Insights</h4>
                <div class="insight-item">
                    <strong>참신성:</strong> <span class="stars">{novelty_stars}</span> ({novelty_score_text})<br/>
                    {insights.get('참신성', '설명 없음').split(' - ')[-1] if ' - ' in insights.get('참신성', '') else ''}
                </div>
                <div class="insight-item">
                    <strong>확장성:</strong> <span class="stars">{scalability_stars}</span> ({scalability_score_text})<br/>
                    {insights.get('확장성', '설명 없음').split(' - ')[-1] if ' - ' in insights.get('확장성', '') else ''}
                </div>
                <div class="insight-item">
                    <strong><span class="icon">🎯</span>핵심 통찰:</strong> {insight_summary}
                </div>
            </div>
        </div>
        <p style="text-align:center; margin-top:30px; font-size:0.8em;">Generated by AI Paper Visualizer (Simulated) - {uuid.uuid4()}</p>
    </div>
</body>
</html>
"""
        return html_template

    async def _call_claude_live(self, prompt: str) -> str:
        """실제 Claude API를 호출합니다. (현재는 사용되지 않음)"""
        # This is where the actual Anthropic API call would be made.
        # Ensure anthropic library is imported and API key is set via self.client.
        # message = await self.client.messages.acreate( # Use acreate for async
        #     model="claude-3-opus-20240229", # Or your preferred model
        #     max_tokens=4000, # Adjust as needed for HTML output
        #     temperature=0.2, # Temperature for creative tasks like this might be slightly higher
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return message.content[0].text # Assuming response is HTML in the first text block
        raise NotImplementedError("Live Claude call is not enabled in this simulation.")

print("paper-analysis-system/visualizer.py created with simulated visualization logic.")
