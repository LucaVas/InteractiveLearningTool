# Session class responsible for welcoming and goodbying
import pyfiglet # type: ignore
from question import Question
from entry import Entry
import sys
import csv
from typing import Any
import json

class Session:

    app_name = "InteLTool"
    modes = {
        0 : "question",
        1 : "statistics",
        2 : "disable/enable questions",
        3 : "practice",
        4 : "test"
    }

    json_file = "../app.json"

    def __init__(self, mode=None) -> None:
        self.mode = mode

    @classmethod
    def welcome(cls) -> None:
        print()
        print(pyfiglet.figlet_format(f"Welcome to {cls.app_name}!", font='digital'))
        print()

    @classmethod
    def show_modes(cls) -> None:
        print()
        print("Available modes:")
        for idx,mode in enumerate(cls.modes.values()):
            print(f"{idx} - {mode.capitalize()} mode")

    @classmethod
    def choose_mode(cls):
        while True:
            choice = input("Select one of the available options (number), or enter 'q' to exit: ").lower().strip()

            if choice == "q":
                print()
                sys.exit("Thank you for using InteLTool. See ya!")

            try:
                choice = int(choice)
            except ValueError:
                print("Not a valid choice.")
                continue
            
            if choice in cls.modes.keys():
                print(f"{cls.modes[choice].capitalize()} mode selected.")
                return cls.modes[choice]
            else:
                print("Not a valid choice.")
                continue

    @staticmethod
    def question_mode(user_id: str) -> bool | None:
        print()
        print("--> Adding question mode: <--")
        print()

        adding_question = True
        while adding_question is True:
            question = Question()
            
            # clear out the question
            question.clear_question()

            question.show_types()
            question.select_question_type()

            question.add_content()
            question.add_answer()

            # show question type and content
            question.recap_question()

            # save question
            if (input("Do you want to save this question (Y/N)? ").strip().lower()) == "y":
                question.save_question(user_id)
                print("Question saved succesfully")
            else:
                print("Question not saved.")           
            

            if (input("Do you want to add another question (Y/N)? ").strip().lower()) == "y":
                continue
            else:
                return False
            
        return None
    
    @staticmethod
    def enable_disable_mode() -> None:
        print()
        print("--> Enable/disable question mode: <--")
        print()

        while True:
            prompt = input("Do you want to enable or disable a question (E/D)? ").strip().lower()
            
            if prompt == "e":
                id = Question.get_question_id()
                Question.enable(id)
                break
            elif prompt == "d":
                id = Question.get_question_id()
                Question.disable(id)  
                break      
            else:
                print("Not a valid choice.")
                continue
        return None
            
    @staticmethod
    def show_statistics(us_id: str) -> None:
        
        with open(Session.json_file, "r") as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

        for user in file_data["users"]:
            if user.get("userId") == us_id:
                for question in file_data["questions"]:
                    print("----------")
                    print(f"Question id: {question['questionId']}")
                    print(f"Type of question: {question['questionType']}")
                    print(f"Question status: {question['questionStatus']}")
                    print(f"Content: {question['questionContent']}")
                    if len(question["questionOptions"]) != 0:
                        print("Options: ")
                        for idx,opt in enumerate(question["questionOptions"]):
                            print(f" {idx+1} - {opt}")
                    for user in question["timesAnswered"]:
                        print(f"Times answered: {user[us_id]}")
                    for user in question["timesShown"]:
                        print(f"Times shown: {user[us_id]}")

    def check_answer(self, question_id: str, answer: int | str) -> Any:
        with open("../files/questions.csv", "r") as file:
            reader = csv.DictReader(file)
            for question in reader:
                if question['id'] == question_id:
                    if question['answer'] == answer:
                        return Entry(True, question['id'])
                    else:
                        return Entry(False, question['id'])
                else:
                    continue
        return None

    def practice_mode(self) -> None:
        
        practice_in_progress = True

        with open("../files/questions.csv", "r") as file:
            reader = csv.DictReader(file)
            while practice_in_progress:
                for question in reader:
                    print(f"ID: {question['id']}")
                    print(f"Question type: {question['type']}")
                    print(f"Question: {question['content']}")

                    

                    if question["type"].strip() == "quiz":
                        print("Options:")
                        for idx,opt in enumerate(eval(question['options'])):
                            print(f"    {idx + 1} - {opt}")

                        answer = input("What is the answer? ")

                        if not answer.isnumeric():
                            print("Not a valid option.")
                            continue

                        entry = self.check_answer(question['id'], str(int(answer)-1))
                    else:
                        answer = input("What is the answer? ")
                        entry = self.check_answer(question['id'], answer)

                    if entry.is_answered is True:
                        print("Correct answer!")
                    elif entry.is_answered is False:
                        print(f"Incorrect! The correct answer is: {question['answer']}")

                    entry.save_entry(question["id"], entry.is_answered)


        


