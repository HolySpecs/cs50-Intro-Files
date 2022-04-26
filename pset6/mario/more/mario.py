from cs50 import get_int

def front(height):
    row = [" "," "," "," "," "," "," "," "]
    for i in range(height+1):
        row[7-i] = '#'
    result = "".join(row)
    return result

def back(height):
    row = [" "," "," "," "," "," "," "," "]
    for i in range(height+1):
        row[i] = '#'
    result = "".join(row)
    return result

while True:
    height = get_int("Height: ")
    if (height >= 1 and height <= 8):
        break
for i in range(height):
    print(front(i) + "  " + back(i))