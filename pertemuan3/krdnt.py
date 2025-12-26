import math

# Input koordinat
x1 = float(input("Masukkan x1: "))
y1 = float(input("Masukkan y1: "))
x2 = float(input("Masukkan x2: "))
y2 = float(input("Masukkan y2: "))

# Menampilkan hasil titik
print("\n=== HASIL ===")
print(f"Titik pertama : ({x1}, {y1})")
print(f"Titik kedua   : ({x2}, {y2})")

# Menghitung jarak antar titik
jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
print(f"Jarak antar titik: {jarak:.2f}")

# Menentukan kuadran titik pertama
if x1 > 0 and y1 > 0:
    kuadran = "Kuadran I"
elif x1 < 0 and y1 > 0:
    kuadran = "Kuadran II"
elif x1 < 0 and y1 < 0:
    kuadran = "Kuadran III"
elif x1 > 0 and y1 < 0:
    kuadran = "Kuadran IV"
else:
    kuadran = "Sumbu (tidak di kuadran)"

print(f"Titik pertama berada di: {kuadran}")

# Menampilkan titik di bidang (grid sederhana)
print("\n")
for y in range(12, -1, -1):   # menampilkan dari atas ke bawah
    for x in range(0, 13):
        if int(x) == int(x1) and int(y) == int(y1):
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
