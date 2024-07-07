import os
import random
import string
user_name='123'
code='123'

import os

def personal_info_check(category,lang):
    if lang=='en':
        print("To confirm your ownership of the account, please fill in the following information:")
        
        tel, email, address = None, None, None
        if category == 'card_address_modification':
            tel = input("Enter your telephone number: ")
            email = input("Enter your email: ")
        elif category == 'update_email':
            tel = input("Enter your telephone number: ")
            address = input("Enter your address: ")
        elif category == 'update_phone_number':
            email = input("Enter your email: ")
            address = input("Enter your address: ")
        else:
            tel = input("Enter your telephone number: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
      
        directory = r'D:\EVA PROJECT\EVA_VENV\EVA\sistem bancar\utilizatori'
        
        for file in os.listdir(directory):
            if file.startswith('user_') and file.endswith('.txt'):
                with open(os.path.join(directory, file), 'r') as f:
                    lines = f.readlines()
                    
                    if len(lines) < 5:
                        continue  
                    
                    stored_email = lines[1].split(": ")[1].strip() if len(lines) > 1 else None
                    stored_address = lines[3].split(": ")[1].strip() if len(lines) > 3 else None
                    stored_tel = lines[4].split(": ")[1].strip() if len(lines) > 4 else None
                    
                    if category == 'card_address_modification' and tel == stored_tel and email == stored_email:
                        print("Personal info confirmed.")
                        return file
                    elif category == 'update_email' and tel == stored_tel and address == stored_address:
                        print("Personal info confirmed.")
                        return file
                    elif category == 'update_phone_number' and email == stored_email and address == stored_address:
                        print("Personal info confirmed.")
                        return file
                    elif email == stored_email and address == stored_address and tel==stored_tel:
                        print("Personal info confirmed.")
                        return file
        
        print("Account info could not be confirmed.")
    else:
        print("Pentru a confirma calitatea de proprietar al contului, vă rugăm să completați următoarele informații:")
        
        tel, email, address = None, None, None
        if category == 'card_address_modification':
            tel = input("Scrie numarul de telefon: ")
            email = input("Scrie adresa de mail: ")
        elif category == 'update_email':
            tel = input("Scrie numarul de telefon: ")
            address = input("Introduce adresa: ")
        elif category == 'update_phone_number':
            email = input("Scrie adresa de mail: ")
            address = input("Introduce adresa: ")
        else:
            tel = input("Scrie numarul de telefon: ")
            email = input("Scrie adresa de mail: ")
            address = input("Introduce adresa: ")


        

        directory = r'D:\EVA PROJECT\EVA_VENV\EVA\sistem bancar\utilizatori'
        
        for file in os.listdir(directory):
            if file.startswith('user_') and file.endswith('.txt'):
                with open(os.path.join(directory, file), 'r') as f:
                    lines = f.readlines()
                    
                    if len(lines) < 5:
                        continue  
                    
                    stored_email = lines[1].split(": ")[1].strip() if len(lines) > 1 else None
                    stored_address = lines[3].split(": ")[1].strip() if len(lines) > 3 else None
                    stored_tel = lines[4].split(": ")[1].strip() if len(lines) > 4 else None
                    
                    if category == 'card_address_modification' and tel == stored_tel and email == stored_email:
                        print("Informatii confirmate")
                        return file
                    elif category == 'update_email' and tel == stored_tel and address == stored_address:
                        print("Informatii confirmate.")
                        return file
                    elif category == 'update_phone_number' and email == stored_email and address == stored_address:
                        print("Informatii confirmate.")
                        return file
                    elif email == stored_email and address == stored_address and tel==stored_tel:
                        print("Informatii confirmate.")
                        return file
        
        print("Informatii cont neconfirmate.")

    return None

from datetime import datetime

def generate_report(file):
    if file is None:
        print("Cannot generate report, account information not confirmed.")
        return
    
    directory = r'D:\EVA PROJECT\EVA_VENV\EVA\sistem bancar\utilizatori'
    filepath = os.path.join(directory, file)
    
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    user_info = {}
    for line in lines:
        key, value = line.split(': ', 1)
        user_info[key.strip()] = value.strip()
    
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = (
        f"Report for card loss:\n"
        f"User: {user_info.get('Name', 'N/A')}\n"
        f"Email: {user_info.get('Email', 'N/A')}\n"
        f"Address: {user_info.get('Adress', 'N/A')}\n"
        f"Tel. number: {user_info.get('Tel. number', 'N/A')}\n"
        f"Current date: {current_date}\n"
    )
    
    print(report)
    
    report_filename = f"report_{user_info.get('Name', 'unknown_user')}.txt"
    report_filepath = os.path.join(directory, report_filename)
    
    with open(report_filepath, 'w') as report_file:
        report_file.write(report)
    
    print(f"Report saved to {report_filepath}")

    

def update_personal_info(category, file):
    if file is None:
        print("Cannot update info, account information not confirmed.")
        return
    
    new_tel, new_email, new_address = None, None, None
    
    if category == 'card_address_modification':
        new_address = input("Enter your new address: ")
    elif category == 'update_email':
        new_email = input("Enter your new email: ")
    elif category == 'update_phone_number':
        new_tel = input("Enter your new telephone number: ")
    
    directory = r'D:\EVA PROJECT\EVA_VENV\EVA\sistem bancar\utilizatori'
    filepath = os.path.join(directory, file)
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    if new_address:
        lines[3] = f"Address: {new_address}\n"
    if new_email:
        lines[1] = f"Email: {new_email}\n"
    if new_tel:
        lines[4] = f"Tel. number: {new_tel}\n"
    
    with open(filepath, 'w') as f:
        f.writelines(lines)
    
    print("Your information has been updated successfully.")


def delete_user_file(file):
    if file is None:
        print("Cannot delete file, file name not provided.")
        return
    
    directory = r'D:\EVA PROJECT\EVA_VENV\EVA\sistem bancar\utilizatori'
    filepath = os.path.join(directory, file)
    
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return
    
    try:
        os.remove(filepath)
        print(f"File {filepath} has been deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")





def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



def get_next_user_id(directory):
    files = [f for f in os.listdir(directory) if f.startswith('user_') and f.endswith('.txt')]
    return len(files) + 1

def create_account(directory):
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    adresa = input("Enter your adress: ")
    tel = input("Enter your telephone number: ")
    email = input("Enter your email: ")
    confirmation_code = generate_random_string()
    user_id = get_next_user_id(directory)
    confirmation_code='1'
    entered_code='1'
    creez_cont=1
    retry=1
    while entered_code != confirmation_code and retry==1:
        entered_code = input("Enter the code sent to your email: ")
        if entered_code==confirmation_code:
            creez_cont=1
            break
        else :
            creez_cont=0
        print("Incorrect confirmation code. Account creation failed.")

        re=input("Would you like to retry entering the code? (yes/no): ")
        if re=='yes':
            retry=1
        else:
            retry=0
            break

    if creez_cont==1:
        file_path = os.path.join(directory, f"user_{user_id}.txt")
        
        with open(file_path, 'w') as f:
            f.write(f"Name: {name}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Password: {(password)}\n")
            f.write(f"Adress: {adresa}\n")
            f.write(f"Tel. number: {tel}\n")

        
        print(f"Account created successfully! Your user ID is {user_id}")
    else:
        print("Account creation failed.")

def login(directory):
    print()
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    hashed_password = password
    
    for file in os.listdir(directory):
        if file.startswith('user_') and file.endswith('.txt'):
            with open(os.path.join(directory, file), 'r') as f:
                lines = f.readlines()
                stored_email = lines[1].split(": ")[1].strip()
                stored_password = lines[2].split(": ")[1].strip()
                stored_user_id = lines[0].split(": ")[1].strip()
                
                if stored_email == email and stored_password == hashed_password:
                    print(f"Login successful! Welcome back, {lines[0].split(': ')[1].strip()}.")
                    print()

                    return True
    
    print("Login failed. Please check your email and password.")
    reset_choice = input("Forgot your password? (yes/no): ").strip().lower()
    if reset_choice == 'yes':
        reset_password(directory, email,stored_user_id)
    
    return False


def reset_password(directory, email,stored_user_id):
    confirmation_code = generate_random_string()
    print(f"Pentru testing , codul este {confirmation_code}")
    
    entered_code=''
    retry=1
    while entered_code != confirmation_code and retry==1:
        entered_code = input("Enter the code sent to your email: ")
        if entered_code==confirmation_code:
            break

        print("Incorrect confirmation code. Account creation failed.")
        re=input("Would you like to retry entering the code? (yes/no): ")
        if re=='yes':
            retry=1
        else:
            retry=0
            break


    new_password = input("Enter your new password: ")
    hashed_new_password = new_password
    
    for file in os.listdir(directory):
        if file.startswith('user_') and file.endswith('.txt'):
            with open(os.path.join(directory, file), 'r') as f:
                lines = f.readlines()
                stored_email = lines[1].split(": ")[1].strip()
                
                if stored_email == email:
                    lines[2] = f"Password: {hashed_new_password}\n"
                    with open(os.path.join(directory, file), 'w') as f:
                        f.writelines(lines)
                    print("Password reset successful.")
                    return
    print("Email not found. Password reset failed.")

def banking():
    directory = r'D:\EVA PROJECT\EVA_VENV\EVA\sistem bancar\utilizatori'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    while True:
        print()
        print("-------------")
        print("1. Create Account")
        print("2. Login")
        print("3. Quit")

        choice = input("Enter your choice (1, 2, or 3): ")
        print()
        if choice == '1':
            create_account(directory)
        elif choice == '2':
            if login(directory):
                print("Choose AI Model to interact with:")
                print("1. Document Summarization Model")
                print("2. Chatbot Model (EVA)")
                print("3. Quit")
                choice2 = input("Enter your choice (1 or 2): ")

                if choice2 == '1':
                    print("Selected: Document Summarization Model")
                    print()
                    return 1
                elif choice2 == '2':
                    print("Selected: Chatbot (EVA)")
                    print()
                    return 2
                elif choice2 == '3':
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

