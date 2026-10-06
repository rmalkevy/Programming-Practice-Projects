// Друга одиниця трансляції для досліду 8. Сама по собі не запускається:
//   FLAGS=extra-push.cpp ./run.sh 08 5
#include <iostream>

bool push(int v) {
    std::cout << "push(" << v << ") з extra-push.cpp\n";
    return true;
}
