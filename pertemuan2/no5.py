# Membuat list berisi tiga pasangan titik
titik_list = [(0, 0), (50, 50), (100, 0)]

# Menampilkan semua titik dengan perulangan for
print("Daftar Titik:")
for titik in titik_list:
    print(titik)

# Menyimpan satu titik dalam tuple bernama pusat
pusat = (0, 0)

# Menampilkan nilai tuple pusat
print("\nTitik pusat:", pusat)

# Membuat dictionary berisi atribut objek
titik_objek = {"x": 10, "y": 20, "warna": "biru"}

# Menampilkan isi dictionary dengan format teks
print(f"\nTitik ({titik_objek['x']}, {titik_objek['y']}) berwarna {titik_objek['warna']}.")
