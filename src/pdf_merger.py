"""
PDF Merger Module
Merges multiple PDF files into a single PDF document
"""

import os
from PyPDF2 import PdfMerger, PdfReader
from datetime import datetime


class PDFMerger:
    """Class to handle PDF merging operations"""
    
    def __init__(self, upload_folder='uploads', output_folder='outputs'):
        """
        Initialize PDF Merger
        
        Args:
            upload_folder: Folder where uploaded PDFs are stored
            output_folder: Folder where merged PDF will be saved
        """
        self.upload_folder = upload_folder
        self.output_folder = output_folder
        
        # Create folders if they don't exist
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)
    
    def merge_pdfs(self, pdf_files, output_filename=None):
        """
        Merge multiple PDF files into one
        
        Args:
            pdf_files: List of PDF file paths to merge (in order)
            output_filename: Optional custom output filename
            
        Returns:
            dict: Information about the merged PDF
        """
        if not pdf_files or len(pdf_files) < 2:
            raise ValueError("At least 2 PDF files are required for merging")
        
        # Verify all files exist and are PDFs
        for pdf_file in pdf_files:
            if not os.path.exists(pdf_file):
                raise FileNotFoundError(f"File not found: {pdf_file}")
            if not pdf_file.lower().endswith('.pdf'):
                raise ValueError(f"Not a PDF file: {pdf_file}")
        
        # Generate output filename if not provided
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'merged_{timestamp}.pdf'
        
        output_path = os.path.join(self.output_folder, output_filename)
        
        # Create PDF merger
        merger = PdfMerger()
        
        try:
            # Add each PDF to the merger
            total_pages = 0
            file_info = []
            
            for pdf_file in pdf_files:
                reader = PdfReader(pdf_file)
                num_pages = len(reader.pages)
                total_pages += num_pages
                
                # Get file info
                file_size = os.path.getsize(pdf_file) / (1024 * 1024)  # MB
                filename = os.path.basename(pdf_file)
                
                file_info.append({
                    'filename': filename,
                    'pages': num_pages,
                    'size_mb': round(file_size, 2)
                })
                
                # Append PDF to merger
                merger.append(pdf_file)
            
            # Write merged PDF
            merger.write(output_path)
            merger.close()
            
            # Get merged file info
            merged_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            
            return {
                'success': True,
                'output_path': output_path,
                'output_filename': output_filename,
                'total_files': len(pdf_files),
                'total_pages': total_pages,
                'merged_size_mb': round(merged_size, 2),
                'files': file_info
            }
            
        except Exception as e:
            if merger:
                merger.close()
            raise Exception(f"Error merging PDFs: {str(e)}")
    
    def get_pdf_info(self, pdf_path):
        """
        Get information about a PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            dict: PDF information
        """
        try:
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)
            file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # MB
            
            return {
                'filename': os.path.basename(pdf_path),
                'pages': num_pages,
                'size_mb': round(file_size, 2)
            }
        except Exception as e:
            return {
                'filename': os.path.basename(pdf_path),
                'error': str(e)
            }


# Example usage
if __name__ == '__main__':
    merger = PDFMerger()
    
    # Example: Merge two PDFs
    pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']
    
    try:
        result = merger.merge_pdfs(pdf_files)
        print(f"✅ Successfully merged {result['total_files']} PDFs")
        print(f"📄 Total pages: {result['total_pages']}")
        print(f"💾 Output size: {result['merged_size_mb']} MB")
        print(f"📁 Saved to: {result['output_filename']}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Made with Bob
