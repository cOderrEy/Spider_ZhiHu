

target_words = [
    "好看",
    "漂亮",
    "可爱",
    "身材",
    "胸",
    "腿",
    "臀",
    "瘦",
    "胖",
]

def is_target(text):
    for word in target_words:
        if word in text:
            return True
    return False