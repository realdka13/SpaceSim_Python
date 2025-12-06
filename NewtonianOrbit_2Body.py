#Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox, CheckButtons
import matplotlib.gridspec as gridspec
from Utils.Trails import TrailManager
import time


##### Simulation Settings Start #####
#Time settings
timeSpeedMultiplier = 1 #For slowing or increasing rate of time
simTime = 0.0           #simulation time in seconds
running = True          #For Start/Pause
lastUpdateTime = None

update_interval = 0.5   # seconds between text box updates
last_text_update = 0.0
last_E_display = None
last_h_display = None

#Constants
G = 50.0   #Gravitational Constant

#Bodies
    #Body1
r1 = np.array([-20.0, 20.0])  # Initial position of body 1
v1 = np.array([7.0, 5.0])  # Initial velocity of body 1
m1 = 100.0                    # Mass of body 1

    #Body 2
r2 = np.array([20.0, -20.0])   # Initial position of body 2
v2 = np.array([-10.0, -4.0])# Initial velocity of body 2
m2 = 1000.0                    # Mass of body 2
##### Simulation Settings End #####





#####  Figure Start #####
#Plot Settings
fig = plt.figure(figsize=(12, 8))
fig.subplots_adjust(bottom=0.3)
gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1.5], wspace=0.3)


axis = fig.add_subplot(gs[0])
axis.set_xlim(-100, 100)
axis.set_ylim(-100, 100)
axis.set_title("Visualization")

axis2 = fig.add_subplot(gs[1])
axis2.grid(True)
axis2.set_xlabel("Time")
axis2.set_xticklabels([])
axis2.set_ylabel("Velocity")
axis2.set_title("Velocity vs Time")

#Plots for Each Body
body1Plot, = axis.plot([], [], marker='o', linestyle='', markersize=6, color='red')
body2Plot, = axis.plot([], [], marker='o', linestyle='', markersize=6, color='blue')

#Trail Plots
trail1Plot, = axis.plot([], [], color='red', linewidth=1)
trail2Plot, = axis.plot([], [], color='blue', linewidth=1)

#Velocities
body1VelPlot, = axis2.plot([], [], color='red', linewidth=1)
body2VelPlot, = axis2.plot([], [], color='blue', linewidth=1)
#####  Figure End #####





##### Additional Features Start #####
#Trails
trailManager = TrailManager(max_length=1000)
trailManager.add_body('body1', r1)
trailManager.add_body('body2', r2)

#Velocity
maxVelHistory = 500
vel1History = [np.linalg.norm(v1)]
vel2History = [np.linalg.norm(v2)]
timeHistory = [0] 
##### Additional Features End #####





#Changes to make every frame
def UpdateFrame(frame):
    global r1, r2, v1, v2 
    global trail1Plot, trail2Plot, trailManager
    global vel1History, vel2History, timeHistory
    global simTime, lastUpdateTime, last_text_update, last_E_display, last_h_display

    #Calculate Time Elapsed
    now = time.time()
    if lastUpdateTime is None:
        lastUpdateTime = now
    true_dt = now - lastUpdateTime
    lastUpdateTime = now

    #Control Sim Time
    if running:
        sim_dt = true_dt * timeSpeedMultiplier
        simTime += sim_dt

    else:
        sim_dt = 0

    #Run Sim
    if sim_dt > 0:
        #Calculate Force vectors Fg
        r12 = r2 - r1                                           #Vector from body 1 to body 2
        Fg = ((G * m1 * m2) * (r12)) / (np.linalg.norm(r12) ** 3)    #This is relative to body 1

        #Calculate acceleration vectors
        a1 = Fg / m1
        a2 = -Fg / m2

        ## Velocity Verlot Integration Start
        vHalf1 = v1 + 0.5 * a1 * sim_dt                      #Calculate Half Time Step
        vHalf2 = v2 + 0.5 * a2 * sim_dt                      #Calculate Half Time Step

        r1 = r1 + vHalf1 * sim_dt                            #Calculate new position
        r2 = r2 + vHalf2 * sim_dt                            #Calculate new position

        r12 = r2 - r1
        newA1 = ((G * m2) * (r12)) / (np.linalg.norm(r12) ** 3)      #Recalculate accerlation with new position
        newA2 = -((G * m1) * (r12)) / (np.linalg.norm(r12) ** 3)     #Recalculate accerlation with new position

        v1 = vHalf1 + 0.5 * newA1 * sim_dt                   #Calcualate new vel
        v2 = vHalf2 + 0.5 * newA2 * sim_dt                   #Calcualate new vel

        #Calulate Specfic Momentum and Specific Energy
        v12 = v2 - v1
        mu = G * (m1 + m2)
        h = np.cross(r12, v12)                                         #Specific angular momentum
        E = (0.5 * np.linalg.norm(v12)**2) - (mu/np.linalg.norm(r12))  #Specific orbital energy
        print(f"Time: {simTime:.2f} | E: {E:.2f}, h: {h:.2f}")

            #Update displays
        #if simTime - last_text_update >= update_interval:
        #    tolerance = 0.01
        #    if last_E_display is not None and abs(E - last_E_display) > tolerance:
        #        energyText.set_val(f"{E:.2f}")
        #    last_E_display = E
        #    if  last_h_display is not None and abs(h - last_h_display) > tolerance:
        #        angMomText.set_val(f"{h:.2f}")
        #    last_h_display = h
        #    last_text_update = simTime


        #Update Trails
        trailManager.update('body1', r1)
        trailManager.update('body2', r2)

        #Update Velocities
        vel1History.append(np.linalg.norm(v1))
        vel2History.append(np.linalg.norm(v2))
        timeHistory.append(simTime)
        vel1History = vel1History[-maxVelHistory:]
        vel2History = vel2History[-maxVelHistory:]
        timeHistory = timeHistory[-maxVelHistory:]


        #Update Plots
        body1Plot.set_data([r1[0]], [r1[1]])
        body2Plot.set_data([r2[0]], [r2[1]])

        body1VelPlot.set_data(timeHistory, vel1History)
        body2VelPlot.set_data(timeHistory, vel2History)

        #Sliding Window for Vel
        velWindow = 10
        max_velocity = max(max(vel1History, default=0), max(vel2History, default=0))
        axis2.set_xlim(simTime - velWindow, simTime + velWindow*0.1)
        axis2.set_ylim(bottom=0, top=max_velocity*1.1)  # add 10% margin



        if show_trails[0]:
            trail1_data = trailManager.get_trail('body1')
            trail2_data = trailManager.get_trail('body2')
            if trail1_data:
                trail1Plot.set_data(*zip(*trail1_data))
            if trail2_data:
                trail2Plot.set_data(*zip(*trail2_data))
        else:
            trail1Plot.set_data([], [])
            trail2Plot.set_data([], [])

    return body1Plot, body2Plot, trail1Plot, trail2Plot, body1VelPlot, body2VelPlot





