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
        self.assertTrue(self.c2.is_takeable())


class TestCourseTake(unittest.TestCase):

    def setUp(self):
        self.c1 = Course('CSC108')
        self.c2 = Course('CSC148', [self.c1])

    def test_take_prereq_satisfied(self):
        self.c1.taken = True
        self.assertFalse(self.c2.taken)
        self.c2.take()
        self.assertTrue(self.c2.taken)


class TestCourseAddPrereq(unittest.TestCase):

    def setUp(self):
        self.c3 = Course('alone101')

    def test_add_prereq_no_prereqs(self):
        prereq = Course('MAT223')
        self.c3.add_prereq(prereq)
        self.assertEqual([prereq], self.c3.prereqs)


class TestCourseMissingPrereqs(unittest.TestCase):

    def setUp(self):
        self.c1 = Course('CSC108')
        self.c2 = Course('CSC148', [self.c1])

    def test_missing_prereqs_one_missing(self):
        self.assertEqual(['CSC108'], self.c2.missing_prereqs())

if __name__ == '__main__':
    unittest.main(exit=False)
