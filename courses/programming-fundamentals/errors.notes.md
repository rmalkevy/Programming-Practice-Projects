# Помилки, які ви точно побачите

Курс: [EN](README.md) · [Українською](README.uk.md) · Поруч: [C++ за годину](cpp-survival-kit.notes.md) · [інструменти й git](setup.notes.md)

Довідник на весь семестр. Тримайте відкритим. Усі повідомлення нижче —
**справжній вивід** clang на macOS; на Linux/gcc формулювання трохи інші, але
структура та сама.

---

## Як читати будь-яку помилку

```txt
e1.cpp:3:14: error: expected ';' at end of declaration
    3 |     int x = 1
      |              ^
```

- `e1.cpp:3:14` — **файл, рядок, колонка**. Починайте звідси, а не з тексту.
- `error:` — не зібралось. `warning:` — зібралось, але підозріло (у нас `-Werror`, тож теж не зібралось). `note:` — не окрема проблема, а підказка до попередньої.
- Стрілочка `^` показує **місце** в рядку.

Три правила:

1. **Читайте першу помилку, виправляйте, збирайте знову.** Одна забута `;` легко дає 20 повідомлень — 19 з них наслідок.
2. **Дивіться на рядок ВИЩЕ за вказаний.** Компілятор помічає проблему там, де вона стає неможливою, а не там, де ви її зробили. Класика — забута крапка з комою.
3. Помилка в рядку, який ви не писали (усередині `<iostream>`) — майже завжди означає, що ви неправильно викликали щось своє. Шукайте в трасуванні рядок зі **своїм** файлом.

---

## 1. Компілятор не переклав

### `expected ';' at end of declaration`

```txt
e1.cpp:3:14: error: expected ';' at end of declaration
    3 |     int x = 1
      |              ^
      |              ;
```

Забута крапка з комою. Компілятор навіть пропонує, куди її поставити. Зверніть увагу: він показує рядок 3, а зламали ви кінець рядка 3 — тут пощастило, збігається.

### `use of undeclared identifier 'std'`

```txt
e2.cpp:2:5: error: use of undeclared identifier 'std'
    2 |     std::cout << "hi\n";
```

Немає `#include <iostream>`. Загальне правило: «невідоме ім'я» = або друкарська помилка, або забутий `#include`.

| Що використовуєте | Що включити |
|---|---|
| `std::cout`, `std::cin` | `<iostream>` |
| `std::string` | `<string>` |
| `std::uint8_t`, `std::uint16_t` | `<cstdint>` |
| `std::size_t` | `<cstddef>` |
| `std::setw`, `std::hex` | `<iomanip>` |
| `std::istringstream` | `<sstream>` |
| `std::memcpy` | `<cstring>` |

### `using the result of an assignment as a condition`

```txt
e3.cpp:4:11: error: using the result of an assignment as a condition without parentheses [-Werror,-Wparentheses]
    4 |     if (x = 1) std::cout << "yes\n";
      |         ~~^~~
e3.cpp:4:11: note: use '==' to turn this assignment into an equality comparison
```

Написали `=` (присвоїти) там, де мали на увазі `==` (порівняти). `-Werror` перетворює це на помилку — і добре. Детально — [Lab 4](lab-04-the-shape-of-control.md).

### `unused variable` / `unused parameter`

```txt
e5.cpp:3:9: error: unused variable 'unused' [-Werror,-Wunused-variable]
    3 |     int unused = 5;
```

Змінна є, а не використовується. Або приберіть її, або справді використайте. Якщо параметр поки не потрібен (заготовка функції) — `(void)name;` глушить попередження; саме так зроблено в `TODO`-заготовках [скелета](starter/README.md).

### `no matching function for call to 'show'`

```txt
f1.cpp:3:14: error: no matching function for call to 'show'
    3 | int main() { show("hello"); }
f1.cpp:2:6: note: candidate function not viable: no known conversion from 'const char[6]' to 'int' for 1st argument
```

Функція є, але аргументи не того типу (або не та кількість). Рядок `note:` — найважливіший: він каже, **що саме** не підійшло. Тут передали текст туди, де очікують число.

### Ще три коротко

