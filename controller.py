from scipy.io import wavfile
from model import Model
class Controller:
    def __init__(self, view):
        #sr, y = wavfile.read("testsound.wav")
        #self.model = Model(y, sr)
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

    def load_file(self):
        self.view.load_audio()
        if self.view.checkforfile() == 1:
            sr, y = wavfile.read("testsound.wav")
            self.model = Model(y, sr)