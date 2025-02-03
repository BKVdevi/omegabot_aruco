import math
import cv2
from cv2 import aruco
import threading
import time



class omegabot_aruco:

    def __init__(self, video_input = 0):
        self.input = video_input
        self.check_dictionary = {}
        self.dictionary_lock = threading.Lock()
        self.task = threading.Thread(target=self.bot_aruco_recog, daemon=True)
        self.task.start()
        if self.task.is_alive():
            print("CV started")
        pass

    def __del__(self):
        self.task.join()
        self.cap.release()
        cv2.destroyAllWindows()

    def bot_aruco_recog(self):
        # Подключение к видеостриму
        self.cap = cv2.VideoCapture(self.input)
        #self.cap = cv2.VideoCapture('output_recorded_aruco.avi')
        #cap = cv2.VideoCapture('rtsp://10.1.100.42:8554/picam_h264')

        if not self.cap.isOpened():
            print("Не удалось открыть видеопоток")
        else:
            dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50) #Стандартный словарь 4x4
            parameters = aruco.DetectorParameters()
            font = cv2.FONT_HERSHEY_SIMPLEX
            while True:
                ret, frame = self.cap.read()  # Чтение кадра из потока
                if not ret:
                    break
                # Преобразуем кадр в оттенки серого
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Create the ArUco detector
                detector = aruco.ArucoDetector(dictionary, parameters)
                # Распознаём маркеры
                corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
                
                self.dictionary_lock.acquire()
                if not ids is None:
                        lenght = 0

                        for id in range(0, ids.size):
                            if str(ids.item(id)) not in self.check_dictionary.keys():
                                self.check_dictionary[str(ids.item(id))] = [2, 0, 0, 0]
                            else:
                                if self.check_dictionary[str(ids.item(id))][0] < 50:
                                    self.check_dictionary[str(ids.item(id))][0] = self.check_dictionary[str(ids.item(id))][0] + 2

                            mesaga = mesaga + str(ids.item(id)) + "("
                            width_x = abs((corners[id][0][0][0] - corners[id][0][2][0]))
                            middle_x = (corners[id][0][0][0] + corners[id][0][2][0])/2
                            middle_y = (corners[id][0][0][1] + corners[id][0][2][1])/2
                            width_y = abs(corners[id][0][0][1] - corners[id][0][2][1])
                            lenght = math.sqrt(pow(width_x,2)+pow(width_y,2))
                            mesaga = mesaga + str(int(middle_x)) + "," + str(int(middle_y)) + "," + str(int(lenght)) + ")"
                            self.check_dictionary[str(ids.item(id))][1] = int(middle_x)
                            self.check_dictionary[str(ids.item(id))][2] = int(middle_y)
                            self.check_dictionary[str(ids.item(id))][3] = int(lenght)

                            #if self.check_dictionary[str(ids.item(id))][0] > 10:
                                #cv2.linine(frame,(int(corners[id][0][0][0]),int(corners[id][0][0][1])),(int(corners[id][0][1][0]),int(corners[id][0][1][1])),(100,0,0),5)
                                #cv2.linine(frame,(int(corners[id][0][2][0]),int(corners[id][0][2][1])),(int(corners[id][0][3][0]),int(corners[id][0][3][1])),(0,0,100),5)
                                #cv2.linine(frame,(int(corners[id][0][0][0]),int(corners[id][0][0][1])),(int(corners[id][0][2][0]),int(corners[id][0][2][1])),(100,100,100),5)

                mesaga = ""   
                for_destroy = []         
                for key in self.check_dictionary.keys():
                    lenght = self.check_dictionary[key][3]
                    middle_x = self.check_dictionary[key][1]
                    middle_y = self.check_dictionary[key][2]
                    self.check_dictionary[key][0] = self.check_dictionary[key][0] - 1
                    if self.check_dictionary[key][0] > 10:
                        #cv2.circle(frame,(int(middle_x),int(middle_y)), int(lenght/10), (255,0,255), -1)
                        #cv2.putText(frame,key,(int(middle_x),int(middle_y)), font, 4,(255,255,255), 5, #cv2.linINE_AA)
                        mesaga = mesaga + "(" + key + "," + str(self.check_dictionary[key]) + ")"
                    if self.check_dictionary[key][0] <= 0:
                        for_destroy.append(key)
                for key in for_destroy:
                    del self.check_dictionary[key]
                self.dictionary_lock.release()
                #print(mesaga)
                # Рисуем границы вокруг распознанных маркеров
                #frame = aruco.drawDetectedMarkers(frame, corners, ids)
                #cv2.imshow('Video Stream', frame)  # Отображение кадра


    #Функция проверки наличия маркера в поле зрения
    def is_aruco_visible(self):
        time.sleep(0.1) #Задержка на случай члишком частого вызова
        self.dictionary_lock.acquire()
        if len(self.check_dictionary) > 0:
            for key in self.check_dictionary.keys():
                if self.check_dictionary[key][0] > 10:
                    self.dictionary_lock.release()
                    return True
            self.dictionary_lock.release()
            return False
        else:
            self.dictionary_lock.release()
            return False

    #Функция для прлучения массива аруко маркеров
    def get_aruco_markers(self):
        self.dictionary_lock.acquire()
        if len(self.check_dictionary) > 0:
            markers = {}
            for key in self.check_dictionary.keys():
                if self.check_dictionary[key][0] > 10:
                    markers[key] = [self.check_dictionary[key][1], self.check_dictionary[key][2], self.check_dictionary[key][3]]
            self.dictionary_lock.release()
            return markers
        else:
            self.dictionary_lock.release()
            return None
        
        
if __name__ == "__main__":
    try:
        recog_aruco = omegabot_aruco('output_recorded_aruco.avi')
        while True:
            if recog_aruco.is_aruco_visible() == True:
                markers = recog_aruco.get_aruco_markers()
                print(markers)
                break
    except KeyboardInterrupt:
        print("CV end")
