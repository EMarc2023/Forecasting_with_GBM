"""Unit tests for predict.py"""

import unittest
import subprocess

class TestPredictScript(unittest.TestCase):
    """Various tests for user input"""

    def test_correct_input(self):
        """Simulate correct input"""
        result = subprocess.run(
            ["python", "predict.py", "2023-02-11 13:00:00"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)  # Expect successful exit
        self.assertIn(
            "Predicted trip volume", result.stdout
        )  # Check if prediction is printed

    def test_incorrect_input_no_arguments(self):
        """Simulate incorrect input (no arguments)"""
        result = subprocess.run(
            ["python", "predict.py"], capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0)  # Expect failure
        self.assertIn("Usage:", result.stdout)  # Check if usage message is printed

    def test_incorrect_input_too_many_arguments(self):
        """Simulate incorrect input (too many arguments)"""
        result = subprocess.run(
            ["python", "predict.py", "2023-02-11 13:00:00", "extra_arg"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)  # Expect failure
        self.assertIn("Usage:", result.stdout)  # Check if usage message is printed

    def test_incorrect_input_invalid_format(self):
        """Simulate incorrect input (invalid datetime format)"""
        result = subprocess.run(
            ["python", "predict.py", "invalid-date"], capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid date and time format", result.stdout)

if __name__ == "__main__":
    unittest.main()
