from quiz import storage
from quiz.game import Quiz

QS = [
    {"category": "A", "difficulty": "Easy", "question": "q1",
     "options": ["x", "y", "z", "w"], "answer": "x"},
    {"category": "A", "difficulty": "Easy", "question": "q2",
     "options": ["x", "y", "z", "w"], "answer": "y"},
]


def test_correct_answer_scores_with_time_bonus():
    quiz = Quiz(QS, shuffle=False)
    result = quiz.submit("x", 10)
    assert result.correct
    assert result.points == 150  # 100 base + 10s * 5
    assert quiz.score == 150


def test_streak_bonus_applies():
    quiz = Quiz(QS, shuffle=False)
    quiz.submit("x", 10)
    result = quiz.submit("y", 10)
    assert result.points == 170  # 100 + 50 + 20 streak bonus
    assert quiz.best_streak == 2


def test_wrong_answer_resets_streak():
    quiz = Quiz(QS, shuffle=False)
    quiz.submit("x", 10)
    quiz.submit("x", 10)  # wrong for q2
    assert quiz.streak == 0
    assert quiz.best_streak == 1


def test_timeout_counts_as_wrong():
    quiz = Quiz(QS, shuffle=False)
    result = quiz.submit(None, 0)
    assert not result.correct
    assert quiz.score == 0


def test_finish_and_accuracy():
    quiz = Quiz(QS, shuffle=False)
    quiz.submit("x", 5)
    quiz.submit("y", 5)
    assert quiz.is_finished()
    assert quiz.accuracy() == 100


def test_fifty_fifty_once_only():
    quiz = Quiz(QS, shuffle=False)
    removed = quiz.use_fifty_fifty()
    assert len(removed) == 2
    assert "x" not in removed
    assert quiz.use_fifty_fifty() == []


def test_leaderboard_ranking(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "SCORE_FILE", tmp_path / "lb.json")
    assert storage.add_score("A", 300, "Python", 3, 8) == 1
    assert storage.add_score("B", 500, "Python", 5, 8) == 1
    assert storage.add_score("C", 100, "Python", 1, 8) == 3
    assert [e["name"] for e in storage.load_leaderboard()] == ["B", "A", "C"]
    assert storage.best_score() == 500