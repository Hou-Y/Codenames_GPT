import random
import time
import os
import sys
import colorama

from game import Game


class CustomGame(Game):
    """Sublcass with custom size and word allocation for testing purposes.

    only the Codemasters receive the key_grid
    (via set_game_state); the Guessers only ever see the word list
    (via set_board), so role assignments stay hidden from them.
    """

    def __init__(self, codemaster_red, guesser_red, codemaster_blue, guesser_blue,
                 red_words, blue_words, civilian_words, assassin_words,
                 shuffle_board=True,
                 seed="time", do_print=True, do_log=True, game_name="custom_test",
                 cmr_kwargs={}, gr_kwargs={}, cmb_kwargs={}, gb_kwargs={},
                 single_team=True):
        #modify single_team to True to test single team mode
        """
        Args:
            red_words, blue_words, civilian_words, assassin_words (list[str]):
                Explicit words to assign to each role. All words must be
                unique across the four lists combined.
            shuffle_board (bool, optional):
                Whether to shuffle the position of words on the board. Defaults to True.
        """

        self.game_winner = None
        self.game_start_time = time.time()
        self.game_end_time = None
        colorama.init()

        self.do_print = do_print
        if not self.do_print:
            self._save_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        self.codemaster_red = codemaster_red("Red", **cmr_kwargs)
        self.guesser_red = guesser_red("Red", **gr_kwargs)
        self.codemaster_blue = codemaster_blue("Blue", **cmb_kwargs)
        self.guesser_blue = guesser_blue("Blue", **gb_kwargs)

        self.cmr_kwargs = cmr_kwargs
        self.gr_kwargs = gr_kwargs
        self.cmb_kwargs = cmb_kwargs
        self.gb_kwargs = gb_kwargs
        self.do_log = do_log
        self.game_name = game_name
        self.single_team = single_team

        self.num_red_words = len(red_words)
        self.num_blue_words = len(blue_words)
        self.num_civilian_words = len(civilian_words)
        self.num_assassin_words = len(assassin_words)

        self.move_history = []

        if seed == 'time':
            self.seed = time.time()
            random.seed(self.seed)
        else:
            self.seed = seed
            random.seed(int(seed))

        print("seed:", self.seed)

        all_words = list(red_words) + list(blue_words) + list(civilian_words) + list(assassin_words)
        assert len(all_words) == len(set(all_words)), \
            "words must be unique across red/blue/civilian/assassin lists"
        assert len(all_words) > 0, "must provide at least one word"

        words_on_board = list(red_words) + list(blue_words) + list(civilian_words) + list(assassin_words)
        key_grid = (["Red"] * self.num_red_words + ["Blue"] * self.num_blue_words +
                    ["Civilian"] * self.num_civilian_words + ["Assassin"] * self.num_assassin_words)

        #  shuffle position
        if shuffle_board: # perchè la posizione invece non cambia?
            paired = list(zip(words_on_board, key_grid))
            random.shuffle(paired)
            words_on_board, key_grid = [list(t) for t in zip(*paired)]

        self.words_on_board = words_on_board
        self.key_grid = key_grid