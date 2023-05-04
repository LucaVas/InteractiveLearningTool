import uuid
import json
from termcolor import colored
import re
from config import json_file

PASS_CLR = "green"
WARNING_CLR = "yellow"
ERROR_CLR = "red"

# User class is responsible for creating, updating and deleting new users
class User:
    def __init__(self, username=None, is_user=False) -> None:
        self.username = username
        self.id = str(uuid.uuid1())
        self.is_user = is_user

    def register_user(self) -> None:
        """
        Function which registers a new user
        """
        registration_in_progress = True
        while registration_in_progress:
            username = input("Enter a new username: ")
            if not username.strip():
                print(colored("Username cannot be blank.", WARNING_CLR))
                continue
            elif self.validate_username(username) is False:
                print(colored("Username must be lowercase and contain at least 1 digit.", WARNING_CLR))
                continue
            else:
                self.username = username
                break

        self.save_new_user()
        self.add_user_to_questions()
        self.welcome_user(False)

    def validate_username(self, username: str) -> bool:
        regex = r"^(?:[0-9]+[a-z]|[a-z]+[0-9])[a-z0-9]*$"
        if re.fullmatch(regex, username) is None:
            return False
        else:
            return True

    def save_new_user(self) -> None:
        """
        Function which saves a new user to the json file
        """

        user_entry = {
            "userId": self.id,
            "userName": self.username,
        }

        with open(json_file, "r+") as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["users"].append(user_entry)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)

    def add_user_to_questions(self) -> None:
        """
        function which adds new user's information to the previously questions added (times shown and times answered)
        """
        with open(json_file, "r+") as file:
            file_data = json.load(file)
            for question in file_data["questions"]:
                question["timesAnswered"][0].update({self.id: 0})
                question["timesShown"][0].update({self.id: 0})
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def login(self) -> None:
        """
        Function which set current user to existing user, if found
        """
        with open(json_file, "r") as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

        while True:
            name = input("Enter your username: ").strip().lower()

            for user in file_data["users"]:
                if user.get("userName") == name:
                    self.username = user["userName"]
                    self.id = user["userId"]
                    self._is_user = True
                    self.welcome_user(True)
                    return
                else:
                    continue
            else:
                print((colored("User not found", ERROR_CLR)))
                continue

    def welcome_user(self, is_new_user: bool) -> None:
        """
        Function which welcome user; if new, confirms registration; if existing, welcomes back
        """

        if is_new_user is True:
            print(colored(f"Welcome back, {self.username}!", PASS_CLR))
        else:
            print(colored(f"Registration succesful. Welcome, {self.username}!", PASS_CLR))
