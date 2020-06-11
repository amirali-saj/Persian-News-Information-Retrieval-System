import matplotlib.pyplot as plt
import numpy as np


def draw_prediction_line_with_actual_points(x_start, x_end, m, b, label, points,x_label='x',y_label='y'):
    x = np.linspace(x_start, x_end, 100)
    print('m',m)
    y = m * x + b
    plt.plot(x, y, '-r', label=label)
    for point in points:
        plt.scatter(point[0], point[1])
    plt.title('Graph of ' + label)
    plt.xlabel(x_label, color='#1C2833')
    plt.ylabel(y_label, color='#1C2833')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()

