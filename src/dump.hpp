// dump.hpp — two ways of looking at bytes.
// GIVEN.
#pragma once

#include "memory.hpp"

// Print the whole box, 16 bytes per line: address, hex, ASCII gutter.
void dump(const Memory& mem);

// Print ONE byte four ways: decimal, hex, binary, character.
// Example for the byte 65:   65  0x41  0b01000001  'A'
// TODO(lab-01, M3): implement in dump.cpp.
void show_byte(Byte b);
