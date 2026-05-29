# PDF to Word Converter & Compressor

A simple and efficient Python tool to convert PDF files to Word documents (.docx format) and compress PDF files to reduce their size.

## Features

### PDF to Word Conversion
- ✅ Convert single PDF files to Word documents
- ✅ Batch convert multiple PDF files at once
- ✅ Preserve text formatting, layout, and structure
- ✅ Command-line interface for easy automation
- ✅ Custom input/output directory support
- ✅ Progress tracking and error handling

### PDF Compression
- ✅ Reduce PDF file size with multiple quality levels
- ✅ Compress single or multiple PDF files
- ✅ Four compression quality presets (low, medium, high, maximum)
- ✅ Detailed compression statistics and size reduction reports
- ✅ Preserve PDF structure and readability

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Clone or download this project**

2. **Navigate to the project directory**
   ```bash
   cd PDF_to_Word_Converter
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
PDF_to_Word_Converter/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   ├── pdf_converter.py   # Core conversion logic
│   └── pdf_compressor.py  # PDF compression logic
├── input/                 # Place your PDF files here
└── output/                # Converted/compressed files will be saved here
```

## Usage

### PDF to Word Conversion

#### Basic Usage - Convert All PDFs

Place your PDF files in the `input/` folder and run:

```bash
python main.py
```

This will convert all PDF files in the `input/` directory and save the Word documents to the `output/` directory.

#### Convert a Single PDF File

```bash
python main.py --file path/to/your/document.pdf
```

#### Convert with Custom Output Path

```bash
python main.py --file input.pdf --output custom_name.docx
```

### PDF Compression

#### Compress All PDFs (Medium Quality)

```bash
python main.py --compress
```

#### Compress a Single PDF

```bash
python main.py --compress --file large_document.pdf
```

#### Compress with Specific Quality Level

```bash
# Low quality (maximum compression)
python main.py --compress --quality low

# Medium quality (balanced)
python main.py --compress --quality medium

# High quality (minimal compression)
python main.py --compress --quality high

# Maximum quality (preserve quality)
python main.py --compress --quality maximum
```

#### Compress with Custom Output Path

```bash
python main.py --compress --file document.pdf --output compressed_doc.pdf
```

### Use Custom Input/Output Directories

```bash
python main.py --input-dir my_pdfs --output-dir my_docs
python main.py --compress --input-dir my_pdfs --output-dir compressed_pdfs
```

## Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--compress` | `-c` | Enable PDF compression mode instead of conversion |
| `--file` | `-f` | Path to a specific PDF file to convert or compress |
| `--output` | `-o` | Custom output path for the converted/compressed file (use with --file) |
| `--input-dir` | `-i` | Input directory containing PDF files (default: input) |
| `--output-dir` | `-d` | Output directory for converted/compressed files (default: output) |
| `--quality` | `-q` | Compression quality level: low, medium, high, maximum (default: medium) |
| `--help` | `-h` | Show help message and exit |

## Compression Quality Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `low` | Maximum compression, smallest file size | Email attachments, web uploads |
| `medium` | Balanced compression and quality | General purpose, archiving |
| `high` | Minimal compression, better quality | Professional documents |
| `maximum` | Preserve quality, minimal size reduction | High-quality documents |

## Examples

### Conversion Examples

#### Example 1: Convert all PDFs in the input folder
```bash
python main.py
```

#### Example 2: Convert a specific PDF
```bash
python main.py --file documents/report.pdf
```

#### Example 3: Convert with custom output name
```bash
python main.py --file report.pdf --output final_report.docx
```

#### Example 4: Use custom directories
```bash
python main.py --input-dir ~/Documents/PDFs --output-dir ~/Documents/Word
```

### Compression Examples

#### Example 5: Compress all PDFs with medium quality
```bash
python main.py --compress
```

#### Example 6: Compress a single PDF with low quality (maximum compression)
```bash
python main.py --compress --file large_file.pdf --quality low
```

#### Example 7: Compress with custom output name
```bash
python main.py --compress --file document.pdf --output small_document.pdf
```

#### Example 8: Compress all PDFs in a custom directory
```bash
python main.py --compress --input-dir ~/Downloads --output-dir ~/Compressed --quality high
```

## Using as a Python Module

You can also use the converter and compressor in your own Python scripts:

### PDF to Word Conversion

```python
from src.pdf_converter import PDFToWordConverter

# Initialize converter
converter = PDFToWordConverter(input_dir="input", output_dir="output")

# Convert a single file
converter.convert_single_pdf("path/to/file.pdf")

# Convert all PDFs in input directory
results = converter.convert_all_pdfs()
print(f"Converted {results['successful']} out of {results['total']} files")

# Get PDF information
info = converter.get_pdf_info("path/to/file.pdf")
print(f"File size: {info['size_mb']} MB")
```

### PDF Compression

```python
from src.pdf_compressor import PDFCompressor

# Initialize compressor
compressor = PDFCompressor(input_dir="input", output_dir="output")

# Compress a single file
result = compressor.compress_pdf_basic(
    "path/to/file.pdf",
    compression_level="medium"
)
print(f"Size reduced by {result['reduction_percent']}%")

# Compress all PDFs in input directory
results = compressor.compress_all_pdfs(compression_level="high")
print(f"Total reduction: {results['total_reduction_mb']} MB")
print(f"Average reduction: {results['average_reduction_percent']}%")

# Get compression information
info = compressor.get_compression_info("path/to/file.pdf")
print(f"File: {info['filename']}")
print(f"Size: {info['size_mb']} MB")
print(f"Pages: {info['page_count']}")
```

## Limitations

### PDF to Word Conversion
- Complex PDF layouts may not convert perfectly
- Scanned PDFs (images) will not be converted to editable text (OCR not included)
- Some advanced PDF features (forms, annotations) may not be preserved
- Large PDF files may take longer to convert

### PDF Compression
- Compression results vary depending on PDF content and structure
- Already compressed PDFs may not reduce significantly
- Some PDFs with complex graphics may have limited compression
- Password-protected PDFs cannot be compressed

## Troubleshooting

### Issue: "No module named 'pdf2docx'" or "No module named 'PyPDF2'"
**Solution:** Install dependencies with `pip install -r requirements.txt`

### Issue: "No PDF files found"
**Solution:** Make sure your PDF files are in the `input/` directory or specify the correct path with `--file`

### Issue: Conversion fails for a specific PDF
**Solution:** Some PDFs may have complex structures. Try:
- Ensuring the PDF is not password-protected
- Checking if the PDF is corrupted
- Converting a simpler PDF first to verify the tool works

### Issue: Compression doesn't reduce file size significantly
**Solution:** Some PDFs are already optimized. Try:
- Using a lower quality setting for more compression
- Checking if the PDF contains mostly images (limited compression)
- Verifying the PDF isn't already compressed

## Technical Details

### PDF to Word Conversion
This tool uses the `pdf2docx` library, which:
- Extracts text, images, and layout information from PDFs
- Reconstructs the document structure in Word format
- Preserves formatting like fonts, colors, and paragraph styles
- Handles tables, images, and multi-column layouts

### PDF Compression
This tool uses `PyPDF2` and `Pillow` libraries, which:
- Compress PDF content streams
- Optimize PDF structure
- Remove redundant data
- Maintain document integrity and readability

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, please create an issue in the project repository.

---

**Happy Converting! 📄 → 📝**