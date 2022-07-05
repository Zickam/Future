import pymem

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
engine_pointer = pm.read_uint(engine + 0x58cfdc)
count = 0

print(engine_pointer + 0x4d90, engine_pointer + 0x4d90 + 0x4)

# while 1:
#     x, y = pm.read_float(engine_pointer + 0x4d90), pm.read_float(engine_pointer + 0x4d90 + 0x4)
#     print(f"{count} {x} {y}")
#     count += 1