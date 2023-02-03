from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

# if plotting does not work comment the following line
matplotlib.use('TkAgg')


class Plotter:

    def __init__(self):
        plt.figure()

    # Creating a method for displaying a polygon, configuring display
    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightgray', label='Polygon')

    # Creating a method for displaying a Minimum Bounding Rectangle, configuring display
    def add_mbr(self, x_max, x_min, y_max, y_min):
        plt.plot([x_min, x_min, x_max, x_max, x_min], [y_min, y_max, y_max, y_min, y_min], 'black', label='MBR')

    # Creating a method for displaying Rays (used in Ray Casting) as arrows, configuring display
    def add_arrow(self, x, y, dx, dy):
        plt.arrow(x, y, dx, dy, color='darkgray', linewidth=None, head_width=0.2, head_length=0.2,
                  length_includes_head=True, label='Rays')

    # Creating a method for displaying points (both in classified and unclassified state), configuring display
    def add_point(self, x, y, kind=None, annotation=None):
        plt.annotate(annotation, (x, y), fontsize=6, xytext=(x + 0.05, y + 0.05))
        if kind == 'outside':
            plt.plot(x, y, 'ro', label='Outside')
        elif kind == 'boundary':
            plt.plot(x, y, 'bo', label='Boundary')
        elif kind == 'inside':
            plt.plot(x, y, 'go', label='Inside')
        else:
            plt.plot(x, y, 'ko', label='Unclassified')

    # General visualization settings, adding axis caption and heading
    def show(self):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.title('Point-in-Polygon Realization', fontsize=16)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.show()
