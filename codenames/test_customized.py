from custom_board import CustomGame
from players.codemaster_GPT import AICodemaster
from players.guesser_GPT import AIGuesser

CustomGame(
    AICodemaster, AIGuesser, AICodemaster, AIGuesser,
    red_words=["IRON", "HAM", "BEIJING"],
    blue_words=["WITCH", "NOTE", "CAT"],
    civilian_words=["BEAR", "AMBULANCE"],
    assassin_words=["FALL"],
    seed=0, do_print=True, game_name="custom_test"
).run()

