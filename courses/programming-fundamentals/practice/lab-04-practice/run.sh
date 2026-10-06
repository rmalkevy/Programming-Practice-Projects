#!/bin/sh
# Зібрати й запустити один дослід:   ./run.sh 02 1 2
# Рядок збірки той самий, що в Notes 01.
#   CXX=g++-14 ./run.sh 02 ...    — інший компілятор
#   NO_WERROR=1 ./run.sh 01 ...   — попередження лишаються попередженнями
set -e
cd "$(dirname "$0")"
n="$1"; shift
src=$(ls "$n"-*.cpp)
werror="-Werror"
[ -n "$NO_WERROR" ] && werror=""
mkdir -p build
"${CXX:-c++}" -std=c++17 -Wall -Wextra $werror -fsanitize=address,undefined "$src" -o "build/$n"
./build/"$n" "$@"
