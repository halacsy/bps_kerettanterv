#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import re

table = []
with open('jog.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            # we skip the header row
            line_count += 1
        else:
            # if the third col is empty then we should create an empty []
            if re.match('^\s*$', row[2]):
                ref = []
            else:
                ref = re.split(',\s*',row[2])
            table.append({'req': row[0],
             'comment': row[1],
             'ref': ref
            })



import jinja2

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

TEMPLATE_FILE = "chapters/pedprogram/5_jogi_referenciak-template.tex"
template = latex_jinja_env.get_template(TEMPLATE_FILE)
outputText = template.render(data=table)  # this is where to put args to the template renderer

print(outputText)
