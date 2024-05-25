from handDetection import HandDetection

import cv2
# Membuat objek HandDetection dengan parameter deteksi dan pelacakan minimal 0.5.
handDetection = HandDetection(min_detection_confidence=0.5, min_tracking_confidence=0.5)

webcam = cv2.VideoCapture() # menggunakan OpenCV untuk membuka kamera dan menangkap video secara real-time
webcam.open(0, cv2.CAP_DSHOW)# mengakses webcam dengan ID 0, dan cv2.CAP_DSHOW adalah flag untuk DirectShow, yang merupakan framework untuk multimedia di Windows

# Loop terus menerus untuk membaca frame dari webcam
while True:
    status, frame = webcam.read() # membaca frame dari webcam
    frame = cv2.flip(frame, 1) # membalik gambar secara horizontal untuk membuatnya terlihat lebih natural, seperti melihat cermin
    handLandMarks = handDetection.findHandLandMarks(image=frame, draw=True) # untuk mendeteksi landmark tangan pada frame. Fungsi findHandLandMarks mengidentifikasi titik-titik kunci di tangan dan menggambar landmark tersebut jika draw=True

    # Periksa apakah tangan terdeteksi
    # Percabangan ini menghitung jumlah jari yang terbuka. Ibu jari dihitung dengan membandingkan posisi landmark 4 dan 3. 
    # Jari lainnya dihitung dengan membandingkan posisi landmark terkait, misalnya untuk jari telunjuk, dibandingkan antara landmark 8 dan 6. 
    # Jari dianggap terbuka jika landmark atas lebih tinggi daripada landmark bawah
    if handLandMarks:
        # Dapatkan jumlah jari yang terbuka
        fingers = []
        # Bagian ini memeriksa posisi x dari ujung ibu jari (handLandMarks[4][1]) dan membandingkannya dengan posisi x dari sendi ibu jari (handLandMarks[3][1]). 
        # Jika posisi x ujung ibu jari lebih besar (yang berarti ibu jari terangkat ke samping), maka ibu jari dihitung sebagai terangkat (1), jika tidak maka dihitung sebagai tidak terangkat (0).
        if handLandMarks[4][1] > handLandMarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Loop ini digunakan untuk mendeteksi jari telunjuk, jari tengah, jari manis, dan jari kelingking. Dalam loop ini, id berjalan dari 1 hingga 4:
        # handLandMarks[5*id][2] adalah posisi y dari ujung jari.
        # handLandMarks[4*id - 2][2] adalah posisi y dari sendi jari.
        # Jika posisi y ujung jari lebih kecil (lebih tinggi) daripada posisi y sendi jari, maka jari tersebut dianggap terangkat (1), jika tidak maka dianggap tidak terangkat (0).
        for id in range(1, 5):
            if handLandMarks[5*id][2] < handLandMarks[4*id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Hitung jumlah jari yang terbuka
        fingerCount = fingers.count(1)
       
        
        # Tambahkan penanganan penutupan tangan
        # Berdasarkan jumlah jari yang terbuka, kode ini menampilkan status "Tangan Terbuka" jika empat atau lebih jari terbuka, 
        # dan "Tangan Menutup" jika kurang dari empat jari terbuka. cv2.putText digunakan untuk menambahkan teks ini pada frame.
        if fingerCount >= 4:
            # print("Tangan Terbuka")
            k="Tangan Terbuka"
            cv2.putText(frame, k, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # print("Tangan Menutup")
            k="Tangan Menutup"
            cv2.putText(frame, k, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("hand Landmark", frame) # menampilkan frame dengan teks yang ditambahkan
    # Program akan terus berjalan hingga tombol 'a' ditekan, yang akan mengakhiri loop, menutup semua jendela OpenCV, dan melepaskan kamera.
    if cv2.waitKey(1) == ord('a'):
        break

cv2.destroyAllWindows() # ini digunakan untuk menutup semua jendela yang telah dibuka oleh OpenCV
webcam.release() # ini digunakan untuk melepaskan objek kamera yang sedang digunakan