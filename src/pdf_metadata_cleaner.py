#!/usr/bin/env python3
"""
PDF Metadata Cleaner
Removes metadata from PDF files for privacy and security
"""

import os
from pathlib import Path
from typing import Dict, Optional
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime


class PDFMetadataCleaner:
    """Clean metadata from PDF files"""
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        """
        Initialize the PDF Metadata Cleaner
        
        Args:
            input_dir: Directory containing input PDF files
            output_dir: Directory for cleaned PDF files
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Create directories if they don't exist
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def get_metadata(self, pdf_path: str) -> Dict:
        """
        Get metadata from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing metadata information
        """
        try:
            reader = PdfReader(pdf_path)
            metadata = reader.metadata
            
            if metadata:
                return {
                    'title': metadata.get('/Title', 'N/A'),
                    'author': metadata.get('/Author', 'N/A'),
                    'subject': metadata.get('/Subject', 'N/A'),
                    'creator': metadata.get('/Creator', 'N/A'),
                    'producer': metadata.get('/Producer', 'N/A'),
                    'creation_date': metadata.get('/CreationDate', 'N/A'),
                    'modification_date': metadata.get('/ModDate', 'N/A'),
                    'keywords': metadata.get('/Keywords', 'N/A'),
                }
            else:
                return {'message': 'No metadata found'}
                
        except Exception as e:
            return {'error': f'Failed to read metadata: {str(e)}'}
    
    def clean_metadata(
        self,
        input_path: str,
        output_path: str,
        keep_basic_info: bool = False
    ) -> Dict:
        """
        Remove metadata from a PDF file
        
        Args:
            input_path: Path to input PDF file
            output_path: Path for cleaned PDF file
            keep_basic_info: If True, keeps title and page count
            
        Returns:
            Dictionary with operation results
        """
        try:
            # Get original metadata for reporting
            original_metadata = self.get_metadata(input_path)
            
            # Read the PDF
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            # Copy all pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Remove all metadata by not adding any
            # Or add minimal metadata if requested
            if keep_basic_info and reader.metadata:
                title = reader.metadata.get('/Title', 'Document')
                writer.add_metadata({
                    '/Title': title,
                    '/Producer': 'PDF Metadata Cleaner',
                    '/CreationDate': datetime.now().strftime("D:%Y%m%d%H%M%S")
                })
            
            # Write the cleaned PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Get file sizes
            original_size = os.path.getsize(input_path)
            cleaned_size = os.path.getsize(output_path)
            
            # Get cleaned metadata
            cleaned_metadata = self.get_metadata(output_path)
            
            return {
                'success': True,
                'original_metadata': original_metadata,
                'cleaned_metadata': cleaned_metadata,
                'original_size_mb': round(original_size / (1024 * 1024), 2),
                'cleaned_size_mb': round(cleaned_size / (1024 * 1024), 2),
                'metadata_removed': len([k for k, v in original_metadata.items() 
                                        if v != 'N/A' and k != 'error']),
                'keep_basic_info': keep_basic_info
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to clean metadata: {str(e)}'
            }
    
    def clean_pdf_file(
        self,
        filename: str,
        keep_basic_info: bool = False
    ) -> Dict:
        """
        Clean metadata from a PDF file in the input directory
        
        Args:
            filename: Name of the PDF file
            keep_basic_info: If True, keeps title and page count
            
        Returns:
            Dictionary with operation results
        """
        input_path = self.input_dir / filename
        output_filename = f"cleaned_{filename}"
        output_path = self.output_dir / output_filename
        
        if not input_path.exists():
            return {
                'success': False,
                'error': f'File not found: {filename}'
            }
        
        result = self.clean_metadata(
            str(input_path),
            str(output_path),
            keep_basic_info
        )
        
        if result.get('success'):
            result['output_filename'] = output_filename
        
        return result
    
    def batch_clean(
        self,
        keep_basic_info: bool = False
    ) -> Dict:
        """
        Clean metadata from all PDF files in the input directory
        
        Args:
            keep_basic_info: If True, keeps title and page count
            
        Returns:
            Dictionary with batch operation results
        """
        pdf_files = list(self.input_dir.glob("*.pdf"))
        
        if not pdf_files:
            return {
                'success': False,
                'error': 'No PDF files found in input directory'
            }
        
        results = []
        successful = 0
        failed = 0
        
        for pdf_file in pdf_files:
            result = self.clean_pdf_file(pdf_file.name, keep_basic_info)
            results.append({
                'filename': pdf_file.name,
                'result': result
            })
            
            if result.get('success'):
                successful += 1
            else:
                failed += 1
        
        return {
            'success': True,
            'total_files': len(pdf_files),
            'successful': successful,
            'failed': failed,
            'results': results
        }


def main():
    """Example usage of PDF Metadata Cleaner"""
    cleaner = PDFMetadataCleaner()
    
    # Example: Clean a single file
    print("PDF Metadata Cleaner")
    print("=" * 50)
    
    # List PDF files in input directory
    pdf_files = list(cleaner.input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"\nFound {len(pdf_files)} PDF file(s):")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"{i}. {pdf_file.name}")
    
    # Clean first file as example
    if pdf_files:
        filename = pdf_files[0].name
        print(f"\nCleaning metadata from: {filename}")
        
        # Show original metadata
        print("\nOriginal Metadata:")
        metadata = cleaner.get_metadata(str(cleaner.input_dir / filename))
        for key, value in metadata.items():
            print(f"  {key}: {value}")
        
        # Clean metadata
        result = cleaner.clean_pdf_file(filename, keep_basic_info=False)
        
        if result.get('success'):
            print(f"\n✓ Metadata cleaned successfully!")
            print(f"  Output: {result['output_filename']}")
            print(f"  Original size: {result['original_size_mb']} MB")
            print(f"  Cleaned size: {result['cleaned_size_mb']} MB")
            print(f"  Metadata fields removed: {result['metadata_removed']}")
        else:
            print(f"\n✗ Error: {result.get('error')}")


if __name__ == "__main__":
    main()

# Made with Bob