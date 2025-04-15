"""
Office Document to PDF Converter
A robust converter that uses multiple methods to ensure success
"""

import os
import sys
import time
import subprocess
from pathlib import Path


def convert_with_docx2pdf(input_file, output_file=None):
    """Convert using docx2pdf library - a reliable third-party solution"""
    try:
        # First try to install docx2pdf if not present
        try:
            from docx2pdf import convert
        except ImportError:
            print("Installing docx2pdf package...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "docx2pdf"])
            time.sleep(2)
            from docx2pdf import convert
            print("docx2pdf installed successfully")
        
        input_path = Path(input_file).resolve()
        
        # Set output path if not specified
        if output_file is None:
            output_path = input_path.with_suffix(".pdf")
        else:
            output_path = Path(output_file).resolve()
        
        print(f"Converting using docx2pdf: {input_path} to {output_path}")
        
        # Convert the file
        convert(str(input_path), str(output_path))
        
        # Check if conversion was successful
        if output_path.exists():
            print(f"Conversion successful: {output_path}")
            return True
        else:
            print(f"docx2pdf conversion failed: Output file not created")
            return False
            
    except Exception as e:
        print(f"Error with docx2pdf conversion: {str(e)}")
        return False


def convert_with_com_direct(input_file, output_file=None):
    """Convert using direct COM automation with Word"""
    try:
        import comtypes.client
        
        input_path = Path(input_file).resolve()
        
        # Set output path if not specified
        if output_file is None:
            output_path = input_path.with_suffix(".pdf")
        else:
            output_path = Path(output_file).resolve()
        
        print(f"Converting using COM automation: {input_path} to {output_path}")
        
        # Kill any existing Word processes to avoid conflicts
        try:
            os.system("taskkill /f /im WINWORD.EXE")
            time.sleep(1)
        except:
            pass
        
        # Create Word application object with visible option for troubleshooting
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = True
        
        try:
            # Specify full path with backward slashes to avoid path issues
            doc = word.Documents.Open(str(input_path))
            
            # Try ExportAsFixedFormat first (more reliable)
            try:
                doc.ExportAsFixedFormat(
                    OutputFileName=str(output_path),
                    ExportFormat=17,  # wdExportFormatPDF
                    OpenAfterExport=False,
                    OptimizeFor=0,    # wdExportOptimizeForPrint
                    Range=0,          # wdExportAllDocument
                    Item=0,           # wdExportDocumentContent
                    IncludeDocProps=True,
                    KeepIRM=True,
                    CreateBookmarks=0, # wdExportCreateNoBookmarks
                    DocStructureTags=True,
                    BitmapMissingFonts=True,
                    UseISO19005_1=False
                )
            except Exception as e:
                print(f"ExportAsFixedFormat failed, trying SaveAs: {str(e)}")
                # Fallback to SaveAs if ExportAsFixedFormat fails
                doc.SaveAs(str(output_path), FileFormat=17)  # wdFormatPDF = 17
                
            # Close the document without saving changes
            doc.Close(SaveChanges=False)
            
            # Check if conversion was successful
            if output_path.exists():
                print(f"COM automation conversion successful: {output_path}")
                return True
            else:
                print("COM automation conversion failed: Output file not created")
                return False
                
        except Exception as e:
            print(f"Error during COM automation: {str(e)}")
            return False
            
        finally:
            # Always make sure Word quits, even if errors occur
            try:
                word.Quit()
            except:
                pass
            
            # Make sure Word process is terminated
            try:
                os.system("taskkill /f /im WINWORD.EXE")
            except:
                pass
                
    except Exception as e:
        print(f"Error setting up COM automation: {str(e)}")
        return False


def convert_with_libreoffice(input_file, output_file=None):
    """Convert using LibreOffice if available"""
    try:
        input_path = Path(input_file).resolve()
        
        # Set output path if not specified
        if output_file is None:
            output_path = input_path.with_suffix(".pdf")
        else:
            output_path = Path(output_file).resolve()
            
        output_dir = output_path.parent
        
        print(f"Attempting conversion with LibreOffice: {input_path} to {output_path}")
        
        # List of possible LibreOffice paths
        libreoffice_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
        
        # Find LibreOffice executable
        libreoffice_path = None
        for path in libreoffice_paths:
            if Path(path).exists():
                libreoffice_path = path
                break
        
        if libreoffice_path is None:
            print("LibreOffice not found, skipping this method")
            return False
            
        # Execute LibreOffice conversion
        cmd = [
            libreoffice_path,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_dir),
            str(input_path)
        ]
        
        process = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check if the default output file exists (LibreOffice may ignore our output filename)
        default_output = output_dir / input_path.with_suffix(".pdf").name
        
        # If default output exists but is different from our target, rename it
        if default_output.exists() and default_output != output_path:
            os.rename(str(default_output), str(output_path))
            
        if output_path.exists():
            print(f"LibreOffice conversion successful: {output_path}")
            return True
        else:
            print("LibreOffice conversion failed")
            return False
            
    except Exception as e:
        print(f"Error with LibreOffice conversion: {str(e)}")
        return False


