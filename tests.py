# tests.py
# Unit tests verifying the correctness of both migration algorithms.


import unittest
from methods import migrateServersBaseline, migrateServersOptimal

class TestMigrationAlgorithms(unittest.TestCase):
    def setUp(self):
        # Format: (files_list, L, expected_server_count)
        self.test_cases = [
            ([7, 3, 2, 4, 5, 8], 10, 3),      # General mixed sizes
            ([1, 2, 3, 4], 4, 3),             # Strict pairing constraints
            ([10, 10, 10], 10, 3),            # All files exact size of L
            ([1, 1, 1, 1], 2, 2),             # All files fit perfectly in pairs
            ([], 5, 0),                       # Empty array edge case
            ([5], 10, 1),                     # Single element edge case
            ([8, 9, 7, 6], 10, 4)             # No files can be paired
        ]

    def test_baseline_correctness(self):
        for files, L, expected in self.test_cases:
            with self.subTest(files=files, L=L):
                self.assertEqual(migrateServersBaseline(files, L), expected)

    def test_optimal_correctness(self):
        for files, L, expected in self.test_cases:
            with self.subTest(files=files, L=L):
                self.assertEqual(migrateServersOptimal(files, L), expected)

if __name__ == '__main__':
    unittest.main()