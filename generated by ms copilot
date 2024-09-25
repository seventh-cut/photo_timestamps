import os
import PyPDF2
import docx
import openpyxl
from PIL import Image
from PIL.ExifTags import TAGS
import time

def extract_pdf_creation_date(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        info = reader.getDocumentInfo()
        if info and '/CreationDate' in info:
            creation_date = info['/CreationDate']
            # Convert PDF date format to timestamp
            creation_date = creation_date[2:16]
            creation_date = time.mktime(time.strptime(creation_date, "%Y%m%d%H%M%S"))
            return creation_date
    return None

def extract_docx_creation_date(file_path):
    doc = docx.Document(file_path)
    core_properties = doc.core_properties
    if core_properties.created:
        creation_date = core_properties.created
        return time.mktime(creation_date.timetuple())
    return None

def extract_xlsx_creation_date(file_path):
    wb = openpyxl.load_workbook(file_path)
    if wb.properties.created:
        creation_date = wb.properties.created
        return time.mktime(creation_date.timetuple())
    return None

def extract_jpeg_creation_date(file_path):
    image = Image.open(file_path)
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "DateTimeOriginal":
                creation_date = value
                return time.mktime(time.strptime(creation_date, "%Y:%m:%d %H:%M:%S"))
    return None

def set_file_timestamp(file_path, timestamp):
    os.utime(file_path, (timestamp, timestamp))

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.pdf'):
                timestamp = extract_pdf_creation_date(file_path)
            elif file.lower().endswith('.docx'):
                timestamp = extract_docx_creation_date(file_path)
            elif file.lower().endswith('.xlsx'):
                timestamp = extract_xlsx_creation_date(file_path)
            elif file.lower().endswith('.jpeg') or file.lower().endswith('.jpg'):
                timestamp = extract_jpeg_creation_date(file_path)
            else:
                continue
            
            if timestamp:
                set_file_timestamp(file_path, timestamp)

# Example usage
directory_to_process = '/path/to/your/directory'
process_directory(directory_to_process)
