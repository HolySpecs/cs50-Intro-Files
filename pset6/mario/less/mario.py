from cs50 import get_int

def layer(height, result, length):
    i = height + 1
    while i > 0:
        result[length -i] = '#'
        i = i -1
    return ''.join(result)

while True:
    height = get_int("Height: ")
    if (height >= 1 and height <= 8):
        break

result = []
for num1 in range(0,height):
    result.append(' ')

for i in range(height):
    print(layer(i, result, height))