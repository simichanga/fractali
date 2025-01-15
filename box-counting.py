import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color

def box_counting(image, min_box_size=2, max_box_size=128):
    """
    Determină dimensiunea fractală a unei imagini folosind metoda Box Counting.
    
    :param image: Imaginea binară (alb-negru) sub formă de matrice numpy
    :param min_box_size: Dimensiunea minimă a grilei
    :param max_box_size: Dimensiunea maximă a grilei
    :return: Dimensiunea fractală estimată
    """
    # Transformă imaginea într-un array binar (0 și 1)
    binary_image = (image > 0).astype(int)

    box_sizes = []
    box_counts = []
    
    sizes = [2**i for i in range(int(np.log2(min_box_size)), int(np.log2(max_box_size)) + 1)]
    
    for box_size in sizes:
        grid_count = 0
        for i in range(0, binary_image.shape[0], box_size):
            for j in range(0, binary_image.shape[1], box_size):
                # Verifică dacă există cel puțin un pixel alb în box-ul curent
                if binary_image[i:i+box_size, j:j+box_size].any():
                    grid_count += 1
        box_sizes.append(box_size)
        box_counts.append(grid_count)
    
    # Calculăm dimensiunea fractală folosind regresia logaritmică
    log_box_sizes = np.log(1 / np.array(box_sizes))
    log_box_counts = np.log(box_counts)
    
    # Determinăm panta dreptei de regresie
    coeffs = np.polyfit(log_box_sizes, log_box_counts, 1)
    fractal_dimension = coeffs[0]
    
    return fractal_dimension, log_box_sizes, log_box_counts

def main():
    # Încarcă imaginea și o binarizează
    image_path = 'fractal_example.png'  # Înlocuiește cu calea imaginii tale
    image = io.imread(image_path)
    gray_image = color.rgb2gray(image)
    binary_image = (gray_image > 0.5).astype(int)  # Binarizare simplă
    
    fractal_dimension, log_sizes, log_counts = box_counting(binary_image)
    
    print(f"Dimensiunea fractală estimată: {fractal_dimension}")
    
    # Plotăm log-log
    plt.plot(log_sizes, log_counts, 'o-', label='Date')
    plt.xlabel('log(1 / dimensiunea celulei)')
    plt.ylabel('log(număr de celule)')
    plt.title('Estimarea dimensiunii fractale')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
