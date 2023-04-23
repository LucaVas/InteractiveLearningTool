import csv

# User class is responsible for creating, updating and deleting new users
class User:
    def __init__(self, username=None, user_id=0, is_user=False) -> None:
        self._username = username
        self._user_id = user_id
        self._is_user = is_user

    """
        Seetters and getters
    """
    @property
    def username(self) -> str:
        return self._username

    # setter to change username
    @username.setter
    def username(self, name: str) -> None:
        # check input
        if not name:
            raise ValueError("Username invalid!")
        self._username = name
    
    @property
    def id(self) -> int:
        return self._user_id
    
    @id.setter
    def id(self, number: int) -> None:
        self._user_id = number

    """
        Registration of new user
    """        

    def register_user(self):
        self.username = input("Enter a new username: ")
        self.id = self.create_new_id()
        self.save_new_user()
        print("Registration succesful!")
        self.welcome_new_user()    
        
    def welcome_new_user(self) -> None:
        print(f"Welcome, {self.username}!")
    
    def create_new_id(self) -> int:
        users = list(csv.reader(open("../users.csv")))
        if not users:
            return 0
        else:
            return int(users[-1][0]) + 1

    def save_new_user(self):
        with open("../users.csv", "a", newline='') as file:
            fieldnames = ['user_id', 'username']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'user_id': self.id, 'username': self.username})

    """
        Login of existing user
    """

    def login(self):
        while True:
            name = input("Enter your username: ").strip().lower()
            if self.find_user(name) is False:
                print("User not found")
                continue
            else:
                self._is_user = True
                self.username = name
                self.id = self.get_user_id()
                self.welcome_current_user()
                break


    def welcome_current_user(self) -> None:
        print(f"Welcome back, {self.username}.")


    def find_user(self, name) -> bool:
        # check if user exists
        with open("../users.csv", 'r') as file:
            reader = csv.DictReader(file)
            for line in reader:
                if line["username"] == name:
                    return True
                else:
                    continue
            return False


    def get_user_id(self) -> str | None:
        with open("../users.csv", "r") as file:
            reader = csv.DictReader(file)
            for line in reader:
                if line["username"] == self.username:
                    return line["user_id"]   
                
        return None



