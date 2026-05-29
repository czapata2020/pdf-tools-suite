"""
PDF Compressor Module
Reduces PDF file size using various compression techniques
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Literal
import PyPDF2
from PIL import Image
import io


class PDFCompressor:
    """Class to handle PDF compression and size reduction"""
    
    # Compression quality presets
    QUALITY_PRESETS = {
        'low': {'image_quality': 30, 'image_dpi': 72},
        'medium': {'image_quality': 50, 'image_dpi': 150},
        'high': {'image_quality': 75, 'image_dpi': 200},
        'maximum': {'image_quality': 95, 'image_dpi': 300}
    }
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        """
        Initialize the PDF compressor
        
        Args:
            input_dir: Directory containing PDF files
            output_dir: Directory to save compressed PDF files
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Create directories if they don't exist
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_file_size(self, file_path: str) -> dict:
        """
        Get file size information
        
        Args:
            file_path: Path to the file
            
        Returns:
            dict: File size information
        """
        try:
            file = Path(file_path)
            if not file.exists():
                return {"error": "File not found"}
            
            size_bytes = file.stat().st_size
            size_kb = size_bytes / 1024
            size_mb = size_kb / 1024
            
            return {
                "bytes": size_bytes,
                "kb": round(size_kb, 2),
                "mb": round(size_mb, 2)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _check_ghostscript(self) -> bool:
        """
        Check if Ghostscript is installed
        
        Returns:
            bool: True if Ghostscript is available
        """
        return shutil.which('gs') is not None
    
    def compress_pdf_ghostscript(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        compression_level: Literal['low', 'medium', 'high', 'maximum'] = 'medium'
    ) -> dict:
        """
        Compress PDF using Ghostscript (more aggressive compression, 30-70% reduction)
        
        Args:
            input_path: Path to input PDF file
            output_path: Optional custom output path
            compression_level: Compression quality preset
            
        Returns:
            dict: Compression results with statistics
        """
        try:
            # Check if Ghostscript is installed
            if not self._check_ghostscript():
                return {
                    "success": False,
                    "error": "Ghostscript not installed. Install with: brew install ghostscript (macOS) or apt-get install ghostscript (Linux)"
                }
            
            input_file = Path(input_path)
            
            if not input_file.exists():
                return {"success": False, "error": "Input file not found"}
            
            if not input_file.suffix.lower() == '.pdf':
                return {"success": False, "error": "File is not a PDF"}
            
            # Generate output path if not provided
            if output_path is None:
                output_filename = input_file.stem + '_compressed.pdf'
                output_file = self.output_dir / output_filename
            else:
                output_file = Path(output_path)
            
            # Get original file size
            original_size = self.get_file_size(str(input_file))
            
            print(f"Compressing with Ghostscript: {input_file.name}")
            print(f"Original size: {original_size['mb']} MB")
            print(f"Compression level: {compression_level}")
            
            # Ghostscript quality settings
            gs_settings = {
                'low': '/screen',      # 72 dpi, maximum compression (30-70% reduction)
                'medium': '/ebook',    # 150 dpi, good compression (20-50% reduction)
                'high': '/printer',    # 300 dpi, minimal compression (10-30% reduction)
                'maximum': '/prepress' # 300 dpi, high quality (5-15% reduction)
            }
            
            quality_setting = gs_settings.get(compression_level, '/ebook')
            
            # Ghostscript command
            gs_command = [
                'gs',
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={quality_setting}',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                '-dDetectDuplicateImages=true',
                '-dCompressFonts=true',
                '-r150',  # Resolution
                f'-sOutputFile={output_file}',
                str(input_file)
            ]
            
            # Run Ghostscript
            result = subprocess.run(
                gs_command,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Ghostscript error: {result.stderr}"
                }
            
            # Get compressed file size
            compressed_size = self.get_file_size(str(output_file))
            
            # Calculate reduction
            reduction_bytes = original_size['bytes'] - compressed_size['bytes']
            reduction_percent = (reduction_bytes / original_size['bytes']) * 100 if original_size['bytes'] > 0 else 0
            
            print(f"Compressed size: {compressed_size['mb']} MB")
            print(f"Size reduction: {round(reduction_percent, 2)}%")
            print(f"✓ Successfully compressed: {input_file.name}")
            
            return {
                "success": True,
                "input_file": str(input_file),
                "output_file": str(output_file),
                "original_size_mb": original_size['mb'],
                "compressed_size_mb": compressed_size['mb'],
                "reduction_mb": round(reduction_bytes / (1024 * 1024), 2),
                "reduction_percent": round(reduction_percent, 2),
                "method": "ghostscript"
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Compression timeout (file too large)"}
        except Exception as e:
            print(f"✗ Error compressing {input_path}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def compress_pdf_basic(
        self, 
        input_path: str, 
        output_path: Optional[str] = None,
        compression_level: Literal['low', 'medium', 'high', 'maximum'] = 'medium'
    ) -> dict:
        """
        Compress PDF using basic PyPDF2 compression (limited reduction, 2-15%)
        
        Args:
            input_path: Path to input PDF file
            output_path: Optional custom output path
            compression_level: Compression quality preset
            
        Returns:
            dict: Compression results with statistics
        """
        try:
            input_file = Path(input_path)
            
            if not input_file.exists():
                return {"success": False, "error": "Input file not found"}
            
            if not input_file.suffix.lower() == '.pdf':
                return {"success": False, "error": "File is not a PDF"}
            
            # Generate output path if not provided
            if output_path is None:
                output_filename = input_file.stem + '_compressed.pdf'
                output_file = self.output_dir / output_filename
            else:
                output_file = Path(output_path)
            
            # Get original file size
            original_size = self.get_file_size(str(input_file))
            
            print(f"Compressing with PyPDF2: {input_file.name}")
            print(f"Original size: {original_size['mb']} MB")
            print(f"Compression level: {compression_level}")
            
            # Read the PDF
            with open(input_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Copy all pages
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    
                    # Compress page content
                    page.compress_content_streams()
                    pdf_writer.add_page(page)
                
                # Write compressed PDF
                with open(output_file, 'wb') as output:
                    pdf_writer.write(output)
            
            # Get compressed file size
            compressed_size = self.get_file_size(str(output_file))
            
            # Calculate reduction
            reduction_bytes = original_size['bytes'] - compressed_size['bytes']
            reduction_percent = (reduction_bytes / original_size['bytes']) * 100 if original_size['bytes'] > 0 else 0
            
            print(f"Compressed size: {compressed_size['mb']} MB")
            print(f"Size reduction: {round(reduction_percent, 2)}%")
            print(f"✓ Successfully compressed: {input_file.name}")
            
            return {
                "success": True,
                "input_file": str(input_file),
                "output_file": str(output_file),
                "original_size_mb": original_size['mb'],
                "compressed_size_mb": compressed_size['mb'],
                "reduction_mb": round(reduction_bytes / (1024 * 1024), 2),
                "reduction_percent": round(reduction_percent, 2),
                "method": "pypdf2"
            }
            
        except Exception as e:
            print(f"✗ Error compressing {input_path}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def compress_pdf_auto(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        compression_level: Literal['low', 'medium', 'high', 'maximum'] = 'medium'
    ) -> dict:
        """
        Automatically choose the best compression method
        Tries Ghostscript first (30-70% reduction), falls back to PyPDF2 if unavailable
        
        Args:
            input_path: Path to input PDF file
            output_path: Optional custom output path
            compression_level: Compression quality preset
            
        Returns:
            dict: Compression results with statistics
        """
        # Try Ghostscript first (better compression)
        if self._check_ghostscript():
            return self.compress_pdf_ghostscript(input_path, output_path, compression_level)
        else:
            print("⚠ Ghostscript not found, using basic compression (2-15% reduction)")
            print("  Install Ghostscript for better compression: brew install ghostscript")
            return self.compress_pdf_basic(input_path, output_path, compression_level)
    
    def compress_all_pdfs(
        self, 
        compression_level: Literal['low', 'medium', 'high', 'maximum'] = 'medium',
        use_ghostscript: bool = True
    ) -> dict:
        """
        Compress all PDF files in the input directory
        
        Args:
            compression_level: Compression quality preset
            use_ghostscript: Use Ghostscript if available (better compression)
            
        Returns:
            dict: Summary of compression results
        """
        pdf_files = list(self.input_dir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {self.input_dir}")
            return {
                "total": 0, 
                "successful": 0, 
                "failed": 0,
                "total_reduction_mb": 0,
                "average_reduction_percent": 0
            }
        
        print(f"\nFound {len(pdf_files)} PDF file(s) to compress\n")
        print("=" * 70)
        
        successful = 0
        failed = 0
        total_reduction_mb = 0
        total_reduction_percent = 0
        
        for pdf_file in pdf_files:
            if use_ghostscript:
                result = self.compress_pdf_auto(str(pdf_file), compression_level=compression_level)
            else:
                result = self.compress_pdf_basic(str(pdf_file), compression_level=compression_level)
            
            if result.get("success"):
                successful += 1
                total_reduction_mb += result.get("reduction_mb", 0)
                total_reduction_percent += result.get("reduction_percent", 0)
            else:
                failed += 1
            
            print("-" * 70)
        
        # Calculate averages
        avg_reduction_percent = total_reduction_percent / successful if successful > 0 else 0
        
        # Print summary
        print("\n" + "=" * 70)
        print("COMPRESSION SUMMARY")
        print("=" * 70)
        print(f"Total files: {len(pdf_files)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Total size reduction: {round(total_reduction_mb, 2)} MB")
        print(f"Average reduction: {round(avg_reduction_percent, 2)}%")
        print("=" * 70)
        
        return {
            "total": len(pdf_files),
            "successful": successful,
            "failed": failed,
            "total_reduction_mb": round(total_reduction_mb, 2),
            "average_reduction_percent": round(avg_reduction_percent, 2)
        }
    
    def get_compression_info(self, pdf_path: str) -> dict:
        """
        Get information about a PDF file for compression analysis
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            dict: PDF file information including page count and size
        """
        try:
            pdf_file = Path(pdf_path)
            
            if not pdf_file.exists():
                return {"error": "File not found"}
            
            size_info = self.get_file_size(str(pdf_file))
            
            # Get page count
            with open(pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
            
            return {
                "filename": pdf_file.name,
                "path": str(pdf_file.absolute()),
                "size_bytes": size_info['bytes'],
                "size_mb": size_info['mb'],
                "page_count": page_count,
                "avg_mb_per_page": round(size_info['mb'] / page_count, 2) if page_count > 0 else 0,
                "ghostscript_available": self._check_ghostscript()
            }
            
        except Exception as e:
            return {"error": str(e)}


def main():
    """Main function to demonstrate usage"""
    print("=" * 70)
    print("PDF Compressor")
    print("=" * 70)
    
    # Initialize compressor
    compressor = PDFCompressor()
    
    # Compress all PDFs in input directory
    results = compressor.compress_all_pdfs(compression_level='medium')
    
    if results["total"] == 0:
        print("\nNo PDF files found in the 'input' directory.")
        print("Please add PDF files to the 'input' folder and run again.")


if __name__ == "__main__":
    main()

# Made with Bob