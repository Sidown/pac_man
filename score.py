import json
import os


class HighScore:
    def __init__(self) -> None:
        self.scores: list[list[str | int]] = []

    def load_high_score(self) -> None:
        if os.path.exists("json_file/highscore.json"):
            with open("json_file/highscore.json", "r") as f:
                try:
                    self.scores = json.load(f)
                except Exception:
                    self.scores = []
            self._check_format()
            self._sort_score()

    def _check_format(self) -> None:
        if self.scores is None or len(self.scores) == 0:
            self.scores = []

    def save_high_score(
        self,
        name: str,
        score: int,
    ) -> None:
        if [name, score] not in self.scores:
            self.scores.append([name, score])
        self._sort_score()
        nb_score = len(self.scores)
        if nb_score > 10:
            self.scores = self.scores[:10]

        with open("json_file/highscore.json", "w") as f:
            json.dump(self.scores, f)

    def _sort_score(self) -> None:
        self.scores = sorted(self.scores, key=lambda s: s[1], reverse=True)
