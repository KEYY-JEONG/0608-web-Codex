import os
import uuid
import asyncio
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Ensure imports work even if files are not yet in the same dir for the subtask
try:
    from scraper import PaperScraper
    from analyzer import PaperAnalyzer
    from visualizer import PaperVisualizer
    from utils.doc_generator import DocumentGenerator
except ImportError:
    print("Note: Scraper, Analyzer, Visualizer, or DocumentGenerator not found yet. This is okay during initial file creation.")
    # Define dummy classes if they are not found, so Flask can still load
    class PaperScraper: async def scrape(self, url): return {}
    class PaperAnalyzer: async def analyze(self, data): return {}
    class PaperVisualizer: async def create(self, data): return ""
    class DocumentGenerator: def generate(self, data): return {}


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

processing_jobs = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_route(): # Renamed to avoid conflict with analyze function if any
    data = request.get_json()
    paper_url = data.get('url')

    if not paper_url:
        return jsonify({'error': 'URL이 필요합니다'}), 400

    job_id = str(uuid.uuid4())
    processing_jobs[job_id] = {
        'status': 'started',
        'progress': 0,
        'message': '논문 분석을 시작합니다...'
    }

    # For now, we are not running asyncio.create_task directly here
    # to simplify flask app startup for the subtask.
    # In a real deployment, this would trigger the background task.
    # We will simulate completion in the status/result routes for now.
    print(f"Job {job_id} created for URL: {paper_url}. Background processing is simulated.")
    # Start the background task
    asyncio.create_task(process_paper(job_id, paper_url))

    return jsonify({'job_id': job_id})

async def process_paper(job_id, paper_url):
    try:
        processing_jobs[job_id].update({'progress': 10, 'message': '스크래핑 시작 중...'})
        # Ensure PaperScraper is properly instantiated if it was dummied up
        if 'PaperScraper' in globals() and not isinstance(globals()['PaperScraper'](), PaperScraper):
             scraper_instance = globals()['PaperScraper']()
        else:
             scraper_instance = PaperScraper()
        paper_data = await scraper_instance.scrape(paper_url)

        processing_jobs[job_id].update({'progress': 40, 'message': 'AI 분석 중...'})
        if 'PaperAnalyzer' in globals() and not isinstance(globals()['PaperAnalyzer'](), PaperAnalyzer):
            analyzer_instance = globals()['PaperAnalyzer']()
        else:
            analyzer_instance = PaperAnalyzer()
        analysis_result = await analyzer_instance.analyze(paper_data)

        processing_jobs[job_id].update({'progress': 70, 'message': '시각화 생성 중...'})
        if 'PaperVisualizer' in globals() and not isinstance(globals()['PaperVisualizer'](), PaperVisualizer):
            visualizer_instance = globals()['PaperVisualizer']()
        else:
            visualizer_instance = PaperVisualizer()
        visualization = await visualizer_instance.create(analysis_result)

        if 'DocumentGenerator' in globals() and not isinstance(globals()['DocumentGenerator'](), DocumentGenerator):
            doc_gen_instance = globals()['DocumentGenerator']()
        else:
            doc_gen_instance = DocumentGenerator()
        full_data_for_docs = {
            'paper_data': paper_data,
            'analysis': analysis_result
        }
        docs = doc_gen_instance.generate(full_data_for_docs)

        processing_jobs[job_id].update({
            'status': 'completed',
            'progress': 100,
            'message': '분석이 완료되었습니다!',
            'result': {
                'paper_data': paper_data,
                'analysis': analysis_result,
                'visualization': visualization,
                'documents': docs
            }
        })

    except Exception as e:
        print(f"Error processing paper for job {job_id}: {e}")
        processing_jobs[job_id].update({
            'status': 'error',
            'message': f'오류 발생: {str(e)}'
        })

@app.route('/status/<job_id>')
def get_status(job_id):
    if job_id not in processing_jobs:
        return jsonify({'error': '잘못된 작업 ID'}), 404

    # Removed simulation from here; actual progress should be driven by process_paper
    return jsonify(processing_jobs[job_id])

@app.route('/result/<job_id>')
def show_result(job_id):
    if job_id not in processing_jobs:
        return render_template('index.html', message='잘못된 작업 ID입니다.') # Or a dedicated error page

    job = processing_jobs[job_id]
    if job['status'] != 'completed':
        return render_template('loading.html', job_id=job_id)

    # Ensure 'result' key exists, provide defaults if not (e.g. if error occurred)
    result_data = job.get('result', {
        'paper_data': {'title': '오류 발생', 'authors': '정보 없음'},
        'analysis': {'raw_analysis': '분석 중 오류가 발생했습니다.', 'sections': {}, 'keywords': [], 'insights': {}},
        'visualization': '<div>오류로 인해 시각화를 표시할 수 없습니다.</div>',
        'documents': {'markdown_url': '#', 'docx_url': '#'}
    })
    return render_template('result.html', **result_data)

@app.route('/download/md/<path:filename>')
def download_md(filename):
    # This is a placeholder. Actual file serving needs secure path handling.
    # For now, it implies files are in 'paper-analysis-system/outputs/markdown/'
    # A better implementation would use send_from_directory.
    # from flask import send_from_directory
    # return send_from_directory(os.path.join('outputs', 'markdown'), filename)
    return f"Simulated download for Markdown file: {filename} (not implemented securely)"

@app.route('/download/docx/<path:filename>')
def download_docx(filename):
    # from flask import send_from_directory
    # return send_from_directory(os.path.join('outputs', 'docx'), filename)
    return f"Simulated download for DOCX file: {filename} (not implemented securely)"

if __name__ == '__main__':
    # For Flask + asyncio, consider using Quart or an ASGI server like Uvicorn with Gunicorn.
    # The default Flask dev server is WSGI and not ideal for asyncio.
    # `asyncio.create_task` might behave unexpectedly without a running asyncio event loop
    # managed by an ASGI server.
    # However, for basic execution, Flask will run, but true async handling of `process_paper`
    # might be imperfect.
    print("Starting Flask app. Note: For robust asyncio, consider an ASGI server.")
    app.run(debug=True, port=5001)
