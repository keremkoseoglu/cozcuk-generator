from synonym import Synonym
import output
from poster import Poster


def generate_puzzles():
    output.write_csv(Synonym().execute(max_read=100000))


def post_to_server():
    Poster().execute()


post_to_server()
