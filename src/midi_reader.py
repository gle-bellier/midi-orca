import pretty_midi
import numpy as np


class MidiReader:

    def __init__(self, resolution: int) -> None:

        self.resolution = resolution

    def get_midi_matrix(self, path: str) -> np.ndarray:

        midi = pretty_midi.PrettyMIDI(path)
        data = midi.instruments[0]
        bpm = np.round(midi.estimate_tempo())

        print(bpm)
        fs = self.resolution * bpm / 60

        notes = data.get_piano_roll(fs)
        print(midi.get_end_time())
        print(notes.shape)


if __name__ == '__main__':
    m = MidiReader(1)
    m.get_midi_matrix("midi/seq.mid")