#####  Widgets Start #####
#plt.axes(x, y, width, height)    (in figure coords)
plt.text(0.19, 0.225, 'Red', transform=fig.transFigure, ha='right', va='center', fontsize=11)
plt.text(0.33, 0.225, 'Blue', transform=fig.transFigure, ha='right', va='center', fontsize=11)

body1MassText = TextBox(plt.axes([0.11, 0.16, 0.13, 0.05]), '  Mass: ', initial=f"{m1:.1f}")
body1PosText = TextBox(plt.axes([0.11, 0.105, 0.13, 0.05]), '  Init Pos: ', initial=f"{r1[0]:.1f}, {r1[1]:.1f}")
body1VelText = TextBox(plt.axes([0.11, 0.05, 0.13, 0.05]), '  Init Vel:  ', initial=f"{v1[0]:.1f}, {v1[1]:.1f}")
body2MassText = TextBox(plt.axes([0.25, 0.16, 0.13, 0.05]), '', initial=f"{m2:.1f}")
body2PosText = TextBox(plt.axes([0.25, 0.105, 0.13, 0.05]), '', initial=f"{r2[0]:.1f}, {r2[1]:.1f}")
body2VelText = TextBox(plt.axes([0.25, 0.05, 0.13, 0.05]), '', initial=f"{v2[0]:.1f}, {v2[1]:.1f}")

energyText = TextBox(plt.axes([0.5, 0.16, 0.13, 0.05]), 'Spec. Energy E', initial="0.0")
energyText.set_active(False)
angMomText = TextBox(plt.axes([0.5, 0.105, 0.13, 0.05]), 'Spec. Ang. Mom. h', initial="0.0")
angMomText.set_active(False)

trailCheck = CheckButtons(plt.axes([0.69, 0.16, 0.075, 0.05]), ['Trails?'], [True])
trailLengthBox = TextBox(plt.axes([0.8, 0.16, 0.07, 0.05]), 'Len', initial=str(trailManager.get_max_length()))

slowerButton = Button(plt.axes([0.69, 0.105, 0.05, 0.05]), '<<')
timeText = TextBox(plt.axes([0.74, 0.105, 0.075, 0.05]), '', initial=str(timeSpeedMultiplier))
fasterButton = Button(plt.axes([0.815, 0.105, 0.05, 0.05]), '>>')

startButton = Button(plt.axes([0.66, 0.05, 0.075, 0.05]), 'Start')
pauseButton = Button(plt.axes([0.74, 0.05, 0.075, 0.05]), 'Pause')
resetButton = Button(plt.axes([0.82, 0.05, 0.075, 0.05]), 'Reset')


