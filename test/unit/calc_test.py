import pytest
import unittest

from app.calc import Calculator


@pytest.mark.unit
class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    
        
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
