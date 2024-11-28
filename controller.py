class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def rawdata(self):
        return self.model.sr, self.model.y
    def data(self):
        return self.model.waveform_graph()
    def analysis(self):
        return self.model.find_resonance(), self.model.find_length(), self.model.find_difference()

    def frequency_check(self,min, max):
        return self.model.frequency_check(min,max)

    def Calculate_RT60(self,min,max):
        return self.model.Calculate_RT60(min,max)

