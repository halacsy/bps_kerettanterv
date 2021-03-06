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

lo.csv:
	 curl "https://docs.google.com/spreadsheets/d/1P3cyZ3f03mc7UVqAjZleDmzc8qKrdJVZ0DbK_pxP0uw/gviz/tq?tqx=out:csv" > lo.csv
chapters/kerettanterv/eredmenyek.tex: lo.csv
	python code/convert_lo.py  > chapters/kerettanterv/eredmenyek.tex
%.docx: %.tex
	pandoc $< -o $@ -f latex -t docx 

cleanall:
	latexmk -C
	rm $(GENERATED_FILE)

clean:
	latexmk -c
	rm $(GENERATED_FILE)