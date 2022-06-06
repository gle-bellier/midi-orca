from dataclasses import dataclass
from typing import List
import pretty_midi
import numpy as np


@dataclass
class Note:
    pitch: int
    start: int
    end: int
    velocity: int

    @property
    def octave(self) -> int:
        return self.pitch // 12

    @property
    def chroma(self) -> int:
        return self.pitch % 12

    @property
    def duration(self) -> int:
        return self.end - self.start

    def encode_midi(self, n: int) -> str:
        n = int((n / 128) * 36)
        return self.encode36(n)

    def encode36(self, n: int) -> str:
        return np.base_repr(n, base=36)

    def encode_chroma(self, n: int) -> str:
        return list("CcDdEFfGgAaB")[n]

    @property
    def orca(self) -> str:
        if self.velocity == 0:
            return "...."
        else:
            octave = str(self.octave)
            chroma = self.encode_chroma(self.chroma)
            vel = self.encode_midi(self.velocity)
            duration = self.encode36(int(self.duration))
            return octave + chroma + vel + duration


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
            s = int(n.start / time_step)
            e = int(n.end / time_step)
            q_notes += [Note(n.pitch, s, e, n.velocity)]

        return q_notes

    def get_mono(self, path: str) -> List[np.ndarray]:

        notes = self.get_notes(path)
        length = notes[-1].start
        length = length + (length - length % self.pattern_length)
        patterns = [Note(0, i, i + 1, 0) for i in range(length)]

        for note in notes:
            patterns[note.start] = note

        print(patterns)
        for note in notes:
            print(note)
        print("_____________________________")
        print("_____________________________")
        print("_____________________________")
        print([n.orca for n in patterns])


if __name__ == '__main__':

    md = MidiReader(resolution=1, pattern_length=8)
    md.get_mono("midi/seq.mid")