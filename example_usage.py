#!/usr/bin/env python3
"""
Example Usage Script for PDF to Word Converter
Demonstrates different ways to use the converter
"""

from src.pdf_converter import PDFToWordConverter


def example_1_convert_all():
    """Example 1: Convert all PDFs in the input directory"""
    print("\n" + "="*70)
    print("Example 1: Convert All PDFs in Input Directory")
    print("="*70)
    
    converter = PDFToWordConverter()
    results = converter.convert_all_pdfs()
    
    print(f"\nResults: {results}")


def example_2_convert_single():
    """Example 2: Convert a single PDF file"""
    print("\n" + "="*70)
    print("Example 2: Convert a Single PDF File")
    print("="*70)
    
    converter = PDFToWordConverter()
    
    # Replace with your actual PDF file path
    pdf_file = "input/sample.pdf"
    
    success = converter.convert_single_pdf(pdf_file)
    
    if success:
        print(f"\n✓ Successfully converted {pdf_file}")
    else:
        print(f"\n✗ Failed to convert {pdf_file}")


def example_3_custom_output():
    """Example 3: Convert with custom output path"""
    print("\n" + "="*70)
    print("Example 3: Convert with Custom Output Path")
    print("="*70)
    
    converter = PDFToWordConverter()
    
    # Replace with your actual paths
    pdf_file = "input/report.pdf"
    output_file = "output/custom_report_name.docx"
    
    success = converter.convert_single_pdf(pdf_file, output_file)
    
    if success:
        print(f"\n✓ Saved to: {output_file}")


def example_4_custom_directories():
    """Example 4: Use custom input/output directories"""
    print("\n" + "="*70)
    print("Example 4: Use Custom Directories")
    print("="*70)
    
    # Create converter with custom directories
    converter = PDFToWordConverter(
        input_dir="my_pdfs",
        output_dir="my_word_docs"
    )
    
    results = converter.convert_all_pdfs()
    print(f"\nResults: {results}")


def example_5_get_pdf_info():
    """Example 5: Get information about a PDF file"""
    print("\n" + "="*70)
    print("Example 5: Get PDF File Information")
    print("="*70)
    
    converter = PDFToWordConverter()
    
    # Replace with your actual PDF file path
    pdf_file = "input/sample.pdf"
    
    info = converter.get_pdf_info(pdf_file)
    
    if "error" not in info:
        print(f"\nFile: {info['filename']}")
        print(f"Path: {info['path']}")
        print(f"Size: {info['size_mb']} MB ({info['size_bytes']} bytes)")
    else:
        print(f"\nError: {info['error']}")


def example_6_batch_with_error_handling():
    """Example 6: Batch conversion with detailed error handling"""
    print("\n" + "="*70)
    print("Example 6: Batch Conversion with Error Handling")
    print("="*70)
    
    converter = PDFToWordConverter()
    
    pdf_files = [
        "input/file1.pdf",
        "input/file2.pdf",
        "input/file3.pdf"
    ]
    
    successful = []
    failed = []
    
    for pdf_file in pdf_files:
        if converter.convert_single_pdf(pdf_file):
            successful.append(pdf_file)
        else:
            failed.append(pdf_file)
    
    print("\n" + "="*70)
    print("Batch Conversion Summary")
    print("="*70)
    print(f"Total files: {len(pdf_files)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed files:")
        for file in failed:
            print(f"  - {file}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("PDF to Word Converter - Example Usage")
    print("="*70)
    print("\nThis script demonstrates various ways to use the converter.")
    print("Uncomment the example you want to run.\n")
    
    # Uncomment the example you want to run:
    
    # example_1_convert_all()
    # example_2_convert_single()
    # example_3_custom_output()
    # example_4_custom_directories()
    # example_5_get_pdf_info()
    # example_6_batch_with_error_handling()
    
    print("\nNote: Make sure to add PDF files to the 'input' directory first!")
    print("Edit this file to uncomment and run specific examples.")


if __name__ == "__main__":
    main()

# Made with Bob
