from PyQt6 import QtWidgets, QtCore, QtGui
import sys, os
from Weather import weather_data
from config import BASE_DIR


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.setWindowFlag(QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowOpacity(0.9)
        self.resize(500, 500)
        pixmap = QtGui.QPixmap(os.path.join(BASE_DIR, "images/weather_back_r2.png"))
        pal = self.palette()
        pal.setBrush(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Window, QtGui.QBrush(pixmap))
        pal.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, QtGui.QBrush(pixmap))
        self.setPalette(pal)
        self.setMask(pixmap.mask())
        self.move(self.width() * -2, 0)

        self.button_exit = QtWidgets.QPushButton("Выход", self)
        self.button_exit.setStyleSheet("QPushButton {\n"
                                       "    background-color: #82a2ff;\n"
                                       "    border-radius: 6;\n"
                                       "    color: white\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed {\n"
                                       "    background-color: #4b6ed3\n"
                                       "}")
        font = QtGui.QFont()
        font.setFamily("Rubik Bubbles")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(20)
        self.button_exit.setFont(font)
        self.button_exit.move(220, 20)
        self.button_exit.resize(70, 20)
        self.button_exit.clicked.connect(QtWidgets.QApplication.instance().quit)

        font1 = QtGui.QFont()
        font1.setFamily("Rubik Bubbles")
        font1.setPointSize(10)
        font1.setWeight(5)
        self.button_enter_city = QtWidgets.QPushButton("Узнать погоду", self)
        self.button_enter_city.setStyleSheet("QPushButton {\n"
                                             "    background-color: #82a2ff;\n"
                                             "    border-radius: 6;\n"
                                             "    color: white\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:pressed {\n"
                                             "    background-color: #4b6ed3\n"
                                             "}")
        self.button_enter_city.setFont(font1)
        self.button_enter_city.move(200, 85)
        self.button_enter_city.resize(110, 19)
        self.button_enter_city.clicked.connect(self.choice_city)

        self.city_selector = QtWidgets.QLineEdit(self)
        self.city_selector.setPlaceholderText("Введите город")
        self.city_selector.resize(162, 25)
        self.city_selector.move(170, 50)
        self.city_selector.setFont(font)
        self.city_selector.setFrame(False)
        self.city_selector.setWindowOpacity(0.9)
        self.city_selector.setStyleSheet("QLineEdit {\n"
                                         "    background-color: #ced1fe;\n"
                                         "    border-radius: 8;\n"
                                         "    color: white\n"
                                         "}")
        self.city_selector.setValidator(
            QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression("^[А-ЯЁ][а-яё]*(?:\s[А-Яа-я]+)*(?:-[А-Яа-я]+)*$")))

        self.forecact_info = QtWidgets.QLabel(self)
        self.forecact_info.resize(270, 90)
        self.forecact_info.move(130, 115)
        self.forecact_info.setFont(font)
        self.forecact_info.setWindowOpacity(0.9)
        self.forecact_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.forecact_info.setStyleSheet("QLabel {\n"
                                         "    border-radius: 8;\n"
                                         "    color: white\n"
                                         "}")

        self.uv_info = QtWidgets.QLabel(self)
        self.uv_info.resize(160, 90)
        self.uv_info.move(170, 265)
        self.uv_info.setFont(font)
        self.uv_info.setWindowOpacity(0.9)
        self.uv_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.uv_info.setStyleSheet("QLabel {\n"
                                   "    border-radius: 8;\n"
                                   "    color: white\n"
                                   "}")

        self.sunrise = QtWidgets.QLabel(self)
        self.sunrise.resize(150, 50)
        self.sunrise.move(50, 320)
        self.sunrise.setFont(font)
        self.sunrise.setWindowOpacity(0.9)
        self.sunrise.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.sunrise.setStyleSheet("QLabel {\n"
                                   "    border-radius: 8;\n"
                                   "    color: white\n"
                                   "}")

        self.sunset = QtWidgets.QLabel(self)
        self.sunset.resize(150, 50)
        self.sunset.move(300, 320)
        self.sunset.setFont(font)
        self.sunset.setWindowOpacity(0.9)
        self.sunset.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.sunset.setStyleSheet("QLabel {\n"
                                  "    border-radius: 8;\n"
                                  "    color: white\n"
                                  "}")

    def choice_city(self):
        if self.city_selector.text():
            try:
                forecast = weather_data.data_weather(self.city_selector.text())
                self.forecact_info.setText(
                    "За окном:\n{}\n{}°\n{} м/с".format(forecast["status"], forecast["temp"], forecast["wind"]))
                self.uv_info.setText("УФ:\n{}".format(forecast["uv"]))

                self.sunrise.setText("Восход в \n{}".format(forecast["sunrise"].strftime("%H:%M")))
                self.sunset.setText("Закат в \n{}".format(forecast["sunset"].strftime("%H:%M")))
            except FileNotFoundError:
                self.forecact_info.setText("Попробуйте другое\nназвание")
            except ConnectionError:
                self.forecact_info.setText("Проверьте соединение")
            except ImportError:
                self.forecact_info.setText("Проверьте ваш API key")
            except Exception:
                self.forecact_info.setText("Что-то пошло не так")

        else:
            self.forecact_info.setText("Введите название\nгорода")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()

    screen_size = window.screen().availableSize()
    x = (screen_size.width() - window.frameSize().width()) // 2
    y = (screen_size.height() - window.frameSize().height()) // 2
    window.move(x, y)
    sys.exit(app.exec())
