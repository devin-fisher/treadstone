import unittest
import os
import sys
import pickle
main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(main_dir)
from lib.video.video_still import *


class SimplisticTest(unittest.TestCase):
    def simple_get_still_test(self):
        actual = get_still(os.path.join(main_dir, "tests", "fodder", 'test.mp4'), 2, show=False)
        with open(os.path.join(main_dir, "tests", "fodder", 'test_2_sec_still'), 'rb') as f:
            expected = pickle.load(f)
        numpy.testing.assert_array_equal(expected, actual)

if __name__ == '__main__':
    unittest.main()