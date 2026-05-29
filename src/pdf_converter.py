"""
PDF to Word Converter Module
Converts PDF files to Word documents using pdf2docx library
"""

import os
from pathlib import Path
from pdf2docx import Converter
from typing import Optional


class PDFToWordConverter:
    """Class to handle PDF to Word conversion"""
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        """
        Initialize the converter with input and output directories
        
        Args:
            input_dir: Directory containing PDF files
            output_dir: Directory to save converted Word files
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Create directories if they don't exist
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def convert_single_pdf(self, pdf_path: str, output_path: Optional[str] = None) -> bool:
        """
        Convert a single PDF file to Word document
        
        Args:
            pdf_path: Path to the PDF file
            output_path: Optional custom output path for the Word file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            pdf_file = Path(pdf_path)
            
            if not pdf_file.exists():
                print(f"Error: PDF file not found: {pdf_path}")
                return False
            
            if not pdf_file.suffix.lower() == '.pdf':
                print(f"Error: File is not a PDF: {pdf_path}")
                return False
            
            # Generate output path if not provided
            if output_path is None:
                output_filename = pdf_file.stem + '.docx'
                output_path = self.output_dir / output_filename
            else:
                output_path = Path(output_path)
            
            print(f"Converting: {pdf_file.name}")
            print(f"Output: {output_path}")
            
            # Create converter and convert
            cv = Converter(str(pdf_file))
            cv.convert(str(output_path))
            cv.close()
            
            print(f"✓ Successfully converted: {pdf_file.name}")
            return True
            
        except Exception as e:
            print(f"✗ Error converting {pdf_path}: {str(e)}")
            return False
    
    def convert_all_pdfs(self) -> dict:
        """
        Convert all PDF files in the input directory
        
        Returns:
            dict: Summary of conversion results
        """
        pdf_files = list(self.input_dir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {self.input_dir}")
            return {"total": 0, "successful": 0, "failed": 0}
        
        print(f"\nFound {len(pdf_files)} PDF file(s) to convert\n")
        print("=" * 60)
        
        successful = 0
        failed = 0
        
        for pdf_file in pdf_files:
            if self.convert_single_pdf(str(pdf_file)):
                successful += 1
            else:
                failed += 1
            print("-" * 60)
        
        # Print summary
        print("\n" + "=" * 60)
        print("CONVERSION SUMMARY")
        print("=" * 60)
        print(f"Total files: {len(pdf_files)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print("=" * 60)
        
        return {
            "total": len(pdf_files),
            "successful": successful,
            "failed": failed
        }
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        Get basic information about a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            dict: PDF file information
        """
        try:
            pdf_file = Path(pdf_path)
            
            if not pdf_file.exists():
                return {"error": "File not found"}
            
            file_size = pdf_file.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            return {
                "filename": pdf_file.name,
                "path": str(pdf_file.absolute()),
                "size_bytes": file_size,
                "size_mb": round(file_size_mb, 2)
            }
            
        except Exception as e:
            return {"error": str(e)}


def main():
    """Main function to demonstrate usage"""
    print("=" * 60)
    print("PDF to Word Converter")
    print("=" * 60)
    
    # Initialize converter
    converter = PDFToWordConverter()
    
    # Convert all PDFs in input directory
    results = converter.convert_all_pdfs()
    
    if results["total"] == 0:
        print("\nNo PDF files found in the 'input' directory.")
        print("Please add PDF files to the 'input' folder and run again.")


if __name__ == "__main__":
    main()

# Made with Bob