| Повідомлення | Що сталось |
|---|---|
| `expected '}'` | незакрита фігурна дужка. Перевірте відступи — вирівняний код показує це очима |
| `redefinition of 'x'` | дві змінні з тим самим іменем в одному блоці |
| `cannot initialize a variable of type 'int' with an lvalue of type 'const char[2]'` | `int x = "a";` — сплутали лапки. `'a'` це символ, `"a"` це текст |

---

## 2. Лінкер: код правильний, але збирати нема з чого

Лінкер працює **після** компілятора, і його помилки виглядають інакше — без `файл:рядок`.

### `Undefined symbols` — оголосили, але не написали

```txt
Undefined symbols for architecture arm64:
  "helper()", referenced from:
      _main in e4-dc2a19.o
ld: symbol(s) not found for architecture arm64
```

(На Linux: `undefined reference to 'helper()'`.)

Функцію оголосили в `.hpp`, а тіло в `.cpp` не написали — або написали, але **цей `.cpp` не доданий у `CMakeLists.txt`**. Другий випадок — найчастіший у Lab 6–8, коли з'являються нові файли:

```cmake
add_executable(ember
    src/main.cpp
    src/memory.cpp
    src/dump.cpp
    src/cpu.cpp      # <- забули цей рядок = Undefined symbols
)
```

### `duplicate symbol` — написали двічі

```txt
duplicate symbol 'push(int)' in:
    .../f3.o
    .../f2.o
ld: 1 duplicate symbols
```

Одна функція визначена у двох `.cpp`. **Одне тіло — один `.cpp`**; у заголовку лише оголошення. `#pragma once` від цього не рятує: він захищає від подвійного включення в *один* файл, а не від двох тіл у двох файлах. [Lab 7](lab-07-call-and-return.md).

---

## 3. Програма запустилась і зламалась

### Анатомія звіту AddressSanitizer

```txt
==58956==ERROR: AddressSanitizer: heap-use-after-free on address 0x6020000000b0 ...
READ of size 4 at 0x6020000000b0 thread T0
    #0 0x000102ee48e4 in main d2.cpp:5
    #1 0x00018abe44e0 in start+0x1b4c (dyld:arm64e+0x204e0)
```

Читайте три речі, в такому порядку:

1. **`ERROR: AddressSanitizer: <вид>`** — *що* сталось (`heap-use-after-free`).
2. **`READ of size 4`** / `WRITE of size 4` — читали чи писали, і скільки байтів.
3. **Рядок `#0`** — **ваш рядок коду**: `d2.cpp:5`. Це винуватець. Рядки `#1`, `#2` і далі — хто його викликав; у них часто службові адреси, які вас не стосуються.

Нижче звіт ще друкує, де цю пам'ять виділили й де звільнили — теж з вашими рядками. Довжина звіту лякає; корисних рядків у ньому три-чотири.

Репорт **не треба переписувати своїми словами** — курс просить вставити його в README як є, і поруч один рядок: що ви зрозуміли.

### Чотири види, які ви зустрінете

**Вихід за масив** ([Lab 3](lab-03-addresses-not-names.md), [Lab 5](lab-05-many-of-one-thing.md)):

```txt
d1.cpp:4:5: runtime error: index 4 out of bounds for type 'int[4]'
==58951==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x00016b722790 ...
WRITE of size 4 at 0x00016b722790 thread T0
    #0 0x0001046dcae8 in main d1.cpp:4
```

Масив на 4 елементи має індекси `0 1 2 3`. `a[4]` — вже чужа пам'ять. Якщо масив у купі, вид буде `heap-buffer-overflow`.

**Читання після `delete`** ([Lab 6](lab-06-named-bundles.md)):

```txt
==58956==ERROR: AddressSanitizer: heap-use-after-free on address 0x6020000000b0 ...
READ of size 4 at 0x6020000000b0
    #0 ... in main d2.cpp:5
```

Об'єкта вже немає, а вказівник лишився — це **завислий вказівник** (dangling pointer). Лікується `p = nullptr;` одразу після `delete`.

**Подвійне звільнення** ([Lab 6](lab-06-named-bundles.md)):

```txt
==58959==ERROR: AddressSanitizer: attempting double-free on 0x6020000000b0 in thread T0
```

