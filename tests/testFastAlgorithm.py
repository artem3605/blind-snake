import unittest
import random
from src.FastAlgorithm import FastAlgorithm

random.seed(42)

class MyTestCase(unittest.TestCase):
    max_S = 10 ** 6
    k = 26

    def run_test(self, A, B):
        alg = FastAlgorithm(self.max_S, self.k)
        row_start = random.randint(0, A - 1)
        col_start = random.randint(0, B - 1)
        row_finish = random.randint(0, A - 1)
        col_finish = random.randint(0, B - 1)
        time = 0

        for step in alg.step():
            time += 1
            if step == "ERROR":
                self.fail("k is too small")
            if step == "RIGHT":
                col_start = (col_start + 1) % B
            if step == "LEFT":
                col_start = (col_start - 1 + B) % B
            if step == "UP":
                row_start = (row_start - 1 + A) % A
            if step == "DOWN":
                row_start = (row_start + 1) % A
            if row_start == row_finish and col_start == col_finish:
                break

        self.assertLess(time, A * B * self.k)

    def test_random(self):
        num_tests = 3
        for _ in range(num_tests):
            A = random.randint(1, self.max_S)
            B = random.randint(1, self.max_S // A)
            self.run_test(A, B)

    def test_thin(self):
        num_tests = 3
        max_A = 10
        for _ in range(num_tests):
            A = random.randint(1, max_A)
            B = random.randint(1, self.max_S // A)
            self.run_test(A, B)

    def test_tall(self):
        num_tests = 3
        max_B = 10
        for _ in range(num_tests):
            B = random.randint(1, max_B)
            A = random.randint(1, self.max_S // B)
            self.run_test(A, B)

if __name__ == '__main__':
    unittest.main()