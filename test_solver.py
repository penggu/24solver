import unittest

from solver import Solver

class TestSolver(unittest.TestCase):
    def test_has_solution(self):
        self.assertTrue(Solver([1, 2, 3, 4]).has_solution())
        self.assertTrue(Solver([5, 5, 5, 1]).has_solution())
        self.assertTrue(Solver([7, 7, 3, 1]).has_solution())
        self.assertTrue(Solver([8, 8, 3, 3]).has_solution())
        self.assertFalse(Solver([1, 1, 1, 1]).has_solution())

    def test_find_solutions(self):
        solutions = Solver([1, 2, 3, 4]).find_solutions()
        self.assertIn('((1 + 3) + 2) * 4', solutions)
        
        solutions = Solver([5, 5, 5, 1]).find_solutions()
        self.assertIn('(5 - (1 / 5)) * 5', solutions)
        
        solutions = Solver([7, 7, 3, 1]).find_solutions()
        self.assertIn('(7 - 1) * (7 - 3)', solutions)
        
        solutions = Solver([8, 8, 3, 3]).find_solutions()
        self.assertIn('8 / (3 - (8 / 3))', solutions)
        
        solutions = Solver([1, 1, 1, 1]).find_solutions()
        self.assertEqual(solutions, [])

if __name__ == '__main__':
   unittest.main()

