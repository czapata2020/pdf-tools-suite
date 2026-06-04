# PDF Tools Suite

A comprehensive web-based and command-line tool for PDF manipulation, conversion, and optimization. Convert PDFs to Word or Markdown, compress files, clean metadata, and merge multiple PDFs - all through an intuitive web interface or CLI.

## 🌟 Features

### 🌐 Web Interface
- **Modern, responsive web UI** accessible via browser
- **Drag-and-drop file upload** for easy file handling
- **Real-time progress tracking** during operations
- **Instant download** of processed files
- **Multiple tools in one interface**

### 📝 PDF to Word Conversion
- ✅ Convert single PDF files to Word documents (.docx)
- ✅ Batch convert multiple PDF files at once
- ✅ Preserve text formatting, layout, and structure
- ✅ Handle tables, images, and multi-column layouts
- ✅ Progress tracking and error handling

### 📋 PDF & Word to Markdown Conversion (NEW!)
- ✅ Convert PDF files to Markdown format
- ✅ Convert Word documents (.docx, .doc) to Markdown
- ✅ Preserve formatting (bold, italic, headings)
- ✅ Convert tables to Markdown table syntax
- ✅ Maintain document structure and hierarchy
- ✅ Support for H1-H6 headings

### 📦 PDF Compression
- ✅ Reduce PDF file size with multiple quality levels
- ✅ Four compression quality presets (low, medium, high, maximum)
- ✅ Detailed compression statistics and size reduction reports
- ✅ Ghostscript integration for high-quality compression
- ✅ Preserve PDF structure and readability

### 🔒 PDF Metadata Cleaning
- ✅ Remove sensitive metadata from PDFs
- ✅ Clean author, creation date, software information
- ✅ Option to keep basic information (title, page count)
- ✅ View metadata before cleaning
- ✅ Protect privacy and security

### 🔗 PDF Merging
- ✅ Combine multiple PDF files into one document
- ✅ Drag-and-drop reordering of files
- ✅ Preview file list before merging
- ✅ Maintain quality and formatting
- ✅ Support for unlimited number of files

## 🚀 Quick Start

### Using Docker/Podman (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/czapata2020/pdf-tools-suite.git
   cd pdf-tools-suite
   ```

2. **Deploy with Podman**
   ```bash
   ./deploy-podman.sh
   ```

3. **Access the web interface**
   ```
   http://localhost:8080
   ```

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/czapata2020/pdf-tools-suite.git
   cd pdf-tools-suite
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web application**
   ```bash
   python app.py
   ```

4. **Access the web interface**
   ```
   http://localhost:5000
   ```

## 📋 Requirements

- Python 3.11 or higher
- pip (Python package installer)
- Ghostscript (optional, for better PDF compression)

### Installing Ghostscript

**macOS:**
```bash
brew install ghostscript
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ghostscript
```

**Windows:**
Download from [Ghostscript official website](https://www.ghostscript.com/download/gsdnld.html)

## 🗂️ Project Structure

```
PDF_Tools_Suite/
├── app.py                      # Flask web application
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── deploy-podman.sh           # Podman deployment script
├── src/
│   ├── pdf_converter.py       # PDF/Word to Word/Markdown conversion
│   ├── pdf_compressor.py      # PDF compression logic
│   ├── pdf_metadata_cleaner.py # Metadata removal
│   └── pdf_merger.py          # PDF merging functionality
├── static/
│   ├── css/style.css          # Web interface styles
│   └── js/app.js              # Frontend JavaScript
├── templates/
│   └── index.html             # Web interface HTML
├── input/                     # Input directory for CLI
├── output/                    # Output directory for CLI
├── uploads/                   # Temporary uploads (web)
└── outputs/                   # Processed files (web)
```

## 🌐 Web Interface Usage

### 1. Convert to Word
- Click the "Convert to Word" tab
- Upload a PDF file (drag-and-drop or click to browse)
- Wait for conversion to complete
- Download the converted .docx file

### 2. Convert to Markdown
- Click the "Convert to Markdown" tab
- Upload a PDF or Word file (.pdf, .docx, .doc)
- Wait for conversion to complete
- Download the converted .md file

### 3. Compress PDF
- Click the "Compress PDF" tab
- Select compression quality (low, medium, high, maximum)
- Upload a PDF file
- View compression statistics
- Download the compressed PDF

### 4. Clean Metadata
- Click the "Clean Metadata" tab
- Optionally view metadata before cleaning
- Choose whether to keep basic information
- Upload a PDF file
- Download the cleaned PDF

### 5. Merge PDFs
- Click the "Merge PDFs" tab
- Upload multiple PDF files
- Reorder files by dragging or using arrow buttons
- Click "Merge PDFs"
- Download the merged PDF

## 💻 Command-Line Usage

### PDF to Word Conversion

```bash
# Convert all PDFs in input folder
python main.py

# Convert a specific PDF
python main.py --file document.pdf

