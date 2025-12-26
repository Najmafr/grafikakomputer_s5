# Menggambar garis dari (0,0) ke (5,3)
x1, y1 = 0, 0
x2, y2 = 5, 3

# Jumlah langkah = perbedaan terbesar
steps = max(abs(x2 - x1), abs(y2 - y1))

# Menghitung perubahan tiap langkah
dx = (x2 - x1) / steps
dy = (y2 - y1) / steps

x, y = x1, y1
print("Koordinat titik-titik garis dari (0,0) ke (5,3):")
for i in range(steps + 1):
    print(f"({round(x)}, {round(y)})")
    x += dx
    y += dy
