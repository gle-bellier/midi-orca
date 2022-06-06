from dataclasses import dataclass
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