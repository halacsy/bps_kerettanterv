#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import re


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
                pass

            # del jelzi, hogy torolni kell.
            if len(lo) < 10:
                continue
            if "három mesetípust" in lo:
                los = lo.split('.')
                los = [lo.strip() + "." for lo in los if len(lo)>4]
                for lo in los:
                    table.append({'semester': semester,
                          'period': row[1],
                          'subject': row[2],
                          'orig_subject': map_orig_subjects(row[3]),
                          'lo': lo,
                          })
            else:
                table.append({'semester': semester,
                          'period': row[1],
                          'subject': row[2],
                          'orig_subject': map_orig_subjects(row[3]),
                          'lo': lo,
                          })


import json
print(json.dumps({'learning_outcomes': table}, sort_keys=True, indent=4, ensure_ascii=False))
