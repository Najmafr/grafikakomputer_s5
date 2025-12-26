lebar = 5
tinggi = 5

for y in range(tinggi):
    for x in range(lebar):
        if x == 2 and y == 3:
            print("X", end=" ") #titik aktif
        else:
            print(".",end=" ")
    print()