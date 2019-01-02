import os, requests, time

class Poster:

    _SERVER_PATH = "/json/add_puzzle"
    _CSV_FOLDER = "data"
    _CSV_FILE_NAME = "output.csv"

    def __init__(self):
        self._username = os.environ["username"]
        self._password = os.environ["password"]
        self._url = os.environ["server"] + self._SERVER_PATH

    def execute(self):

        csv_path = os.path.join(os.getcwd(), self._CSV_FOLDER, self._CSV_FILE_NAME)
        with open(csv_path) as f:
            tmp_lines = f.read().splitlines()

        pos = 0
        for line in tmp_lines:
            pos += 1
            words = line.split(";")
            post_data = {
                "username": self._username,
                "password": self._password,
                "question": words[1],
                "hint": words[2],
                "answer": words[0]
            }

            print("\r Posting {0} of {1}".format(str(pos), str(len(tmp_lines))))
            requests.post(self._url, data=post_data)
            time.sleep(0.1)

