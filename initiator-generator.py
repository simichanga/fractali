import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def koch_snowflake(order, length=1):
    def generate_segment(p1, p2, order):
        if order == 0:
            return [p1, p2]
        else:
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            s = [p1[0] + dx / 3, p1[1] + dy / 3]
            t = [p1[0] + dx * 2 / 3, p1[1] + dy * 2 / 3]
            u = [
                (p1[0] + p2[0]) / 2 - np.sqrt(3) * (p2[1] - p1[1]) / 6,
                (p1[1] + p2[1]) / 2 + np.sqrt(3) * (p2[0] - p1[0]) / 6,
            ]
            return (
                generate_segment(p1, s, order - 1) +
                generate_segment(s, u, order - 1) +
                generate_segment(u, t, order - 1) +
                generate_segment(t, p2, order - 1)[:-1]
            )

    p1, p2, p3 = [0, 0], [length, 0], [length / 2, np.sqrt(3) * length / 2]
    segments = generate_segment(p1, p2, order) + generate_segment(p2, p3, order) + generate_segment(p3, p1, order)
    x, y = zip(*segments)
    return x, y

def sierpinski_triangle(order):
    def subdivide(vertices, order):
        if order == 0:
            return [vertices]
        else:
            midpoints = [
                [(vertices[0][0] + vertices[1][0]) / 2, (vertices[0][1] + vertices[1][1]) / 2],
                [(vertices[1][0] + vertices[2][0]) / 2, (vertices[1][1] + vertices[2][1]) / 2],
                [(vertices[2][0] + vertices[0][0]) / 2, (vertices[2][1] + vertices[0][1]) / 2],
            ]
            return (
                subdivide([vertices[0], midpoints[0], midpoints[2]], order - 1) +
                subdivide([midpoints[0], vertices[1], midpoints[1]], order - 1) +
                subdivide([midpoints[2], midpoints[1], vertices[2]], order - 1)
            )

    vertices = [[0, 0], [1, 0], [0.5, np.sqrt(3) / 2]]
    triangles = subdivide(vertices, order)
    return triangles

def update_koch(val):
    order = int(slider_koch.val)
    ax1.clear()
    x, y = koch_snowflake(order)
    ax1.plot(x, y)
    ax1.set_title("Koch Snowflake")
    fig.canvas.draw_idle()

def update_sierpinski(val):
    order = int(slider_sierpinski.val)
    ax2.clear()
    triangles = sierpinski_triangle(order)
    for triangle in triangles:
        x, y = zip(*triangle + [triangle[0]])
        ax2.plot(x, y)
    ax2.set_title("Sierpiński Triangle")
    fig.canvas.draw_idle()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)

# Initial Plots
x, y = koch_snowflake(order=2)
ax1.plot(x, y)
ax1.set_title("Koch Snowflake")

triangles = sierpinski_triangle(order=2)
for triangle in triangles:
    x, y = zip(*triangle + [triangle[0]])
    ax2.plot(x, y)
ax2.set_title("Sierpiński Triangle")

# Add sliders
ax_slider_koch = plt.axes([0.2, 0.1, 0.65, 0.03])
slider_koch = Slider(ax_slider_koch, 'Koch Order', 0, 6, valinit=2, valstep=1)
slider_koch.on_changed(update_koch)

ax_slider_sierpinski = plt.axes([0.2, 0.05, 0.65, 0.03])
slider_sierpinski = Slider(ax_slider_sierpinski, 'Sierpiński Order', 0, 6, valinit=2, valstep=1)
slider_sierpinski.on_changed(update_sierpinski)

plt.show()
