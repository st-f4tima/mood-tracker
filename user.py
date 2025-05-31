import csv
import os
from utils import hash_password

class User():
    def __init__(self, user_id, password):
        self.__user_id = user_id
        self.__password = password
    
    def create_account(self):
        hash_pass = hash_password(self.__password)
        user_info = [self.__user_id, hash_pass]
        
        file_exists = os.path.exists('data/users.csv')
        with open('data/users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['user_id', 'password'])  # add header once
            writer.writerow(user_info)
        
        print("Account created successfully!")

        user_filename = f'{self.__user_id}.csv'
        with open(user_filename, 'a', newline='') as file:
            pass

    def log_in(self):
        hashed_input_password = hash_password(self.__password)
        try:
            with open('data/users.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader, None) 
                for row in reader:
                    saved_user_id, saved_password = row
                    if self.__user_id == saved_user_id and hashed_input_password == saved_password:
                        print("Login successful!")
                        return True
                print("Login failed: Incorrect user ID or password.")
                return False
        except FileNotFoundError:
            print("User data file not found.")
            return False

def account_management():
    while True:
        print("\n─────────────🙂 Mood Tracker 🙂─────────────\n")
        print("Choose an option:")
        print("1. Create Account")
        print("2. Log in")
        print("3. Quit")

        while True: 
            choice = input('Enter your choice (1-3): ').strip()
            if choice.isdigit() and 1 <= int(choice) <= 3:
                break
            else:
                print("Error: Invalid option. Please choose a number between 1 and 3.\n")

        if choice == '1':
            user_id = input('\nInput a user-ID: ').strip()
            while True: 
                password = input('Enter your password: ').strip()
                confirm_password = input('Confirm your password: ').strip()
                if password == confirm_password:
                    break
                else:
                    print("Passwords do not match. Please try again.\n")
            
            new_user = User(user_id, password)
            new_user.create_account()
        
        elif choice == '2':
            user_id = input('\nInput a user-ID: ').strip()
            password = input('Enter your password: ').strip()

            user = User(user_id, password)
            if user.log_in():
                print(f"Welcome back, {user_id}!")
                break
            else:
                print("Login unsuccessful. Please try again.\n")
        
        elif choice == '3':
            print("Thank you for using Mood Tracker. Goodbye!")
            break
