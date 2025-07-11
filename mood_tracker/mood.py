import csv
import os
from mood_tracker.utils import cipher_suite
from datetime import datetime

class Entry:
    def __init__(self, mood="", tags="", message=""):
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
        filename = f'data/moods/{self.user_id}_entries.csv'
        file_exists = os.path.exists(filename)

        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists or os.path.getsize(filename) == 0:
                writer.writerow(["Date", "Mood", "Tags", "Message"])

            encrypted_date = cipher_suite.encrypt(self.date.encode()).decode()
            encrypted_mood = cipher_suite.encrypt(self.mood.encode()).decode()
            encrypted_tags = cipher_suite.encrypt(self.tags.encode()).decode()
            encrypted_message= cipher_suite.encrypt(self.message.encode()).decode()

            writer.writerow([encrypted_date, encrypted_mood, encrypted_tags, encrypted_message])

            print("\nMood entry saved successfully!")

    def view_all(self):
        filename = f'data/moods/{self.user_id}_entries.csv'

        if not os.path.exists(filename):
            print("❌ No mood entries found.")
            return

        with open(filename, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader, None)  

            found_any = False
            for idx, row in enumerate(csv_reader, start=1):
                if len(row) != 4:
                    print(f"⚠️ Skipped malformed entry at line {idx + 1}")
                    continue

                try:
                    decrypted_row = [cipher_suite.decrypt(col.encode()).decode() for col in row]
                    print(f"Entry #{idx}")
                    print(f"📅  Date:    {decrypted_row[0]}")
                    print(f"🙂  Mood:    {decrypted_row[1]}")
                    print(f"🏷️   Tags:    {decrypted_row[2]}")
                    print(f"🗨️   Message: {decrypted_row[3]}\n")
                    print("-" * 48)
                    found_any = True
                except Exception as e:
                    print(f"❌ Failed to decrypt entry #{idx}: {e}")

            if not found_any:
                print("📭 No valid mood entries to display.")


    def get_average_mood(self):
        mood_values = []
        filename = f'data/moods/{self.user_id}_entries.csv'

        if not os.path.exists(filename):
            print("❌ No mood entries found.")
            return None
        
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  

            for row in csv_reader:
                if len(row) < 2:
                    continue

                try:
                    encrypted_mood = row[1]
                    decrypted_mood = cipher_suite.decrypt(encrypted_mood.encode()).decode().strip()

                    if decrypted_mood.startswith('5'):
                        mood_values.append(5)
                    elif decrypted_mood.startswith('4'):
                        mood_values.append(4)
                    elif decrypted_mood.startswith('3'):
                        mood_values.append(3)
                    elif decrypted_mood.startswith('2'):
                        mood_values.append(2)
                    elif decrypted_mood.startswith('1'):
                        mood_values.append(1)
                    else:
                        mood_values.append(0)
                except Exception as e:
                    print(f"⚠️ Error decrypting mood: {e}")
        
        if not mood_values:
            return None

        return sum(mood_values) / len(mood_values)
    
    def delete_account(self):
        filename = f'data/users.csv'
        users_data = []
        username_to_delete = self.user_id

        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != username_to_delete:
                    users_data.append(row)

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users_data)
        
        print(f"\nDeleted account with username: {username_to_delete}")
        quit()



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
        print("4. Manage Account")
        print("5. Quit")

        while True: 
            choice = input('Enter your choice (1-4): ').strip()
            if choice.isdigit() and 1 <= int(choice) <= 4:
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
            print("\n─────────────📘 All Mood Entries 📘─────────────\n")
            entry = Entry("","","")
            entry.set_user_id(user)
            entry.view_all()
            input("\nPress Enter to return to the main menu...")

        elif choice == '3':
            clear_screen()
            print("\n─────────────📈📊 Mood Summary 📈📊─────────────\n")
            
            entry = Entry("", "", "")
            entry.set_user_id(user)
            average = entry.get_average_mood()

            if average is None:
                print("No mood data found. Please add some entries first.")
            else:
                average = float(average)

                def get_mood_label(avg):
                    if avg >= 4.5:
                        return "😄 Very Happy"
                    elif avg >= 3.5:
                        return "🙂 Happy"
                    elif avg >= 2.5:
                        return "😐 Okay"
                    elif avg >= 1.5:
                        return "😟 Sad"
                    else:
                        return "😢 Very Sad"

                mood_label = get_mood_label(average)

                scale = ["😢", "😟", "😐", "🙂", "😄"]
                index = min(4, max(0, round(average) - 1))
                arrow_line = "     " * index + " ↑"
                interpretation = {
                    "😄 Very Happy": "You're in a great place emotionally!",
                    "🙂 Happy": "You're doing well—keep it up!",
                    "😐 Okay": "You're feeling neutral. That’s totally okay.",
                    "😟 Sad": "It seems like you've been feeling a bit low.",
                    "😢 Very Sad": "Hang in there—better days are coming!"
                }

                print(f"🟢 Average Mood Score : {average:.1f}")
                print(f"{mood_label.split()[0]} Mood Interpretation : {mood_label.split(' ', 1)[1]}\n")
                print("Mood Scale:")
                print("   ".join(scale))
                print(arrow_line)
                print("     " * index + "Your Mood")
                print("\n" + interpretation[mood_label])
                print("──────────────────────────────────────────────\n")

                input("Press Enter to return to the main menu...")
        
        elif choice == '4':
            clear_screen()
            print("\n─────────────👤 Manage Account 👤─────────────\n")
            print('1. Edit Account')
            print('2. Delete Account')

            while True:
                sub_choice = input('\nEnter your choice (1-2): ').strip()
                if sub_choice == '1':
                    pass
                elif sub_choice == '2':
                    user_choice = input("\nAre you sure you want to delete your account? (yes/no): ").strip().lower()
                    if user_choice == 'yes':
                        entry = Entry("","","")
                        entry.set_user_id(user)
                        entry.delete_account()
                    else:
                        break
                else:
                    print("Error: Invalid option. Please choose a number between 1 and 2.")
                    continue

        elif choice == '5':
            print(f"\nThank you for using Mood Tracker, {user}. Goodbye!")
            quit()








