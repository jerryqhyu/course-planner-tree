# Assignment 2 - Course Planning!
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
"""Course prerequisite data structure.

This module contains the class that should store all of the
data about course prerequisites and track taken courses.
Note that by tracking "taken" courses, we are restricting the use
of this class to be one instance per student (otherwise,
"taken" doesn't make sense).

Course: a course and its prerequisites.
"""

class PrerequisiteError(Exception):
    pass

class UntakeableError(Exception):
    pass


class Course:
    """A tree representing a course and its prerequisites.

    This class not only tracks the underlying prerequisite relationships,
    but also can change over time by allowing courses to be "taken".

    Attributes:
    - name (str): the name of the course
    - prereqs (list of Course): a list of the course's prerequisites
    - taken (bool): represents whether the course has been taken or not
    """

    # Core Methods - implement all of these
    
    def __init__(self, name, prereqs=None):
        """ (Course, str, list of Courses) -> NoneType

        Create a new course with given name and prerequisites.
        By default, the course has no prerequisites (represent this
        with an empty list, NOT None).
        The newly created course is not taken.
        """
        if prereqs == None:
            prereqs = []
            
        self.name = name
        self.prereqs = prereqs
        self.taken = False

    def is_takeable(self):
        """ (Course) -> bool

        Return True if the user can take this course.
        A course is takeable if and only if all of its prerequisites are taken.
        """
        if self.prereqs == []:
            return True
        else:
            count = 0
            for i in range(len(self.prereqs)):
                if self.prereqs[i].taken == False:
                    count += 1

            if count == 0:
                return True
            else:
                return False
                

    def take(self):
        """ (Course) -> NoneType

        If this course is takeable, change self.taken to True.
        Do nothing if self.taken is already True.
        Raise UntakeableError if this course is not takeable.
        """
        if self.is_takeable() == False:
            raise UntakeableError
        else:
            if self.taken == False:
                self.taken = True            
        

    def add_prereq(self, prereq):
        """ (Course, Course) -> NoneType

        Add a prereq as a new prerequisite for this course.

        Raise PrerequisiteError if either:
        - prereq has this course in its prerequisite tree, or
        - this course already has prereq in its prerequisite tree
        """
        if self == prereq:
            raise PrerequisiteError  
        elif prereq in self.prereqs:
            raise PrerequisiteError
        elif self in prereq.prereqs:
            raise PrerequisiteError
        else:
            self.prereqs.append(prereq)
            
            

    def missing_prereqs(self):
        """ (Course) -> list of str

        Return a list of all of the names of the prerequisites of this course
        that are not taken.

        The returned list should be in alphabetical order, and should be empty
        if this course is not missing any prerequisites.
        """
        
        untaken_list = []
        if len(self.prereqs) == 0:
            return untaken_list
        else:
            for item in self.prereqs:
                if item.taken == False:
                    untaken_list.append(item.name)
                    item.missing_prereqs()
            untaken_list.sort()
            return untaken_list
            
            
    def __contains__(self, item):
        if self.name == item:
            return True
        elif self.prereqs == []:
            return False
        else:
            for item2 in self.prereqs:
                if item2.__contains__(item):
                    return True
            return False
        
