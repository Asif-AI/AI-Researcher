from langchain_core.tools import tool
import io
import PyPDF2
import requests

#Access PDF from URL

def read_pdf(url: str) -> str:
    """function to read a PDF from a URL and return its text content.
    Args:
        url (str): The URL of the PDF file.
    Returns: 
        str: The text content of the PDF."""
    
    response = requests.get(url)
    pdf_file = io.BytesIO(response.content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    #Extract text from each page
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    print(f"Extracted text from {num_pages} pages.")
    return text.strip()
url= "https://arxiv.org/pdf/2508.08244.pdf"
print(read_pdf(url))


#Convert to bytes

#Retrieve text from PDF

