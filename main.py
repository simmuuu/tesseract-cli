import inquirer
from yaspin import yaspin
from login import Login
from subject import Subject
import time
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
def subjectsHandler():
    Subject()   

def dashboard():
    dashboard = [
    inquirer.List(
        "dashboard",
        message="Tesseract-CLI",
        choices=["👤 Login", "📚 Subjects", "🚪 Exit"],
    ),
    ]

    cls()
    option = inquirer.prompt(dashboard)["dashboard"]
    match option:
        case "👤 Login":
            Login()
        case "📚 Subjects":
            cls()
            subjectsHandler()
        case "🚪 Exit":
            cls()
            print("Exiting program...")
            exit(0)
        case _:
            print("Invalid option")
            

def main():
    while True:
        dashboard()
    
if __name__ == '__main__':
    main()