Один `new` — один `delete`.

**Переповнення знакового `int`** — це вже UBSan, не ASan ([Lab 1](lab-01-a-box-of-bytes.md)):

```txt
d4.cpp:4:11: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior d4.cpp:4:11
-2147483648
```

Зверніть увагу: програма **не впала**, вона надрукувала `-2147483648` і пішла далі. Без UBSan ви б цього не побачили взагалі. Саме тому санітайзери не вимикають.

### Витоки пам'яті: на Apple Silicon їх не видно

```bash
ASAN_OPTIONS=detect_leaks=1 ./scratch
```

```txt
==58976==AddressSanitizer: detect_leaks is not supported on this platform.
```

LeakSanitizer працює на Linux (і в WSL), але **не** на macOS з процесором Apple. Це не ваша помилка й не помилка налаштування.

Що робити на Mac у [Lab 6](lab-06-named-bundles.md), де треба показати витік:

- зібрати той самий `scratch.cpp` у Docker чи на будь-якій Linux-машині, або
- показати `use-after-free` і `double-free` (вони на Mac ловляться) і **пояснити** витік на пальцях: об'єкт живий, вказівника на нього немає, звільнити його вже нікому.

Обидва варіанти зараховуються — так і напишіть у README.

### Програма просто впала, без звіту

```txt
zsh: segmentation fault  ./scratch
```

Ви зібрали **без** санітайзерів. Перезберіть із `-fsanitize=address,undefined` і запустіть ще раз — замість трьох слів отримаєте рядок коду.

### Програма нічого не друкує і не завершується

Нескінченний цикл. Ctrl-C зупиняє. Шукайте `while`, у якому лічильник не змінюється, або `JMP` на самого себе в програмі всередині `ember` — саме через це `run` у [Lab 4](lab-04-the-shape-of-control.md) зобов'язаний мати ліміт кроків.

---

## 4. Збірка й термінал

### `does not appear to contain CMakeLists.txt`

```txt
CMake Error: The source directory ".../empty" does not appear to contain CMakeLists.txt.
```

`cmake -S . -B build` треба запускати з теки, де лежить `CMakeLists.txt`. Перевірте `pwd` і `ls`.

### `no such file or directory: ./build/ember`

Збірки ще не було або вона впала. Послідовність завжди така:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug   # один раз
cmake --build build                            # після кожної зміни коду
./build/ember
```

Якщо `cmake --build` надрукував помилку — бінарника немає. Не запускайте старий; полагодьте й зберіть знову.

### Додали файл, а компілятор його не бачить

`CMakeLists.txt` не перечитується сам, коли ви створили `cpu.cpp`. Додайте файл у `add_executable(...)` і запустіть `cmake --build build` — CMake помітить, що список змінився.

### `permission denied: ./build/ember`

```bash
chmod +x build/ember
```

Буває після копіювання проєкту між машинами.

---

## Шпаргалка

| Побачили | Проблема | Куди дивитись |
|---|---|---|
| `expected ';'` | синтаксис | рядок, вказаний у помилці, **і попередній** |
| `use of undeclared identifier` | забутий `#include` або друкарська помилка | таблиця включень вище |
| `no matching function` | не ті аргументи | рядок `note: candidate function not viable` |
| `unused variable` | `-Werror` | приберіть або `(void)x;` |
| `Undefined symbols` / `undefined reference` | тіла функції немає, або `.cpp` не в CMake | `add_executable(...)` |
| `duplicate symbol` | два тіла однієї функції | заголовок оголошує, `.cpp` визначає |
| `AddressSanitizer: *-buffer-overflow` | вихід за масив | рядок `#0` |
| `heap-use-after-free` | завислий вказівник | `p = nullptr` після `delete` |
| `attempting double-free` | два `delete` | один `new` — один `delete` |
| `UndefinedBehaviorSanitizer` | UB, програма не впала | рядок у `runtime error:` |
| `detect_leaks is not supported` | macOS на Apple Silicon | Linux/WSL або пояснення словами |
| `segmentation fault` без звіту | зібрано без санітайзерів | додайте `-fsanitize=address,undefined` |
| нічого не друкує | нескінченний цикл | Ctrl-C, потім лічильник циклу |
