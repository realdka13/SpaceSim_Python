#https://www.youtube.com/watch?v=nT16-yQrnFk

#Libs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

time = np.linspace(0, 10, 100)
y = np.sin(time)

fig, axis = plt.subplots()
axis.set_xlim([min(time), max(time)])
axis.set_ylim(-2, 2)
animated_plot, = axis.plot([], [])

def update(frame):
    animated_plot.set_data(time[:frame], y[:frame])

    return animated_plot,

animation = FuncAnimation(
    fig = fig,
    func=update,
    frames=len(time),
    interval=25
)

animation.save('sine_wave_animation.gif')
plt.show()