"""
Name: InteLTool
Author: Luca Vassos
Date: 2023/04/15

InteLTool is an interactive learning tool that allows users to create, 
practice, and test their knowledge using multiple-choice and freeform text questions.
If you wanna know more, please refer to README file.
"""

from user import User
from session import Session
from termcolor import colored

PASS_CLR = "green"
WARNING_CLR = "yellow"
ERROR_CLR = "red"
MODE_CLR = "blue"

def main() -> None:

    # Initiate new session
    session = Session()
    # Welcome user
    session.welcome()

    print(colored("--> Registration/Login process <--\n", MODE_CLR))
    # Initialize new user
    user = User()

    # New user?
    while True:
        res = input("Are you a new user? (Y/N) ").strip().lower()
        if res == "y":
            user.register_user()
            break
        elif res == "n":
            user.login()
            break
        else:
            print(colored("Not a valid option", WARNING_CLR))
            continue

    # modes available
    choosing_mode = True
    while choosing_mode:
        session.show_modes()
        mode = session.choose_mode()
        if mode == "question":
            # Add questions mode
            if session.question_mode(user) is False:
                continue
        elif mode == "statistics":
            # View statistics mode
            session.show_statistics(user)
        elif mode == "disable/enable questions":
            # Enable/disable questions mode
            session.enable_disable_mode()
        elif mode == "practice":
            # Practice mode
            session.practice_mode(user)
        elif mode == "test":
            # Test mode
            session.test_mode(user)
        elif mode == "reset questions":
            # Reset questions statistics for user
            session.reset_questions_mode(user)
        else:
            print(colored("Mode not available.", ERROR_CLR))


if __name__ == "__main__":
    main()
