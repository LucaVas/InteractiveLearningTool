import csv
import pandas as pd
import uuid
import json
    
class Question:

    types = {
        0: "quiz",
        1: "free-form"
    }

    json_file = "../app.json"

    def __init__(self, type=None, content=None, options=[]) -> None:
        self.type = type
        self.content = content
        self.options = options
        self.number_of_options = 0
        self.answer = None
        self.status = "enabled"
        self.id = str(uuid.uuid1())


    def clear_question(self) -> None:
        """
            function that clears the options and answer
        """
        self.options = []
        self.answer = None


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

    def add_answer(self):
        print("What is the correct answer to this question? ", end=" ")

        if self.type == "quiz":
            while True:
                answer = input("Enter the option number: ")

                try:
                    answer = int(answer)
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
        """
            Function which saves question to json
        """
        question_entry = {
            "questionId": self.id,
            "questionStatus": self.status,
            "questionType": self.type,
            "questionContent": self.content,
            "questionOptions": self.options,
            "questionAnswer": self.answer,
            "timesAnswered": [
                {user_id: 0}
            ],
            "timesShown": [
                {user_id: 0}
            ]
        }
        
        with open(self.json_file,'r+') as file:
          # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["questions"].append(question_entry)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
        

    @staticmethod
    def get_question_id():
        while True:
            id = input("Enter the ID of the question: ").strip()
            if not id:
                print("Id cannot be blank")
                continue
            
            with open(Question.json_file, "r") as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                # Join new_data with file_data inside emp_details
                for question in file_data["questions"]:
                    if question.get("questionId") == id:
                        return id
                    else:
                        continue
            
            print("Question not found")
            continue
         

    @staticmethod
    def disable(id) -> None:
        """
            Function which disables a question by id
        """
        with open(Question.json_file, "r+") as file:
            file_data = json.load(file)
            for question in file_data["questions"]:
                if question.get("questionId") == id:
                    question["questionStatus"] = "disabled"
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
            file.truncate()
        
        print(f"Question with id: {id} is now disabled.")   

    @staticmethod
    def enable(id) -> None:
        """
            function which enables a question by id
        """
        with open(Question.json_file, "r+") as file:
            file_data = json.load(file)
            for question in file_data["questions"]:
                if question.get("questionId") == id:
                    question["questionStatus"] = "enabled"
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
            file.truncate()
        
        print(f"Question with id: {id} is now enabled.")       
    
    @classmethod
    def show_types(cls):
        print("Possible types of questions: ")
        for idx,type in enumerate(cls.types.values()):
            print(f"{idx} - {type} question")

    