# Assignment 2 - Unit Tests for Course (Sample tests)
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
import unittest

from planner import TermPlanner, parse_course_data
from course import Course


class TestParser(unittest.TestCase):

    def test_binary_simple(self):
        filename = 'tests/binary_simple.txt'

        actual = parse_course_data(filename)
        self.assertEqual('CSC207', actual.name)

        prereqs = actual.prereqs
        prereq_names = [p.name for p in prereqs]
        # User assertCountEqual when order doesn't matter
        self.assertCountEqual(['CSC165', 'CSC148'], prereq_names)

        for p in prereqs:
            self.assertEqual([], p.prereqs)

    def test_all_in_course(self):
        filename = 'tests/lol.txt'
        top = parse_course_data(filename)
        with open(filename, 'r') as source:
                for line in source:
                    classes = line.split()
                    self.assertTrue(classes[0] in top)
                    self.assertTrue(classes[1] in top)


class TestIsValid(unittest.TestCase):
    def setUp(self):

        # Single prereq
        self.single = TermPlanner('tests/lol.txt')

    def test_single_two(self):
        self.assertTrue(self.single.is_valid([['101'], ['102']]))

    def test_valid_many(self):
        self.assertTrue(self.single.is_valid([['101','102','204','209','103'], ['201','202','104','105','106'],['203'],['301']]))
        self.assertTrue(self.single.is_valid([['110','111','112','113','114'], ['207','208','209'],['303']]))
        self.assertTrue(self.single.is_valid([[], ['101'],['209']]))
        self.assertTrue(self.single.is_valid([[],[],[],[],[],[],[],[],[]]))


    def test_invalid_many(self):
        self.assertFalse(self.single.is_valid([['101'],['301']]))
        self.assertFalse(self.single.is_valid([['101','201']]))

    def test_invalid_repeat(self):
        self.assertFalse(self.single.is_valid([['101'],['101']]))

    def test_invalid_not_in_tree(self):
        self.assertFalse(self.single.is_valid([['999']]))

class TestPlanner(unittest.TestCase):
    def setUp(self):
        # Single prereq
        self.single = TermPlanner('tests/single.txt')

    def gen_test(self, tp, courses):
        s = tp.generate_schedule(courses)
        # Uncomment this line if you implement good_schedule.
        #self.assertTrue(good_schedule(tp, s, courses))

    def test_one_prereq(self):
        self.gen_test(self.single, ['CSC108', 'CSC148'])


def good_schedule(tp, schedule, courses):
    """ (TermPlanner, list of (list of str)) -> bool
    Return True if schedule is an acceptable output
    of tp.generate_courses(courses).
    """
    # Implement this function yourself if you want to use it!


if __name__ == '__main__':
    unittest.main(exit=False)
