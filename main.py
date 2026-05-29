#!/usr/bin/env python3
"""
PDF to Word Converter - Main Entry Point
Simple command-line tool to convert PDF files to Word documents and compress PDFs
"""

import sys
import argparse
from pathlib import Path
from src.pdf_converter import PDFToWordConverter
from src.pdf_compressor import PDFCompressor


def main():
    """Main entry point for the PDF to Word converter and compressor"""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to Word documents (.docx) or compress PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all PDFs in the input folder
  python main.py
  
  # Convert a specific PDF file
  python main.py --file path/to/document.pdf
  
  # Convert with custom output path
  python main.py --file input.pdf --output custom_output.docx
  
  # Compress a PDF file
  python main.py --compress --file document.pdf
  
  # Compress all PDFs with high quality
  python main.py --compress --quality high
  
  # Use custom input/output directories
  python main.py --input-dir my_pdfs --output-dir my_docs
        """
    )
    
    parser.add_argument(
        '--compress', '-c',
        action='store_true',
        help='Compress PDF files instead of converting to Word'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Path to a specific PDF file to convert or compress'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Custom output path for the converted/compressed file (only with --file)'
    )
    
    parser.add_argument(
        '--input-dir', '-i',
        type=str,
        default='input',
        help='Input directory containing PDF files (default: input)'
    )
    
    parser.add_argument(
        '--output-dir', '-d',
        type=str,
        default='output',
        help='Output directory for converted/compressed files (default: output)'
    )
    
    parser.add_argument(
        '--quality', '-q',
        type=str,
        choices=['low', 'medium', 'high', 'maximum'],
        default='medium',
        help='Compression quality level (default: medium) - only for compression'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    
    if args.compress:
        print("PDF Compressor".center(70))
        print("=" * 70)
        
        # Initialize compressor
        compressor = PDFCompressor(
            input_dir=args.input_dir,
            output_dir=args.output_dir
        )
    
        try:
            if args.file:
                # Compress single file
                if args.output and not args.file:
                    print("Error: --output can only be used with --file")
                    sys.exit(1)
                
                result = compressor.compress_pdf_auto(
                    args.file,
                    args.output,
                    compression_level=args.quality
                )
                
                if result.get("success"):
                    print("\n✓ Compression completed successfully!")
                    sys.exit(0)
                else:
                    print(f"\n✗ Compression failed: {result.get('error', 'Unknown error')}")
                    sys.exit(1)
            else:
                # Compress all files in input directory
                results = compressor.compress_all_pdfs(compression_level=args.quality)
                
                if results["total"] == 0:
                    print("\nNo PDF files found in the input directory.")
                    print(f"Please add PDF files to '{args.input_dir}' and run again.")
                    sys.exit(0)
                
                if results["failed"] > 0:
                    print(f"\n⚠ Some compressions failed ({results['failed']}/{results['total']})")
                    sys.exit(1)
                else:
                    print("\n✓ All compressions completed successfully!")
                    sys.exit(0)
                    
        except KeyboardInterrupt:
            print("\n\nCompression interrupted by user.")
            sys.exit(130)
        except Exception as e:
            print(f"\n✗ Unexpected error: {str(e)}")
            sys.exit(1)
    
    else:
        # Convert mode (default)
        print("PDF to Word Converter".center(70))
        print("=" * 70)
        
        # Initialize converter
        converter = PDFToWordConverter(
            input_dir=args.input_dir,
            output_dir=args.output_dir
        )
        
        try:
            if args.file:
                # Convert single file
                if args.output and not args.file:
                    print("Error: --output can only be used with --file")
                    sys.exit(1)
                
                success = converter.convert_single_pdf(args.file, args.output)
                
                if success:
                    print("\n✓ Conversion completed successfully!")
                    sys.exit(0)
                else:
                    print("\n✗ Conversion failed!")
                    sys.exit(1)
            else:
                # Convert all files in input directory
                results = converter.convert_all_pdfs()
                
                if results["total"] == 0:
                    print("\nNo PDF files found in the input directory.")
                    print(f"Please add PDF files to '{args.input_dir}' and run again.")
                    sys.exit(0)
                
                if results["failed"] > 0:
                    print(f"\n⚠ Some conversions failed ({results['failed']}/{results['total']})")
                    sys.exit(1)
                else:
                    print("\n✓ All conversions completed successfully!")
                    sys.exit(0)
                    
        except KeyboardInterrupt:
            print("\n\nConversion interrupted by user.")
            sys.exit(130)
        except Exception as e:
            print(f"\n✗ Unexpected error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
