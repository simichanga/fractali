import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, util

def fractal_dimension_local(image, box_size, stride=1):
    """
    Determină harta de colorare a dimensiunii fractale locale folosind metoda Box Counting.
    
    :param image: Imaginea binară (2D numpy array).
    :param box_size: Dimensiunea pătratului pentru analiza locală.
    :param stride: Pasul de deplasare al ferestrei locale.
    :return: O hartă 2D cu dimensiunea fractală locală.
    """
    h, w = image.shape
    local_fd_map = np.zeros((h - box_size + 1, w - box_size + 1))

    for i in range(0, h - box_size + 1, stride):
        for j in range(0, w - box_size + 1, stride):
            local_patch = image[i:i + box_size, j:j + box_size]
            local_fd_map[i // stride, j // stride] = box_counting_fractal_dimension(local_patch)
    
    return local_fd_map

def box_counting_fractal_dimension(binary_patch):
    """
    Calculează dimensiunea fractală folosind metoda Box Counting pe un patch local.
    
    :param binary_patch: O regiune binară a imaginii.
    :return: Dimensiunea fractală estimată.
    """
    sizes = [2, 4, 8, 16]
    counts = []
    
    for size in sizes:
        S = size
        n = 0
        for i in range(0, binary_patch.shape[0], S):
            for j in range(0, binary_patch.shape[1], S):
                patch = binary_patch[i:i + S, j:j + S]
                if np.any(patch):  # Dacă pătratul conține părți din fractal
                    n += 1
        counts.append(n)
    
    # Calculăm dimensiunea fractală prin regresia log-log
    log_sizes = np.log(1.0 / np.array(sizes))
    log_counts = np.log(np.array(counts))
    coeffs = np.polyfit(log_sizes, log_counts, 1)
    return -coeffs[0]  # Panta regresiei este dimensiunea fractală

# Încarcă imaginea fractală
image_path = "mandelbrot_fractal.png"
image = io.imread(image_path)
if image.shape[-1] == 4:  # Verifică dacă există un canal alfa
    image = image[..., :3]  # Elimină canalul alfa
image_gray = color.rgb2gray(image)
image_binary = util.img_as_bool(image_gray > 0.5)  # Binarizare

# Parametri
box_size = 16  # Dimensiunea ferestrei locale
stride = 4     # Pasul de deplasare

# Calculăm harta dimensiunii fractale locale
fd_map = fractal_dimension_local(image_binary, box_size, stride)

# Afișăm harta
plt.figure(figsize=(10, 10))
plt.imshow(fd_map, cmap='plasma', extent=(0, image_binary.shape[1], 0, image_binary.shape[0]))
plt.colorbar(label="Dimensiunea fractală locală")
plt.title("Hartă de colorare a dimensiunii fractale locale")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
