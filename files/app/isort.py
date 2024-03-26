import re
from typing import List, Self
import subprocess
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ISortError:
    file: Path
    title: str
    message: str
    line: int


class GHFormatter:
    @property
    def errors(self: Self) -> List[ISortError]:
        return self._errors

    def __init__(self: Self, output: str) -> None:
        if not output:
            raise ValueError("isort output must be provided.")
        
        error_list: List[ISortError] = []

        regex: re.Pattern = re.compile(
            r'---\s(?P<path>.+?\.py):before.*?@@.*?\n(?P<code>.+?)(?=\n---|\Z)',
            re.IGNORECASE|re.DOTALL,
        )

        matches = [m.groupdict() for m in regex.finditer(output)]
        for match in matches:
            error_list.append(
                ISortError(
                    file=match["path"].strip(),
                    title="Imports are incorrectly sorted and/or formatted.",
                    message=match["code"].strip(),
                    line=1
                )
            )

        self._errors = error_list


output: str = subprocess.run(
    args=[
        "isort",
        "--check-only",
        "--quiet",
        "--diff",
        "--profile",
        "black",
        "--trailing-comma",
        "--use-parenthesis",
        "--line-length",
        "100",
        "--split-on-trailing-comma",
        "." # /github/workspace
    ],
    shell=False,
    capture_output=True,
    text=True,
)

formatter: GHFormatter = GHFormatter(output=output)

output: str = ""

for error in formatter.errors:
    print(f"::error file={error.file},title={error.title},line={error.line},::{error.message}")