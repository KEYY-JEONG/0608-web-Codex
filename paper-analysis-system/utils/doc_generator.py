# paper-analysis-system/utils/doc_generator.py

import os
from datetime import datetime

# Attempt to import python-docx, but make it optional for environments where it might not be installed.
try:
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("Warning: python-docx library not found. DOCX generation will be simulated as plain text.")

class DocumentGenerator:
    """
    분석 결과를 Markdown 및 DOCX (if library available) 문서로 변환합니다.
    """
    def __init__(self):
        self.output_base_dir = 'paper-analysis-system/outputs'
        # Ensure base output directories exist within the paper-analysis-system folder
        # The subtask runs from the repo root, so paths should be relative to that.
        os.makedirs(os.path.join(self.output_base_dir, 'markdown'), exist_ok=True)
        os.makedirs(os.path.join(self.output_base_dir, 'docx'), exist_ok=True)
        print(f"DocumentGenerator Initialized. DOCX available: {DOCX_AVAILABLE}")
        print(f"Output directory set to: {os.path.abspath(self.output_base_dir)}")


    def generate(self, data_for_docs: dict) -> dict:
        """
        MD와 DOCX 문서를 생성하고, 다운로드 가능한 URL 경로를 반환합니다.
        `data_for_docs` 딕셔너리는 'paper_data'와 'analysis' 키를 포함해야 합니다.
        'analysis'는 'raw_analysis' 키를 포함해야 합니다.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        paper_data = data_for_docs.get('paper_data', {})
        analysis_sub_dict = data_for_docs.get('analysis', {}) # This is the dict from PaperAnalyzer

        title = paper_data.get('title', 'N/A')
        authors = paper_data.get('authors', 'N/A')
        # raw_analysis is a key within the 'analysis' sub-dictionary
        raw_analysis_content = analysis_sub_dict.get('raw_analysis', '분석 내용 없음.')

        print(f"DocumentGenerator: Generating documents for '{title}' (Timestamp: {timestamp})")

        # Markdown 생성
        md_filename = f'analysis_{timestamp}.md'
        md_filepath = os.path.join(self.output_base_dir, 'markdown', md_filename)
        self._generate_markdown(md_filepath, title, authors, raw_analysis_content)

        # DOCX 생성 (실제 .docx 또는 시뮬레이션된 .txt)
        docx_filename = f'analysis_{timestamp}.docx'
        docx_filepath = os.path.join(self.output_base_dir, 'docx', docx_filename)
        self._generate_docx(docx_filepath, title, authors, raw_analysis_content)

        # Flask 앱의 @app.route('/download/md/<filename>') 에 맞춰 URL 생성
        # os.path.basename()을 사용하여 파일명만 URL에 포함
        return {
            'markdown_url': f'/download/md/{os.path.basename(md_filepath)}',
            'docx_url': f'/download/docx/{os.path.basename(docx_filepath)}'
        }

    def _generate_markdown(self, filepath: str, title: str, authors: str, raw_analysis: str):
        """Markdown 문서를 생성하고 저장합니다."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"**저자**: {authors}\n\n")
                f.write("---\n\n")
                # raw_analysis는 이미 개행문자를 포함한 텍스트 블록일 것으로 예상됨
                # Python 문자열의 \n이 실제 파일의 개행으로 잘 변환되도록 직접 작성
                for line in raw_analysis.split('\n'): # raw_analysis가 이스케이프된 \n을 가질 경우
                    f.write(line + '\n')
            print(f"Markdown document successfully generated: {filepath}")
        except Exception as e:
            print(f"Error writing Markdown file {filepath}: {e}")
            # 오류 발생 시 빈 파일이라도 생성하여 경로 반환은 유지 (혹은 오류 처리)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Error generating Markdown for {title}\nError: {e}")


    def _generate_docx(self, filepath: str, title: str, authors: str, raw_analysis: str):
        """DOCX 문서를 생성하고 저장합니다. python-docx가 없으면 .txt로 시뮬레이션합니다."""
        if DOCX_AVAILABLE:
            try:
                doc = Document()

                # 제목
                heading = doc.add_heading(title, level=0) # Level 0 for main title
                heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

                # 저자
                author_para = doc.add_paragraph()
                author_para.add_run(f"저자: {authors}").italic = True
                author_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                doc.add_paragraph() # Add a space after authors

                # 분석 내용 - raw_analysis의 각 줄을 처리
                # raw_analysis가 "### Section Title" 같은 마크다운 스타일 헤더를 포함할 수 있음
                current_heading_level = 1
                for line in raw_analysis.split('\n'): # raw_analysis가 이스케이프된 \n을 가질 경우
                    stripped_line = line.strip()
                    if stripped_line.startswith('### '): # H3 in Markdown
                        doc.add_heading(stripped_line.replace('### ', ''), level=3)
                    elif stripped_line.startswith('## '): # H2 in Markdown
                        doc.add_heading(stripped_line.replace('## ', ''), level=2)
                    elif stripped_line.startswith('# '): # H1 in Markdown (though unlikely within raw_analysis body)
                        doc.add_heading(stripped_line.replace('# ', ''), level=1)
                    elif stripped_line.startswith('- '): # List item
                        # Simple list item, add with bullet. More complex list needed proper paragraph style
                        doc.add_paragraph(stripped_line, style='ListBullet')
                    elif stripped_line: # Non-empty line
                        doc.add_paragraph(stripped_line)
                    # else: skip empty lines or add paragraph break if desired
                        # doc.add_paragraph() # for explicit empty line

                # 기본 폰트 설정 (예시)
                style = doc.styles['Normal']
                font = style.font
                font.name = 'Calibri' # Or another common font
                font.size = Pt(11)

                doc.save(filepath)
                print(f"DOCX document successfully generated: {filepath}")
                return
            except Exception as e:
                print(f"Error writing DOCX file {filepath} using python-docx: {e}")
                # Fallback to text simulation if docx saving fails for some reason
                self._simulate_docx_as_text(filepath, title, authors, raw_analysis, error_message=str(e))
        else:
            # python-docx is not available, simulate with a .txt file (though extension is .docx)
            self._simulate_docx_as_text(filepath, title, authors, raw_analysis)

    def _simulate_docx_as_text(self, filepath: str, title: str, authors: str, raw_analysis: str, error_message: str = None):
        """DOCX 생성을 텍스트 파일로 시뮬레이션합니다."""
        sim_filepath = filepath # Keep .docx extension as planned, but content will be text
        try:
            with open(sim_filepath, 'w', encoding='utf-8') as f:
                f.write(f"--- DOCX SIMULATION (python-docx not available or failed) ---\n\n")
                if error_message:
                    f.write(f"--- Original DOCX Generation Error: {error_message} ---\n\n")
                f.write(f"Title: {title}\n")
                f.write(f"Authors: {authors}\n\n")
                f.write("--- Analysis Content ---\n")
                for line in raw_analysis.split('\n'):
                    f.write(line + '\n')
            print(f"Simulated DOCX (as plain text) generated: {sim_filepath}")
        except Exception as e:
            print(f"Error writing simulated DOCX text file {sim_filepath}: {e}")


