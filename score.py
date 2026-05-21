import json
import os

# [
#    ["name", 13000]
#    ["cle", 5000]
# ]


class HighScore:
    def __init__(self) -> None:
        self.scores: list[list[str | int]] = []

    def load_high_score(self) -> None:
        if os.path.exists("json_file/highscore.json"):
            with open("json_file/highscore.json", "r") as f:
                self.scores = json.load(f)

    def save_high_score(
        self,
        name: str,
        score: int,
    ) -> None:
        self.scores.append([name, score])
        self._sort_score()
        nb_score = len(self.scores)
        if nb_score > 10:
            self.scores = self.scores[:10]

        with open("json_file/highscore.json", "w") as f:
            json.dump(score, f)

    def _sort_score(self) -> None:
        self.scores = sorted(self.scores, key=lambda s: s[1])