def convert_with_powershell(input_file, output_file=None):
    """Convert using PowerShell and Word automation"""
    try:
        input_path = Path(input_file).resolve()
        
        # Set output path if not specified
        if output_file is None:
            output_path = input_path.with_suffix(".pdf")
        else:
            output_path = Path(output_file).resolve()
            
        print(f"Attempting conversion with PowerShell: {input_path} to {output_path}")
        
        # Create a temporary PowerShell script
        ps_script = """
        $word = New-Object -ComObject Word.Application
        $word.Visible = $false
        $doc = $word.Documents.Open("${input}")
        $doc.SaveAs([ref] "${output}", [ref] 17)
        $doc.Close()
        $word.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
        """
        
        ps_script = ps_script.replace("${input}", str(input_path))
        ps_script = ps_script.replace("${output}", str(output_path))
        
        # Save the script to a temporary file
        script_path = Path(os.environ.get('TEMP', '.')) / 'convert_to_pdf.ps1'
        with open(script_path, 'w') as f:
            f.write(ps_script)
            
        # Execute the PowerShell script
        cmd = [
            'powershell', 
            '-ExecutionPolicy', 'Bypass',
            '-File', str(script_path)
        ]
        
        process = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up the temporary file
        try:
            os.remove(script_path)
        except:
            pass
            
        # Check if conversion was successful
        if output_path.exists():
            print(f"PowerShell conversion successful: {output_path}")
            return True
        else:
            print("PowerShell conversion failed")
            return False
            
    except Exception as e:
        print(f"Error with PowerShell conversion: {str(e)}")
        return False


def convert_document_to_pdf(input_file, output_file=None):
    """Try multiple conversion methods until one succeeds"""
    input_path = Path(input_file)
    
    # Validate input file exists
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found")
        return False
        
    # Check file extension
    file_ext = input_path.suffix.lower()
    if file_ext not in ['.doc', '.docx', '.docm', '.ppt', '.pptx', '.xls', '.xlsx']:
        print(f"Warning: File extension '{file_ext}' might not be supported")
    
    # Set default output filename if not provided
    if output_file is None:
        output_path = input_path.with_suffix(".pdf")
    else:
        output_path = Path(output_file)
    
    # Kill any Office processes that might interfere
    try:
        os.system("taskkill /f /im WINWORD.EXE >nul 2>&1")
        os.system("taskkill /f /im EXCEL.EXE >nul 2>&1")
        os.system("taskkill /f /im POWERPNT.EXE >nul 2>&1")
    except:
        pass
    
    print("=" * 60)
    print(f"Converting: {input_path.resolve()}")
    print(f"Output to: {output_path.resolve()}")
    print("=" * 60)
    
    # Try each conversion method in order of reliability
    print("\n1. Trying docx2pdf method...")
    if convert_with_docx2pdf(input_file, output_file):
        return True
    
    print("\n2. Trying COM automation method...")
    if convert_with_com_direct(input_file, output_file):
        return True
    
    print("\n3. Trying PowerShell method...")
    if convert_with_powershell(input_file, output_file):
        return True
    
    print("\n4. Trying LibreOffice method...")
    if convert_with_libreoffice(input_file, output_file):
        return True
    
    print("\nAll conversion methods failed")
    return False


def print_troubleshooting_tips():
    """Print helpful troubleshooting tips"""
    print("\n" + "=" * 60)
    print("TROUBLESHOOTING TIPS".center(60))
    print("=" * 60)
    print("1. Make sure Microsoft Office is installed and activated")
    print("2. Try opening and resaving the document manually first")
    print("3. Check if the document is password protected")
    print("4. Make sure you have write permissions in the output directory")
    print("5. Try saving the document with a simpler name (no spaces or special characters)")
    print("6. Convert the document manually by opening it and using 'Save As PDF'")
    print("7. Install LibreOffice as a fallback conversion option")
    print("=" * 60)


def main():
    """Main function"""
    print("=" * 60)
    print("Office Document to PDF Converter".center(60))
    print("=" * 60)
    
    # Check if we have enough arguments
    if len(sys.argv) < 2:
        print("Usage: python converter.py input_file [output_file]")
        print("Example: python converter.py document.docx output.pdf")
        return 1
    
    # Get input and optional output file
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Convert the document
    success = convert_document_to_pdf(input_file, output_file)
    
    if not success:
        print_troubleshooting_tips()
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
