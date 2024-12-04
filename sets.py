import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Julia Set Calculation
def julia_set(c, xlim, ylim, resolution, max_iter):
    x = np.linspace(xlim[0], xlim[1], resolution)
    y = np.linspace(ylim[0], ylim[1], resolution)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    img = np.zeros(Z.shape, dtype=int)
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        img[mask] = i
        Z[mask] = Z[mask] ** 2 + c
    return img

# Mandelbrot Set Calculation
def mandelbrot_set(xlim, ylim, resolution, max_iter):
    x = np.linspace(xlim[0], xlim[1], resolution)
    y = np.linspace(ylim[0], ylim[1], resolution)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros(C.shape, dtype=complex)
    img = np.zeros(C.shape, dtype=int)
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        img[mask] = i
        Z[mask] = Z[mask] ** 2 + C[mask]
    return img

# Update Function for Zooming
def update_plot():
    global xlim, ylim, resolution, max_iter, ax_julia, ax_mandelbrot

    ax_julia.clear()
    ax_mandelbrot.clear()

    # Update Julia Set
    julia = julia_set(c, xlim, ylim, resolution, max_iter)
    ax_julia.imshow(julia, extent=(*xlim, *ylim), cmap="hot")
    ax_julia.set_title("Julia Set")
    
    # Update Mandelbrot Set
    mandelbrot = mandelbrot_set(xlim, ylim, resolution, max_iter)
    ax_mandelbrot.imshow(mandelbrot, extent=(*xlim, *ylim), cmap="hot")
    ax_mandelbrot.set_title("Mandelbrot Set")
    
    fig.canvas.draw_idle()

# Keyboard Interaction
def on_key(event):
    global xlim, ylim, zoom_factor, max_iter

    x_center = (xlim[0] + xlim[1]) / 2
    y_center = (ylim[0] + ylim[1]) / 2
    width = xlim[1] - xlim[0]
    height = ylim[1] - ylim[0]

    # Zoom In and Out
    if event.key == 'up':  # Zoom in
        xlim = [x_center - width / (2 * zoom_factor), x_center + width / (2 * zoom_factor)]
        ylim = [y_center - height / (2 * zoom_factor), y_center + height / (2 * zoom_factor)]
    elif event.key == 'down':  # Zoom out
        xlim = [x_center - width * zoom_factor / 2, x_center + width * zoom_factor / 2]
        ylim = [y_center - height * zoom_factor / 2, y_center + height * zoom_factor / 2]

    # Adjust Max Iterations
    elif event.key == 'right':  # Increase iterations
        max_iter += 50
    elif event.key == 'left':  # Decrease iterations
        max_iter = max(50, max_iter - 50)

    update_plot()

# Initialize Parameters
xlim = [-2, 2]
ylim = [-2, 2]
resolution = 500
max_iter = 300
zoom_factor = 1.5
c = -0.8 + 0.156j  # Julia Set constant

# Plot Initialization
fig, (ax_julia, ax_mandelbrot) = plt.subplots(1, 2, figsize=(12, 6))
update_plot()

# Connect Keyboard Interaction
fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()
