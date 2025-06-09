import csv
import os
from user import User
from utils import cipher_suite
from datetime import datetime

class Entry:
    def __init__(self, mood, tags, message=""):
        self.mood = mood
        self.tags = tags
        self.message = message
        now = datetime.now()
        self.user_id = None

        date_str = now.strftime("%b %d, %Y - %I:%M %p")
        date_str = date_str.replace(" 0", " ")       
        date_str = date_str.lstrip("0")               
        self.date = date_str.lower().replace("am", "am").replace("pm", "pm")
        
    def set_user_id(self, obj):
        self.user_id = obj.get_user_id()
    
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
                input("Press Enter to return to the main menu...")
        
        def view_specfic_entry(self):
            pass

        def view_all(self):
            pass

        def get_average_mood(self):
            pass