# Convert with custom output
python main.py --file input.pdf --output custom_name.docx
```

### PDF to Markdown Conversion

```bash
# Convert PDF to Markdown
python -c "from src.pdf_converter import PDFToWordConverter; \
converter = PDFToWordConverter(); \
converter.convert_to_markdown('input.pdf', 'output.md')"
```

### Word to Markdown Conversion

```bash
# Convert Word to Markdown
python -c "from src.pdf_converter import PDFToWordConverter; \
converter = PDFToWordConverter(); \
converter.convert_word_to_markdown('document.docx', 'output.md')"
```

### PDF Compression

```bash
# Compress with medium quality
python main.py --compress

# Compress with specific quality
python main.py --compress --file large.pdf --quality low

# Compress all PDFs
python main.py --compress --quality high
```

## 🐳 Docker/Podman Deployment

### Using Podman (Recommended)

```bash
# Deploy the application
./deploy-podman.sh

# View logs
podman logs -f pdf-converter-app

# Stop the application
podman stop pdf-converter-app

# Restart the application
podman restart pdf-converter-app

# Remove the container
podman rm -f pdf-converter-app
```

### Using Docker

```bash
# Build the image
docker build -t pdf-tools-suite .

# Run the container
docker run -d \
  --name pdf-tools-app \
  -p 8080:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  pdf-tools-suite

# Access at http://localhost:8080
```

## 📊 API Endpoints

The web application provides the following REST API endpoints:

- `POST /api/convert` - Convert PDF to Word
- `POST /api/convert-to-markdown` - Convert PDF or Word to Markdown
- `POST /api/compress` - Compress PDF
- `POST /api/clean-metadata` - Remove PDF metadata
- `POST /api/view-metadata` - View PDF metadata
- `POST /api/merge` - Merge multiple PDFs
- `POST /api/info` - Get PDF information
- `GET /health` - Health check endpoint

## 🔧 Configuration

### Environment Variables

- `SECRET_KEY` - Flask secret key (default: dev-secret-key-change-in-production)
- `MAX_CONTENT_LENGTH` - Maximum upload size (default: 100MB)

### Port Configuration

The application runs on:
- **Web Interface**: Port 8080 (Podman) or 5000 (local)
- **Internal**: Port 5000 (container)

## 📝 Markdown Conversion Features

### Supported Formatting

**From PDF:**
- Text extraction with layout preservation
- Headings and structure
- Tables
- Lists
- Basic formatting

**From Word:**
- Headings (H1-H6)
- Bold text (`**bold**`)
- Italic text (`*italic*`)
- Bold + Italic (`***bold italic***`)
- Tables with proper Markdown syntax
- Paragraphs and line breaks

### Example Output

```markdown
# Main Heading

## Subheading

This is a paragraph with **bold text** and *italic text*.

### Table Example

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Data 1 | Data 2 | Data 3 |
| Data 4 | Data 5 | Data 6 |
```

## 🎯 Use Cases

- **Document Conversion**: Convert PDFs to editable Word documents
- **Content Migration**: Extract content from PDFs/Word to Markdown for websites
- **File Optimization**: Reduce PDF sizes for email or web upload
- **Privacy Protection**: Remove sensitive metadata from documents
- **Document Management**: Merge multiple PDFs into single files
- **Documentation**: Convert technical documents to Markdown format

## ⚙️ Technical Stack

- **Backend**: Flask (Python web framework)
- **PDF Processing**: PyMuPDF, pdf2docx, PyPDF2
- **Markdown Conversion**: pymupdf4llm, python-docx
- **Compression**: Ghostscript, Pillow
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Deployment**: Gunicorn, Docker/Podman
- **Server**: 4 Gunicorn workers with 300s timeout

## 🔒 Security Features

- File size limits (100MB max)
- Secure filename handling
- Temporary file cleanup (1 hour)
- Metadata removal capabilities
- No data persistence (files auto-deleted)

## 🚨 Limitations

### PDF to Word Conversion
- Complex PDF layouts may not convert perfectly
- Scanned PDFs require OCR (not included)
- Some advanced PDF features may not be preserved

### Markdown Conversion
- Complex formatting may be simplified
- Images are not embedded in Markdown
- Some PDF elements may not convert perfectly

### PDF Compression
- Results vary by PDF content
- Already compressed PDFs may not reduce significantly
- Password-protected PDFs cannot be compressed

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process using port 8080
lsof -ti:8080 | xargs kill -9

# Or use a different port
podman run -p 9090:5000 ...
```

### Podman Connection Issues
```bash
# Restart Podman machine
podman machine stop
podman machine start
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📚 Documentation

- [Compression Guide](COMPRESSION_GUIDE.md) - Detailed compression options
- [Deployment Guide](DEPLOYMENT.md) - Production deployment instructions
- [Quick Start Guide](QUICK_START.md) - Get started quickly

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available for personal and commercial use.

## 🙏 Acknowledgments

- pdf2docx - PDF to Word conversion
- pymupdf4llm - PDF to Markdown conversion
- PyMuPDF - PDF processing
- Ghostscript - PDF compression
- Flask - Web framework

## 📧 Support

For issues or questions:
- Create an issue in the GitHub repository
- Check existing documentation
- Review troubleshooting section

---

**Made with ❤️ by Bob**

**Happy Converting! 📄 → 📝 → 📋**