from cs50 import get_int

# input Higth and ceck height number range 1 to 8
while True:
    height = get_int("Height: ")
    if height > 0 and height <= 8:
        break


# Create mario
for i in range(height):
    print(" " * (height - (i + 1)), end="")
    print("#" * (i + 1), end="")
    print("  " + "#" * (i + 1))