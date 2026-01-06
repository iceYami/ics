import snap7

plc = snap7.client.Client()
plc.connect('10.10.10.11', 0, 1)

# Get PLC info
cpu_info = plc.get_cpu_info()
print(f"PLC: {cpu_info.ModuleTypeName}")
print(f"Firmware: {cpu_info.ASName}")

# List blocks
blocks = plc.list_blocks()
print(f"Blocks: {blocks}")

# Upload OB1 (main program block)
ob1 = plc.upload('OB', 1)
with open("OB1.mc7", "wb") as f:
    f.write(ob1)

print("[+] Uploaded OB1 for analysis")

plc.disconnect()
