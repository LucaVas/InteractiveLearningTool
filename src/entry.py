import csv

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

    def generate_id(self):
        with open("../statistics.csv", "r") as file:
            lines = file.readlines()
            if lines[-1][0].isnumeric():
                self.id = int(lines[-1][0]) + 1
            else:
                self.id = 0

    def save_entry(self):
        with open("../statistics.csv", "a", newline="") as file:
            self.generate_id()
            fieldnames = ["id", "is_answered", "question_id"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({"id": self.id, "is_answered": self.is_answered, "question_id": self.question_id})
