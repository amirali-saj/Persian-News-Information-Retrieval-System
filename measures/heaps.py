from math import log10

from measures.plot import draw_prediction_line_with_actual_points


def draw_heaps_plot(m1, t1, m2, t2, m_total, t_total):
    b = (log10(m2) - log10(m1)) / (log10(t2) - log10(t1))
    k = log10(m1) - b * log10(t1)
    draw_prediction_line_with_actual_points(0, 1000, b, k, 'Heaps law', [(log10(t_total), log10(m_total))], 'log10 T',
                                            'log10 M')


draw_heaps_plot(57694,1001478,90549,2948209,196819,10905979)

draw_heaps_plot(37461,983920,55695,2896813,124778,10711423)
