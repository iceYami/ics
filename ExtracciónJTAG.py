# Using OpenOCD with JTAG adapter (Bus Pirate, J-Link, ST-Link)
# Connect to PLC's JTAG test points (locate via PCB inspection)

# OpenOCD configuration for ARM Cortex-M4 PLC
cat > plc_target.cfg <<EOF
source [find interface/jlink.cfg]
transport select jtag
source [find target/stm32f4x.cfg]
reset_config srst_only
EOF

# Launch OpenOCD
openocd -f plc_target.cfg

# In separate terminal, connect with telnet
telnet localhost 4444

# Dump flash memory
> halt
> flash read_bank 0 firmware_dump.bin 0 0x100000
> shutdown
