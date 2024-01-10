h = int(input("Height: "))
while h<1 or h>8:
    
for i in range(1,h+1):
    print(" " * (h-i) + "#" * i)
