import random
from dataclasses import dataclass

DIFFICULTY_POINTS = {"Easy": 100, "Medium": 150, "Hard": 200}
TIME_PER_QUESTION = 15
TIME_BONUS_PER_SECOND = 5
STREAK_BONUS = 20


@dataclass
class AnswerResult:
    correct: bool
    points: int
    correct_answer: str


class Quiz:
    def __init__(self, questions, shuffle=True, time_limit=TIME_PER_QUESTION):
        self.questions = [dict(q, options=list(q["options"])) for q in questions]
        if shuffle:
            random.shuffle(self.questions)
            for q in self.questions:
                random.shuffle(q["options"])
        self.time_limit = time_limit
        self.index = 0
        self.score = 0
        self.correct_count = 0
        self.streak = 0
        self.best_streak = 0
        self.fifty_used = False

    @property
    def total(self):
        return len(self.questions)

    @property
    def current(self):
        return self.questions[self.index]

    def is_finished(self):
        return self.index >= self.total

    def submit(self, choice, time_left):
        """Check an answer (choice=None means time ran out) and move on."""
        question = self.current
        correct = choice == question["answer"]
        points = 0

        if correct:
            self.correct_count += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            base = DIFFICULTY_POINTS.get(question["difficulty"], 100)
            time_bonus = int(max(time_left, 0)) * TIME_BONUS_PER_SECOND
            streak_bonus = (self.streak - 1) * STREAK_BONUS
            points = base + time_bonus + streak_bonus
            self.score += points
        else:
            self.streak = 0

        self.index += 1
        return AnswerResult(correct, points, question["answer"])

    def use_fifty_fifty(self):
        """Return two wrong options to hide. Works once per game."""
        if self.fifty_used or self.is_finished():
            return []
        self.fifty_used = True
        question = self.current
        wrong = [o for o in question["options"] if o != question["answer"]]
        return random.sample(wrong, 2) if len(wrong) >= 2 else []

    def accuracy(self):
        if not self.total:
            return 0
        return round(self.correct_count / self.total * 100)