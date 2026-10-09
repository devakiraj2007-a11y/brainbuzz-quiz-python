import math
import tkinter as tk
from tkinter import messagebox

from quiz import storage
from quiz.game import Quiz
from quiz.questions import ICONS, category_names, count_questions, get_questions

BG = "#0b1020"
CARD = "#151c33"
CARD_HOVER = "#1e2745"
TRACK = "#1f2a48"
TEXT = "#e5eefb"
MUTED = "#9aa7c2"
PRIMARY = "#7c3aed"
PRIMARY_HOVER = "#8b5cf6"
ACCENT = "#a78bfa"
GOOD = "#22c55e"
BAD = "#ef4444"
WARN = "#fbbf24"
FONT = "Segoe UI"


def make_button(parent, text, command, bg=CARD, hover=CARD_HOVER, fg=TEXT,
                font=None, **kwargs):
    btn = tk.Button(
        parent, text=text, command=command, bg=bg, fg=fg,
        activebackground=hover, activeforeground=fg, disabledforeground=fg,
        relief="flat", bd=0, cursor="hand2",
        font=font or (FONT, 12, "bold"), **kwargs,
    )

    def on_enter(_):
        if str(btn["state"]) == "normal":
            btn.config(bg=hover)

    def on_leave(_):
        if str(btn["state"]) == "normal":
            btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def stat_card(parent, value, label, color=TEXT):
    frame = tk.Frame(parent, bg=CARD, padx=24, pady=14)
    tk.Label(frame, text=value, font=(FONT, 22, "bold"), bg=CARD, fg=color).pack()
    tk.Label(frame, text=label, font=(FONT, 10), bg=CARD, fg=MUTED).pack()
    return frame


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BrainBuzz - Quiz Game Platform")
        self.configure(bg=BG)
        self.geometry(self._center(860, 700))
        self.minsize(780, 660)

        self.player_name = tk.StringVar(value="Player")
        self.category = "Mixed"
        self.quiz = None
        self.locked = False
        self.time_left = 0.0
        self.timer_job = None
        self.next_job = None
        self.option_buttons = []

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True, padx=30, pady=22)
        self.show_home()

    # ---------- helpers ----------
    def _center(self, w, h):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        return f"{w}x{h}+{(sw - w) // 2}+{max((sh - h) // 2 - 20, 0)}"

    def clear(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        if self.next_job:
            self.after_cancel(self.next_job)
            self.next_job = None
        for widget in self.container.winfo_children():
            widget.destroy()

    def label(self, parent, text, size=12, bold=False, color=TEXT, **kwargs):
        return tk.Label(parent, text=text, bg=kwargs.pop("bg", BG), fg=color,
                        font=(FONT, size, "bold" if bold else "normal"), **kwargs)

    def build_leaderboard(self, parent, limit):
        box = tk.Frame(parent, bg=CARD, padx=20, pady=12)
        entries = storage.load_leaderboard(limit)
        if not entries:
            self.label(box, "No scores yet - be the first!", 12,
                       color=MUTED, bg=CARD).pack(pady=10)
            return box
        medals = ["🥇", "🥈", "🥉"]
        for i, e in enumerate(entries):
            row = tk.Frame(box, bg=CARD)
            row.pack(fill="x", pady=3)
            rank = medals[i] if i < 3 else f"{i + 1}."
            self.label(row, rank, 12, True, bg=CARD, width=3).pack(side="left")
            self.label(row, e["name"], 12, True, bg=CARD, anchor="w",
                       width=16).pack(side="left")
            self.label(row, e.get("category", ""), 10, color=MUTED, bg=CARD,
                       anchor="w", width=18).pack(side="left")
            self.label(row, f"{e['score']} pts", 12, True, color=ACCENT,
                       bg=CARD, anchor="e").pack(side="right")
        return box

    # ---------- home ----------
    def show_home(self):
        self.clear()
        c = self.container
        self.label(c, "⚡ BRAINBUZZ", 36, True, color=ACCENT).pack(pady=(6, 0))
        self.label(c, "Pick a topic, beat the clock, climb the leaderboard.",
                   12, color=MUTED).pack(pady=(4, 18))

        row = tk.Frame(c, bg=BG)
        row.pack(pady=(0, 18))
        self.label(row, "Your name", 12, color=MUTED).pack(side="left", padx=(0, 10))
        tk.Entry(row, textvariable=self.player_name, font=(FONT, 13), bg=CARD,
                 fg=TEXT, insertbackground=TEXT, relief="flat", width=20,
                 justify="center").pack(side="left", ipady=7)

        grid = tk.Frame(c, bg=BG)
        grid.pack()
        self.cat_buttons = {}
        for i, cat in enumerate(category_names()):
            text = f"{ICONS[cat]}\n{cat}\n{count_questions(cat)} questions"
            btn = tk.Button(
                grid, text=text, font=(FONT, 11, "bold"), fg=TEXT, relief="flat",
                bd=0, cursor="hand2", width=18, height=5,
                bg=PRIMARY if cat == self.category else CARD,
                activebackground=PRIMARY_HOVER, activeforeground=TEXT,
                command=lambda name=cat: self.select_category(name),
            )
            btn.bind("<Enter>", lambda e, n=cat: self.cat_hover(n, True))
            btn.bind("<Leave>", lambda e, n=cat: self.cat_hover(n, False))
            btn.grid(row=i // 3, column=i % 3, padx=8, pady=8)
            self.cat_buttons[cat] = btn

        self.label(c, f"🏆 Best score: {storage.best_score()}", 13, True,
                   color=WARN).pack(pady=(18, 10))

        make_button(c, "▶  START QUIZ", self.start_game, bg=PRIMARY,
                    hover=PRIMARY_HOVER, font=(FONT, 15, "bold"),
                    padx=40, pady=12).pack(pady=(0, 10))
        make_button(c, "🏆 Leaderboard", self.show_leaderboard,
                    font=(FONT, 11, "bold"), padx=24, pady=8).pack()

    def select_category(self, name):
        self.category = name
        for cat, btn in self.cat_buttons.items():
            btn.config(bg=PRIMARY if cat == name else CARD)

    def cat_hover(self, name, entering):
        if name == self.category:
            return
        self.cat_buttons[name].config(bg=CARD_HOVER if entering else CARD)

    def show_leaderboard(self):
        self.clear()
        c = self.container
        self.label(c, "🏆 Leaderboard", 28, True, color=ACCENT).pack(pady=(10, 16))
        self.build_leaderboard(c, 10).pack(fill="x", padx=60)
        make_button(c, "← Back", self.show_home, padx=30, pady=10).pack(pady=20)

    # ---------- quiz ----------
    def start_game(self):
        name = self.player_name.get().strip()[:16] or "Player"
        self.player_name.set(name)
        self.quiz = Quiz(get_questions(self.category))
        self.build_quiz_screen()
        self.load_question()

    def build_quiz_screen(self):
        self.clear()
        c = self.container

        header = tk.Frame(c, bg=BG)
        header.pack(fill="x")
        self.chip_label = tk.Label(header, font=(FONT, 11, "bold"), bg=CARD,
                                   fg=ACCENT, padx=14, pady=6)
        self.chip_label.pack(side="left")
        self.progress_label = self.label(header, "", 11, True, color=MUTED)
        self.progress_label.pack(side="right")

        stats = tk.Frame(c, bg=BG)
        stats.pack(fill="x", pady=(14, 8))
        self.score_label = self.label(stats, "⭐ Score: 0", 14, True)
        self.score_label.pack(side="left")
        self.streak_label = self.label(stats, "🔥 Streak: 0", 14, True, color=WARN)
        self.streak_label.pack(side="left", padx=24)
        self.time_label = self.label(stats, "", 14, True, color=GOOD)
        self.time_label.pack(side="right")

        self.timer_canvas = tk.Canvas(c, height=14, bg=BG, highlightthickness=0)
        self.timer_canvas.pack(fill="x", pady=(0, 18))

        card = tk.Frame(c, bg=CARD, padx=26, pady=26)
        card.pack(fill="x")
        self.question_label = tk.Label(card, font=(FONT, 19, "bold"), bg=CARD,
                                       fg=TEXT, wraplength=720, justify="left")
        self.question_label.pack(anchor="w")

        self.options_frame = tk.Frame(c, bg=BG)
        self.options_frame.pack(fill="both", expand=True, pady=(14, 0))
        self.options_frame.columnconfigure(0, weight=1, uniform="opt")
        self.options_frame.columnconfigure(1, weight=1, uniform="opt")

        self.feedback_label = self.label(c, "", 13, True)
        self.feedback_label.pack(pady=(6, 8))

        bottom = tk.Frame(c, bg=BG)
        bottom.pack(fill="x")
        self.fifty_btn = make_button(bottom, "✂ 50/50", self.use_fifty,
                                     font=(FONT, 11, "bold"), padx=18, pady=8)
        self.fifty_btn.pack(side="left")
        make_button(bottom, "✕ Quit", self.quit_quiz, font=(FONT, 11, "bold"),
                    fg=MUTED, padx=18, pady=8).pack(side="right")

    def load_question(self):
        quiz = self.quiz
        q = quiz.current
        self.locked = False
        self.chip_label.config(
            text=f"{ICONS.get(q['category'], '❓')} {q['category']}  •  {q['difficulty']}")
        self.progress_label.config(text=f"Question {quiz.index + 1} / {quiz.total}")
        self.question_label.config(text=q["question"])
        self.feedback_label.config(text="")

        for btn in self.option_buttons:
            btn.destroy()
        self.option_buttons = []
        for i, opt in enumerate(q["options"]):
            btn = make_button(
                self.options_frame, f"{'ABCD'[i]}   {opt}",
                lambda o=opt: self.on_answer(o),
                font=(FONT, 12, "bold"), anchor="w", justify="left",
                wraplength=330, padx=18, pady=16,
            )
            btn.grid(row=i // 2, column=i % 2, sticky="nsew", padx=8, pady=8)
            self.option_buttons.append(btn)

        self.start_timer()

    def start_timer(self):
        self.time_left = float(self.quiz.time_limit)
        self.tick()

    def tick(self):
        self.draw_timer()
        if self.time_left <= 0:
            self.on_answer(None)
            return
        self.time_left = round(self.time_left - 0.1, 2)
        self.timer_job = self.after(100, self.tick)

    def draw_timer(self):
        width = max(self.timer_canvas.winfo_width(), 2)
        frac = max(self.time_left / self.quiz.time_limit, 0)
        color = GOOD if frac > 0.5 else WARN if frac > 0.25 else BAD
        self.timer_canvas.delete("all")
        self.timer_canvas.create_rectangle(0, 0, width, 14, fill=TRACK, outline="")
        self.timer_canvas.create_rectangle(0, 0, width * frac, 14, fill=color,
                                           outline="")
        self.time_label.config(text=f"⏱ {math.ceil(max(self.time_left, 0))}s",
                               fg=color)

    def on_answer(self, choice):
        if self.locked:
            return
        self.locked = True
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        q = self.quiz.current
        result = self.quiz.submit(choice, self.time_left)

        for btn, opt in zip(self.option_buttons, q["options"]):
            btn.config(state="disabled")
            if opt == q["answer"]:
                btn.config(bg=GOOD, fg="white")
            elif opt == choice:
                btn.config(bg=BAD, fg="white")

        if result.correct:
            self.feedback_label.config(text=f"✅ Correct!  +{result.points} points",
                                       fg=GOOD)
        elif choice is None:
            self.feedback_label.config(
                text=f"⏰ Time's up!  Answer: {result.correct_answer}", fg=WARN)
        else:
            self.feedback_label.config(
                text=f"❌ Not quite.  Answer: {result.correct_answer}", fg=BAD)

        self.score_label.config(text=f"⭐ Score: {self.quiz.score}")
        self.streak_label.config(text=f"🔥 Streak: {self.quiz.streak}")
        self.next_job = self.after(1400, self.advance)

    def advance(self):
        self.next_job = None
        if self.quiz.is_finished():
            self.finish_game()
        else:
            self.load_question()

    def use_fifty(self):
        if self.locked:
            return
        removed = self.quiz.use_fifty_fifty()
        if not removed:
            return
        for btn, opt in zip(self.option_buttons, self.quiz.current["options"]):
            if opt in removed:
                btn.config(state="disabled", bg=BG, fg=MUTED,
                           disabledforeground=MUTED)
        self.fifty_btn.config(state="disabled", text="✂ 50/50 used", fg=MUTED,
                              disabledforeground=MUTED)

    def quit_quiz(self):
        if messagebox.askyesno("Quit quiz", "Leave this quiz? Your score won't be saved."):
            self.show_home()

    # ---------- result ----------
    def finish_game(self):
        quiz = self.quiz
        rank = storage.add_score(self.player_name.get(), quiz.score, self.category,
                                 quiz.correct_count, quiz.total)
        self.show_result(rank)

    def show_result(self, rank):
        self.clear()
        c = self.container
        quiz = self.quiz
        acc = quiz.accuracy()

        if acc >= 90:
            msg = "🏆 Legendary run!"
        elif acc >= 70:
            msg = "🔥 Great job, you're on fire!"
        elif acc >= 40:
            msg = "👍 Nice effort - one more round?"
        else:
            msg = "🌱 Everyone starts somewhere. Try again!"

        self.label(c, msg, 22, True, color=ACCENT).pack(pady=(4, 0))
        self.label(c, str(quiz.score), 60, True, color=TEXT).pack()
        self.label(c, "points", 12, color=MUTED).pack(pady=(0, 12))

        cards = tk.Frame(c, bg=BG)
        cards.pack(pady=(0, 12))
        stat_card(cards, f"{quiz.correct_count}/{quiz.total}", "Correct",
                  GOOD).grid(row=0, column=0, padx=8)
        stat_card(cards, f"{acc}%", "Accuracy", ACCENT).grid(row=0, column=1, padx=8)
        stat_card(cards, str(quiz.best_streak), "Best streak",
                  WARN).grid(row=0, column=2, padx=8)

        rank_text = (f"You are #{rank} on the leaderboard!" if rank <= 10
                     else "Keep going to reach the top 10!")
        self.label(c, rank_text, 12, True, color=WARN).pack(pady=(0, 8))
        self.build_leaderboard(c, 5).pack(fill="x", padx=60)

        buttons = tk.Frame(c, bg=BG)
        buttons.pack(pady=16)
        make_button(buttons, "↻ Play Again", self.start_game, bg=PRIMARY,
                    hover=PRIMARY_HOVER, padx=28, pady=10).pack(side="left", padx=8)
        make_button(buttons, "⌂ Home", self.show_home, padx=28,
                    pady=10).pack(side="left", padx=8)