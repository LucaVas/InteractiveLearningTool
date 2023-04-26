import csv
import uuid
import json

# User class is responsible for creating, updating and deleting new users
class User:
    def __init__(self, username=None, is_user=False) -> None:
        self.username = username
        self.id = str(uuid.uuid1())
        self.is_user = is_user
        self.json_file = "../app.json"
    
    
    def register_user(self) -> None:
        """
            Function which registers a new user
        """
        registration_in_progress = True
        while registration_in_progress:
            username = input("Enter a new username: ")
            if not username.strip():
                print("Username cannot be blank.")
                continue
            else:
                self.username = username
                break

        self.save_new_user()
        self.welcome_user(False)    
        
    def save_new_user(self) -> None:
        """
            Function which saves a new user to the json file
        """

        user_entry = {
            "userId": self.id,
            "userName": self.username,
        }
        
        with open(self.json_file,'r+') as file:
          # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["users"].append(user_entry)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)

    """
        Login of existing user
    """

    def login(self) -> None:
        """
            Function which set current user to existing user, if found
        """
        while True:
            name = input("Enter your username: ").strip().lower()
            if self.find_user(name) is False:
                print("User not found")
                continue
            else:
                user_dict = self.find_user(name)
                self._is_user = True
                self.username = name
                self.id = user_dict.get("userId")
                print(self.welcome_user(True))
                break


    def find_user(self, name) -> dict[str, str] | bool:
        """
            Function that checks if user with same username is already registered
        """
        with open(self.json_file,'r') as file:
          # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            for user in file_data["users"]:
                if user.get("userName") == name:
                    return user
                else:
                    continue
                
            return False
        
    def welcome_user(self, is_new_user: bool) -> str:
        """
            Function which welcome user; if new, confirms registration; if existing, welcomes back
        """

        if is_new_user is True:
            return f"Welcome back, {self.username}!"
        else:
            return f"Registration succesfull. Welcome, {self.username}!"

