# Assignment 2 - Unit Tests for Course (Sample tests)
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
#
#
#
# ---------------------------------------------
"""Unit tests for course.py

Submit this file, containing *thorough* unit tests
for your code in course.py.
Note that you should not have any tests involving
standard input or output in here.
"""
import unittest
from course import Course, UntakeableError, PrerequisiteError


class TestCourseInit(unittest.TestCase):
    def test_init_with_prereq(self):
        prereq1 = Course('CSC108')
        prereq2 = Course('CSC165')
        course = Course('CSC148', [prereq1, prereq2])
        self.assertEqual('CSC148', course.name)
        self.assertFalse(course.taken)
        self.assertEqual(course.prereqs, [prereq1, prereq2])


class TestCourseIsTakeable(unittest.TestCase):
    def setUp(self):
        self.c1 = Course('CSC108')
        self.c2 = Course('CSC148', [self.c1])

    def test_takeable_one_prereq_satisfied(self):
        self.c1.taken = True
        self.assertTrue(self.c2.is_takeable)

    def test_takeable_many_prereqs_satisfied(self):
        self.c1 = Course('CSC108')
        self.c2 = Course('CSC148', [self.c1])
        self.c3 = Course('CSC165', [self.c1])
        self.c4 = Course('CSC207', [self.c1, self.c2, self.c3])
        self.c1.taken = True
        self.assertTrue(self.c2.is_takeable())
        self.assertTrue(self.c3.is_takeable())
        self.c2.taken = True
        self.c3.taken = True
        self.assertTrue(self.c4.is_takeable())

    def test_not_takeable(self):
        self.c1 = Course('CSC108')
        self.c2 = Course('CSC148', [self.c1])
        self.assertFalse(self.c2.is_takeable())

    def test_takeable_taken(self):
        self.c1 = Course('CSC108')
        self.c1.taken = True
        self.assertTrue(self.c1.is_takeable())


class TestCourseTake(unittest.TestCase):

    def setUp(self):
        self.c1 = Course('CSC108')
        self.c2 = Course('CSC148', [self.c1])
        self.c3 = Course('CSC207', [self.c2])

    def test_take_prereq_satisfied(self):
        self.c1.taken = True
        self.assertFalse(self.c2.taken)
        self.c2.take()
        self.assertTrue(self.c2.taken)

    def test_take_taken(self):
        self.c1.taken = True
        self.c1.take()
        self.assertTrue(self.c1.taken)

    def test_take_many_in_a_row(self):
        self.c1.take()
        self.c2.take()
        self.c3.take()
        self.assertTrue(self.c3.taken)

    def test_take_error(self):
        self.c1.taken = False
        self.assertRaises(UntakeableError, self.c2.take)


class TestCourseAddPrereq(unittest.TestCase):

    def setUp(self):
        self.c1 = Course('Highschoolcalc')
        self.c2 = Course('MAT136')
        self.c3 = Course('MAT137', [self.c1])
        self.c4 = Course('MAT237', [self.c2, self.c3])

    def test_add_prereq_no_prereqs(self):
        prereq = Course('MAT223')
        self.c1.add_prereq(prereq)
        self.assertEqual([prereq], self.c1.prereqs)

    def test_add_prereqs_many_prereqs(self):
        prereq = Course('MAT136')
        self.c1.add_prereq(prereq)
        self.assertEqual(prereq.name, self.c1.prereqs[-1].name)

    def test_error_in_tree(self):
        self.assertRaises(PrerequisiteError, self.c3.add_prereq, self.c1)
        self.assertRaises(PrerequisiteError, self.c4.add_prereq, self.c1)

    def test_error_in_prereq_tree(self):
        self.assertRaises(PrerequisiteError, self.c1.add_prereq, self.c3)
        self.assertRaises(PrerequisiteError, self.c1.add_prereq, self.c4)

    def test_error_add_self(self):
        self.assertRaises(PrerequisiteError, self.c3.add_prereq, self.c3)


class TestCourseMissingPrereqs(unittest.TestCase):

    def setUp(self):
        self.c1 = Course('CSC108')
        self.c2 = Course('CSC148', [self.c1])
        self.c3 = Course('CSC207', [self.c2])
        self.c4 = Course('CSC208', [self.c3])
        self.c5 = Course('CSC209', [self.c4])
        self.c6 = Course('CSC301', [self.c5])
        self.c7 = Course('CSC302', [self.c6])

    def test_missing_prereqs_one_missing(self):
        self.assertEqual(['CSC108'], self.c2.missing_prereqs())

    def test_missing_prereqs_many_missing(self):
        lst = ['CSC108', 'CSC148', 'CSC207', 'CSC208', 'CSC209', 'CSC301']
        self.assertEqual(lst, self.c7.missing_prereqs())

    def test_not_missing_prereq(self):
        self.c1.taken = True
        self.c2.taken = True
        self.c3.taken = True
        self.c4.taken = True
        self.c5.taken = True
        self.c6.taken = True
        self.assertEqual([], self.c7.missing_prereqs())


if __name__ == '__main__':
    unittest.main(exit=False)
