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
"""Program for helping users plan schedules.

This module contains the main class that is used to interact with users
who are trying to plan their schedules. It requires the course module
to store prerequisite information.

TermPlanner: answers queries about schedules based on prerequisite tree.
"""
from course import Course


def parse_course_data(filename):
    """ (str) -> Course

    Read in prerequisite data from the file called filename,
    create the Course data structures for the data,
    and then return the root (top-most) course.

    See assignment handout for details.
    """
    course_list = {}
    with open(filename, 'r') as my_file:
        for line in my_file:
            course_name = line.split()
            if course_name[0] not in course_list:
                course_list[course_name[0]] = Course(course_name[0])
                
                if course_name[1] not in course_list:
                    course_list[course_name[1]] = Course(course_name[1])
                    course_list[course_name[1]].add_prereq(course_list[course_name[0]])
                    
                else:
                    course_list[course_name[1]].add_prereq(course_list[course_name[0]])
                
            else:
                
                if course_name[1] not in course_list:
                    course_list[course_name[1]] = Course(course_name[1])
                    course_list[course_name[1]].add_prereq(course_list[course_name[0]])
                    
                else:
                    if course_list[course_name[1]].__contains__(course_name[0]) == False:
                        
                        course_list[course_name[1]].add_prereq(course_list[course_name[0]])
    return top_course(course_list)

def top_course(course_list):
    for class1 in course_list:
        count = 0
        for class2 in course_list:
            if course_list[class2].__contains__(course_list[class1].name):
                count += 1
        if count == 1:
            return course_list[class1]
            
class TermPlanner:
    """Tool for planning course enrolment over multiple terms.

    Attributes:
    - course (Course): tree containing all available courses
    """

    def __init__(self, filename):
        """ (TermPlanner, str) -> NoneType

        Create a new term planning tool based on the data in the file
        named filename.

        You may not change this method in any way!
        """
        self.course = parse_course_data(filename)

    def is_valid(self, schedule):
        """ (TermPlanner, list of (list of str)) -> bool

        Return True if schedule is a valid schedule.
        Note that you are *NOT* required to specify why a schedule is invalid,
        though this is an interesting exercise!
        """
        #reset_tree(self.course)
        
        exist_count = 0 
        master_course_list = []
        for course_item_list in schedule:
            for course_item in course_item_list:
                master_course_list.append(course_item)
                if not self.course.__contains__(course_item):
                    exist_count += 1
 
        no_duplicate_count = 0
        for i in range(len(master_course_list)):
            for j in range(i+1, len(master_course_list)):
                if master_course_list[i] == master_course_list[j]:
                    no_duplicate_count += 1
        pre_list = []
        intree_count = 0
        if exist_count == 0 and no_duplicate_count == 0:            
            for level in range(len(schedule)):
                #if level == 0:
                    #for i in range(len(schedule[level])):
                        #item = schedule[level][i]
                        #if if_is_leaf(self.course, item) == False:
                        #if self.course.find_prereq_course(item).prereqs == []:
                            #return False
                            #intree_count += 1
                        #else:    
                            #take_the_course(self.course, item)
                    #pre_list += schedule[level] 
                            
                #else:
                    #for i in range(len(schedule[level])):
                        #item = schedule[level][i]
                        
                        #if course_takeable(self.course, item) == False:
                            #return False
                        #if is_takeable
                            #intree_count += 1
                        #else:    
                            #take_the_course(self.course, item)
                            #pre_list.append(lst)
                for i in range(len(schedule[level])):
                    item = schedule[level][i]
                    item_course = find_prereq_course(self.course,item)
                    if not item_course.is_takeable():
                        if not biglst_smal_lst(pre_list,item_course.missing_prereqs()):
                            intree_count += 1
                            
                        
                    
                pre_list += schedule[level]
                
                
            if intree_count == 0:
                return True
            else:
                return False
        else:
            return False
        
       

    def generate_schedule(self, selected_courses):
        """ (TermPlanner, list of str) -> list of (list of str)

        Return a schedule containing the courses in selected_courses that
        satisfies the restrictions given in the assignment specification.

        You may assume that all the courses in selected_courses appear in
        self.course.

        If no valid schedule can be formed from these courses, return an
        empty list.
        """
        reset_tree(self.course)
        if test_duplicate(selected_courses) == False:
            return []
        elif exist_in_tree(self.course, selected_courses) == False:
            return []
        else: 
            for course_code in selected_courses:
                item_course = find_prereq_course(self.course, course_code)
                #if item_course.taken == True:
                    #item_course.taken = False
                    
                if biglst_smal_lst(selected_courses,item_course.missing_prereqs()) == False:
                    return []
               
            
            
            
            
            
            
            enrolled_list = []                    
            while selected_courses != []:
                row_list = []
                for items in selected_courses: 
                    if course_takeable(self.course, items):
                        row_list.append(items)       
                if len(row_list) > 0: 
                    for items in row_list[:min(5,len(row_list))]:
                        take_the_course(self.course, items)
                    enrolled_list.append(row_list[:min(5,len(row_list))])
                    remove_list(selected_courses, row_list[:min(5,len(row_list))])
                else:
                    break
            if selected_courses == []:
                return enrolled_list
            else:
                return []
    
def if_is_leaf(top_course, course_code):
    if top_course.name == course_code:
        return top_course.prereqs == []
    else: 
        for items in top_course.prereqs:
            if if_is_leaf(items,course_code):
                return True
        return False

def take_the_course(top_course, course_code):
    if top_course.name == course_code:
        top_course.take()
    else:
        for items in top_course.prereqs:
            take_the_course(items, course_code)
            
def course_takeable(top_course, course_code):
    if top_course.name == course_code:
        if top_course.is_takeable():
            return True
        else:
            return False
    else:
        for items in top_course.prereqs:
            if course_takeable(items, course_code):
                return True
        else:
            return False
        
def remove_list(bigger_list, smaller_list):
    for items in smaller_list:
        bigger_list.remove(items)
    return bigger_list

def test_duplicate(lst):
    no_duplicate_count = 0
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]:
                no_duplicate_count += 1
    if no_duplicate_count == 0:
        return True
    else:
        return False
    
def exist_in_tree(top_course,lst):
    exist_count = 0
    for items in lst:
        if not top_course.__contains__(items):
            exist_count += 1
    if exist_count == 0:
        return True
    else:
        return False
    
def find_prereq_course(top_course, name):
    if top_course.name == name:
        return top_course
    for items in top_course.prereqs:
        find = find_prereq_course(items,name)
        if find:
            return find
    return False

def reset_tree(top_course):
    if top_course.taken == True:
        top_course.taken = False
    for items in top_course.prereqs:
        reset_tree(items)
                
def biglst_smal_lst(lst1,lst2):
    count = 0
    for items in lst2:
        if items not in lst1:
            count += 1
    if count == 0:
        return True
    else:
        return False
    
    
    
#def all_pre(top_course,course_code):
    #if top_course.name == course_code:
        #return top_course.missing_prereqs()
    #else:
        #for items in top_course.prereqs:
            #if item
            #return all_pre(items, course_code)
            
        
#def exist_in_tree(course1, course2):
    #exist_count = 0
    #if course2.name == course1.name


        
            
            
        
