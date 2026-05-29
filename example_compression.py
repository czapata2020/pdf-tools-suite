#!/usr/bin/env python3
"""
Example Usage: PDF Compression
Demonstrates how to use the PDF compression functionality
"""

from src.pdf_compressor import PDFCompressor
from pathlib import Path


def example_1_compress_single_file():
    """Example 1: Compress a single PDF file with medium quality"""
    print("\n" + "=" * 70)
    print("Example 1: Compress a Single PDF File")
    print("=" * 70)
    
    compressor = PDFCompressor(input_dir="input", output_dir="output")
    
    # Compress a single file
    result = compressor.compress_pdf_basic(
        "input/sample.pdf",
        compression_level="medium"
    )
    
    if result.get("success"):
        print(f"\n✓ Success!")
        print(f"Original size: {result['original_size_mb']} MB")
        print(f"Compressed size: {result['compressed_size_mb']} MB")
        print(f"Reduction: {result['reduction_percent']}%")
    else:
        print(f"\n✗ Failed: {result.get('error')}")


def example_2_compress_with_quality_levels():
    """Example 2: Compress the same file with different quality levels"""
    print("\n" + "=" * 70)
    print("Example 2: Compare Different Quality Levels")
    print("=" * 70)
    
    compressor = PDFCompressor(input_dir="input", output_dir="output")
    
    quality_levels = ['low', 'medium', 'high', 'maximum']
    
    for quality in quality_levels:
        print(f"\nCompressing with {quality} quality...")
        result = compressor.compress_pdf_basic(
            "input/sample.pdf",
            output_path=f"output/sample_{quality}.pdf",
            compression_level=quality
        )
        
        if result.get("success"):
            print(f"  Size: {result['compressed_size_mb']} MB")
            print(f"  Reduction: {result['reduction_percent']}%")


def example_3_compress_all_files():
    """Example 3: Compress all PDF files in the input directory"""
    print("\n" + "=" * 70)
    print("Example 3: Compress All PDFs in Input Directory")
    print("=" * 70)
    
    compressor = PDFCompressor(input_dir="input", output_dir="output")
    
    # Compress all files with high quality
    results = compressor.compress_all_pdfs(compression_level="high")
    
    print(f"\n✓ Compression Summary:")
    print(f"Total files processed: {results['total']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"Total size reduction: {results['total_reduction_mb']} MB")
    print(f"Average reduction: {results['average_reduction_percent']}%")


def example_4_get_file_info():
    """Example 4: Get information about a PDF file before compression"""
    print("\n" + "=" * 70)
    print("Example 4: Get PDF File Information")
    print("=" * 70)
    
    compressor = PDFCompressor(input_dir="input", output_dir="output")
    
    # Get file information
    info = compressor.get_compression_info("input/sample.pdf")
    
    if "error" not in info:
        print(f"\nFile: {info['filename']}")
        print(f"Size: {info['size_mb']} MB ({info['size_bytes']:,} bytes)")
        print(f"Pages: {info['page_count']}")
        print(f"Average MB per page: {info['avg_mb_per_page']} MB")
    else:
        print(f"\n✗ Error: {info['error']}")


def example_5_custom_directories():
    """Example 5: Use custom input and output directories"""
    print("\n" + "=" * 70)
    print("Example 5: Custom Input/Output Directories")
    print("=" * 70)
    
    # Create compressor with custom directories
    compressor = PDFCompressor(
        input_dir="my_pdfs",
        output_dir="compressed_pdfs"
    )
    
    print(f"Input directory: {compressor.input_dir}")
    print(f"Output directory: {compressor.output_dir}")
    
    # Compress all files in custom directory
    results = compressor.compress_all_pdfs(compression_level="medium")
    
    print(f"\nProcessed {results['total']} files")


def example_6_batch_compression_with_stats():
    """Example 6: Batch compression with detailed statistics"""
    print("\n" + "=" * 70)
    print("Example 6: Batch Compression with Statistics")
    print("=" * 70)
    
    compressor = PDFCompressor(input_dir="input", output_dir="output")
    
    # Get list of all PDF files
    pdf_files = list(Path("input").glob("*.pdf"))
    
    if not pdf_files:
        print("\nNo PDF files found in input directory")
        return
    
    print(f"\nFound {len(pdf_files)} PDF file(s)")
    
    total_original_size = 0
    total_compressed_size = 0
    
    for pdf_file in pdf_files:
        result = compressor.compress_pdf_basic(
            str(pdf_file),
            compression_level="medium"
        )
        
        if result.get("success"):
            total_original_size += result['original_size_mb']
            total_compressed_size += result['compressed_size_mb']
    
    if total_original_size > 0:
        total_reduction = total_original_size - total_compressed_size
        total_reduction_percent = (total_reduction / total_original_size) * 100
        
        print(f"\n✓ Batch Compression Complete!")
        print(f"Total original size: {round(total_original_size, 2)} MB")
        print(f"Total compressed size: {round(total_compressed_size, 2)} MB")
        print(f"Total reduction: {round(total_reduction, 2)} MB ({round(total_reduction_percent, 2)}%)")


def main():
    """Run all examples"""
    print("=" * 70)
    print("PDF Compression Examples".center(70))
    print("=" * 70)
    
    # Note: Make sure you have PDF files in the 'input' directory
    # before running these examples
    
    try:
        # Run examples
        example_1_compress_single_file()
        example_2_compress_with_quality_levels()
        example_3_compress_all_files()
        example_4_get_file_info()
        example_5_custom_directories()
        example_6_batch_compression_with_stats()
        
        print("\n" + "=" * 70)
        print("All examples completed!".center(70))
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you have PDF files in the 'input' directory")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()

# Made with Bob