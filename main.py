from user import account_management
from mood import main_menu

def main():
    user = account_management()
    main_menu(user)
    
if __name__ == '__main__':
    main()