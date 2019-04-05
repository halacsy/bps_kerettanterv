#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
err_occur = []                         # The list where we will store results.

ST_START = 0
ST_INPRINT = 1

def extract_chunk(file, section_title, out):
    state = ST_START

    # Compile a case-insensitive regex pattern.
    pattern = re.compile("\\\\(sub)*section{([^}]+)}", re.IGNORECASE)
    # open file for reading text.
    with open(file, 'rt') as in_file:
        # Keep track of line numbers.
        for linenum, line in enumerate(in_file):
            match = pattern.search(line)
            if match != None:
                if state == ST_START and match.group(2) == section_title:
                    out.write(line)
                    state = ST_INPRINT
                elif state == ST_INPRINT:
                    state = ST_START
            elif state == ST_INPRINT:
                out.write(line)

extract_chunk(
"../chapters/pedprogram/0_iskola_celja.tex",
"Emberkép", sys.stdout)