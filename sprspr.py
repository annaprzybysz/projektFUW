import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# arr = []
# for i in range(100):
#     c = np.random.rand(10, 10)
#     arr.append(c)
# plt.imshow(arr[45])
# plt.show()

def data_gen():
    while True:
        yield np.random.rand(10)
fig, ax = plt.subplots()
line, = ax.plot(np.random.rand(10))
ax.set_ylim('1', '2', '3')

def update(data):
    line.set_ydata(data)
    return line,

ani = FuncAnimation(fig, update, data_gen, interval=100)
plt.show()