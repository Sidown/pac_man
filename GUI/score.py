import json
import os


class HighScore:
    """
    Manage the highscore leaderboard stored in a json file
    """
    def __init__(self) -> None:
        """
        Initialise with an empty score list
        """
        self.scores: list[list[str | int]] = []

    def load_high_score(self) -> None:
        """
        Load scores from the json file if it exists
        If the file is missing or is invalid, reset the score list
        """
        if os.path.exists("json_file/highscore.json"):
            with open("json_file/highscore.json", "r") as f:
                try:
                    self.scores = json.load(f)
                except Exception:
                    self.scores = []
            self._check_format()
            self._sort_score()

    def _check_format(self) -> None:
        """
        Reset scores to an empty list if there are no scores
        """
        if self.scores is None or len(self.scores) == 0:
            self.scores = []

    def save_high_score(
        self,
        name: str,
        score: int,
    ) -> None:
        """
        Append a new entry and keep the top 10 scores
        duplicate name/score are ignored
        arguments:
        name -> player name
        score -> player score
        """
        if [name, score] not in self.scores:
            self.scores.append([name, score])
        self._sort_score()
        nb_score = len(self.scores)
        if nb_score > 10:
            self.scores = self.scores[:10]

        with open("json_file/highscore.json", "w") as f:
            json.dump(self.scores, f)

    def _sort_score(self) -> None:
        """
        Sort the score in a descending order
        """
        self.scores = sorted(self.scores, key=lambda s: s[1], reverse=True)
