#!/bin/bash

function count_imports() {
    local module="$1"
    local path="$2"
    egrep -R -w "^(import|from) $module" --exclude-dir=".*tox" $your_project  | wc -l
}


if [ $# -eq 0 ]; then
    echo "Please specify path to your project."
    exit 1
else
    your_project="$1"
fi

command -v bc >/dev/null 2>&1 || { echo "I require bc but it's not installed.  Aborting." >&2; exit 1; }

total_imports=$(egrep -R -w "^(import|from)" --exclude-dir=".*tox" $your_project  | wc -l)
neutron_imports=$(count_imports neutron $your_project)
lib_imports=$(count_imports neutron_lib $your_project)
total_neutron_related_imports=$((neutron_imports + lib_imports))

echo "You have $total_imports total imports"
echo "You imported Neutron $neutron_imports times"
echo "You imported Neutron-Lib $lib_imports times"

if [ "$lib_imports" -eq 0 ]; then
    echo "Your project does not import neutron-lib once, you suck!"
fi

goal=$(bc -l <<< "scale=4; ($lib_imports/$total_neutron_related_imports*100)")
target=$(bc <<< "$goal>50")

if [ "$target" -eq 0 ]; then
    echo "You need to get to 100%, you are this far: $goal%, get on with it!"
else
    echo "You need to get to 100%, you are close: $goal%, good job!"
fi
