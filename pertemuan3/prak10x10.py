lebar = 10
tinggi = 10

for y in range(tinggi):
    for x in range(lebar):
        if x == 4 and y == 6:
            print("X", end=" ") #titik aktif
        else:
            print(".",end=" ")
    print()