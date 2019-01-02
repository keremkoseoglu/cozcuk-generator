import os, random


class Synonym:

    _CSV_FOLDER = "data"
    _CSV_FILE_NAME = "esanlamlilar.csv"
    _MIN_SYNONYM_LEN = 3

    _UNWANTED_PREFIX = {
        "mak",
        "mek",
        "lık",
        "lik"
    }

    def __init__(self):
        self._attempted_words = {}
        self._dictionary = {}
        self._file_lines = []
        self._max_read = 0
        self._puzzles = {}

    def execute(self, max_read=0) -> {}:
        self._max_read = max_read
        self._load_csv()
        self._build_dictionary()
        self._generate_puzzles()
        return self._puzzles

    def _build_dictionary(self):
        for file_line in self._file_lines:
            main_word_pos = -1

            while main_word_pos+1 < len(file_line):
                main_word_pos += 1
                main_word = file_line[main_word_pos]
                if main_word not in self._dictionary:
                    self._dictionary[main_word] = []
                pos = 0
                for word in file_line:
                    if pos != main_word_pos:
                        self._dictionary[main_word].append(word)
                    pos += 1

        tmp_dict = self._dictionary.copy()
        self._dictionary = {}

        for word in tmp_dict:
            if len(tmp_dict[word]) == 0:
                continue
            self._dictionary[word] = list(set(tmp_dict[word]))

    def _generate_puzzles(self):
        read_count = 0
        for file_line in self._file_lines:
            read_count += 1
            if (self._max_read > 0) and (read_count > self._max_read):
                return

            for word in file_line:
                if word in self._attempted_words or word == "":
                    continue
                self._attempted_words[word] = True

                subwords = self._get_subwords(word)
                if subwords is None or len(subwords) <= 0:
                    continue

                puzzle = self._get_best_encryption_of_subwords(subwords)
                if puzzle is None or puzzle["encrypted"] == "":
                    continue

                self._puzzles[word] = puzzle

    def _get_best_encryption_of_subwords(self, subwords: []) -> {}:
        candidates = []

        for subword in subwords:
            puzzle = self._get_best_encryption_of_word(subword)
            if puzzle is None or puzzle["encrypted"] == "" or puzzle["replacement"] == 0:
                continue
            candidates.append(puzzle)

        if len(candidates) == 0:
            return None

        candidates.sort(key=lambda x: x["replacement"], reverse=True)
        return candidates[0]

    def _get_best_encryption_of_word(self, word: str) -> {}:
        output = {
            "encrypted": "",
            "replacement": 0,
            "hint": ""
        }

        frags = word.split(" ")

        for frag in frags:
            rev_frag = frag[::-1]

            if frag in self._dictionary:
                candidates = self._dictionary[frag]
                if len(candidates) == 0:
                    output["encrypted"] += frag
                    output["hint"] += " " + frag
                else:
                    rnd_index = random.randint(0, len(candidates)-1)
                    output["encrypted"] += candidates[rnd_index]
                    output["hint"] += " " + candidates[rnd_index]
                    output["replacement"] += abs(len(frag) - len(output["encrypted"]))
            elif rev_frag in self._dictionary:
                candidates = self._dictionary[rev_frag]
                if len(candidates) == 0:
                    output["encrypted"] += frag
                    output["hint"] += " " + frag
                else:
                    rnd_index = random.randint(0, len(candidates)-1)
                    output["encrypted"] += candidates[rnd_index][::-1]
                    output["hint"] += " " + candidates[rnd_index][::-1]
                    output["replacement"] += abs(len(frag) - len(output["encrypted"]))
            else:
                output["encrypted"] += frag
                output["hint"] += " " + frag

        while output["hint"][:1] == " ":
            output["hint"] = output["hint"][1:len(output["hint"])]

        return output

    def _get_split_list(self, word: str, span1: int, span2: int) -> []:
        output = []
        part1 = word[:span1]
        part2 = word[-span2:]
        split_word = part1 + " " + part2
        output.append(split_word)

        sub1 = self._get_subwords(part1)
        sub2 = self._get_subwords(part2)

        for s1 in sub1:
            for s2 in sub2:
                split_word = s1 + " " + s2
                output.append(split_word)

        return output

    def _get_subwords(self, word: str) -> []:
        output = []

        span = len(word)

        while span > 2:
            span -= 1
            span2 = len(word) - span
            output += self._get_split_list(word, span, span2)
            if span != span2:
                output += self._get_split_list(word, span2, span)

        return list(set(output))

    def _get_words_in_line(self, line: str) -> []:
        output = []
        tmp = line.split(",")
        for word in tmp:
            if len(word) >= self._MIN_SYNONYM_LEN:
                output.append(word)
        return output

    def _load_csv(self):
        self._file_lines = []

        csv_path = os.path.join(os.getcwd(), self._CSV_FOLDER, self._CSV_FILE_NAME)
        with open(csv_path) as f:
            tmp_lines = f.read().splitlines()

        for line in tmp_lines:
            new_line = line.replace(";", ",")
            new_line = new_line.replace(", ", ",")
            new_line = new_line.replace(" ,", "")
            if " " in new_line:
                continue

            words = self._get_words_in_line(new_line)
            file_line = []
            for word in words:
                if len(word) > 3 and word[-3:] in self._UNWANTED_PREFIX:
                    continue

                file_line.append(word)

            if len(file_line) == 0:
                continue

            self._file_lines.append(file_line)
