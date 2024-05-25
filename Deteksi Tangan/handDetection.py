#library open cv2 digunakan untuk pemrosesan gambar, sementara mediapipe digunakan untuk untuk deteksi tangan  
import mediapipe as mp
import cv2


mpHands = mp.solutions.hands # mengakses solusi deteksi tangan dari mediapipe
mpDraw = mp.solutions.drawing_utils # Mengakses utilitas gambar dari MediaPipe untuk menggambar landmark dan koneksinya.

# max_num_hands: Batas maksimum jumlah tangan yang dideteksi.
# min_detection_confidence: Kepercayaan minimum untuk mendeteksi tangan.
# min_tracking_confidence: Kepercayaan minimum untuk melacak tangan yang sudah terdeteksi.
class HandDetection:
    def __init__(self,max_num_hands=2,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        self.hands = mpHands.Hands(max_num_hands=max_num_hands,min_detection_confidence=min_detection_confidence,
                            min_tracking_confidence=min_tracking_confidence)


    def findHandLandMarks(self,image,handNumber=0,draw=False):
            originalImage = image # Menyimpan citra asli
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # Mengonversi citra dari format BGR ke RGB, karena MediaPipe menggunakan format RGB.
            results = self.hands.process(image) # kemudian di proses menggunakan self.hands

            landMarkList = []
            # Jika terdapat landmark tangan yang terdeteksi, 
            # metode ini akan mengekstrak posisi setiap landmark dan menyimpannya dalam landMarkList. 
            # Jika parameter draw adalah True, gambar tangan dan koneksinya akan digambar pada originalImage.
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[handNumber] # Mengandung informasi deteksi landmark tangan
                for id,landMark in enumerate(hand.landmark): # perulangan untuk setiap landmark tangan
                    imgH,imgW,imgC = originalImage.shape # mendapatkan tinggi, lebar dari citra asli
                    xPos,yPos = int(landMark.x*imgW),int(landMark.y*imgH) # Mengonversi koordinat relatif dari landmark menjadi koordinat piksel absolut pada citra asli.
                    landMarkList.append([id,xPos,yPos]) # Menyimpan ID dan posisi landmark dalam daftar
                if draw: # menggambar landmark dan koneksi pada citra asli menggunakan mpDraw.draw_landmarks
                    mpDraw.draw_landmarks(originalImage,hand,mpHands.HAND_CONNECTIONS)

            return landMarkList 
    
# Inisialisasi Hands: Mengatur parameter deteksi dan pelacakan tangan
# Konversi Warna: Mengonversi citra dari BGR ke RGB
# Pemrosesan Deteksi: Memproses citra untuk mendeteksi tangan dan landmark
# Ekstraksi Landmark: Menyimpan posisi landmark tangan dalam koordinat piksel
# Visualisasi: Opsi untuk menggambar landmark pada citra asli