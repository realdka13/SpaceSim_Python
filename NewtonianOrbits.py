#Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


##### 2 Body Problem #####

#Time settings
deltaTime = 0.001   #Time change per step
numSteps = 100    #Total number of time steps

#Constants
G = 50.0   #Gravitational Constant

#Bodies
    #Body1
r1 = np.array([-20.0, 20.0])  # Initial position of body 1
v1 = np.array([7.0, 5.0])  # Initial velocity of body 1
m1 = 500.0                    # Mass of body 1

r2 = np.array([20.0, -20.0])   # Initial position of body 2
v2 = np.array([-10.0, -4.0])# Initial velocity of body 2
m2 = 500.0                    # Mass of body 2

#Plot Settings
    #Body 2
fig, axis = plt.subplots()
axis.set_xlim(-100, 100)
axis.set_ylim(-100, 100)

#Plots for Each Body
body1Plot, = axis.plot([], [], marker='o', linestyle='', markersize=6, color='red')
body2Plot, = axis.plot([], [], marker='o', linestyle='', markersize=6, color='blue')

#Changes to make every frame
def UpdateFrame(frame):
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

    #Update Plot
    body1Plot.set_data([r1[0]], [r1[1]])
    body2Plot.set_data([r2[0]], [r2[1]])
    return body1Plot, body2Plot


animation = FuncAnimation(
    fig=fig,
    func=UpdateFrame,
    frames=numSteps,
    interval=0,
    blit = True
)

plt.show()