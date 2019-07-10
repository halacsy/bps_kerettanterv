#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import re
import jinja2

map = {}
translationFile = "/Users/bp268/Documents/Code/kerettanterv/traslations.csv"
if translationFile is not None:
    with open(translationFile, mode='r') as infile:
        reader = csv.reader(infile)
        map = {rows[0]: rows[1] for rows in reader}


""" ez valahol elveszett
"9-10-STEM-Fizika",,,
"Hőtani alapfogalmak, a hőtan főtételei, hőerőgépek. Annak ismerete, hogy gépeink működtetése, az élő szervezetek működése csak energia befektetése árán valósítható meg, a befektetett energia jelentős része elvész, a működésben nem hasznosul, „örökmozgó” létezése elvileg kizárt.
"""

map_subject_names = {
    'Fizika b változat': 'Fizika',
    'Ének-zene﻿  b változat': 'Ének-zene',
    'Ének-zene  b változat': 'Ének-zene',
    'Biológia-egészségtanb változat': 'Biológia-egészségtan',
    'Biológia-egészségtan b változat': 'Biológia-egészségtan',
    'Kémia  b változat': 'Kémia'
}

def map_orig_subjects(name):
    if name in map_subject_names:
        return map_subject_names[name]
    
    if 'Magyar nyelv és irodalom' in name:
        return 'Magyar nyelv és irodalom'
    return name

table = []
with open('lo.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
 
    for row in csv_reader:
  
        if line_count == 0:
            # we skip the header row
            line_count += 1
        else:
            semester = 0
            try:
                semester = int(row[0])
            except:
                pass
            lo = row[4]
            if (lo in map):

                lo = map[lo]

            else:
                print("% no translations found", lo)

            # del jelzi, hogy torolni kell.
            if len(lo) < 10:
                continue

            table.append({'semester': semester,
                          'period': row[1],
                          'subject': row[2],
                          'orig_subject': map_orig_subjects(row[3]),
                          'lo': lo,
                          })



periods = ["1-2", "3-4", "5-6", "7-8", "9-10", "11-12"]
semesters = [0,1, 2, 3, 4]
integrated_subjects = ['STEM', 'KULT', 'Harmónia']
kiemelt_subject = ['Magyar nyelv és irodalom'
                   ,'Történelem, társadalmi és állampolgári ismeretek', 'Matematika', "Testnevelés és sport", "Idegen nyelv"]



def select(semester, period, kiemelt_subject):
    return [lo for lo in table if lo['semester'] == semester and lo['period'] == period and lo['orig_subject'] == kiemelt_subject]


def collect_high_priority_subject_lo(subject):
    result = []
    for p in periods:

        r_semesters = []
        for s in semesters:
            r_semesters.append({"semester": s,
                              "los": select(s, p, subject)
            })
            
        result.append({'years': p, "semesters": r_semesters})

    return {'name': subject, 'periods': result}

def collect_integrated_subject_lo(subject):
    result = []
    for p in periods:

        r_semesters = []
        for s in semesters:
            cucc =  [lo for lo in table if lo['semester'] == s and lo['period'] == p and lo['subject'] == subject]

            r_semesters.append({"semester": s,
                              "los": cucc
            })
            
        result.append({'years': p, "semesters": r_semesters})

    return {'name': subject, 'periods': result}

curriculum = {
    'high_priority_subjects': [],
    'integrated_subjects': []
}

curriculum['high_priority_subjects'] = [ collect_high_priority_subject_lo(s) for s in kiemelt_subject]
curriculum['integrated_subjects']= [ collect_integrated_subject_lo(s) for s in integrated_subjects]

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)

latex_jinja_env = jinja2.Environment(
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=templateLoader)

TEMPLATE_FILE = "chapters/kerettanterv/eredmenyek-template.tex"
template = latex_jinja_env.get_template(TEMPLATE_FILE)
# this is where to put args to the template renderer
outputText = template.render(curriculum=curriculum)

print(outputText)
