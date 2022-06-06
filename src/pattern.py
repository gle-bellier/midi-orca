from dataclasses import dataclass
import numpy as np


@dataclass
class Pattern:
    index: int
    seq: np.ndarray

    def encode36(self, n: int) -> str:
        return np.base_repr(n, base=36)

    def __repr__(self):
        n = self.encode36(self.index)
        s = "#PTRN0#\n#.OPVL#\n"
        for note in self.seq:
            s += f"#.{note.orca}#\n"

        return s
