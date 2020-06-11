from math import log10

from measures.plot import draw_prediction_line_with_actual_points


def draw_hepas_plot(m1, t1, m2, t2):
    b = (log10(m2) - log10(m1)) / (log10(t2) - log10(t1))
    k = log10(m1) - b * log10(t1)
    draw_prediction_line_with_actual_points(2, 1000, b, k, 'Heaps law', [(0, 100), (50, 50)])
