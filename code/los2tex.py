import jinja2
import json
import sys

periods = ["1-2", "3-4", "5-6", "7-8", "9-10", "11-12"]
semesters = [0, 1, 2, 3, 4]
integrated_subjects = ['STEM', 'KULT', 'Harmónia']
kiemelt_subject = ['Magyar nyelv és irodalom', 'Történelem, társadalmi és állampolgári ismeretek',
                   'Matematika', "Testnevelés és sport", "Idegen nyelv"]


def select(semester, period, kiemelt_subject):
    return [lo for lo in table if lo['semester'] == semester and lo['period'] == period and lo['orig_subject'] == kiemelt_subject]


def collect_high_priority_subject_lo(subject):
    result = []
    for p in periods:

        r_semesters = []
        for s in semesters:
            los = select(s, p, subject)
            if len(los) > 0:
                r_semesters.append({"semester": s,
                                    "los": select(s, p, subject)
                                    })
        if(len(r_semesters) > 0):
            result.append({'years': p, "semesters": r_semesters})

    return {'name': subject, 'periods': result}


def collect_integrated_subject_lo(subject):
    result = []
    for p in periods:

        r_semesters = []
        for s in semesters:
            cucc = [lo for lo in table if lo['semester'] ==
                    s and lo['period'] == p and lo['subject'] == subject]

            r_semesters.append({"semester": s,
                                "los": cucc
                                })

        result.append({'years': p, "semesters": r_semesters})

    return {'name': subject, 'periods': result}


with open(sys.argv[1]) as json_file:
    table = json.load(json_file)['learning_outcomes']


orig_subjects = {}
for lo in table:
    s = lo['orig_subject']
    if s in orig_subjects:
        orig_subjects[s] += 1
    else:
        orig_subjects[s] = 1

kiemelt_subject = [s for s, freq in orig_subjects.items()]
kiemelt_subject.sort()
kiemelt_subject = ['Biológia-egészségtan', 'Dráma és tánc', 'Ének-zene', 'Erkölcstan', 'Etika', 'Fizika', 'Földrajz', 'Hon- és népismeret', 'Idegen nyelv', 'Informatika', 'Kémia', 'Környezetismeret', 'Magyar nyelv és irodalom',
                   'Matematika', 'Mozgóképkultúra és médiaismeret', 'Technika, életvitel és gyakorlat', 'Természetismeret', 'Testnevelés és sport', 'Történelem, társadalmi és állampolgári ismeretek', 'Vizuális kultúra']


curriculum = {
    'high_priority_subjects': [],

}

curriculum['high_priority_subjects'] = [
    collect_high_priority_subject_lo(s) for s in kiemelt_subject]

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
