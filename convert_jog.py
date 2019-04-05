import csv
table = []
with open('jog.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(", ".join(row))
            line_count += 1
        else:
            table.append({'req': row[0],
             'comment': row[1],
             'ref': row[2].split(',')})

    print(line_count)

import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "jog.jtex"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(data=table)  # this is where to put args to the template renderer

print(outputText)