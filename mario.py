h = None
while True:
    h = input("Height: ")
    try:
        h = int(h)
        if h >= 1 and h <= 8:
            break
    except:
        pass

for i in range(1, h + 1):
    print(" " * (h - i) + "#" * i)
