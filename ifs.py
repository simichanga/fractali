import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import random

# Barnsley Fern (IFS)
def barnsley_fern(iterations):
    points = []
    x, y = 0, 0
    for _ in range(iterations):
        r = random.random()
        if r < 0.01:
            x, y = 0, 0.16 * y
        elif r < 0.86:
            x, y = 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
        elif r < 0.93:
            x, y = 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
        else:
            x, y = -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44
        points.append((x, y))
    return zip(*points)

# Sierpiński Triangle (IFS)
def sierpinski_triangle_ifs(iterations):
    points = []
    x, y = 0, 0
    for _ in range(iterations):
        r = random.random()
        if r < 1/3:
            x, y = 0.5 * x, 0.5 * y
        elif r < 2/3:
            x, y = 0.5 * x + 0.5, 0.5 * y
        else:
            x, y = 0.5 * x + 0.25, 0.5 * y + 0.5
        points.append((x, y))
    return zip(*points)

# Update function for Barnsley Fern
def update_barnsley(val):
    iterations = int(slider_fern.val)
    ax1.clear()
    x, y = barnsley_fern(iterations)
    ax1.scatter(x, y, s=0.1, color="green")
    ax1.set_title("Barnsley Fern")
    ax1.axis("equal")
    fig.canvas.draw_idle()

# Update function for Sierpiński Triangle
def update_sierpinski(val):
    iterations = int(slider_sierpinski.val)
    ax2.clear()
    x, y = sierpinski_triangle_ifs(iterations)
    ax2.scatter(x, y, s=0.1, color="blue")
    ax2.set_title("Sierpiński Triangle (IFS)")
    ax2.axis("equal")
    fig.canvas.draw_idle()

# Setup the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(bottom=0.25)

# Initial plots
x, y = barnsley_fern(10000)
ax1.scatter(x, y, s=0.1, color="green")
ax1.set_title("Barnsley Fern")
ax1.axis("equal")

x, y = sierpinski_triangle_ifs(10000)
ax2.scatter(x, y, s=0.1, color="blue")
ax2.set_title("Sierpiński Triangle (IFS)")
ax2.axis("equal")

# Add sliders for Barnsley Fern
ax_slider_fern = plt.axes([0.2, 0.15, 0.65, 0.03])
slider_fern = Slider(ax_slider_fern, 'Fern Iterations', 1000, 50000, valinit=10000, valstep=1000)
slider_fern.on_changed(update_barnsley)

# Add sliders for Sierpiński Triangle
ax_slider_sierpinski = plt.axes([0.2, 0.05, 0.65, 0.03])
slider_sierpinski = Slider(ax_slider_sierpinski, 'Triangle Iterations', 1000, 50000, valinit=10000, valstep=1000)
slider_sierpinski.on_changed(update_sierpinski)

plt.show()
