#!/bin/sh
# Зібрати й запустити один дослід:   ./run.sh 03 10 2
# Рядок збірки той самий, що в Notes 01.
#   CXX=g++-14 ./run.sh 02 ...                 — інший компілятор
#   NO_WERROR=1 ./run.sh 02 ...                — попередження лишаються попередженнями
#   FLAGS=-fno-sanitize=address ./run.sh 05 …  — додаткові прапорці компілятора
set -e
cd "$(dirname "$0")"
n="$1"; shift
src=$(ls "$n"-*.cpp)
werror="-Werror"
[ -n "$NO_WERROR" ] && werror=""
mkdir -p build
"${CXX:-c++}" -std=c++17 -Wall -Wextra $werror -fsanitize=address,undefined $FLAGS "$src" -o "build/$n"
./build/"$n" "$@"
