# exit when any command fails
set -e

rm -rf old diff 
create_diff() {
    FILE=$1
    echo "procession $FILE"
    DIR=$(dirname "${FILE}")
    if [ -z "$DIR" ]
    then
        echo "using root"
    else
        mkdir -pv old/$DIR
        mkdir -pv diff/$DIR
    fi

    if git show 7d2dd867e946e89787b1de071d9b575b5a0e9838:$FILE > old/$FILE ; then
        echo "found in git"
    else 
        if [ $FILE ==  "chapters/pedprogram/regi_struktura_bevezeto.tex"  ]
        then
            cat $FILE > old/$FILE
        else
            echo "" > old/$FILE
        fi
    fi

    latexdiff  old/$FILE $FILE > diff/$FILE


}
FILES=`find chapters -name "*.tex"`
for FILE in $FILES
do
    if [ $FILE !=  "chapters/kerettanterv/eredmenyek-template.tex"  ]
    then    
        if [ $FILE != "chapters/kerettanterv/eredmenyek.tex" ]
        then
            create_diff $FILE
        fi
    fi


done

#create_diff pedprog.tex
create_diff kerettanterv.tex
cp references.bib diff/
cd diff
latexmk -pdf kerettanterv.tex
cat $FILES | tr ' ' $'\n' | grep "\DIFadd{" |wc -l

cd ..