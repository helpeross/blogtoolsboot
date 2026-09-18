import struct, os

static = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# PNG-compressed ICO entry (Vista+ standard). Embed the 32x32 PNG into a real .ico.
png_path = os.path.join(static, "favicon-32x32.png")
with open(png_path, "rb") as f:
    png = f.read()

w = h = 32
header = struct.pack("<HHH", 0, 1, 1)  # reserved, type=icon, count
entry = struct.pack("<BBBBHHII", w, h, 0, 0, 1, 32, len(png), 22)
with open(os.path.join(static, "favicon.ico"), "wb") as f:
    f.write(header + entry + png)

print("ICO_OK", len(header) + len(entry) + len(png), "bytes")
