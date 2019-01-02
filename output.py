import os

_CSV_FILE = "output.csv"
_DATA_DIR = "data"


def write_csv(puzzles: {}):
    file_path = os.path.join(os.getcwd(), _DATA_DIR, _CSV_FILE)
    with open(file_path, "w") as f:
        for word in puzzles:
            puzzle = puzzles[word]
            line = "{0};{1};{2}\r\n".format(word, puzzle["encrypted"], puzzle["hint"])
            f.write(line)