#Reset Button Logic
def reset(event):
    global r1, r2, v1, v2, body1Plot, body2Plot, trail1Plot, trail2Plot, trailManager, vel1History, timeHistory

    # reset positions
    r1[:] = initial_r1
    r2[:] = initial_r2
    
    # reset velocities
    v1[:] = initial_v1
    v2[:] = initial_v2

    #reset trails
    trailManager.clear("body1")
    trailManager.clear("body2")
    
    # update plot instantly
    body1Plot.set_data([r1[0]], [r1[1]])
    body2Plot.set_data([r2[0]], [r2[1]])
    trail1Plot.set_data([], [])
    trail2Plot.set_data([], [])
    plt.draw()

    #reset histories
    vel1History.clear()
    vel1History.append(np.linalg.norm(v1))
    vel2History.clear()
    vel2History.append(np.linalg.norm(v2))
    timeHistory.clear()
    timeHistory = [0]

initial_r1 = r1.copy()
initial_r2 = r2.copy()
initial_v1 = v1.copy()
initial_v2 = v2.copy()
resetButton.on_clicked(reset)

#Pause Button Logic
def pause(event):
    global running
    running = False
pauseButton.on_clicked(pause)

#Start Button Logic
def start(event):
    global running
    running = True
startButton.on_clicked(start)

#Slowdown
def slower(event):
    global timeSpeedMultiplier
    timeSpeedMultiplier = max(timeSpeedMultiplier * 0.5, 0.0001)
    timeText.set_val(f"{timeSpeedMultiplier:.4f}")
slowerButton.on_clicked(slower)

#Speedup
def faster(event):
    global timeSpeedMultiplier
    timeSpeedMultiplier *= 2
    timeText.set_val(f"{timeSpeedMultiplier:.4f}")
fasterButton.on_clicked(faster)

#Text Box
def update_time_multiplier(text):
    global timeSpeedMultiplier
    try:
        val = float(text)
        if val > 0:
            timeSpeedMultiplier = val
        else:
            timeText.set_val(str(timeSpeedMultiplier))
    except:
        timeText.set_val(str(timeSpeedMultiplier))
timeText.on_submit(update_time_multiplier)

#Trails
def toggle_trails(label):
    global show_trails
    show_trails[0] = not show_trails[0]  # toggle boolean
trailCheck.on_clicked(toggle_trails)
show_trails = [True]

def update_trail_length(text):
    global max_trail_length
    try:
        val = int(text)
        if val > 0:
            max_trail_length = val
        else:
            trailLengthBox.set_val(str(max_trail_length))
    except:
        trailLengthBox.set_val(str(max_trail_length))

trailLengthBox.on_submit(update_trail_length)

#Initial Conditions
def update_body1_mass(text):
    global m1
    try:
        val = float(text)
        if val > 0:
            m1 = val
        body1MassText.set_val(f"{m1:.1f}")
    except:
        body1MassText.set_val(f"{m1:.1f}")
body1MassText.on_submit(update_body1_mass)

def update_body1_pos(text):
    try:
        x, y = map(float, text.split(','))
        x = max(-100, min(100, x))
        y = max(-100, min(100, y))
        initial_r1[:] = [x, y]
        body1PosText.set_val(f"{initial_r1[0]:.1f}, {initial_r1[1]:.1f}")
    except:
        body1PosText.set_val(f"{initial_r1[0]:.1f}, {initial_r1[1]:.1f}")
    plt.draw()
body1PosText.on_submit(update_body1_pos)

def update_body1_vel(text):
    try:
        vx, vy = map(float, text.split(','))
        initial_v1[:] = [vx, vy]
    except:
        body1VelText.set_val(f"{v1[0]:.1f}, {v1[1]:.1f}")
    plt.draw()
body1VelText.on_submit(update_body1_vel)

def update_body2_mass(text):
    global m2
    try:
        val = float(text)
        if val > 0:
            m2 = val
        body2MassText.set_val(f"{m2:.1f}")
    except:
        body2MassText.set_val(f"{m2:.1f}")
body2MassText.on_submit(update_body2_mass)

def update_body2_pos(text):
    try:
        x, y = map(float, text.split(','))
        x = max(-100, min(100, x))
        y = max(-100, min(100, y))
        initial_r2[:] = [x, y]
        body2PosText.set_val(f"{initial_r2[0]:.1f}, {initial_r2[1]:.1f}")
    except:
        body2PosText.set_val(f"{initial_r2[0]:.1f}, {initial_r2[1]:.1f}")
    plt.draw()
body2PosText.on_submit(update_body2_pos)

def update_body2_vel(text):
    try:
        vx, vy = map(float, text.split(','))
        initial_v2[:] = [vx, vy]
    except:
        body2VelText.set_val(f"{v2[0]:.1f}, {v2[1]:.1f}")
    plt.draw()
body2VelText.on_submit(update_body2_vel)
#####  Widgets End #####





#####  Plots Start #####
animation = FuncAnimation(
    fig=fig,
    func=UpdateFrame,
    frames=None,
    interval=10,
    blit = True
)

plt.show()
#####  Plots End #####