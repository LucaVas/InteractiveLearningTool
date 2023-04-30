# Session class responsible for welcoming and goodbying
import pyfiglet # type: ignore
from question import Question
from user import User
import sys
import json
import random

class Session:

    app_name = "InteLTool"
    modes = {
        1 : "question",
        2 : "statistics",
        3 : "disable/enable questions",
        4 : "practice",
        5 : "test"
    }

    json_file = "../app.json"
    results_file = "../results.txt"

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
            print(f"{idx+1} - {mode.capitalize()} mode")

    @classmethod
    def choose_mode(cls) -> str:
        while True:
            choice = input("Select one of the available options (number), or enter 'q' to exit: ").lower().strip()

            if choice == "q":
                print()
                sys.exit("Thank you for using InteLTool. See ya!")

            try:
                int(choice)
            except ValueError:
                print("Not a valid choice.")
                continue
            
            if int(choice) in cls.modes.keys():
                print(f"{cls.modes[int(choice)].capitalize()} mode selected.")
                return cls.modes[int(choice)]
            else:
                print("Not a valid choice.")
                continue

    @staticmethod
    def question_mode(user: User) -> bool | None:
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
                question.save_question(user.id)
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
            if prompt not in ["e", "d"]:
                print("Not a valid choice")
                continue
            else:
                question = Question.get_question_id()
            
                if prompt == "e":
                    while True:
                        choice = input(f"Are you sure you want to enable the following question: \"{question['questionContent']}\" (Y/N)?" ).strip().lower()
                        if choice == "y":
                            Question.enable(question["questionId"])
                            return
                        elif choice == "n":
                            print("Question not enabled.")
                            return
                        else:
                            print("Not a valid option")
                            continue
                elif prompt == "d":
                    while True:
                        choice = input(f"Are you sure you want to disable the following question: \"{question['questionContent']}\" (Y/N)?" ).strip().lower()
                        if choice == "y":
                            Question.disable(question["questionId"])
                            return
                        elif choice == "n":
                            print("Question not disabled.")
                            return
                        else:
                            print("Not a valid option")
                            continue    
            
    @staticmethod
    def show_statistics(user: User) -> None:

        print()
        print("--> Statistics mode started <--")
        print()

        with open(Session.json_file, "r") as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
        
        for us in file_data["users"]:
            if us.get("userId") == user.id:
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
                    
                    times_answered = question["timesAnswered"][0][user.id]
                    times_shown = question["timesShown"][0][user.id]

                    if times_shown == 0:
                        score = 0.0
                    else:
                        score = times_answered / times_shown * 100


                    print(f"Answer score: {int(score)} %")

                    print(f"Times shown: {times_shown}")

        print()
        print("--> Statistics mode ended <--")
        print()

    def practice_mode(self, user: User) -> None:
        
        print()
        print("--> Practice mode started <--")
        print() 

        practice_in_progress = True

        # indexes of questions enabled
        available_questions_idx: list[int] = []


        with open(self.json_file, "r+") as file:
            file_data = json.load(file)

            for question in file_data["questions"]:
                if question["questionStatus"] == "enabled":
                    available_questions_idx.append(file_data["questions"].index(question))

            if len(available_questions_idx) < 5:
                print("You need to have at least 5 questions enabled to enter practice mode.")
            else:
                while practice_in_progress:
                    # get list of scores (weights)
                    weights = Question.weight_questions(file_data["questions"], available_questions_idx, user)
                    try:
                        weighted_list = random.choices(available_questions_idx, weights=weights, k=len(available_questions_idx))
                    # if none of the questions have yet been shown or answered
                    except ValueError:
                        weighted_list = available_questions_idx

                    for idx in weighted_list:
                        question = file_data["questions"][idx]

                        print(f"ID: {question['questionId']}")
                        print(f"Weight: {weights, weighted_list}")
                        print(f"Question: {question['questionContent']}")

                        if question["questionType"] == "quiz":
                            print("Options: ")
                            for idx,opt in enumerate(question["questionOptions"]):
                                print(f"    {idx+1} - {opt}")

                        answer = input("What is the answer? ")
                        if answer == question["questionAnswer"]:
                            print("Correct answer")
                            question["timesAnswered"][0][user.id] += 1
                            print("----------")
                        else:
                            print(f"Incorrect. The correct answer is: {question['questionAnswer']}\n")
                        
                        question["timesShown"][0][user.id] += 1

                        if not (input("Would you like to continue in practice mode? Press Enter to continue, or any other key to stop: ").lower().strip()):
                            print("----------")
                            continue
                        else:
                            practice_in_progress = False
                            break

                    # Sets file's current position at offset.
                    file.seek(0)
                    # convert back to json.
                    json.dump(file_data, file, indent = 4)


        print()
        print("--> Practice mode ended <--")
        print()

    def test_mode(self, user: User) -> None:
        """
            function which starts test mode and saves results in results.txt
        """
                
        print()
        print("--> Test mode started <--")
        print()

        test_in_progress = True
        answers = 0.0
        # Ask user how many question they want to play
        with open(self.json_file, "r+") as file:
            file_data = json.load(file)
            
            idx_of_questions_available: list[int] = []

            for question in file_data["questions"]:
                if question["questionStatus"] == "enabled":
                    idx_of_questions_available.append(file_data["questions"].index(question))


            if len(idx_of_questions_available) < 5:
                print("You need to have at least 5 questions enabled to enter test mode.")
            else:
                while test_in_progress:
                    num_of_questions = input(f"How many questions would you like to play with? Available: {len(idx_of_questions_available)} ")
                    if not num_of_questions:
                        print("Cannot be blank")
                        continue

                    try:
                        int(num_of_questions)
                    except TypeError:
                        print("Not a valid option")
                        continue
                    
                    if int(num_of_questions) > len(idx_of_questions_available):
                        print("Not enough questions")
                        continue
                    
                    
                    for idx in random.sample(idx_of_questions_available, int(num_of_questions)):
                        question = file_data["questions"][idx]
                        print(f"ID: {question['questionId']}")
                        print(f"Question: {question['questionContent']}")

                        answer: int | str

                        if question["questionType"] == "quiz":
                            print("Options: ")
                            for idx,opt in enumerate(question["questionOptions"]):
                                print(f"    {idx+1} - {opt}")

                            answer = int(input("What is the answer? "))
                        else:
                            answer = input(("What is the answer? "))

                        if answer == question["questionAnswer"]:
                            print("Correct answer")
                            question["timesAnswered"][0][user.id] += 1
                            answers += 1
                            print("----------")
                        else:
                            print(f"Incorrect. The correct answer is: {question['questionAnswer']}")
                            print("----------")
                        
                        question["timesShown"][0][user.id] += 1
                    
                    test_in_progress = False


                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent = 4)

        if answers != 0.0: 
            score = (answers / int(num_of_questions)) * 100

            results_output = [
                f"Questions shown: {num_of_questions}",
                f"Questions answered correctly: {int(answers)}",
                f"You scored: {score:.2f} %\n"
            ]

            results_to_file = [
                f"User ID: {user.id}",
                f"Questions shown: {num_of_questions}",
                f"Questions answered correctly: {int(answers)}",
                f"Score: {score:.2f} %",
                "\n"
            ]

            with open(self.results_file, "a") as file:
                file.write("\n".join(results_to_file))


            print()
            print("Results: ")
            print("\n".join(results_output))

        print()
        print("--> Test mode ended <--")
        print()
