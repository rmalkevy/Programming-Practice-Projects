#!/bin/sh
# Перезібрати всі схеми курсу: ./build.sh            — усі
#                              ./build.sh pointers   — одну
# <тема>.py пише img/<тема>.uk.svg, <тема>_en.py перекладає його в img/<тема>.svg.
set -e
cd "$(dirname "$0")"
topics="$*"
[ -z "$topics" ] && topics=$(ls *.py | grep -v '_en\.py$' | sed 's/\.py$//')
for t in $topics; do
    python3 "$t.py" "../$t.uk.svg"
    python3 "${t}_en.py" "../$t.uk.svg" "../$t.svg"
    xmllint --noout "../$t.uk.svg" "../$t.svg"
    echo "img/$t.uk.svg, img/$t.svg"
done
