# PDF Compression Guide

## Overview

The PDF Compressor is a new feature added to the PDF to Word Converter project that allows you to reduce the size of PDF files while maintaining readability and document structure.

## Features

- **Multiple Quality Levels**: Choose from 4 compression presets (low, medium, high, maximum)
- **Batch Processing**: Compress multiple PDFs at once
- **Detailed Statistics**: Get compression ratios and size reduction reports
- **Flexible Output**: Custom output paths and directories
- **Safe Compression**: Preserves document structure and content

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `PyPDF2` - For PDF manipulation and compression
- `Pillow` - For image processing (if needed)

### Basic Usage

#### Compress a Single PDF

```bash
python main.py --compress --file document.pdf
```

#### Compress All PDFs in Input Directory

```bash
python main.py --compress
```

#### Compress with Specific Quality

```bash
python main.py --compress --file document.pdf --quality low
```

## Compression Quality Levels

| Level | Compression | Quality | Best For |
|-------|-------------|---------|----------|
| **low** | Maximum | Lower | Email attachments, web uploads, maximum size reduction |
| **medium** | Balanced | Good | General purpose, archiving, daily use |
| **high** | Minimal | Better | Professional documents, presentations |
| **maximum** | Very Minimal | Best | High-quality documents, printing |

## Command-Line Options

```bash
python main.py --compress [OPTIONS]
```

### Options

- `--compress` or `-c`: Enable compression mode
- `--file FILE` or `-f FILE`: Compress a specific PDF file
- `--output OUTPUT` or `-o OUTPUT`: Custom output path
- `--quality LEVEL` or `-q LEVEL`: Compression quality (low/medium/high/maximum)
- `--input-dir DIR` or `-i DIR`: Input directory (default: input)
- `--output-dir DIR` or `-d DIR`: Output directory (default: output)

## Examples

### Example 1: Compress for Email

Reduce file size significantly for email attachments:

```bash
python main.py --compress --file report.pdf --quality low --output email_report.pdf
```

### Example 2: Batch Compress with Medium Quality

Compress all PDFs in the input folder:

```bash
python main.py --compress --quality medium
```

### Example 3: Compress from Custom Directory

```bash
python main.py --compress --input-dir ~/Documents/PDFs --output-dir ~/Documents/Compressed --quality high
```

### Example 4: Preserve Quality

Minimal compression for high-quality documents:

```bash
python main.py --compress --file presentation.pdf --quality maximum
```

## Using as a Python Module

### Basic Compression

```python
from src.pdf_compressor import PDFCompressor

# Initialize compressor
compressor = PDFCompressor(input_dir="input", output_dir="output")

# Compress a single file
result = compressor.compress_pdf_basic(
    "input/document.pdf",
    compression_level="medium"
)

if result.get("success"):
    print(f"Original: {result['original_size_mb']} MB")
    print(f"Compressed: {result['compressed_size_mb']} MB")
    print(f"Reduction: {result['reduction_percent']}%")
```

### Batch Compression

```python
from src.pdf_compressor import PDFCompressor

compressor = PDFCompressor()

# Compress all PDFs
results = compressor.compress_all_pdfs(compression_level="high")

print(f"Processed: {results['total']} files")
print(f"Successful: {results['successful']}")
print(f"Total reduction: {results['total_reduction_mb']} MB")
print(f"Average reduction: {results['average_reduction_percent']}%")
```

### Get File Information

```python
from src.pdf_compressor import PDFCompressor

compressor = PDFCompressor()

# Get PDF information
info = compressor.get_compression_info("document.pdf")

print(f"File: {info['filename']}")
print(f"Size: {info['size_mb']} MB")
print(f"Pages: {info['page_count']}")
print(f"Avg MB/page: {info['avg_mb_per_page']}")
```

## Compression Results

### What to Expect

Compression results vary based on:
- **PDF Content**: Text-heavy PDFs compress better than image-heavy ones
- **Existing Compression**: Already optimized PDFs may not reduce much
- **Quality Level**: Lower quality = more compression
- **PDF Structure**: Complex layouts may have limited compression

### Typical Results

| PDF Type | Low Quality | Medium Quality | High Quality |
|----------|-------------|----------------|--------------|
| Text-heavy | 40-60% | 30-40% | 15-25% |
| Mixed content | 30-50% | 20-30% | 10-20% |
| Image-heavy | 20-40% | 15-25% | 5-15% |
| Already compressed | 5-15% | 3-10% | 1-5% |

## Tips for Best Results

1. **Choose the Right Quality Level**
   - Use `low` for maximum size reduction when quality is less critical
   - Use `medium` for balanced results (recommended for most cases)
   - Use `high` or `maximum` when quality is important

2. **Batch Processing**
   - Process multiple files at once for efficiency
   - Use consistent quality levels for similar documents

3. **Check Results**
   - Always verify compressed PDFs open correctly
   - Compare file sizes before and after compression
   - Test readability on different devices

4. **Storage Optimization**
   - Compress archived documents with medium quality
   - Keep originals of important documents
   - Use low quality for temporary or disposable files

## Troubleshooting

### Issue: Minimal Size Reduction

**Possible Causes:**
- PDF is already compressed
- PDF contains mostly images
- PDF has complex graphics

**Solutions:**
- Try a lower quality setting
- Check if the PDF is already optimized
- Consider if compression is necessary

### Issue: Compression Fails

**Possible Causes:**
- Password-protected PDF
- Corrupted PDF file
- Insufficient permissions

**Solutions:**
- Remove password protection first
- Verify PDF opens in a reader
- Check file permissions

### Issue: Quality Loss

**Possible Causes:**
- Quality level too low
- PDF contains high-resolution images

**Solutions:**
- Use higher quality setting (high or maximum)
- Keep original files as backup
- Test different quality levels

## Technical Details

### How It Works

The PDF compressor uses `PyPDF2` library to:
1. Read the PDF structure
2. Compress content streams
3. Remove redundant data
4. Optimize PDF structure
5. Write the compressed PDF

### Compression Techniques

- **Content Stream Compression**: Reduces size of text and vector graphics
- **Structure Optimization**: Removes unnecessary PDF objects
- **Data Deduplication**: Eliminates redundant information

### Limitations

- Cannot compress encrypted/password-protected PDFs
- Image compression is limited (use image-specific tools for better results)
- Some complex PDFs may not compress significantly
- Compression is lossless for text, may be lossy for images

## Best Practices

1. **Always Keep Originals**: Store uncompressed versions of important documents
2. **Test First**: Try compression on a sample file before batch processing
3. **Choose Appropriate Quality**: Match quality level to document purpose
4. **Verify Results**: Check compressed PDFs open and display correctly
5. **Document Settings**: Keep track of quality levels used for consistency

## Integration with Conversion

You can use both conversion and compression features:

```bash
# First convert PDF to Word
python main.py --file document.pdf

# Then compress the original PDF
python main.py --compress --file document.pdf --quality medium
```

Or use them separately based on your needs.

## Support

For issues or questions:
- Check the main README.md for general troubleshooting
- Review this guide for compression-specific help
- Ensure all dependencies are installed correctly

---

**Happy Compressing! 📄 → 📦**