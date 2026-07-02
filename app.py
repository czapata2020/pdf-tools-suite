#!/usr/bin/env python3
"""
PDF Converter & Compressor Web Application
Flask-based web service for PDF conversion and compression
"""

import os
import uuid
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify, url_for
from werkzeug.utils import secure_filename
from src.pdf_converter import PDFToWordConverter
from src.pdf_compressor import PDFCompressor
from src.pdf_metadata_cleaner import PDFMetadataCleaner
from src.pdf_merger import PDFMerger
import shutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Create necessary directories
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}
ALLOWED_MARKDOWN_EXTENSIONS = {'pdf', 'docx', 'doc', 'pptx', 'ppt'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_markdown_file(filename):
    """Check if file extension is allowed for markdown conversion"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_MARKDOWN_EXTENSIONS

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    import time
    current_time = time.time()
    
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        for file_path in Path(folder).glob('*'):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > 3600:  # 1 hour
                    try:
                        file_path.unlink()
                    except:
                        pass

@app.after_request
def add_header(response):
    """Add headers to prevent caching of static files"""
    if 'static' in request.path:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        # Remove ETag to force fresh content
        response.headers.pop('ETag', None)
        response.headers.pop('Last-Modified', None)
    return response

@app.route('/')
def index():
    """Render the main page"""
    cleanup_old_files()
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert_pdf():
    """Convert PDF to Word"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        input_path = Path(app.config['UPLOAD_FOLDER']) / f"{unique_id}_{filename}"
        
        # Save uploaded file
        file.save(input_path)
        
        # Convert PDF to Word
        output_filename = f"{unique_id}_{Path(filename).stem}.docx"
        output_path = Path(app.config['OUTPUT_FOLDER']) / output_filename
        
        converter = PDFToWordConverter(
            input_dir=app.config['UPLOAD_FOLDER'],
            output_dir=app.config['OUTPUT_FOLDER']
        )
        
        success = converter.convert_single_pdf(str(input_path), str(output_path))
        
        if success:
            # Get file info
            original_size = input_path.stat().st_size / (1024 * 1024)  # MB
            converted_size = output_path.stat().st_size / (1024 * 1024)  # MB
            
            return jsonify({
                'success': True,
                'download_url': url_for('download_file', filename=output_filename),
                'original_size': round(original_size, 2),
                'converted_size': round(converted_size, 2),
                'filename': output_filename
            })
        else:
            return jsonify({'error': 'Conversion failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/convert-to-markdown', methods=['POST'])
def convert_to_markdown():
    """Convert PDF or Word document to Markdown"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_markdown_file(file.filename):
            return jsonify({'error': 'Only PDF, Word, and PowerPoint files (.pdf, .docx, .doc, .pptx, .ppt) are allowed'}), 400
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_ext = Path(filename).suffix.lower()
        input_path = Path(app.config['UPLOAD_FOLDER']) / f"{unique_id}_{filename}"
        
        # Save uploaded file
        file.save(input_path)
        
        # Convert to Markdown
        output_filename = f"{unique_id}_{Path(filename).stem}.md"
        output_path = Path(app.config['OUTPUT_FOLDER']) / output_filename
        
        converter = PDFToWordConverter(
            input_dir=app.config['UPLOAD_FOLDER'],
            output_dir=app.config['OUTPUT_FOLDER']
        )
        
        # Choose conversion method based on file type
        if file_ext == '.pdf':
            success = converter.convert_to_markdown(str(input_path), str(output_path))
            file_type = 'PDF'
        elif file_ext in ['.docx', '.doc']:
            success = converter.convert_word_to_markdown(str(input_path), str(output_path))
            file_type = 'Word'
        elif file_ext in ['.pptx', '.ppt']:
            success = converter.convert_pptx_to_markdown(str(input_path), str(output_path))
            file_type = 'PowerPoint'
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        if success:
            # Get file info
            original_size = input_path.stat().st_size / (1024 * 1024)  # MB
            converted_size = output_path.stat().st_size / (1024 * 1024)  # MB
            
            return jsonify({
                'success': True,
                'download_url': url_for('download_file', filename=output_filename),
                'original_size': round(original_size, 2),
                'converted_size': round(converted_size, 2),
                'filename': output_filename,
                'file_type': file_type
            })
        else:
            return jsonify({'error': f'Conversion from {file_type} to Markdown failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compress', methods=['POST'])
def compress_pdf():
    """Compress PDF file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        quality = request.form.get('quality', 'medium')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        if quality not in ['low', 'medium', 'high', 'maximum']:
            quality = 'medium'
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        input_path = Path(app.config['UPLOAD_FOLDER']) / f"{unique_id}_{filename}"
        
        # Save uploaded file
        file.save(input_path)
        
        # Compress PDF
        output_filename = f"{unique_id}_compressed_{Path(filename).stem}.pdf"
        output_path = Path(app.config['OUTPUT_FOLDER']) / output_filename
        
        compressor = PDFCompressor(
            input_dir=app.config['UPLOAD_FOLDER'],
            output_dir=app.config['OUTPUT_FOLDER']
        )
        
        result = compressor.compress_pdf_auto(
            str(input_path),
            str(output_path),
            compression_level=quality
        )
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'download_url': url_for('download_file', filename=output_filename),
                'original_size': result['original_size_mb'],
                'compressed_size': result['compressed_size_mb'],
                'reduction_percent': result['reduction_percent'],
                'reduction_mb': result['reduction_mb'],
                'method': result.get('method', 'unknown'),
                'filename': output_filename
            })
        else:
            return jsonify({'error': result.get('error', 'Compression failed')}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/info', methods=['POST'])
def get_pdf_info():
    """Get PDF file information"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        input_path = Path(app.config['UPLOAD_FOLDER']) / f"{unique_id}_{filename}"
        
        # Save uploaded file temporarily
        file.save(input_path)
        
        # Get PDF info
        compressor = PDFCompressor()
        info = compressor.get_compression_info(str(input_path))
        
        # Clean up
        input_path.unlink()
        
        if 'error' not in info:
            return jsonify({
                'success': True,
                'filename': info['filename'],
                'size_mb': info['size_mb'],
                'page_count': info['page_count'],
                'avg_mb_per_page': info['avg_mb_per_page'],
                'ghostscript_available': info['ghostscript_available']
            })
        else:
            return jsonify({'error': info['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clean-metadata', methods=['POST'])
def clean_metadata():
    """Remove metadata from PDF file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        keep_basic_info = request.form.get('keep_basic_info', 'false').lower() == 'true'
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        input_path = Path(app.config['UPLOAD_FOLDER']) / f"{unique_id}_{filename}"
        
        # Save uploaded file
        file.save(input_path)
        
        # Clean metadata
        output_filename = f"{unique_id}_cleaned_{Path(filename).stem}.pdf"
        output_path = Path(app.config['OUTPUT_FOLDER']) / output_filename
        
        cleaner = PDFMetadataCleaner(
            input_dir=app.config['UPLOAD_FOLDER'],
            output_dir=app.config['OUTPUT_FOLDER']
        )
        
        result = cleaner.clean_metadata(
            str(input_path),
            str(output_path),
            keep_basic_info=keep_basic_info
        )
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'download_url': url_for('download_file', filename=output_filename),
                'original_size': result['original_size_mb'],
                'cleaned_size': result['cleaned_size_mb'],
                'metadata_removed': result['metadata_removed'],
                'original_metadata': result['original_metadata'],
                'cleaned_metadata': result['cleaned_metadata'],
                'keep_basic_info': keep_basic_info,
                'filename': output_filename
            })
        else:
            return jsonify({'error': result.get('error', 'Metadata cleaning failed')}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/view-metadata', methods=['POST'])
def view_metadata():
    """View metadata from PDF file without cleaning"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        input_path = Path(app.config['UPLOAD_FOLDER']) / f"{unique_id}_{filename}"
        
        # Save uploaded file temporarily
        file.save(input_path)
        
        # Get metadata
        cleaner = PDFMetadataCleaner()
        metadata = cleaner.get_metadata(str(input_path))
        
        # Get file size
        file_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
        
        # Clean up
        input_path.unlink()
        
        if 'error' not in metadata:
            return jsonify({
                'success': True,
                'filename': filename,
                'size_mb': round(file_size, 2),
                'metadata': metadata
            })
        else:
            return jsonify({'error': metadata['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/merge', methods=['POST'])
def merge_pdfs():
    """Merge multiple PDF files into one"""
    try:
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files[]')
        
        if len(files) < 2:
            return jsonify({'error': 'At least 2 PDF files are required for merging'}), 400
        
        # Validate all files
        for file in files:
            if file.filename == '':
                return jsonify({'error': 'One or more files have no name'}), 400
            if not allowed_file(file.filename):
                return jsonify({'error': f'File {file.filename} is not a PDF'}), 400
        
        # Generate unique ID for this merge operation
        unique_id = str(uuid.uuid4())
        
        # Save all uploaded files
        saved_files = []
        try:
            for idx, file in enumerate(files):
                filename = secure_filename(file.filename)
                input_path = Path(app.config['UPLOAD_FOLDER']) / f"{unique_id}_{idx}_{filename}"
                file.save(input_path)
                saved_files.append(str(input_path))
            
            # Merge PDFs
            merger = PDFMerger(
                upload_folder=app.config['UPLOAD_FOLDER'],
                output_folder=app.config['OUTPUT_FOLDER']
            )
            
            output_filename = f"{unique_id}_merged.pdf"
            result = merger.merge_pdfs(saved_files, output_filename)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'total_files': result['total_files'],
                    'total_pages': result['total_pages'],
                    'merged_size': result['merged_size_mb'],
                    'files': result['files'],
                    'download_url': url_for('download_file', filename=output_filename)
                })
            else:
                return jsonify({'error': 'Merge failed'}), 500
                
        finally:
            # Clean up uploaded files
            for file_path in saved_files:
                try:
                    Path(file_path).unlink()
                except:
                    pass
                    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download converted/compressed file"""
    try:
        file_path = Path(app.config['OUTPUT_FOLDER']) / filename
        if file_path.exists():
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    compressor = PDFCompressor()
    return jsonify({
        'status': 'healthy',
        'ghostscript_available': compressor._check_ghostscript()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

# Made with Bob