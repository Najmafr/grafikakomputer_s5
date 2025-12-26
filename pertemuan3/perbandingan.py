# Program menampilkan tabel perbandingan Raster dan Vektor

# Data tabel disimpan dalam list berisi tuple
tabel = [
    ("Aspek", "Raster", "Vektor"),
    ("Representasi", "Tersusun dari piksel (titik-titik warna)", "Tersusun dari garis, kurva, dan bentuk matematis"),
    ("Ketika diperbesar", "Gambar menjadi pecah (blur)", "Gambar tetap tajam"),
    ("Ukuran file", "Umumnya lebih besar", "Biasanya lebih kecil"),
    ("Cocok untuk", "Foto, citra digital", "Logo, peta, desain grafis"),
    ("Contoh format", "JPG, PNG, BMP", "SVG, AI, EPS")
]

# Menentukan lebar kolom agar tabel rapi
lebar_aspek = 20
lebar_raster = 45
lebar_vektor = 45

# Mencetak header tabel
print("=" * (lebar_aspek + lebar_raster + lebar_vektor))
print(f"{tabel[0][0]:<{lebar_aspek}} | {tabel[0][1]:<{lebar_raster}} | {tabel[0][2]:<{lebar_vektor}}")
print("=" * (lebar_aspek + lebar_raster + lebar_vektor))

# Mencetak isi tabel
for baris in tabel[1:]:
    print(f"{baris[0]:<{lebar_aspek}} | {baris[1]:<{lebar_raster}} | {baris[2]:<{lebar_vektor}}")

print("=" * (lebar_aspek + lebar_raster + lebar_vektor))
