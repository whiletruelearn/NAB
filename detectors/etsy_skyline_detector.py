from anomaly_detector import AnomalyDetector

from skyline.algorithms import (median_absolute_deviation,
                                first_hour_average,
                                stddev_from_average,
                                stddev_from_moving_average,
                                mean_subtraction_cumulation,
                                least_squares,
                                histogram_bins)

class EtsySkylineDetector(AnomalyDetector):

  def __init__(self, probationaryPeriod, *args, **kwargs):
    
    # Store our running history
    self.timeseries = []
    self.recordCount = 0
    self.probationaryPeriod = probationaryPeriod

    self.algorithms =    [median_absolute_deviation,
                         first_hour_average,
                         stddev_from_average,
                         stddev_from_moving_average,
                         mean_subtraction_cumulation,
                         least_squares,
                         histogram_bins]


    super(EtsySkylineDetector, self).__init__(*args, **kwargs)

  def getOutputPrefix(self):
    return "skyline"

  def handleRecord(self, inputData):
    """
    Returns a list [anomalyScore].
    """

    score = 0.0
    inputRow = [inputData["timestamp"], inputData["value"]]
    self.timeseries.append(inputRow)
    if self.recordCount < self.probationaryPeriod:
      self.recordCount += 1
    else:
      for algo in self.algorithms:
        score += algo(self.timeseries)

    normalizedScore = score / len(self.algorithms)
    return [normalizedScore]