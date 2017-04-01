import numpy as np
from detect_peaks import detect_peaks

class BrushingStatistics():
    def __init__(self, data, secondsBrushing):
        self.secondsBrushing = secondsBrushing
        self.data = np.asarray(data)
        self.peaks = self.data[detect_peaks(self.data)]
        self.valleys = self.data[detect_peaks(self.data, valley=True)]


    def mean_maximum_force(self):
        return np.mean(self.peaks)
        

    def mean_sustained_force(self):
        return np.mean(self.valleys)


    def mean_brushing_force(self):
        return np.mean(self.data)


    def mean_stroke_rate(self):
        return float(len(self.peaks)) / self.secondsBrushing 


if __name__ == "__main__":
    stats = BrushingStatistics([0, 1, 3, 1, 0, 1, 2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 0.5, 6], 1.0)

    print(stats.peaks)
    print(stats.valleys)

    print("")
    print(stats.mean_maximum_force())
    print(stats.mean_sustained_force())
    print(stats.mean_stroke_rate())
    print(stats.mean_brushing_force())