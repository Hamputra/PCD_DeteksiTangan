import os
import numpy as np
from PIL import Image

# Membaca gambar dan mengubahnya menjadi array dua dimensi dari nilai piksel
def read_image(file_path): 
    img = Image.open(file_path)# Membuka gambar dari path file yang diberikan
    width, height = img.size # Mendapatkan lebar dan tinggi gambar
    pixels = list(img.getdata()) # Mendapatkan daftar nilai piksel dari gambar
    img_array = [[pixels[i * width + j] for j in range(width)] for i in range(height)] # Mengonversi daftar piksel menjadi array 2D yang mewakili gambar
    return img_array # Mengembalikan array 2D dari gambar

# Mengubah gambar RGB menjadi gambar skala abu-abu.
def rgb_to_grayscale(image):
    height, width = len(image), len(image[0])
    grayscale_image = [[0] * width for _ in range(height)] # Inisialisasi array 2D untuk menyimpan nilai grayscale
    for i in range(height): # Iterasi melalui setiap piksel, menghitung nilai grayscale berdasarkan komponen RGB menggunakan rumus yang ditentukan
        for j in range(width):
            r, g, b = image[i][j]
            grayscale_image[i][j] = int(0.2989 * r + 0.5870 * g + 0.1140 * b) #Mengubah gambar RGB menjadi gambar skala abu-abu.
    return grayscale_image # Mengembalikan array 2D dari gambar grayscale

#Menerapkan blur Gaussian sederhana dengan rata-rata kotak 5x5.
def apply_gaussian_blur(grayscale_image):
    height, width = len(grayscale_image), len(grayscale_image[0])
    blurred_image = [[0] * width for _ in range(height)] # menyimpan array 2D dari gambar yang telah di blur
    for i in range(height):
        for j in range(width):
            sum_val = 0
            for m in range(-2, 3):
                for n in range(-2, 3):
                    if 0 <= i + m < height and 0 <= j + n < width:
                        sum_val += grayscale_image[i + m][j + n]
            blurred_image[i][j] = int(sum_val / 25) #Menggunakan rata-rata nilai piksel dalam jendela 5x5
    return blurred_image 

#Mendeteksi tepi menggunakan algoritma Sobel
def sobel_edge_detection(blurred_image):
    height, width = len(blurred_image), len(blurred_image[0])
    Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]] # untuk deteksi tepi horizontal
    Gy = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]] # untuk deteksi tepi vertikal
    edge_image = [[0] * width for _ in range(height)] #menyimpan array 2D dari gambar yang telah dilakukan deteksi tepi
    for i in range(1, height - 1): # iterasi untuk menghitung gradien gambar
        for j in range(1, width - 1):
            px = sum(Gx[m][n] * blurred_image[i + m - 1][j + n - 1] for m in range(3) for n in range(3))
            py = sum(Gy[m][n] * blurred_image[i + m - 1][j + n - 1] for m in range(3) for n in range(3))
            edge_image[i][j] = min(255, int((px**2 + py**2)**0.5))
    return edge_image

#Menghitung jumlah piksel hitam (nilai kurang dari 128)
def count_black_pixels(image):
    height, width = len(image), len(image[0])
    black_pixel_count = sum(image[i][j] < 128 for i in range(height) for j in range(width)) #Jumlah piksel hitam
    return black_pixel_count
 
 #Menampilkan gambar proses pengolahan citra
def display_image(image, title):
    img = Image.fromarray(np.array(image, dtype=np.uint8))
    img.show(title)

# Mengklasifikasikan gambar tangan apakah terbuka atau tertutup
def classify_hand(file_path):
    img_array = read_image(file_path) # membaca gambar dan mengubahnya menjadi array
    grayscale_image = rgb_to_grayscale(img_array) # Mengkonversi ke grayscale 
    display_image(grayscale_image, 'Grayscale Image')
    blurred_image = apply_gaussian_blur(grayscale_image) #Menerapkan blur Gaussian
    display_image(blurred_image, 'Blurred Image')
    edge_image = sobel_edge_detection(blurred_image) # Mendeteksi tepi dan menampilkan gambar
    display_image(edge_image, 'Edge Image')
    black_pixel_count_edge = count_black_pixels(edge_image)
    black_pixel_count_original = count_black_pixels(grayscale_image)
    ratio = black_pixel_count_edge / black_pixel_count_original # Menghitung jumlah piksel hitam pada gambar tepi dan gambar asli.
    threshold_open = 1.95  # Menghitung rasio dan mengklasifikasikan berdasarkan threshold.
    threshold_closed = 1.98  
    if ratio < threshold_open:
        return 'Tangan Terbuka'
    elif ratio > threshold_closed:
        return 'Tangan Tertutup'
    else:
        return 'Unknown'

current_folder = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_folder, 'gambar1.jpg')

print(classify_hand(image_path))