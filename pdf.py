# Takes a List of PDF Links. Downloads them into a tmp folder, merges them, and opens the merged pdf in default browser
import requests
import webbrowser as wb
import os
from yaspin import yaspin
from pypdf import PdfWriter
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

tmp_folder = os.path.join(os.getcwd(), "tmp")
download_folder = os.path.join(os.getcwd(), "downloaded")

def Pdf(pdfs_list, subject, unit):
    with yaspin(text="Initializing download...", color="green") as sp:
        os.makedirs(tmp_folder, exist_ok=True)
        os.makedirs(download_folder, exist_ok=True)
        tmp_pdfs_path = []

        cls()
        sp.text = "Fetching PDFs"
        for index, pdf_url in enumerate(pdfs_list, start=1):
            sp.text = f"Fetching PDF {index}/{len(pdfs_list)}"
            response = requests.get(pdf_url, stream=True)
            
            pdf_filename = f"{subject}_{unit}_{index}.pdf"
            pdf_path = os.path.join(tmp_folder, pdf_filename)
            tmp_pdfs_path.append(pdf_path)

            with open(pdf_path, "wb") as file:
                file.write(response.content)

        sp.text = "Fetched all PDFs. Merging Under Process"
        
        pdf_merger = PdfWriter()
        for pdf in tmp_pdfs_path:
            pdf_merger.append(pdf)
        
        final_pdf_name = f"{subject}_{unit}.pdf"
        final_pdf_path = os.path.join(download_folder, final_pdf_name)
        pdf_merger.write(final_pdf_path)
        

        sp.ok(f"Merged PDF in downloaded/. Opening in Default PDF Application...")
        time.sleep(3)
        wb.open_new(final_pdf_path)
        time.sleep(2)


    
