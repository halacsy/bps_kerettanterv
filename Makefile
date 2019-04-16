# Latex Makefile using latexmk
# Modified by Dogukan Cagatay <dcagatay@gmail.com>
# Originally from : http://tex.stackexchange.com/a/40759
#

# Change only the variable below to the name of the main tex file.
PROJNAME=pedprog

.PHONY: $(PROJNAME).pdf all clean jog.csv


# You want latexmk to *always* run, because make does not have all the info.
# Also, include non-file targets in .PHONY so they are run regardless of any
# file of the given name existing.
.PHONY: $(PROJNAME).pdf all clean

GENERATED_FILE=chapters/pedprogram/5_jogi_referenciak.tex

%.tex: %-template.tex jog.csv
	./code/convert_jog.py $< > $@
jog.csv:
	curl "https://docs.google.com/spreadsheets/d/1Uwk-rL1bD5udxe049fYklE_2xjiyIbVir5Nc_IYF4DE/gviz/tq?tqx=out:csv" > jog.csv
$(PROJNAME).pdf: $(PROJNAME).tex  $(GENERATED_FILE)
	latexmk -g -pdf -pdflatex="pdflatex -interactive=nonstopmode" -use-make $<

cleanall:
	latexmk -C
	rm $(GENERATED_FILE)

clean:
	latexmk -c
	rm $(GENERATED_FILE)