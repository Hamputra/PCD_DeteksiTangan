import os
from PIL import Image

def read_image(file_path):
    img = Image.open(file_path)
    width, height = img.size
    pixels = list(img.getdata())
    img_array = [[pixels[i * width + j] for j in range(width)] for i in range(height)]
    return img_array

def rgb_to_grayscale(image):
    height, width = len(image), len(image[0])
    grayscale_image = [[0] * width for _ in range(height)]
    for i in range(height):
        for j in range(width):
            r, g, b = image[i][j]
            grayscale_image[i][j] = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
    return grayscale_image

def sobel_edge_detection(grayscale_image):
    height, width = len(grayscale_image), len(grayscale_image[0])
    Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    Gy = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    edge_image = [[0] * width for _ in range(height)]
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            px = sum(Gx[m][n] * grayscale_image[i + m - 1][j + n - 1] for m in range(3) for n in range(3))
            py = sum(Gy[m][n] * grayscale_image[i + m - 1][j + n - 1] for m in range(3) for n in range(3))
            edge_image[i][j] = min(255, int((px**2 + py**2)**0.5))
    return edge_image

def count_black_pixels(image):
    height, width = len(image), len(image[0])
    black_pixel_count = sum(image[i][j] < 128 for i in range(height) for j in range(width))
    return black_pixel_count

def classify_hand(file_path):
    img_array = read_image(file_path)
    grayscale_image = rgb_to_grayscale(img_array)
    edge_image = sobel_edge_detection(grayscale_image)
    black_pixel_count_edge = count_black_pixels(edge_image)
    black_pixel_count_original = count_black_pixels(grayscale_image)
    ratio = black_pixel_count_edge / black_pixel_count_original
    threshold_open = 1.95  # threshold for open hand
    threshold_closed = 1.98  # threshold for closed hand
    if ratio < threshold_open:
        return 'Tangan Terbuka'
    elif ratio > threshold_closed:
        return 'Tangan Tertutup'
    else:
        return 'Unknown'

current_folder = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_folder, 'gambar10.jpg')

print(classify_hand(image_path))