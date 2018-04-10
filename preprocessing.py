# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 15:41:36 2018

@author: fchen
"""

# Defining class for data retrieval and cleaning
'''
Class Attributes for Use:
    Dataframes
        - enrolls
        - cancels
        - rmcaps
        - specprg
        - depaloc
        - selects
        - timeslots

    Methods
        - form_timeslots(days_input = 'MTWHFSU', hour_split = 2, day_beginning_time = 8, day_ending_time = 22)
        - popular_course_groups(n = 2)
'''
import os
import pandas as pd
import numpy as np
from collections import Counter
from itertools import combinations
import datetime

class course_data:
    # Reading necessary files in from Raw Data file
    
    # Section to cleaning enrollment data
    enroll_cols = ['Course', 'Course Prefix', 'Course Suffix', 'Department', 'First Instructor UID',
                   'First Begin Time', 'First Days', 'First End Time',
                   'First Room', 'Max Units', 'Min Units',
                   'Reg Count', 'Seats', 'Second Instructor UID', 'Second Begin Time', 'Second Days',
                   'Second End Time', 'Second Room', 'Section', 'Session', 'Term']
    nonrooms = ['DEN@Viterbi', 'TBA', 'OFF CAMPUS', 'OFFICE', 'OCC', 'JKP', 'SAN DIEGO', 'SHANGHAI', 'ONLINE']
    enrolls = pd.read_excel(os.getcwd() + '\Raw Data\Marshall_Course_Enrollment_1516_1617.xlsx')
    enrolls = enrolls[enrolls['First Room'].isin(nonrooms) == False][enroll_cols]
    enrolls = enrolls[(enrolls['First Days'].isnull() & enrolls['Second Days'].isnull()) == False]
    enrolls = enrolls[enrolls['First Days'].isnull() == False]
    enrolls = enrolls[enrolls['First Begin Time'].isnull() == False]
    enrolls = enrolls[enrolls['First Begin Time'] != 'TBA']
    enrolls = enrolls.reset_index()[enrolls.columns]
    enrolls['First Days'] = enrolls['First Days'].replace(to_replace=['TH','SU'], value=['H','U'])
    enrolls['Second Days'] = enrolls['Second Days'].replace(to_replace=['TH','SU'], value=['H','U'])
    
    # Reading in secondary data
    cancels = pd.read_excel(os.getcwd() + '\Raw Data\Cancelled_Courses_1516_1617.xlsx')
    rmcaps = pd.read_excel(os.getcwd() + '\Raw Data\Marshall_Room_Capacity_Chart.xlsx')
    specprg = pd.read_excel(os.getcwd() + '\Raw Data\Summary_Special_Session_Codes_1516_1617.xlsx')
    depaloc = pd.read_excel(os.getcwd() + '\Raw Data\Department_Allocations_20171.xlsx')
    depaloc['Days'] = depaloc['Days'].replace(to_replace=['TH','SU'], value=['H','U'])
    selects = pd.read_excel(os.getcwd() + '\Raw Data\Student_Course_Selection_1516.xlsx')
    
    # Function for creating timeslots dataframe
    def form_timeslots(days_input = 'MTWHFSU', hour_split = 2, 
                       day_beginning_time = 8, day_ending_time = 22):
        timeslot_dict = {'Weekday': [], 'Time': [], 'DayTimeIdx': []}
        for day in days_input:
            daytimeidx = 0
            for hour in range(day_beginning_time, day_ending_time + 1):
                for minutes in np.arange(0, 60, 60/hour_split):
                    if hour != day_ending_time:
                        timeslot_dict['Weekday'].append(day)
                        timeslot_dict['Time'].append(datetime.time(hour, int(minutes)))
                        timeslot_dict['DayTimeIdx'].append(daytimeidx)
                    elif minutes != int(60/hour_split):
                        timeslot_dict['Weekday'].append(day)
                        timeslot_dict['Time'].append(datetime.time(hour, int(minutes)))
                        timeslot_dict['DayTimeIdx'].append(daytimeidx)
                    daytimeidx += 1
        return pd.DataFrame(timeslot_dict, index = range(len(timeslot_dict['Time'])))
    
    timeslots = form_timeslots()
    # Tagging Timeslots for Department Allocations
    depaloc['Timeslots'] = np.nan
    depaloc['Slotslength'] = np.nan
    for idx, row in depaloc.iterrows():
        curr_slots = []
        class_start = row['Start Time']
        class_end = row['End Time']
        for day in row.Days:
            temp_timeslots = timeslots[timeslots['Weekday'] == day]
            for ts_idx, ts_row in temp_timeslots.iterrows():
                if (ts_row.Time >= class_start) and (ts_row.Time <= class_end):
                    curr_slots.append(ts_idx)
        depaloc.loc[idx,'Slotslength'] = len(curr_slots)
        depaloc.loc[idx,'Timeslots'] = str(curr_slots).replace('[','').replace(']','').replace(',','')
        
    # Tagging Timeslots for Course Allocations
    enrolls['Timeslots'] = np.nan
    enrolls['Slotslength'] = np.nan
    for idx, row in enrolls.iterrows():
        curr_slots = []
        class_start = row['First Begin Time']
        class_end = row['First End Time']
        for day in row['First Days']:
            temp_timeslots = timeslots[timeslots['Weekday'] == day]
            for ts_idx, ts_row in temp_timeslots.iterrows():
                if (ts_row.Time >= class_start) and (ts_row.Time <= class_end):
                    curr_slots.append(ts_idx)
        enrolls.loc[idx,'Slotslength'] = len(curr_slots)
        enrolls.loc[idx,'Timeslots'] = str(curr_slots).replace('[','').replace(']','').replace(',','')
    
    # Creating top pairs dataframe
    # Finding classes taken commonly together
    def popular_course_groups(self, n = 2):
        course_aggs = self.selects[['Randomized Unique Identifier',
                                    'Course',
                                    'Term']].drop_duplicates().groupby(['Randomized Unique Identifier', 'Term']).apply(lambda x: list(x.Course))
        course_groups = []
        for group in course_aggs:
            course_groups.append(group)

        # Finding most common course enrollment pairs
        d  = Counter()
        for sub in course_groups:
            if len(course_groups) < n:
                continue
            sub.sort()
            for comb in combinations(sub, n):
                d[comb] += 1

        course_group_dict = {'Counts': []}
        for i in range(n):
            course_group_dict['Course {0}'.format(i)] = []

        for tupl in d.most_common():
            for i, course_name in enumerate(tupl[0]):
                course_group_dict['Course {0}'.format(i)].append(course_name)
            course_group_dict['Counts'].append(tupl[1])

        return pd.DataFrame(course_group_dict, index = range(len(course_group_dict['Course {0}'.format(i)])))