import pytest
import os
from main import main

def test_main():
    file_path = "/Users/chetan/Desktop/Internships/GoCargo/GC-Internship/Chetan_Krishna/src/Internshala.csv"

    if os.path.exists(file_path):
        os.remove(file_path)

    main()

    assert os.path.exists(file_path)