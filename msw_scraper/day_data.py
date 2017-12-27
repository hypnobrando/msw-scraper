class DayData:
    def __init__(self, day, data_list):
        self.data = data_list
        self.day = day
        self.heights = [data_point['height'] for data_point in self.data]
        self.maxHeights = [data_point['height']['max'] for data_point in self.data]
        self.minHeights = [data_point['height']['min'] for data_point in self.data]
        self.avgHeights = [(float(data_point['height']['max']) + float(data_point['height']['min']))/2.0 for data_point in self.data]
        self.times = [data_point['time'] for data_point in self.data]
        self.qualities = [data_point['quality'] for data_point in self.data]

    def __str__(self):
        return '%s: %s\n' % (self.day, self.data)

    def __repr__(self):
        return '%s: %s\n' % (self.day, self.data)
