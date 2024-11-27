from model import Model

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def remakemodel(self, y, sr):
        self.model = Model(y, sr)

    def rawdata(self):
        return self.model.sr, self.model.y
    def data(self):
        return self.model.waveform_graph()

