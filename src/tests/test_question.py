from src.question import Question

def main():
    test_init()
    test_clear_question()


def test_init():
    question_one = Question()
    assert question_one.type == None
    assert question_one.content == None
    assert question_one.options == []
    assert question_one.number_of_options == 0
    assert question_one.answer == ""
    assert question_one.status == "enabled"

def test_clear_question():
    question_two = Question()
    question_two.content = ["item one", "item two", "item three"]
    question_two.answer = "test answer"
    question_two.clear_question()
    assert question_two.answer == ""


if __name__ == "__main__":
    main()