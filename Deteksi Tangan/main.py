from handDetection import HandDetection

import cv2

handDetection = HandDetection(min_detection_confidence=0.5, min_tracking_confidence=0.5)

webcam = cv2.VideoCapture()
webcam.open(0, cv2.CAP_DSHOW)

while True:
    status, frame = webcam.read()
    frame = cv2.flip(frame, 1)
    handLandMarks = handDetection.findHandLandMarks(image=frame, draw=True)

    # Periksa apakah tangan terdeteksi
    if handLandMarks:
        # Dapatkan jumlah jari yang terbuka
        fingers = []
        if handLandMarks[4][1] > handLandMarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if handLandMarks[5*id][2] < handLandMarks[4*id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Hitung jumlah jari yang terbuka
        fingerCount = fingers.count(1)
        cv2.putText(frame, str(fingerCount), (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
       
        
        # Tambahkan penanganan penutupan tangan
        if fingerCount >= 4:
            # print("Tangan Terbuka")
            k="Tangan Terbuka"
            cv2.putText(frame, k, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # print("Tangan Menutup")
            k="Tangan Menutup"
            cv2.putText(frame, k, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("hand Landmark", frame)
    if cv2.waitKey(1) == ord('a'):
        break

cv2.destroyAllWindows()
webcam.release()