# Install AFL++
git clone https://github.com/AFLplusplus/AFLplusplus
cd AFLplusplus
make
sudo make install

# Create target program (Modbus parser)
cat > modbus_parser.c << 'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void parse_modbus(unsigned char *data, size_t len) {
    if (len < 8) return;

    unsigned short trans_id = (data[0] << 8) | data[1];
    unsigned short proto_id = (data[2] << 8) | data[3];
    unsigned short length = (data[4] << 8) | data[5];
    unsigned char unit_id = data[6];
    unsigned char func_code = data[7];

    printf("Trans ID: 0x%04X\n", trans_id);
    printf("Function Code: 0x%02X\n", func_code);

    // Vulnerable code (buffer overflow)
    if (func_code == 0x03) {  // Read Holding Registers
        unsigned short start_addr = (data[8] << 8) | data[9];
        unsigned short count = (data[10] << 8) | data[11];

        char buffer[64];
        if (count > 100) {  // Intentional vulnerability
            memcpy(buffer, data, count);  // Overflow!
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "rb");
    if (!fp) return 1;

    unsigned char buffer[1024];
    size_t len = fread(buffer, 1, sizeof(buffer), fp);
    fclose(fp);

    parse_modbus(buffer, len);
    return 0;
}
EOF

# Compile with AFL instrumentation
afl-gcc -o modbus_parser modbus_parser.c

# Create seed inputs (valid Modbus packets)
mkdir -p afl_in afl_out
echo -ne '\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x0A' > afl_in/valid1.bin

# Run AFL fuzzer
afl-fuzz -i afl_in -o afl_out -- ./modbus_parser @@

# Monitor crashes in afl_out/crashes/
