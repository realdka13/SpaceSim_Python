#Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox, CheckButtons
import matplotlib.gridspec as gridspec


#Time settings
deltaTime = 0.01   #Time change per step
numSteps = 100     #Total number of time steps
running = True    #For Start/Pause

#Constants
G = 50.0   #Gravitational Constant

#Bodies
    #Body1
r1 = np.array([-20.0, 20.0])  # Initial position of body 1
v1 = np.array([7.0, 5.0])  # Initial velocity of body 1
m1 = 500.0                    # Mass of body 1

    #Body 2
r2 = np.array([20.0, -20.0])   # Initial position of body 2
v2 = np.array([-10.0, -4.0])# Initial velocity of body 2
m2 = 500.0                    # Mass of body 2



#Changes to make every frame
def UpdateFrame(frame):
    global r1, r2, v1, v2, trail1, trail2, v1_history, t_history
    if running:
        #Calculate Normalized Vectors Between Bodies
        r12 = r2 - r1   #Vector from body 1 to body 2               #***** Verify

        r_mag = np.linalg.norm(r12)

        r12_Norm = r12 / r_mag

        #Calculate Force vectors Fg
        Fg_mag = (G * m1 * m2) / (r_mag ** 2)
        Fg1_vec = Fg_mag * r12_Norm
        Fg2_vec = Fg_mag * -r12_Norm


        #Calculate acceleration vectors
        a1 = Fg1_vec / m1
        a2 = Fg2_vec / m2

        #Update Velocity
        v1[0] += a1[0] * deltaTime
        v1[1] += a1[1] * deltaTime

        v2[0] += a2[0] * deltaTime
        v2[1] += a2[1] * deltaTime

        #Update Position
        r1[0] += v1[0] * deltaTime
        r1[1] += v1[1] * deltaTime

        r2[0] += v2[0] * deltaTime
        r2[1] += v2[1] * deltaTime

        #Update Trails
        trail1.append(r1.copy())
        trail2.append(r2.copy())
        trail1 = trail1[-max_trail_length:]
        trail2 = trail2[-max_trail_length:]

        #Update Velocities
        v1_history.append(v1.copy())
        t_history.append(frame * deltaTime)
        v1_history = v1_history[-max_points:]
        t_history = t_history[-max_points:]
        v1_mag = [np.linalg.norm(v) for v in v1_history]


        #Update Plot
    body1Plot.set_data([r1[0]], [r1[1]])
    body2Plot.set_data([r2[0]], [r2[1]])
    body1VelPlot.set_data(t_history, v1_mag)
    if show_trails[0]:
        trail1Plot.set_data(*zip(*trail1))
        trail2Plot.set_data(*zip(*trail2))
    else:
        trail1Plot.set_data([], [])
        trail2Plot.set_data([], [])

    axis2.relim()         # recompute limits
    axis2.autoscale_view()  # rescale view

    return body1Plot, body2Plot, trail1Plot, trail2Plot, body1VelPlot


##### Additional Features #####
#Trails
max_trail_length = 1000
trail1 = [r1.copy()]
trail2 = [r2.copy()]

#Velocity
max_points = 100
v1_history = [v1.copy()]
t_history = [0] 

##### Below is code for Plotting #####

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
axis2.set_ylabel("Velocity")
axis2.set_title("Velocity vs Time")

#Plot Widgets  #plt.axes(x, y, width, height)    (in figure coords)
plt.text(0.192, 0.165, 'Red', transform=fig.transFigure, ha='right', va='center', fontsize=11)
plt.text(0.335, 0.165, 'Blue', transform=fig.transFigure, ha='right', va='center', fontsize=11)

body1PosText = TextBox(plt.axes([0.11, 0.105, 0.13, 0.05]), '  Init Pos: ', initial=f"{r1[0]:.1f}, {r1[1]:.1f}")
body1VelText = TextBox(plt.axes([0.11, 0.05, 0.13, 0.05]), '  Init Vel:  ', initial=f"{v1[0]:.1f}, {v1[1]:.1f}")
body2PosText = TextBox(plt.axes([0.25, 0.105, 0.13, 0.05]), '', initial=f"{r2[0]:.1f}, {r2[1]:.1f}")
body2VelText = TextBox(plt.axes([0.25, 0.05, 0.13, 0.05]), '', initial=f"{v2[0]:.1f}, {v2[1]:.1f}")

trailCheck = CheckButtons(plt.axes([0.69, 0.16, 0.075, 0.05]), ['Trails?'], [True])
trailLengthBox = TextBox(plt.axes([0.8, 0.16, 0.07, 0.05]), 'Len', initial=str(max_trail_length))

slowerButton = Button(plt.axes([0.69, 0.105, 0.05, 0.05]), '<<')
timeText = TextBox(plt.axes([0.74, 0.105, 0.075, 0.05]), '', initial=str(deltaTime))
fasterButton = Button(plt.axes([0.815, 0.105, 0.05, 0.05]), '>>')

startButton = Button(plt.axes([0.66, 0.05, 0.075, 0.05]), 'Start')
pauseButton = Button(plt.axes([0.74, 0.05, 0.075, 0.05]), 'Pause')
resetButton = Button(plt.axes([0.82, 0.05, 0.075, 0.05]), 'Reset')

#Reset Button Logic
def reset(event):
    global r1, r2, v1, v2, trail1, trail2, body1Plot, body2Plot, trail1Plot, trail2Plot

    # reset positions
    r1[:] = initial_r1
    r2[:] = initial_r2
    
    # reset velocities
    v1[:] = initial_v1
    v2[:] = initial_v2

    #reset trails
    trail1 = [r1.copy()]
    trail2 = [r2.copy()]
    
    # update plot instantly
    body1Plot.set_data([r1[0]], [r1[1]])
    body2Plot.set_data([r2[0]], [r2[1]])
    trail1Plot.set_data([], [])
    trail2Plot.set_data([], [])
    plt.draw()

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
    global deltaTime
    deltaTime = max(deltaTime * 0.5, 0.0001)
    timeText.set_val(f"{deltaTime:.4f}")
slowerButton.on_clicked(slower)

#Speedup
def faster(event):
    global deltaTime
    deltaTime *= 2
    timeText.set_val(f"{deltaTime:.4f}")
fasterButton.on_clicked(faster)

#Text Box
def update_dt(text):
    global deltaTime
    try:
        val = float(text)
        if val > 0:
            deltaTime = val
        else:
            timeText.set_val(str(deltaTime))
    except:
        timeText.set_val(str(deltaTime))
timeText.on_submit(update_dt)

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


#Plots for Each Body
body1Plot, = axis.plot([], [], marker='o', linestyle='', markersize=6, color='red')
body2Plot, = axis.plot([], [], marker='o', linestyle='', markersize=6, color='blue')

#Trail Plots
trail1Plot, = axis.plot([], [], color='red', linewidth=1)
trail2Plot, = axis.plot([], [], color='blue', linewidth=1)

#Velocities
body1VelPlot, = axis2.plot([], [], color='red', linewidth=1)

animation = FuncAnimation(
    fig=fig,
    func=UpdateFrame,
    frames=numSteps,
    interval=0,
    blit = True
)

plt.show()