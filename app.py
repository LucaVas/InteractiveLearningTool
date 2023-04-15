"""
Name: InteLTool
Author: Luca Vassos
Date: 2023/04/15

InteLTool is an interactive learning tool that allows users to create, 
practice, and test their knowledge using multiple-choice and freeform text questions.
If you wanna know more, please refer to README file.
"""

import csv

# User class is responsible for creating, updating and deleting new users
class User:
    def __init__(self, username=None, user_id=0, is_user=False) -> None:
        self._username = username
        self._user_id = user_id
        self._is_user = is_user

    # getter to get username
    @property
    def username(self) -> str:
        return self._username

    # setter to change username
    @username.setter
    def username(self, name: str) -> bool | None:
        # check input
        if not name:
            raise ValueError("Username invalid!")
        self._username = name

    def find_user(self, name) -> bool:
        # check if user exists
        with open("users.csv", 'r') as file:
            reader = csv.DictReader(file)
            for line in reader:
                if line["username"] == name:
                    self._is_user = True
                    return True
                else:
                    continue
            return False

    def welcome_current_user(self) -> None:
        print(f"Welcome back, {self._username}. Your id is {self._user_id}")
    
    def welcome_new_user(self) -> None:
        print(f"Welcome, {self._username}. Your id is {self._user_id}")

    def create_new_id(self) -> None:
        users = list(csv.reader(open("users.csv")))
        if not users:
            return 0
        else:
            return int(users[-1][0]) + 1

    def get_user_id(self) -> int:
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for line in reader:
                if line["username"] == self._username:
                    return line["user_id"]


    @property
    def id(self) -> int:
        return self._user_id
    
    @id.setter
    def id(self, number: int) -> None:
        self._user_id = number
    


# Session class responsible for welcoming and goodbying
class Session:

    app_name = "InteLTool"

    def __init__(self) -> None:
        pass

    @classmethod
    def welcome(cls) -> None:
        print(f"Welcome to {cls.app_name}!")



def main(): 

    # Initiate new session
    session = Session()
    # Welcome user
    session.welcome()

    # Initialize new user
    user = User()
    # New user?
    res = input("Are you a new user? (Y/N) ").strip().lower()
    if res == "y":
        user.username = input("Enter a new username: ")
        new_id = user.create_new_id()
        user.id = new_id
        user.welcome_current_user()
    elif res == "n":
        while True:
            name = input("Enter your username: ")
            if user.find_user(name) is False:
                print("User not found")
                continue
            else:
                user.username = name
                user.id = user.get_user_id()
                user.welcome_current_user()
                break


            


    
    # Prompt user for choice
    # Validate input
    
    # TODO: USER CAN CHOOSE BETWEEN SEVERAL OPTIONS
    # ADD QUESTIONS
    # VIEW STATISTICS
    # DISABLE/ENABLE QUESTIONS
    # PRACTICE MODE
    # TEST MODE
    # PROFILE SELECT


def welcome_user():
    ...

if __name__ == "__main__":
    main()