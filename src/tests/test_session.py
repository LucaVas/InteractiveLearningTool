from src.session import Session
import pytest

def main():
    test_init()
    test_choose_mode()   


def test_init():
    session_one = Session()
    assert session_one.mode == None


if __name__ == "__main__":
    main()