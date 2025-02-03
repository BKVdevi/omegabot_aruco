Простая реализация класа для работы робота с Aruco метками.

Убедитесь, что у вас установлены следующие библиотеки:
- OpenCV (cv2)
- Аруко-библиотека для OpenCV (aruco)
Вы можете установить их через pip:
```
pip install opencv-python
pip install opencv-contrib-python
```
Подключите файл к своему Python скрипту
```
from aruco_api_rpi import omegabot_aruco
```
Создайте экземпляр класса и передайте адерес источника видео
```
recog_aruco = omegabot_aruco('output_recorded_aruco.avi')
```

 Теперь вы можете пользоваться функциями
 ```
recog_aruco.is_aruco_visible()
recog_aruco.get_aruco_markers()
```
is_aruco_visible - проверяет видит ли робот  метку возвращате true или false
get_aruco_markers - возвращет словарь ключем которого является номер метки,
а значением массив содержащий [0]позиция центра маркера в камере по X,
[1]позиция центра маркера в камере по Y, [2] Длинна диаголнали маркера(можно примерно определить его размер на изображении)
