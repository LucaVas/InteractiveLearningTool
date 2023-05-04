from ..user import User

def main():
    test_init()
    test_validate_username()

def test_init():

    user_one = User()
    assert user_one.username == None
    assert user_one.is_user == False
    assert user_one.json_file == "../app.json"

def test_validate_username():
    user_two = User()
    assert user_two.validate_username("luca") == False
    assert user_two.validate_username("1234") == False
    assert user_two.validate_username("luca1234") == True


if __name__ == "__main__":
    main()