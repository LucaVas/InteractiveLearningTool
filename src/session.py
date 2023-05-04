# Session class responsible for welcoming and goodbying
import pyfiglet  # type: ignore
from question import Question 
from user import User
import sys
import json
import random
from config import json_file, results_file, app_name
from termcolor import colored

PASS_CLR = "green"
WARNING_CLR = "yellow"
ERROR_CLR = "red"
MODE_CLR = "blue"


class Session:

    modes = {
        1: "question",
        2: "statistics",
        3: "disable/enable questions",
        4: "practice",
        5: "test",
        6: "reset questions",
    }


    def __init__(self, mode=None) -> None:
        self.mode = mode

    @classmethod
    def welcome(cls) -> None:
        """
            function which welcomes the user to inteltool
        """
        print(pyfiglet.figlet_format(f"\nWelcome to {app_name}!", font="digital"))

    @classmethod
    def show_modes(cls) -> None:
        """
            function which prints out to user the available
        """
        print("\nAvailable modes:")
        for idx, mode in enumerate(cls.modes.values()):
            print(f"{idx+1} - {mode.capitalize()} mode")

    @classmethod
    def choose_mode(cls) -> str:
        """
            function which asks user to choose one of the available options
        """
        while True:
            choice = (
                input(
                    "Select one of the available options (number), or enter 'q' to exit: "
                )
                .lower()
                .strip()
            )

            if choice == "q":
                print()
                sys.exit(colored("Thank you for using InteLTool. See ya!", MODE_CLR))

            try:
                int(choice)
            except ValueError:
                print(colored("Not a valid choice.", ERROR_CLR))
                continue

            if int(choice) in cls.modes.keys():
                print(colored(f"{cls.modes[int(choice)].capitalize()} mode selected.", PASS_CLR))
                return cls.modes[int(choice)]
            else:
                print(colored("Not a valid choice.", ERROR_CLR))
                continue

    @staticmethod
    def question_mode(user: User) -> bool | None:
        """
            function which initializes and processes the mode responsible for adding questions
        """
        print(colored("\n--> Adding question mode started <--\n", MODE_CLR))

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
            if (
                input("Do you want to save this question (Y/N)? ").strip().lower()
            ) == "y":
                question.save_question()
                print(colored("Question saved succesfully", PASS_CLR))
            else:
                print(colored("Question not saved.", ERROR_CLR))

            if (
                input("Do you want to add another question (Y/N)? ").strip().lower()
            ) == "y":
                continue
            else:
                print(colored("\n--> Adding question mode finished <--\n", MODE_CLR))
                return False

        return None

    @staticmethod
    def enable_disable_mode() -> None:
        """
            function which initializes and process the mode responsible for enabling and disabling questions
        """
        print(colored("\n--> Enable/disable question mode started <--\n", MODE_CLR))

        while True:
            prompt = (
                input("Do you want to enable or disable a question (E/D)? ")
                .strip()
                .lower()
            )
            if prompt not in ["e", "d"]:
                print(colored("Not a valid choice", WARNING_CLR))
                continue
            else:
                question = Question.get_question_id()

                if prompt == "e":
                    while True:
                        choice = (
                            input(
                                f"Are you sure you want to enable the following question: \"{question['questionContent']}\" (Y/N)? "
                            )
                            .strip()
                            .lower()
                        )
                        if choice == "y":
                            Question.enable(question["questionId"])
                            break
                        elif choice == "n":
                            print(colored("Question not enabled.", PASS_CLR))
                            break
                        else:
                            print(colored("Not a valid option", WARNING_CLR))
                            break
                elif prompt == "d":
                    while True:
                        choice = (
                            input(
                                f"Are you sure you want to disable the following question: \"{question['questionContent']}\" (Y/N)?"
                            )
                            .strip()
                            .lower()
                        )
                        if choice == "y":
                            Question.disable(question["questionId"])
                            break
                        elif choice == "n":
                            print(colored("Question not disabled.", PASS_CLR))
                            break
                        else:
                            print(colored("Not a valid option", WARNING_CLR))
                            continue
                break

        print(colored("\n--> Enable/disable question mode ended <--\n", MODE_CLR))

    @staticmethod
    def show_statistics(user: User) -> None:
        """
            function which initializes and processes the mode responsible for outputting statistics to the user.
            Statistics are shown based only for the specific user results.
        """

        print(colored("\n--> Statistics mode started <--\n", MODE_CLR))

        with open(json_file, "r") as file:
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
                        for idx, opt in enumerate(question["questionOptions"]):
                            print(f" {idx+1} - {opt}")

                    times_answered = question["timesAnswered"][0][user.id]
                    times_shown = question["timesShown"][0][user.id]

                    if times_shown == 0:
                        score = 0.0
                    else:
                        score = times_answered / times_shown * 100

                    print(f"Answer score: {int(score)} %")

                    print(f"Times shown: {times_shown}")

        print(colored("\n--> Statistics mode ended <--\n", MODE_CLR))

    def practice_mode(self, user: User) -> None:
        """
            function which initializes and processes the mode responsible for allowing the user to practice
            questions are prompted out in random weighted choice order
            user can stops at any time the practice by entering an input different than enter
        """

        print(colored("\n--> Practice mode started <--\n", MODE_CLR))

        practice_in_progress = True

        # indexes of questions enabled
        available_questions_idx: list[int] = []

        with open(json_file, "r+") as file:
            file_data = json.load(file)

            for question in file_data["questions"]:
                if question["questionStatus"] == "enabled":
                    available_questions_idx.append(
                        file_data["questions"].index(question)
                    )

            if len(available_questions_idx) < 5:
                print(
                    colored("You need to have at least 5 questions enabled to enter practice mode.", WARNING_CLR)
                )
            else:
                while practice_in_progress:
                    # get list of scores (weights)
                    weights = Question.weight_questions(
                        file_data["questions"], available_questions_idx, user
                    )
                    try:
                        weighted_list = random.choices(
                            available_questions_idx,
                            weights=weights,
                            k=len(available_questions_idx),
                        )
                    # if none of the questions have yet been shown or answered
                    except ValueError:
                        weighted_list = available_questions_idx

                    for idx in weighted_list:
                        question = file_data["questions"][idx]

                        print(f"ID: {question['questionId']}")
                        print(f"Question: {question['questionContent']}")

                        if question["questionType"] == "quiz":
                            print("Options: ")
                            for idx, opt in enumerate(question["questionOptions"]):
                                print(f"    {idx+1} - {opt}")

                        answer = input("What is the answer? ")
                        if answer == question["questionAnswer"]:
                            print(colored("Correct answer", PASS_CLR))
                            question["timesAnswered"][0][user.id] += 1
                            print("----------")
                        else:
                            print(
                                colored(f"Incorrect. The correct answer is: {question['questionAnswer']}\n", ERROR_CLR)
                            )

                        question["timesShown"][0][user.id] += 1

                        if not (
                            input(
                                "Would you like to continue in practice mode? Press Enter to continue, or any other key & enter to stop: "
                            )
                            .lower()
                            .strip()
                        ):
                            print("----------")
                            continue
                        else:
                            practice_in_progress = False
                            break

                    # Sets file's current position at offset.
                    file.seek(0)
                    # convert back to json.
                    json.dump(file_data, file, indent=4)

        print(colored("\n--> Practice mode ended <--", MODE_CLR))

    def test_mode(self, user: User) -> None:
        """
        function which initializes and processes the mode responsible for testing, and saves results in results.txt
        """

        print(colored("\n--> Test mode started <--\n", MODE_CLR))

        test_in_progress = True
        answers = 0.0
        # Ask user how many question they want to play
        with open(json_file, "r+") as file:
            file_data = json.load(file)

            idx_of_questions_available: list[int] = []

            for question in file_data["questions"]:
                if question["questionStatus"] == "enabled":
                    idx_of_questions_available.append(
                        file_data["questions"].index(question)
                    )

            if len(idx_of_questions_available) < 5:
                print(
                    colored("You need to have at least 5 questions enabled to enter test mode.", WARNING_CLR)
                )
            else:
                while test_in_progress:
                    num_of_questions = input(
                        f"How many questions would you like to play with? (Available: {len(idx_of_questions_available)})   "
                    )
                    if not num_of_questions:
                        print(colored("Cannot be blank", WARNING_CLR))
                        continue

                    try:
                        int(num_of_questions)
                    except TypeError:
                        print(colored("Not a valid option", WARNING_CLR))
                        continue

                    if int(num_of_questions) > len(idx_of_questions_available):
                        print(colored("Not enough questions", WARNING_CLR))
                        continue

                    for idx in random.sample(
                        idx_of_questions_available, int(num_of_questions)
                    ):
                        question = file_data["questions"][idx]
                        print(f"\nID: {question['questionId']}")
                        print(f"Question: {question['questionContent']}")

                        answer: int | str

                        if question["questionType"] == "quiz":
                            print("Options: ")
                            for idx, opt in enumerate(question["questionOptions"]):
                                print(f"    {idx+1} - {opt}")

                            answer = input("What is the answer? Select a number: ")
                        else:
                            answer = input(("What is the answer? (Careful, it's case sensitive) : "))

                        if answer == question["questionAnswer"]:
                            print(colored("Correct answer", PASS_CLR))
                            question["timesAnswered"][0][user.id] += 1
                            answers += 1
                            print("----------")
                        else:
                            print(
                                colored(f"Incorrect. The correct answer is: {question['questionAnswer']}", ERROR_CLR)
                            )
                            print("----------")

                        question["timesShown"][0][user.id] += 1

                    test_in_progress = False

                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent=4)

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
                f"Score: {score:.2f} %#\n",
                "\n",
                "Your results are saved in results.txt for future consultation.\n"
            ]

            with open(results_file, "a") as file:
                file.write("\n".join(results_to_file))

            print()
            print("Results: ")
            print("\n".join(results_output))

        print(colored("\n--> Test mode ended <--\n", MODE_CLR))

    def reset_questions_mode(self, user: User) -> None:
        """
            function which initializes and processes the mode responsbile for resetting user's statistics
            only the specific user's (who is using this mode) statistics are resetted
        """
        print(colored("\n--> Reset questions mode started <--\n", MODE_CLR))

        print(
            "The reset questions mode allows you to reset all statistics of questions answered related to your OWN user. All other users' statistics remain the same."
        )
        choice = (
            input(
                "If you wish to continue and reset your user's statistics, press Enter - otherwise, press any other key, and enter: "
            )
            .lower()
            .strip()
        )
        if not choice:
            if (
                input(
                    colored(f"Are you sure you want to reset your ({user.username}) statistics? (Y/N) ", WARNING_CLR)
                )
                .lower()
                .strip()
            ) == "y":
                with open(json_file, "r+") as file:
                    file_data = json.load(file)

                    for question in file_data["questions"]:
                        question["timesAnswered"][0][user.id] = 0
                        question["timesShown"][0][user.id] = 0

                    file.seek(0)
                    json.dump(file_data, file, indent=4)

                    print(colored("Your statistics have been reset succesfully.", PASS_CLR))
            else:
                print(colored("Your statistics have not been reset.", PASS_CLR))
        else:
            print(colored("Your statistics have not been reset.", PASS_CLR))

        print(colored("\n--> Reset questions mode ended <--\n", MODE_CLR))
