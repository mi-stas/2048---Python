import sys
import random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.gameTableSize = QDesktopWidget().screenGeometry().height() - QDesktopWidget().screenGeometry().height() / 5 # находим ширину и высоту игровой области(4/5 от высоты экрана)
        self.windowSize = self.gameTableSize + self.gameTableSize/10 # находим координаты окна
        windowX = (QDesktopWidget().screenGeometry().width() - self.gameTableSize) / 2 # находим X координту размещения окна
        windowY = self.windowSize / 20 # находим Y координату размещения окна(1/30 от высоты окна)

        QFontDatabase.addApplicationFont('game_shrift.ttf') # открываем игровой шрифт

        self.buttons = []
        for i in range(1, 17):
            self.buttons.append(QPushButton(self)) # добавляем в список 16 кнопок
            self.buttons[i - 1].resize(self.gameTableSize / 4.5, self.gameTableSize / 4.5) # меняем размер под экран
            self.buttons[i - 1].move(self.gameTableSize/4.5/5+self.gameTableSize/4.5 *((i - 1) % 4),
                                     (self.gameTableSize/4.5/5+self.gameTableSize/4.5 *((i - 1) // 4))) # помещаем кнопки в нужные места
            self.buttons[i - 1].setEnabled(False) # делаем кнопки неактивными при нажатии или наведении курсора
            self.buttons[i - 1].setFont(QFont('Panforte Pro', 60)) # устанавливаем шрифт и его размер
            self.buttons[i - 1].hide() # скрываем кнопки

        self.setGeometry(windowX, windowY, self.gameTableSize, self.windowSize) # размещаем окно
        self.setWindowTitle('2048') # задаём назавание окна

        self.play = True # переменная, отвечающая за игровой процесс
        self.score = 0 # очки
        self.label = QLabel("Счёт: 0", self)
        self.label.resize(self.gameTableSize, self.windowSize/10)
        self.label.move(0, self.windowSize-self.windowSize/10)

        self.label.setFont(QFont('Panforte Pro', 50))
        self.label.show()

        newGameAct = QAction(QIcon("new_game.png"), "Новая игра", self)
        newGameAct.triggered.connect(self.newGame)
        recordsAct = QAction(QIcon("records.png"), "Рекорды", self)
        recordsAct.triggered.connect(self.showRecords)
        exitAct = QAction(QIcon("exit.png"),"Выход", self)
        exitAct.triggered.connect(sys.exit)
        menubar = self.menuBar()
        gameMenu = menubar.addMenu("Игра")
        gameMenu.addAction(newGameAct)
        gameMenu.addAction(recordsAct)
        gameMenu.addAction(exitAct)

        self.name = ""
        self.showDialog()

        self.show()  # отображаем окно

        self.gameStep()  # запускаем первый игровой шаг

    def showRecords(self):
        global records # объявляем переменную records глобальной, чтобы окно отобразилось в приложении
        records = QWidget()
        records.resize(self.gameTableSize, self.gameTableSize/2.8) # размеры окна
        records.setWindowTitle("Рекорды")
        scores = [] # в эти списки будем добавлять и обрабатывать данные из файлов
        names = []
        numberOfPlayers = 0 # количество игроков
        topIndexes = [] # переменная, которая отвечает за сортировку имён и очков от 1 до 5 места(в каком порядке расположить переменные из scores и names)
        names_file_r = open("names.txt", "r") # открываем файлы для четния
        scores_file_r = open("scores.txt", "r")


        for line in scores_file_r.readlines(): # переносим информацию из файлов в списки
            if "\n" in line:
                line = line[:len(line)-1]
            scores.append(int(line))
            numberOfPlayers += 1
        for line in names_file_r.readlines():
            if "\n" in line:
                line = line[:len(line)-1]
            names.append(line)
        scoresExample = scores[:]# эта переменная используется для выявления 5 самых больших чисел
        for i in range(numberOfPlayers):
            topIndexes.append(scoresExample.index(max(scoresExample)))# находим наибольшее число и добавляем информацию в topIndexes
            scoresExample.insert(scoresExample.index(max(scoresExample)), 0)# вставляем 0(чтобы при удалении макс. элемента последующие элементы не изменили свою индексацию на -1)
            scoresExample.remove(scoresExample[scoresExample.index(max(scoresExample))])# удаляем максимальный элемент(чтобы в следующем шаге цикла найти счёт, который стоит на ступени ниже)


        if numberOfPlayers > 0: # если кол-во игроков > 0
            top1 = QLabel("1. " + names[topIndexes[0]] + ":   " + str(scores[topIndexes[0]]), records)# создаём надпись
            top1.setFont(QFont('Panforte Pro', 40)) # устанавливаем шрифт и его размер
            if numberOfPlayers > 1:
                top2 = QLabel("2. " + names[topIndexes[1]] + ":   " + str(scores[topIndexes[1]]), records)
                top2.setFont(QFont('Panforte Pro', 35))
                top2.move(0, 70) # помещаем надпись ниже
                if numberOfPlayers > 2:
                    top3 = QLabel("3. " + names[topIndexes[2]] + ":   " + str(scores[topIndexes[2]]), records)
                    top3.setFont(QFont('Panforte Pro', 30))
                    top3.move(0, 125)
                    if numberOfPlayers > 3:
                        top4 = QLabel("4. " + names[topIndexes[3]] + ":   " + str(scores[topIndexes[3]]), records)
                        top4.setFont(QFont('Panforte Pro', 20))
                        top4.move(0, 175)
                        if numberOfPlayers > 4:
                            top5 = QLabel("5. " + names[topIndexes[4]] + ":   " + str(scores[topIndexes[4]]), records)
                            top5.setFont(QFont('Panforte Pro', 18))
                            top5.move(0, 215)
        records.show() # показываем окно

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Имя', 'Введите имя: ')

        if ok: # если нажали да
            self.name = str(text) # заносим значение в переменную
        else: self.name = "unnamed"

    def keyPressEvent(self, event):  # обработка нажатий клавиш
        if event.key() == Qt.Key_Left:
            if self.play: # если идёт игровой процесс:
                self.moveLeft() # двигаемя в нужную сторону
                self.gameStep() # запускаем игровой шаг
        elif event.key() == Qt.Key_Right:
            if self.play:
                self.moveRight()
                self.gameStep()
        elif event.key() == Qt.Key_Up:
            if self.play:
                self.moveUp()
                self.gameStep()
        elif event.key() == Qt.Key_Down:
            if self.play:
                self.moveDown()
                self.gameStep()

    def gameStep(self):  # игровой шаг
        self.label.setText("Очки: " + str(int(self.score)))
        if self.numberOfSquares() < 16:# если есть свободные клетки:
            self.createNewSquare() # создаём новый объект
            self.screenUpdate() # "обновляем" экран
        else:
            if self.freeSteps() == False: # если не осталось ходов
                self.play = False # прерываем игровой процесс
                buttonReply = QMessageBox.question(self, "Вы проиграли!", "Ваш счёт: " + str(int(self.score)) + "\nХотите начать новую игру?", # выводим сообщение
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

                names_file_a = open("names.txt", "a") # открываем файлы для добавления имени и счёта
                scores_file_a = open("scores.txt", "a")

                names_file_a.write(self.name + "\n")
                scores_file_a.write(str(int(self.score)) + "\n")

                if buttonReply == QMessageBox.Yes: # если нажали "Да"
                    self.newGame() # запускаем новую игру

                else:
                    sys.exit() # в другом случае выходим

            else: self.screenUpdate()


    def moveLeft(self, wait = False): # wait - это переменная, которая предотвращает ошибку "слипания блоков"
        for i in range(1,len(self.buttons)): # для каждой кнопки
            if self.buttons[i].text() != "": # если кнопка в данный момент является игровым объектом( и видна игроку )
                if i % 4 != 0: # если на пути объекта нет "стены"
                    if self.buttons[i-1].text() == "": # если клетка на пути движения объекта свободнв
                        while self.buttons[i-1].text() == "": # пока на пути есть свободные клетки
                            self.buttons[i-1].setText(self.buttons[i].text()) # движемся на свободную клетку
                            self.buttons[i].setText("")                       # ( меняем имена объектов )
                            if (i-1) % 4 != 0: # проверяем, не станет ли объект при следующем прохождении цикла перед "стеной".
                                i -= 1         # если это произойдёт, то он попытается перейти барьер
                            else: break        # если мы уже подошли к "стене", прерываем цикл
                    if self.buttons[i].text() == self.buttons[i-1].text() and wait == False: # если объект на пути такой же как и текущий:
                        self.buttons[i-1].setText(str(int(self.buttons[i].text()) * 2)) # "создаём" новый объект
                        self.buttons[i].setText("") # "стираем" старый объъект
                        self.addToScore(self.buttons[i-1]) # обновляем игровые очки
                        wait = True
                    else: wait = False
                else: wait = False
            else: wait = False

    def moveRight(self, wait = False):
        for i in range(len(self.buttons)-2, -1, -1):
            if self.buttons[i].text() != "":
                if (i+1) % 4 != 0:
                    if self.buttons[i+1].text() == "":
                        while self.buttons[i+1].text() == "":
                            self.buttons[i+1].setText(self.buttons[i].text())
                            self.buttons[i].setText("")
                            if (i+2) % 4 != 0:
                                i += 1
                            else: break
                    if self.buttons[i].text() == self.buttons[i+1].text() and wait == False:
                        self.buttons[i+1].setText(str(int(self.buttons[i].text()) * 2))
                        self.buttons[i].setText("")
                        self.addToScore(self.buttons[i+1])
                        wait = True
                    else: wait = False
                else: wait = False
            else: wait = False

    def moveUp(self, wait = False):
        for i in range(4,len(self.buttons)):
            if self.buttons[i].text() != "":
                if i % 4 == 0: # в этом месте кода в вертикальных осях я обрабатываю ошибку,
                    wait = False # когда wait остаётся включенным на границе верхнего и нижнего этажей
                if self.buttons[i-4].text() == "":
                    while self.buttons[i-4].text() == "":
                        self.buttons[i-4].setText(self.buttons[i].text())
                        self.buttons[i].setText("")
                        if (i-4) // 4 != 0:
                            i -= 4
                        else: break
                if self.buttons[i].text() == self.buttons[i-4].text() and wait == False:
                    self.buttons[i-4].setText(str(int(self.buttons[i].text()) * 2))
                    self.buttons[i].setText("")
                    self.addToScore(self.buttons[i-4])
                    wait = True
                else: wait = False
            else: wait = False

    def moveDown(self, wait = False):
        for i in range(len(self.buttons) - 5, -1, -1):
            if self.buttons[i].text() != "":
                if (i + 1) % 4 == 0:
                    wait = False
                if self.buttons[i+4].text() == "":
                    while self.buttons[i+4].text() == "":
                        self.buttons[i+4].setText(self.buttons[i].text())
                        self.buttons[i].setText("")
                        if (i + 4) // 4 - 3 != 0:
                            i += 4
                        else:break
                if self.buttons[i].text() == self.buttons[i+4].text() and wait == False:
                    self.buttons[i+4].setText(str(int(self.buttons[i].text()) * 2))
                    self.buttons[i].setText("")
                    self.addToScore(self.buttons[i+4])
                    wait = True
                else: wait = False
            else: wait = False

    def createNewSquare(self): # создаём новый объект
        newSquare = random.randint(0,15) # расположение объекта
        squareType = random.randint(0,9) # какого типа будет объект(90% - 2, 10% - 4)

        while self.buttons[newSquare].text() != "": # если место занято
            newSquare = random.randint(0, 15)

        if 0 <= squareType <= 8:
            self.buttons[newSquare].setText("2")
        else:self.buttons[newSquare].setText("4")


    def numberOfSquares(self): # считаем количество занятых клеток
        self.squares = 0
        for i in range(len(self.buttons)):
            if self.buttons[i].text() != "": self.squares += 1
        return self.squares

    def freeSteps(self): # проверяем, есть ли свободные ходы( если в цикле попадается 2 одинаковых объекта, то возвращаем True )
        self.steps = 0
        for i in range(4):
            for j in range(i*4+1, i*4+4):
                if self.buttons[j].text() == self.buttons[j-1].text():
                    return True
                    break

        for i in range(4):
            for j in range(i+4, len(self.buttons), 4):
                if self.buttons[j].text() == self.buttons[j-4].text():
                    return True
                    break

        return False

    def screenUpdate(self): # "обновление" экрана
        for i in range(len(self.buttons)):
            if self.buttons[i].text() == "": # если пустое имя кнопки, скрываем её
                self.buttons[i].hide()
            else:
                self.buttons[i].show() #  другом случае, показываем её
                self.setSquareColor(self.buttons[i]) # и задаём цвет

    def addToScore(self, squareType): # обновление очков
        self.score += int(squareType.text()) * 2.5 # формула

    def setSquareColor(self, button): # цвета для кнопок
        if button.text() == "2" or button.text() == "4": button.setStyleSheet("QPushButton {background-color: rgb(238,228,218)}")
        elif button.text() == "8": button.setStyleSheet("QPushButton {background-color: rgb(245,179,119)}")
        elif button.text() == "16": button.setStyleSheet("QPushButton {background-color: rgb(245,149,99)}")
        elif button.text() == "32": button.setStyleSheet("QPushButton {background-color: rgb(245,124,95)}")
        elif button.text() == "64": button.setStyleSheet("QPushButton {background-color: rgb(245,95,60)}")
        elif button.text() == "128": button.setStyleSheet("QPushButton {background-color: rgb(237,206,113)}")
        elif button.text() == "256": button.setStyleSheet("QPushButton {background-color: rgb(237,204,97)}")
        elif button.text() == "512": button.setStyleSheet("QPushButton {background-color: rgb(236,200,80)}")
        elif button.text() == "1024": button.setStyleSheet("QPushButton {background-color: rgb(236,196,62)}")
        elif button.text() == "2048": button.setStyleSheet("QPushButton {background-color: rgb(238,194,46)}")
        else: button.setStyleSheet("QPushButton {background-color: rgb(61,58,51)}")

    def newGame(self):
        self.score = 0  # обнуляем очки
        for i in self.buttons:  # очищаем игровое поле
            i.setText("")
        self.gameStep()  # делаем игровой шаг
        self.play = True  # включаемм игровой процесс

if __name__ == '__main__':
    app = QApplication(sys.argv)
    G = Game()
    sys.exit(app.exec_())