# Multiply a distribution by another distribution.
# 06_c_multiply_distribution
from pylab import plot, show
from distribution import *


def multiply(a, b):
    """Multiply two distributions and return the resulting distribution."""

    vals = []
    for i in range(min(a.start(), b.start()), max(a.stop(), b.stop()) + 1):
        vals.append((a.value(i) * b.value(i)))

    # Modify this to return your result.
    distribution = Distribution(min(a.offset, b.offset), vals)
    multiplication_result = distribution.normalize()
    
    return multiplication_result  # Modify this to return your result.


if __name__ == '__main__':
    arena = (0,1000)

    # Here is our assumed position. Plotted in blue.
    position_value = 400
    position_error = 100
    position = Distribution.triangle(position_value, position_error)
    plot(position.plotlists(*arena)[0], position.plotlists(*arena)[1],
         color='b', linestyle='steps')

    # Here is our measurement. Plotted in green.
    # That is what we read from the instrument.
    measured_value = 410
    measurement_error = 200
    measurement = Distribution.triangle(measured_value, measurement_error)
    plot(measurement.plotlists(*arena)[0], measurement.plotlists(*arena)[1],
         color='g', linestyle='steps')

    # Now, we integrate our sensor measurement. Result is plotted in red.
    position_after_measurement = multiply(position, measurement)
    plot(position_after_measurement.plotlists(*arena)[0],
         position_after_measurement.plotlists(*arena)[1],
         color='r', linestyle='steps')

    show()
