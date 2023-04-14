# InteLTool
## Interactive Learning Tool
### Description:
This is an interactive learning tool that allows users to create, practice, and test their knowledge using multiple-choice and freeform text questions. The program tracks user statistics and provide options to manage the questions. 

## Functionalities:
InteLTool provides several functionalities, among which you can find:
1. Adding questions.
2. Statistics viewing.
3. Disable/enable questions.
4. Practice mode.
5. Test mode.
6. Profile Select

**Adding Questions mode**

Users are able to add 2 types of questions: 
1. quiz questions: the user is required to choose one of the given answer options.
2. free-form text questions: the user is required to enter some text and compare it with the expected answer to determine whether it is correct
Questions are saved and stored for later use.
**Important**: A user cannot enter practice or test mode until at least 5 questions have been added. Also, questions are saved and remain available for all profiles (*see "Profile Select mode"*).

**Statistics viewing mode**

Users can print out all the questions currently saved. Each question lists:
1. unique ID number
2. status, i.e. whether the question is active or not
3. question text
4. number of times it was shown during practice or tests
5. percentage of times it was answered correctly

**Disable/Enable Questions mode**

Users can enable or disable questions by entering the ID of the question. The question information (question text, answer) is then shown and the user is asked asked to confirm whether they want to disable/enable it. Disabled questions do not appear in practice and test modes. 

**Practice mode**

In this mode, questions are given non-stop so that the user can practice. Questions are chosen in such a way that the questions that are answered correctly become less likely to appear, while questions that are answered incorrectly become more likely to appear. 

**Test mode**

In this mode, users can test their knowledge. Users first select the number of questions for the test, not more than the number of questions added. The questions get chosen fully randomly and each question appears only once in the test. At the end of the questions, the user is shown the score. The list of scores is saved in the results.txt file, with date and time added next to the score.

**Profile Select mode**

Users can select a profile which they want to play with. Each profile has individual statistics of how many times a question was answered correctly and individual probabilities of getting those questions in the practice mode. In the test mode, saved scores also say which profile achieved each of the scores there. **Important**: Questions are shared between all profiles.