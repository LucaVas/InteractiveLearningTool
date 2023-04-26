import csv
import pandas as pd
import uuid
    
class Question:

    types = {
        0: "quiz",
        1: "free-form"
    }

    def __init__(self, type=None, content=None, options=[]) -> None:
        self._type = type
        self._content = content
        self._options = options
        self._number_of_options = 0
        self._answer = None
        self._status = "enabled"
        self._id = None

    """
        Setters and getters
    """
    @property
    def content(self):
        return self._content
                
    @content.setter
    def content(self, cont):
        self._content = cont
                
    @property
    def type(self):
        return self._type
                    
    @type.setter
    def type(self, t):
        self._type = t

    @property
    def options(self):
        return self._options
    
    @options.setter
    def options(self, lst):
        self._options = lst

    def clear_options(self) -> None:
        """
            function that clears the options once the quiz question is saved
        """
        self.options = []

    @property
    def number_of_options(self):
        return self._number_of_options
    
    @number_of_options.setter
    def number_of_options(self, num):
        if 1 < num < 6:
            self._number_of_options = num

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status: str):
        self._status = status

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, n):
        self._id = n

    @property
    def answer(self):
        return self._answer
    
    @answer.setter
    def answer(self, a) -> None:
        self._answer = a
    

    def set_id(self) -> None:
        self.id = uuid.uuid1()


    def select_question_type(self):
            while True:
                choice = input("Select the type of question: ").strip()
                try:
                    choice = int(choice)
                except ValueError:
                    print("Not a valid choice.")
                    continue

                if choice in Question.types.keys():
                    self.type = Question.types[choice]
                    break
                else:
                    print("Not a valid choice.")
                    continue

    def add_content(self):
              
        if self.type == "quiz":
            self.content = input("Enter your quiz question: ").strip()

            while True:
                num_of_options = input("Choose the number of options between 2 and 5: ")
                try:
                    self.number_of_options = int(num_of_options)
                except TypeError:
                    print("Not a valid number.")
                    continue

                if self.number_of_options != 0:
                    break
                else:
                    continue
            
            for i in range(self.number_of_options):
                while True:
                    opt = input(f"Enter option {i+1}: ")
                    if not opt:
                        print("The option cannot be blank.")
                        continue
                    else:
                        self.options.append(opt)
                        break
    
        else:
            self.content = input("Enter your free-form question content: ").strip()

    def clear_answer(self) -> None:
        """
            function that clears out the answer for a new question
        """
        self.answer = None

    def add_answer(self):
        print("What is the correct answer to this question? ", end=" ")

        if self.type == "quiz":
            while True:
                answer = input("Enter the option number: ")

                try:
                    answer = int(answer) - 1
                except TypeError:
                    print("Not a valid option.")
                    continue

                if answer not in range(self.number_of_options):
                    print("Not one of the options available")
                    continue

                self.answer = answer
                break
        else:
            while True:
                answer = input("Enter a free-text answer: ")

                if not answer:
                    print("Answer cannot be blank.")
                    continue

                self.answer = answer
                break


    def recap_question(self):
        print("Question created!")
        print(f"    Type of question: {self.type}")
        print(f"    Question content: {self.content}")
        if self.type == "quiz":
            print(f"    Options:")
            for idx,opt in enumerate(self.options):
                print(f"        {idx+1} - {opt}")
            print(f"    Answer: {self.answer + 1}")
        else:
            print(f"    Answer: {self.answer}")


    def save_question(self, user_id):  
        
        choice = input("Would you like to save this question (Y/N)? ").lower().strip()
        if choice == "y":
            self.set_id()
            with open("../files/questions.csv", "a", newline='') as file:
                fieldnames = ["id", "type", "content", "options", "status", "answer", "times_answered" ,"times_shown", "user_id"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if self.type == "free-form":
                    writer.writerow({'id': self.id, "type": self.type, "content": self.content, "options": "", "status": self.status, "answer": self.answer, "times_answered": 0,"times_shown": 0, "user_id": user_id})
                else:
                    writer.writerow({'id': self.id, "type": self.type, "content": self.content, "options": self.options, "status": self.status, "answer": self.answer, "times_answered": 0,"times_shown": 0, "user_id": user_id})

            print("Question saved succesfully!")
            
        else:
            print("Question not saved.")


    @staticmethod
    def get_question_by_id():
        while True:
            id = input("Enter the ID of the question: ").strip()
            try:
                int(id)
            except TypeError:
                print("Not a valid question")
                continue
            
            with open("../files/questions.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["id"] == id:
                        return id
                    else:
                        continue
            print("Question not found!")
            continue
                    

    @staticmethod
    def disable(id):
        
        file = pd.read_csv("../files/questions.csv")
        file.head(3)
        file.at[int(id), "status"]="disabled"
        file.to_csv("../files/questions.csv", index=False)
        print(f"Question with id: {id} is now disabled.")   
        return False

    @staticmethod
    def enable(id):

        file = pd.read_csv("../files/questions.csv")
        file.head(3)
        file.at[int(id), "status"]="enabled"
        file.to_csv("../files/questions.csv", index=False)
        print(f"Question with id: {id} is now enabled.")      
        return False      
    
    @classmethod
    def show_types(cls):
        print("Possible types of questions: ")
        for idx,type in enumerate(cls.types.values()):
            print(f"{idx} - {type} question")

    