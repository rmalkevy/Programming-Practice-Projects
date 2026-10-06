#!/bin/sh
# Зібрати й запустити один дослід:   ./run.sh 04 3
# Рядок збірки той самий, що в Notes 01.
#   CXX=g++-14 ./run.sh 04 ...              — інший компілятор
#   NO_WERROR=1 ./run.sh 06 ...             — попередження лишаються попередженнями
#   FLAGS=-DDIRECT ./run.sh 06              — додаткові прапорці компілятора
#   FLAGS=extra-push.cpp ./run.sh 08        — ще один .cpp до тієї самої програми
set -e
cd "$(dirname "$0")"
n="$1"; shift
src=$(ls "$n"-*.cpp)
werror="-Werror"
[ -n "$NO_WERROR" ] && werror=""
mkdir -p build
"${CXX:-c++}" -std=c++17 -Wall -Wextra $werror -fsanitize=address,undefined $FLAGS "$src" -o "build/$n"
./build/"$n" "$@"
