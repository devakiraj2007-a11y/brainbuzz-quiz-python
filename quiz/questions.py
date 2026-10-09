import random

MIXED_COUNT = 10


def _q(question, options, answer, difficulty="Easy"):
    return {
        "question": question,
        "options": options,
        "answer": answer,
        "difficulty": difficulty,
    }


QUESTIONS = {
    "Python": [
        _q("Which keyword is used to define a function in Python?",
           ["func", "def", "function", "lambda"], "def"),
        _q("What does len([1, 2, 3]) return?",
           ["2", "3", "4", "Error"], "3"),
        _q("Which of these data types is mutable?",
           ["tuple", "str", "list", "int"], "list"),
        _q("What is the result of 2 ** 3?",
           ["6", "8", "9", "5"], "8"),
        _q("Which symbol starts a single-line comment in Python?",
           ["//", "#", "--", "/*"], "#"),
        _q("What does the 'pip' command do?",
           ["Installs Python packages", "Compiles Python code",
            "Formats your code", "Runs unit tests"],
           "Installs Python packages", "Medium"),
        _q("What does 7 // 2 return?",
           ["3", "3.5", "4", "2"], "3", "Medium"),
        _q("Which keyword turns a function into a generator?",
           ["return", "yield", "async", "break"], "yield", "Hard"),
    ],
    "Science": [
        _q("What planet is known as the Red Planet?",
           ["Venus", "Mars", "Jupiter", "Mercury"], "Mars"),
        _q("Which gas do plants absorb from the air?",
           ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], "Carbon dioxide"),
        _q("What is the hardest natural substance?",
           ["Gold", "Iron", "Quartz", "Diamond"], "Diamond"),
        _q("Approximately how fast does light travel?",
           ["300,000 km/s", "150,000 km/s", "30,000 km/s", "3,000,000 km/s"],
           "300,000 km/s", "Medium"),
        _q("What is the largest organ of the human body?",
           ["Liver", "Skin", "Heart", "Lungs"], "Skin", "Medium"),
        _q("What is the chemical symbol for gold?",
           ["Ag", "Au", "Gd", "Go"], "Au", "Medium"),
        _q("Which part of the cell is called its powerhouse?",
           ["Nucleus", "Ribosome", "Mitochondria", "Golgi body"],
           "Mitochondria", "Medium"),
        _q("What is the atomic number of carbon?",
           ["6", "12", "8", "4"], "6", "Hard"),
    ],
    "Technology": [
        _q("What does HTML stand for?",
           ["HyperText Markup Language", "HighText Machine Language",
            "Hyper Transfer Markup Language", "Home Tool Markup Language"],
           "HyperText Markup Language"),
        _q("Who co-founded Microsoft?",
           ["Steve Jobs", "Bill Gates", "Linus Torvalds", "Tim Berners-Lee"],
           "Bill Gates"),
        _q("What does CPU stand for?",
           ["Central Processing Unit", "Computer Power Unit",
            "Core Program Utility", "Central Program Update"],
           "Central Processing Unit"),
        _q("Which language is mainly used to style web pages?",
           ["Python", "CSS", "SQL", "C++"], "CSS"),
        _q("Which company develops the Android operating system?",
           ["Apple", "Microsoft", "Google", "Samsung"], "Google", "Medium"),
        _q("What does SQL stand for?",
           ["Structured Query Language", "Simple Question Language",
            "Sequential Query Logic", "System Queue Language"],
           "Structured Query Language", "Medium"),
        _q("Which data structure follows the LIFO principle?",
           ["Queue", "Stack", "Array", "Graph"], "Stack", "Medium"),
        _q("What is the time complexity of binary search?",
           ["O(n)", "O(n log n)", "O(log n)", "O(1)"], "O(log n)", "Hard"),
    ],
    "General Knowledge": [
        _q("Which is the largest ocean on Earth?",
           ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
           "Pacific Ocean"),
        _q("How many continents are there?",
           ["5", "6", "7", "8"], "7"),
        _q("What is the capital of Japan?",
           ["Kyoto", "Osaka", "Tokyo", "Seoul"], "Tokyo"),
        _q("Who wrote 'Pride and Prejudice'?",
           ["Jane Austen", "Emily Bronte", "Charlotte Bronte", "Mary Shelley"],
           "Jane Austen", "Medium"),
        _q("Which is the smallest country in the world by area?",
           ["Monaco", "Vatican City", "Malta", "San Marino"],
           "Vatican City", "Medium"),
        _q("Who painted the Mona Lisa?",
           ["Michelangelo", "Raphael", "Leonardo da Vinci", "Van Gogh"],
           "Leonardo da Vinci", "Medium"),
        _q("In which year did World War II end?",
           ["1939", "1945", "1950", "1918"], "1945", "Medium"),
        _q("What is the capital of Australia?",
           ["Sydney", "Melbourne", "Canberra", "Perth"], "Canberra", "Hard"),
    ],
}

ICONS = {
    "Python": "🐍",
    "Science": "🔬",
    "Technology": "💻",
    "General Knowledge": "🌍",
    "Mixed": "🎲",
}


def category_names():
    return list(QUESTIONS) + ["Mixed"]


def _tag(category, items):
    return [dict(q, category=category, options=list(q["options"])) for q in items]


def get_questions(category):
    if category == "Mixed":
        pool = [q for cat, items in QUESTIONS.items() for q in _tag(cat, items)]
        random.shuffle(pool)
        return pool[:MIXED_COUNT]
    return _tag(category, QUESTIONS[category])


def count_questions(category):
    if category == "Mixed":
        total = sum(len(items) for items in QUESTIONS.values())
        return min(MIXED_COUNT, total)
    return len(QUESTIONS[category])