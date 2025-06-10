# tests/test_module.py
import unittest
from mylibrary.module import greet

class GreetTestCase(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Alice"), "Hello, Alice! Welcome to my library.")
        self.assertEqual(greet("Bob"), "Hello, Bob! Welcome to my library.")

if __name__ == "__main__":
    unittest.main()