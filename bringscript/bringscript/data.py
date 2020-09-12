from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass(frozen=True)
class TemplateRenderArgument:
    src: Path
    dest: Path
    context: Dict
