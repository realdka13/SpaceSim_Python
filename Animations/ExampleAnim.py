import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np

# -------------------------------
# Physical parameters
# -------------------------------
G = 6.67430e-11  # gravitational constant
time_speed = 5000  # speed-up factor
dt = 10  # simulation timestep in seconds

# Masses
m_earth = 5.972e24
m_moon = 7.348e22

# Initial positions
r_earth = np.array([0.0, 0.0])
r_moon = np.array([384400000.0, 0.0])  # 384,400 km

# Initial velocities (tangential for circular orbit)
v_earth = np.array([0.0, 0.0])
v_moon = np.array([0.0, 1022.0])  # m/s

# Center-of-mass correction
v_com = (m_earth * v_earth + m_moon * v_moon) / (m_earth + m_moon)
v_earth -= v_com
v_moon -= v_com

# Save initial states for reset
init_r_earth = r_earth.copy()
init_v_earth = v_earth.copy()
init_r_moon = r_moon.copy()
init_v_moon = v_moon.copy()

# Trails
trail_length = 500
trail_earth = [r_earth.copy()]
trail_moon = [r_moon.copy()]

# -------------------------------
# PyQtGraph setup
# -------------------------------
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(show=True, title="Earth-Moon Orbit")
plot = win.addPlot(title="Orbit")
plot.setAspectLocked(True)
plot.setXRange(-500, 500)
plot.setYRange(-500, 500)

earth_curve = plot.plot(pen=None, symbol='o', symbolBrush='b', symbolSize=12)
moon_curve = plot.plot(pen=None, symbol='o', symbolBrush='gray', symbolSize=6)
trail_earth_curve = plot.plot(pen=pg.mkPen('b', width=2))
trail_moon_curve = plot.plot(pen=pg.mkPen('gray', width=1))

# -------------------------------
# Info Text Items
# -------------------------------
energy_text = pg.TextItem(text="E: 0", anchor=(0,1))
momentum_text = pg.TextItem(text="h: 0", anchor=(0,1))
plot.addItem(energy_text)
plot.addItem(momentum_text)
energy_text.setPos(-500, 500)
momentum_text.setPos(-500, 450)

# -------------------------------
# Reset button
# -------------------------------
def reset():
    global r_earth, r_moon, v_earth, v_moon, trail_earth, trail_moon
    r_earth[:] = init_r_earth
    v_earth[:] = init_v_earth
    r_moon[:] = init_r_moon
    v_moon[:] = init_v_moon
    trail_earth = [r_earth.copy()]
    trail_moon = [r_moon.copy()]

reset_btn = QtWidgets.QPushButton("Reset")
proxy = pg.QtWidgets.QGraphicsProxyWidget()
proxy.setWidget(reset_btn)
win.addItem(proxy)
reset_btn.clicked.connect(reset)

# -------------------------------
# Update function
# -------------------------------
def update():
    global r_earth, r_moon, v_earth, v_moon, trail_earth, trail_moon

    # Compute gravitational force
    r_vec = r_moon - r_earth
    r_mag = np.linalg.norm(r_vec)
    F = G * m_earth * m_moon * r_vec / r_mag**3
    a_earth = F / m_earth
    a_moon = -F / m_moon

    # Velocity Verlet integration
    v_half_earth = v_earth + 0.5 * a_earth * dt * time_speed
    v_half_moon = v_moon + 0.5 * a_moon * dt * time_speed

    r_earth += v_half_earth * dt * time_speed
    r_moon += v_half_moon * dt * time_speed

    r_vec_new = r_moon - r_earth
    r_mag_new = np.linalg.norm(r_vec_new)
    a_earth_new = G * m_moon * r_vec_new / r_mag_new**3
    a_moon_new = -G * m_earth * r_vec_new / r_mag_new**3

    v_earth[:] = v_half_earth + 0.5 * a_earth_new * dt * time_speed
    v_moon[:] = v_half_moon + 0.5 * a_moon_new * dt * time_speed

    # Update trails
    trail_earth.append(r_earth.copy())
    trail_moon.append(r_moon.copy())
    trail_earth = trail_earth[-trail_length:]
    trail_moon = trail_moon[-trail_length:]

    # Update plots (scaled for visualization)
    scale = 1e6
    earth_curve.setData([r_earth[0]/scale], [r_earth[1]/scale])
    moon_curve.setData([r_moon[0]/scale], [r_moon[1]/scale])
    trail_earth_curve.setData(np.array(trail_earth)[:,0]/scale, np.array(trail_earth)[:,1]/scale)
    trail_moon_curve.setData(np.array(trail_moon)[:,0]/scale, np.array(trail_moon)[:,1]/scale)

    # Compute specific orbital energy and angular momentum
    v_rel = v_moon - v_earth
    r_rel = r_moon - r_earth
    mu = G * (m_earth + m_moon)
    E = 0.5 * np.linalg.norm(v_rel)**2 - mu / np.linalg.norm(r_rel)   # specific orbital energy
    h = np.cross(r_rel, v_rel)                                         # specific angular momentum

    # Update text
    energy_text.setText(f"E: {E:.2e}")
    momentum_text.setText(f"h: {h:.2e}")

# -------------------------------
# Timer
# -------------------------------
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)  # ~100 FPS

# Run the Qt event loop
QtWidgets.QApplication.instance().exec()



#import sys
#from PyQt6 import QtWidgets, QtCore
#import pyqtgraph as pg
#import numpy as np

#Instantiate pyqtgraph
#app = QtWidgets.QApplication(sys.argv)

#Create window
#win = pg.PlotWidget()
#win.show()

#Graph Setup
#x = np.linspace(0, 2*np.pi, 200)
#phase = 0
#curve = win.plot(x, np.sin(x))

#Graph Animation
#def update():
#    global phase
#    phase += 0.1
#    y = np.sin(x + phase)
#    curve.setData(x, y)



#Animation Timer
#timer = QtCore.QTimer()
#timer.timeout.connect(update)
#timer.start(16)  # ~60 FPS

#Run Graph
#sys.exit(app.exec())