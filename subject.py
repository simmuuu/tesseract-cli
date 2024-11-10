from db.dbPy import getDB
import inquirer
import requests
from yaspin import yaspin
from pdf import Pdf
import os
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def get_subjects():
    regulation_id = getDB("regulationId")
    branch_id = getDB("branchId")
    token = getDB("access_token")
    sem = getDB("yearsemesterCode")
    subjects_url = f"https://api.tesseractonline.com/studentmaster/subjects/{regulation_id}/{branch_id}"
    
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json"   
    }
    
    try:
        response = requests.get(subjects_url, headers=headers)
        data = response.json()
        
        # error checking
        if data.get('Error'):
            # cls()
            print("Please Login")
            exit(1)
        
        subject_list = []
        
        for subject in data.get("payload", []):
            if subject.get("yearsemester_code") == sem:
                subject_list.append({
                        "subject_id": subject["subject_id"],
                        "subject_name": subject["subject_name"]
                    })
        
        return subject_list
    except:
        print("Error: subject.py -> get_subjects()")
        exit(1)
        
def get_units(subject_id):
    unitURL = f"https://api.tesseractonline.com/studentmaster/get-subject-units/{subject_id}"
    token = getDB("access_token")
    
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json"   
    }
    
    try:
        response = requests.get(unitURL, headers=headers)
        data = response.json()
        
        # error checking
        if data.get('Error'):
            # cls()
            print("Please Login")
            exit(1)
        
        unit_list = []
        
        for unit in data.get("payload", []):
            unit_list.append({
                    "unitId": unit["unitId"],
                    "unitName": unit["unitName"]
                })
        
        return unit_list
    except:
        print("Error: subject.py -> get_units()")
        exit(1)
        
def get_pdfs(unit_id):
    topicsURL = f"https://api.tesseractonline.com/studentmaster/get-topics-unit/{unit_id}"
    pdf_url = "https://api.tesseractonline.com"
    token = getDB("access_token")
    
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json"   
    }
    
    try:
        response = requests.get(topicsURL, headers=headers)
        data = response.json()
        
        # error checking
        if data.get('Error'):
            # cls()
            print("Please Login")
            exit(1)
        
        pdf_list = []
        
        for topic in data.get("payload", [])["topics"]:
            if topic.get("pdf") not in [None, "null"]:
                pdf_list.append(f"{pdf_url}/{topic.get("pdf")}")
                
        return pdf_list    
    except:
        print("Error: subject.py -> get_pdfs()")
        exit(1)
    
        

def Subject():
    # SUBJECT -> Gets User Requested Subject ID
    subjects = get_subjects()
    subject_question = [
                    inquirer.List('subject',
                                  message="Tesseract-CLI",
                                  choices=[subject["subject_name"] for subject in subjects],
                                  ),
                ]
    selected_subject = inquirer.prompt(subject_question)["subject"]
    
    for subject in subjects:
        if subject["subject_name"] == selected_subject:
            selected_subject_id = subject["subject_id"]
            break
    
    # UNIT -> Gets User Requested Unit ID
    units = get_units(selected_subject_id)
    cls()
    unit_question = [
                    inquirer.List('unit',
                                  message="Tesseract-CLI",
                                  choices=[unit["unitName"] for unit in units],
                                  ),
                ]
    selected_unit = inquirer.prompt(unit_question)["unit"]
    
    for unit in units:
        if unit["unitName"] == selected_unit:
            selected_unit_id = unit["unitId"]
            break
    
    # PDF -> Returns a List of PDF's
    pdf_list = get_pdfs(selected_unit_id)
        
    if pdf_list == []:
        print("No PDF's Available.", flush=True)
        time.sleep(2)
        return;
    
    Pdf(pdf_list, selected_subject, selected_unit)    
    