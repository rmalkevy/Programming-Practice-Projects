#!/bin/sh
# Зібрати й запустити один дослід:   ./run.sh 01 65 300
# Рядок збірки той самий, що в Notes 01.
#   CXX=g++-14 ./run.sh 01 ...           — інший компілятор
#   NO_WERROR=1 ./run.sh 04 ...          — попередження лишаються попередженнями
#   FLAGS=-DMIX ./run.sh 04              — додаткові прапорці компілятора
set -e
cd "$(dirname "$0")"
n="$1"; shift
src=$(ls "$n"-*.cpp)
werror="-Werror"
[ -n "$NO_WERROR" ] && werror=""
mkdir -p build
"${CXX:-c++}" -std=c++17 -Wall -Wextra $werror -fsanitize=address,undefined $FLAGS "$src" -o "build/$n"
./build/"$n" "$@"
