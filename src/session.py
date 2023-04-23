# Session class responsible for welcoming and goodbying
import pyfiglet # type: ignore
from question import Question
from entry import Entry
import sys
import csv
from typing import Optional

class Session:

    app_name = "InteLTool"
    modes = {
        0 : "question",
        1 : "statistics",
        2 : "disable/enable questions",
        3 : "practice",
        4 : "test"
    }

    def __init__(self, mode=None) -> None:
        self.mode = mode

    @classmethod
    def welcome(cls) -> None:
        print()
        print(pyfiglet.figlet_format(f"Welcome to {cls.app_name}!", font='digital'))
        print()

    @classmethod
    def show_modes(cls):
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
    def question_mode(user_id):
        print()
        print("--> Adding question mode: <--")
        print()

        adding_question = True
        while adding_question is True:
            question = Question()
            question.show_types()
            question.select_question_type()
            question.add_content()
            question.add_answer()

            # show question type and content
            question.recap_question()

            # save question
            question.save_question(user_id)

            if (input("Do you want to add another question (Y/N)? ").strip().lower()) == "y":
                continue
            else:
                adding_question = False
                return False
    
    @staticmethod
    def enable_disable_mode():
        print()
        print("--> Enable/disable question mode: <--")
        print()

        while True:
            prompt = input("Do you want to enable or disable a question (E/D)? ").strip().lower()
            
            if prompt == "e":
                id = Question.get_question_by_id()
                Question.enable(id)
                break
            elif prompt == "d":
                id = Question.get_question_by_id()
                Question.disable(id)  
                break      
            else:
                print("Not a valid choice.")
                continue
            
    @staticmethod
    def show_statistics(us_id):
        stats = {}

        # id,is_answered,question_id
        with open("../statistics.csv") as file:
            reader = csv.DictReader(file)
            for line in reader:
                if line["question_id"] in stats:
                    if line["is_answered"] is True:
                        stats[line["question_id"]]["answers"] += 1
                    else:
                        stats[line["question_id"]]["answers"] += 1
                    stats[line["question_id"]]["shown"] += 1
                    
                else:
                    if line["is_answered"] is True:
                        stats[line["question_id"]] = {"answers" : 1, "shown" : 1}
                    else:
                        stats[line["question_id"]] = {"answers" : 0, "shown" : 1}


        # id,type,content,options,status,user_id
        with open("../questions.csv") as file:
            reader = csv.DictReader(file)
            for line in reader:
                if line["user_id"] == str(us_id):
                        print("----------")
                        print(f"Question id: {line['id']}")
                        print(f"Type of question: {line['type']}")
                        print(f"Question status: {line['status']}")
                        print(f"Content: {line['content']}")
                        if line["options"]:
                            print(f"Options: {line['options']}")
                        if stats.get(line['id']) is not None:
                            print(f"Times answered: {stats.get(line['id'])['answers']}")
                            print(f"Times shown: {stats.get(line['id'])['shown']}")
                        else:
                            print(f"Times answered: 0")
                            print(f"Times shown: 0")
                        print("----------")

    def check_answer(self, question_id: str, answer: str) -> bool | Entry:
        with open("../questions.csv", "r") as file:
            reader = csv.DictReader(file)
            for question in reader:
                if question['id'] == question_id:
                    if question['answer'] == answer:
                        return Entry(True, question['id'])
                    else:
                        return Entry(False, question['id'])
                else:
                    continue
        return True

    def practice_mode(self):
        
        practice_in_progress = True

        with open("../questions.csv", "r") as file:
            reader = csv.DictReader(file)
            while practice_in_progress:
                for question in reader:
                    print(f"ID: {question['id']}")
                    print(f"Question type: {question['type']}")
                    print(f"Question: {question['content']}")
                    if question["type"] == "quiz":
                        print(f"{question['options']}")

                    answer = input("What is the answer? ")

                    entry = self.check_answer(question['id'], answer)
                    if entry.is_answered is True:
                        print("Correct answer!")
                    else:
                        print(f"Incorrect! The correct answer is: {question['answer']}")
                    entry.save_entry()

        


