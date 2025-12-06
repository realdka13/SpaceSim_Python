import sys
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np

#Instantiate pyqtgraph
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

#Add Orbital Space
layout = QtWidgets.QHBoxLayout(window)                      #Hbox to hold all elements
orbitalSpace = pg.PlotWidget()
orbitalSpace.setAspectLocked(True)
orbitalSpace.enableAutoRange(False)
layout.addWidget(orbitalSpace)

#Orbital Space Setup
x = np.linspace(0, 2*np.pi, 200)

#Add Controls
controls = QtWidgets.QWidget()
controlsLayout = QtWidgets.QVBoxLayout(controls)            #Vbox to contain all controls
controlsLayout.setSpacing(5)                                #Vertical spacing
controlsLayout.setContentsMargins(0, 0, 0, 0)
textBoxes = []
for i in range(5):
    label = QtWidgets.QLabel(f"Label {i+1}")                #Labels
    tbox = QtWidgets.QLineEdit()
    tbox.setPlaceholderText(f"Box {i+1}")
    controlsLayout.addWidget(label)
    controlsLayout.addWidget(tbox)
    textBoxes.append(tbox)
layout.addWidget(controls)

#Controls Setup
#****************

#Add Bodies
body1 = pg.ScatterPlotItem([0], [0], size=30, brush='r')
body2 = pg.ScatterPlotItem([0], [5], size=10, brush='b')
orbitalSpace.addItem(body1)
orbitalSpace.addItem(body2)





#Animation
def update():
    pass





#Animation Timer
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(16)  # ~60 FPS

#Run Graph
window.show()
sys.exit(app.exec())