#include "memory.hpp"

Byte mem_get(const Memory& mem, std::size_t addr) {
    if (addr >= MEM_SIZE) {
        return 0;
    }
    return mem.data[addr];
}

bool mem_set(Memory& mem, std::size_t addr, Byte value) {
    if (addr >= MEM_SIZE) {
        return false;
    }
    mem.data[addr] = value;
    return true;
}