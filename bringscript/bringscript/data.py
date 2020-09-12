from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple


@dataclass(frozen=True)
class TemplateRenderArgument:
    src: Path
    dest: Path
    context: Dict

    def as_tuple(self) -> Tuple:
        return (self.src, self.dest, self.context)
