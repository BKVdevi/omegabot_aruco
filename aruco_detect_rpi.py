#import numpy
import math
import cv2
#import cv2.aruco as aruco
from cv2 import aruco

# Подключение к видеостриму
#cap = cv2.VideoCapture('output_recorded_aruco.avi')
cap = cv2.VideoCapture('rtsp://10.1.100.27:8554/picam_h264')

if not cap.isOpened():
    print("Не удалось открыть видеопоток")
else:
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50) #Стандартный словарь 4x4
    parameters = aruco.DetectorParameters()
    font = cv2.FONT_HERSHEY_SIMPLEX
    check_dictionary = {}
    while True:
        ret, frame = cap.read()  # Чтение кадра из потока
        if not ret:
            break
        # Преобразуем кадр в оттенки серого
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create the ArUco detector
        detector = aruco.ArucoDetector(dictionary, parameters)
        # Распознаём маркеры
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
        

        if not ids is None:
                lenght = 0

                for id in range(0, ids.size):
                    if str(ids.item(id)) not in check_dictionary.keys():
                        check_dictionary[str(ids.item(id))] = [2, 0, 0, 0]
                    else:
                        if check_dictionary[str(ids.item(id))][0] < 50:
                            check_dictionary[str(ids.item(id))][0] = check_dictionary[str(ids.item(id))][0] + 2

                    mesaga = mesaga + str(ids.item(id)) + "("
                    width_x = abs((corners[id][0][0][0] - corners[id][0][2][0]))
                    middle_x = (corners[id][0][0][0] + corners[id][0][2][0])/2
                    middle_y = (corners[id][0][0][1] + corners[id][0][2][1])/2
                    width_y = abs(corners[id][0][0][1] - corners[id][0][2][1])
                    lenght = math.sqrt(pow(width_x,2)+pow(width_y,2))
                    mesaga = mesaga + str(int(middle_x)) + "," + str(int(middle_y)) + "," + str(int(lenght)) + ")"
                    check_dictionary[str(ids.item(id))][1] = int(middle_x)
                    check_dictionary[str(ids.item(id))][2] = int(middle_y)
                    check_dictionary[str(ids.item(id))][3] = int(lenght)

                    if check_dictionary[str(ids.item(id))][0] > 10:
                        cv2.line(frame,(int(corners[id][0][0][0]),int(corners[id][0][0][1])),(int(corners[id][0][1][0]),int(corners[id][0][1][1])),(100,0,0),5)
                        cv2.line(frame,(int(corners[id][0][2][0]),int(corners[id][0][2][1])),(int(corners[id][0][3][0]),int(corners[id][0][3][1])),(0,0,100),5)
                        cv2.line(frame,(int(corners[id][0][0][0]),int(corners[id][0][0][1])),(int(corners[id][0][2][0]),int(corners[id][0][2][1])),(100,100,100),5)

        mesaga = ""   
        for_destroy = []         
        for key in check_dictionary.keys():
            lenght = check_dictionary[key][3]
            middle_x = check_dictionary[key][1]
            middle_y = check_dictionary[key][2]
            check_dictionary[key][0] = check_dictionary[key][0] - 1
            if check_dictionary[key][0] > 10:
                cv2.circle(frame,(int(middle_x),int(middle_y)), int(lenght/10), (255,0,255), -1)
                cv2.putText(frame,key,(int(middle_x),int(middle_y)), font, 4,(255,255,255), 5, cv2.LINE_AA)
                mesaga = mesaga + "(" + key + "," + str(check_dictionary[key]) + ")"
            if check_dictionary[key][0] <= 0:
                for_destroy.append(key)
        for key in for_destroy:
            del check_dictionary[key]
        print(mesaga)
        # Рисуем границы вокруг распознанных маркеров
        #frame = aruco.drawDetectedMarkers(frame, corners, ids)
        cv2.imshow('Video Stream', frame)  # Отображение кадра
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()