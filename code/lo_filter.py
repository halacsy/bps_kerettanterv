import json
import sys
import re

periods = ["1-2", "3-4", "5-6", "7-8", "9-10", "11-12"]
semesters = [0, 1, 2, 3, 4]
integrated_subjects = ['STEM', 'KULT', 'Harmónia']
kiemelt_subject = ['Magyar nyelv és irodalom', 'Történelem, társadalmi és állampolgári ismeretek',
                   'Matematika', "Testnevelés és sport", "Idegen nyelv"]


def select(semester, period, subject, lo_pattern):
    prog = None
    if lo_pattern:
       prog = re.compile(lo_pattern)
       

    def filter(lo):
        semester_term = True
        period_term = True
        subject_term = True
        lo_term = True 

        if semester is not None:
            semester_term = lo['semester'] == semester 
        
        if period is not None:
            period_term = lo['period'] == period 
        
        if subject is not None:
            subject_term = lo['orig_subject'] == subject

        if lo_pattern is not None:
            lo_term =  prog.match(lo['lo'])

        return (semester_term and period_term and subject_term and lo_term)
    
    return [lo for lo in table if filter(lo)]

def select_short(semester, period, subject, lo_pattern):
    def length_filter(lo):
        return (len(lo['lo'])< 20)

    return [lo for lo in table if length_filter(lo)]

with open(sys.argv[1]) as json_file:
    table = json.load(json_file)['learning_outcomes']
    filtered = select(None, None, "Kémia", ".*k.sérlet.*")
    
    for lo in filtered:
        print (lo['lo'])
    print(len(filtered))


kiemelt_subject = ['Biológia-egészségtan', 'Dráma és tánc', 'Ének-zene', 'Erkölcstan', 'Etika', 'Fizika', 'Földrajz', 'Hon- és népismeret', 'Idegen nyelv', 'Informatika', 'Kémia', 'Környezetismeret', 'Magyar nyelv és irodalom',
                   'Matematika', 'Mozgóképkultúra és médiaismeret', 'Technika, életvitel és gyakorlat', 'Természetismeret', 'Testnevelés és sport', 'Történelem, társadalmi és állampolgári ismeretek', 'Vizuális kultúra']


