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
from question import Question

def main(): 

    # Initiate new session
    session = Session()
    # Welcome user
    session.welcome()


    print("--> Registration/Login process <--")
    print()
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
            print("Not a valid option")
            continue
    
    # modes available
    choosing_mode = True
    while choosing_mode:
        session.show_modes()
        mode = session.choose_mode()
        if mode == "question":
            # Add questions mode
            if session.question_mode(user.id) is False:
                continue
        elif mode == "statistics":
            # View statistics mode
            session.show_statistics(user.id)
        elif mode == "disable/enable questions":
            # Enable/disable questions mode
            session.enable_disable_mode() is False
        elif mode == "practice":
            # Practice mode
            session.practice_mode(user.id) is False
        elif mode == "test":
            # Test mode
            session.test_mode(user.id)
        else:
            print("Mode not available.")

        
    
    # Prompt user for choice
    # Validate input
    
    # TODO: USER CAN CHOOSE BETWEEN SEVERAL OPTIONS
    # ADD QUESTIONS
    # VIEW STATISTICS
    # DISABLE/ENABLE QUESTIONS
    # PRACTICE MODE
    # TEST MODE
    # PROFILE SELECT


if __name__ == "__main__":
    main()