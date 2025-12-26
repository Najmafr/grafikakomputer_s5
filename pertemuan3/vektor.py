x1, y1 = 0, 0
x2, y2 = 5, 3

n = 5
for i in range(n + 1):
    x = x1 + (x2 - x1) * i / n
    y = y1 + (y2 - y1) * i / n
    print(f"titik ke-{i}: ({x:.1f}, {y:.1f})") 