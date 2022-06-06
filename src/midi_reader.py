from typing import List
import pretty_midi
import numpy as np


class MidiReader:

    def __init__(self, resolution: int, pattern_length: int) -> None:

        self.resolution = resolution
        self.pattern_length = pattern_length

    def get_notes(self, path: str) -> np.ndarray:

        midi = pretty_midi.PrettyMIDI(path)
        notes = midi.instruments[0].notes

        bpm = np.round(midi.estimate_tempo())
        time_step = 60 / (self.resolution * bpm)

        # quantize
        q_notes = []
        for n in notes:
            s = np.round(n.start / time_step)
            e = np.round(n.end / time_step)
            q_notes += [Note(n.pitch, int(s), int(e), n.velocity)]

        return q_notes

    def get_mono(self, path: str) -> List[np.ndarray]:

        notes = self.get_notes(path)
        length = notes[-1].start + 1
        length += (self.pattern_length - length % self.pattern_length) * (
            length % self.pattern_length != 0)
        patterns = [Note(0, i, i + 1, 0) for i in range(length)]

        for note in notes:
            patterns[note.start] = note

        patterns = np.array(patterns)
        patterns = patterns.reshape((-1, self.pattern_length))

        print(patterns)


if __name__ == '__main__':

    md = MidiReader(resolution=1, pattern_length=8)
    md.get_mono("midi/seq.mid")