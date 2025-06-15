import csv
import os
from utils import cipher_suite
from datetime import datetime

class Entry:
    def __init__(self, mood, tags="", message=""):
        self.mood = mood
        self.tags = tags
        self.message = message
        now = datetime.now()
        self.user_id = None

        date_str = now.strftime("%b %d, %Y - %I:%M %p")
        date_str = date_str.replace(" 0", " ")       
        date_str = date_str.lstrip("0")               
        self.date = date_str.lower().replace("am", "am").replace("pm", "pm")
        
    def set_user_id(self, user_id):
        self.user_id = user_id
    
    def save_entry(self):
        filename = f'data/moods/{self.user_id}.csv'
        file_exists = os.path.exists(filename)

        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Mood", "Tags", "Message"]) 

            encrypted_date = cipher_suite.encrypt(self.date.encode()).decode()
            encrypted_mood = cipher_suite.encrypt(self.mood.encode()).decode()
            encrypted_tags = cipher_suite.encrypt(self.tags.encode()).decode()
            encrypted_message= cipher_suite.encrypt(self.message.encode()).decode()

            writer.writerow([encrypted_date, encrypted_mood, encrypted_tags, encrypted_message])

            print("\nMood entry saved successfully!")

    def view_all(self):
        filename = f'data/moods/{self.user_id}.csv'
        if not os.path.exists(filename):
            print("❌ No mood entries found.")
            return
        
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = reader(file)
        # TODO: Finish this
            

    def get_average_mood(self):
        # TODO: Add this method
        pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(user):
    while True:
        clear_screen()
        print("\n─────────────🙂 Main Menu 🙂─────────────\n")
        print(f'Welcome back, {user}!')
        print("\nChoose an option:")
        print("1. Set mood today")
        print("2. View all mood entries")
        print("3. Get average mood")
        print("4. Quit")

        while True: 
            choice = input('Enter your choice (1-5): ').strip()
            if choice.isdigit() and 1 <= int(choice) <= 5:
                break
            else:
                print("Error: Invalid option. Please choose a number between 1 and 5.\n")

        if choice == '1':
            while True:
                clear_screen()
                print("\n─────────────🙂 Set Mood 🙂─────────────\n")
                print(f'💗 How are you, {user}?\n')
                print('5. 😄  (Very Happy)')
                print('4. 😊  (Happy)')
                print('3. 🫤  (Neutral)')
                print('2. 😓  (Sad)')
                print('1. 🥲  (Very Sad)')

                while True:
                    mood = input('\nEnter your choice (1-5): ').strip()
                    if mood.isdigit() and 1 <= int(mood) <= 5:
                        if mood == '5':
                            mood = '5. 😄  (Very Happy)'
                        elif mood == '4':
                            mood = '4. 😊  (Happy)'
                        elif mood == '3':
                            mood = '3. 🫤  (Neutral)'
                        elif mood == '2':
                            mood = '2. 😓  (Sad)'
                        else:
                            mood = '1. 🥲  (Very Sad)'
                        break
                    else:
                        print("Error: Invalid option. Please choose a number between 1 and 5.\n")

                while True:
                    tags = input('\n🏷️  Tags (use #tag format): ').strip()
                    if '#' in tags:
                        break
                    else:
                        print("Error: Tags must contain '#' symbol. Please try again.\n")

                message = input('🗨️  Message (optional): ').strip()

                entry = Entry(mood, tags, message)
                entry.set_user_id(user)
                entry.save_entry()
                input("Press Enter to return to the main menu...")
                break

        elif choice == '2':
            clear_screen()
            print("\n─────────────🙂 Search specific dates 🙂─────────────\n")
        elif choice == '3':
            # TODO: Implement feature to view all mood entries
            pass
        elif choice == '4':
            # TODO: Implement feature to calculate and display average mood
            pass
        elif choice == '5':
            # TODO: Add exit logic or return to main menu
            pass
        








