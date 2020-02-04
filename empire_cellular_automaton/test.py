import random
import matplotlib.pyplot as plt


def generate_colors(n):
    rgb_values = []
    hex_values = []
    r = int(random.random() * 256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)
    step = 256 / n
    for _ in range(n):
        r += step
        g += step
        b += step
        r = int(r) % 256
        g = int(g) % 256
        b = int(b) % 256
        r_hex = hex(r)[2:]
        g_hex = hex(g)[2:]
        b_hex = hex(b)[2:]
        hex_values.append('#' + r_hex + g_hex + b_hex)
        rgb_values.append((r, g, b))
    return rgb_values, hex_values


color_count = 6

# generate values and print them
rgb_values, hex_values = generate_colors(6)
print(rgb_values, hex_values)

# show generated colors
fig = plt.figure(figsize=(1, color_count))
for i in range(color_count):
    fig.add_subplot(1, color_count, i + 1)
    plt.imshow([[rgb_values[i]]])
plt.show()