if __name__ == '__main__':
    # Example Usage
    # Create a dummy outputs structure for local testing if it doesn't exist
    if not os.path.exists('paper-analysis-system/outputs/markdown'):
        os.makedirs('paper-analysis-system/outputs/markdown')
    if not os.path.exists('paper-analysis-system/outputs/docx'):
        os.makedirs('paper-analysis-system/outputs/docx')

    generator = DocumentGenerator()
    sample_doc_data = {
        'paper_data': {
            'title': 'My Sample Analysis Paper',
            'authors': 'Dr. AI, Prof. Simulation'
        },
        'analysis': {
            # Simulating raw_analysis with escaped newlines
            'raw_analysis': ("### 1. Simulated Abstract\nThis is the abstract of the simulated analysis.\nIt contains key findings.\n\n"
                             "### 2. Simulated Introduction\n- Point one\n- Point two\n\nThis is the intro text.")
        }
    }
    generated_files = generator.generate(sample_doc_data)
    print("\nGenerated File URLs:")
    print(f"  Markdown: {generated_files['markdown_url']}")
    print(f"  DOCX: {generated_files['docx_url']}")

    # Verify files were created (paths are relative to repo root for subtask)
    print("\nVerifying file creation (paths relative to repo root):")
    md_path_to_check = generated_files['markdown_url'].replace('/download/md/', 'paper-analysis-system/outputs/markdown/')
    docx_path_to_check = generated_files['docx_url'].replace('/download/docx/', 'paper-analysis-system/outputs/docx/')
    print(f"  MD file exists: {os.path.exists(md_path_to_check)} at {md_path_to_check}")
    print(f"  DOCX file exists: {os.path.exists(docx_path_to_check)} at {docx_path_to_check}")
    if DOCX_AVAILABLE and os.path.exists(docx_path_to_check):
        print(f"  DOCX file size: {os.path.getsize(docx_path_to_check)} bytes")


print("paper-analysis-system/utils/doc_generator.py created.")
