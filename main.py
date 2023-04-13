from gui import *
import sys

app = QtWidgets.QApplication(sys.argv)
gui = GuiMainWindow("Main Window")
gui.show()
sys.exit(app.exec_())
