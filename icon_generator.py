from PyQt5 import QtWidgets, QtGui, QtCore
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel()
        self.gridLayout.addWidget(self.label)

        self.edit = QtWidgets.QPlainTextEdit()
        self.edit.setPlainText('308W\n175grn')
        self.edit.setMaximumWidth(64)
        self.edit.setMaximumHeight(64)
        self.gridLayout.addWidget(self.edit)

        self.size_sb = QtWidgets.QSpinBox()
        self.size_sb.setMinimum(6)
        self.size_sb.setMaximum(20)
        self.size_sb.setSingleStep(1)
        self.size_sb.setValue(12)
        self.gridLayout.addWidget(self.size_sb)

        self.stretch = QtWidgets.QComboBox()

        stretchs = {
            'Unstretched': 100,
            'SemiCondensed': 87,
            'Condensed': 75,
            'ExtraCondensed': 62,
            'UltraCondensed': 50,
        }

        for k, v in stretchs.items():
            self.stretch.addItem(k, v)
        self.gridLayout.addWidget(self.stretch)

        self.font_cb = QtWidgets.QComboBox()
        self.families = ['Arial Narrow', 'MS UI Gothic', 'Times New Roman', 'MS Gothic', 'default']

        self.font_cb.addItems(self.families)
        self.font_cb.setCurrentIndex(self.font_cb.findText('Arial Narrow'))
        self.gridLayout.addWidget(self.font_cb)

        self.save = QtWidgets.QPushButton('Save')
        self.gridLayout.addWidget(self.save)

        self.label2 = QtWidgets.QLabel()
        self.label2.setText("Recomended:\nArial Narrow, 12px, for 2 rows\nMS UI Gothic, 12px, for 3 rows")
        self.gridLayout.addWidget(self.label2)

        MainWindow.setCentralWidget(self.centralwidget)


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.generate_icon()

        self.edit.textChanged.connect(self.generate_icon)
        self.size_sb.valueChanged.connect(self.generate_icon)
        self.stretch.currentIndexChanged.connect(self.generate_icon)
        self.font_cb.currentIndexChanged.connect(self.generate_icon)

        self.save.clicked.connect(self.save_bmp)

    def save_bmp(self):
        text = self.edit.toPlainText()
        filename = '_'.join(text.split('\n')) + '.bmp'
        self.label.pixmap().save(filename, 'BMP')

    def generate_icon(self):
        text = self.edit.toPlainText()

        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtCore.Qt.white)
        self.label.setPixmap(pixmap)

        painter = QtGui.QPainter(self.label.pixmap())
        rows = text.split('\n')
        row_count = len(rows)
        row_size = int(32 / row_count)

        selected_font = self.font_cb.currentText()
        if selected_font == 'default':
            font = QtGui.QFont()
        else:
            font = QtGui.QFont(selected_font)

        font.setStretch(self.stretch.currentData())

        font.setPixelSize(self.size_sb.value())
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        painter.setFont(font)

        if row_count == 2:
            for i in range(1, row_count):
                painter.drawLine(0, int(row_size * i), 32, int(row_size * i))
                painter.drawLine(0, int(row_size * i) + 1, 32, int(row_size * i) + 1)

        for i, r in enumerate(rows):
            rect = QtCore.QRect(0, int(row_size * i), 32, row_size)
            painter.drawText(rect, QtCore.Qt.AlignCenter, rows[i])


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.setWindowIcon(QtGui.QIcon('Icon.png'))
    app.exec_()


if __name__ == '__main__':
    main()
