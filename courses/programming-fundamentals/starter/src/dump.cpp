// dump.cpp — hex + ASCII, like the Unix tool `hexdump -C`.
//
// The `dump` function below is GIVEN and working, except for one TODO.
// Read it before you change it: it is the shape of nearly every loop you will
// write this semester (an outer loop over rows, an inner loop over columns).
//
// `show_byte` at the bottom is YOUR WORK.
#include "dump.hpp"

#include <iomanip>
#include <iostream>

// How many bytes we print on one line. Try changing it to 8 and rebuilding.
const std::size_t BYTES_PER_LINE = 16;

// Is this byte something a terminal can print as a glyph?
// 0x20 is space, 0x7E is '~'. Everything outside that range we show as '.'.
static bool is_printable(Byte b) { return b >= 0x20 && b <= 0x7E; }

void dump(const Memory& mem) {
    // std::hex switches the stream to hexadecimal; setfill/setw pad with zeros
    // so every number is the same width and the columns line up.
    for (std::size_t row = 0; row < MEM_SIZE; row += BYTES_PER_LINE) {

        // The address column: 0000, 0010, 0020, ...
        std::cout << std::hex << std::setfill('0') << std::setw(4) << row << "  ";

        // The hex column: 16 bytes, two digits each.
        for (std::size_t col = 0; col < BYTES_PER_LINE; ++col) {
            Byte b = mem.data[row + col];
            std::cout << std::setw(2) << (int)b << ' ';
        }

        std::cout << " |";

        // The ASCII gutter.
        for (std::size_t col = 0; col < BYTES_PER_LINE; ++col) {
            Byte b = mem.data[row + col];
            // TODO(lab-01, M2): when the byte IS printable, print the byte
            //                   itself instead of the dot. One token changes.
            //                   Hint: a Byte sent to std::cout prints as a
            //                   character already - that is the whole joke of
            //                   Lab 1. Right now every byte looks unprintable.
            if (is_printable(b)) {
                std::cout << '.';
            } else {
                std::cout << '.';
            }
        }

        std::cout << "|\n";
    }

    // Put the stream back to decimal, or every number you print later is hex.
    std::cout << std::dec << std::setfill(' ');
}

void show_byte(Byte b) {
    // TODO(lab-01, M3): print these four things on one line, separated by
    // two spaces, then a newline:
    //
    //   1. b as a decimal number          -> 65
    //      Careful: `std::cout << b` prints a CHARACTER, because Byte is a
    //      one-byte type. Use (int)b to print the number.
    //   2. b as hex, with a 0x prefix     -> 0x41
    //      std::hex switches the stream; std::dec switches it back.
    //   3. b as 8 binary digits, 0b first -> 0b01000001
    //      There is no std::bin. Loop from bit 7 down to bit 0 and print
    //      ((b >> i) & 1). That expression is Lab 2 arriving early.
    //   4. b as a character in quotes     -> 'A'
    //      Use is_printable(b); print '.' for bytes a terminal cannot show.
    //
    // Expected for `set 0 65` then `get 0`:
    //   65  0x41  0b01000001  'A'
    std::cout << "show_byte: not implemented yet (byte was "
              << (int)b << ")\n";
}
