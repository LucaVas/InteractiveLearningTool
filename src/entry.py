import csv
import pandas as pd

class Entry():
    def __init__(self, is_answered: bool, question_id: str) -> None:
        self._id = 0
        self._is_answered = is_answered
        self._question_id = question_id

    @property 
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, n: int) -> None:
        self._id = n
    
    @property
    def is_answered(self) -> bool:
        return self._is_answered
    
    @is_answered.setter
    def is_answered(self, b: bool) -> None:
        self._is_answered = b
    
    @property
    def question_id(self) -> str:
        return self._question_id
    
    @question_id.setter
    def question_id(self, s: str) -> None:
        self._question_id = s

    def get_shown_and_answered_values(self, question_id: str) -> tuple[int, int, int]:
        """
            function which returns int values of how many times the question was answered and shown        
        """
        times_answered_val = 0
        times_shown_val = 0
        row_num = 0
        
        # get times_answered and times_shown values
        with open("../files/questions.csv") as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader):
                if row["id"] == question_id:
                    times_answered_val = int(row["times_answered"])
                    times_shown_val = int(row["times_shown"])
                    row_num = idx
        
        return times_answered_val, times_shown_val, row_num

    def save_entry(self, question_id: str, is_answered: bool):
        """
            function which saves result of answer in questions.csv. 
            'times_shown' is increased by 1 every time the question is shown
            if the question is answered correctly, add 1 to 'times_answered' value for that question
        """
        times_answered, times_shown, row_num = self.get_shown_and_answered_values(question_id)

        file = pd.read_csv("../files/questions.csv")
        if is_answered is True:
            # [row number, column name]
            file.at[row_num, "times_answered"] = times_answered + 1
        file.at[row_num, "times_shown"] = times_shown + 1
        file.to_csv("../files/questions.csv", index=False)
