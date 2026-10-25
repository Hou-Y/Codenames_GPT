# TODO: GloVe, word2vec, BERT, Nomic, embedding, 
#glove cosine similarity, word2vec cosine similarity
import gensim.downloader as gdl
#from sentence_transformers import SentenceTransformer
from guesser import Guesser
from embedding.utils import _l2_normalize, cosine_sim

#nomic_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
glove_model = gdl.load("glove-twitter-25")
word2vec_model = gdl.load("word2vec-google-news-300")



class glove_Guesser(Guesser):
    
    def __init__(self, team="Red"):
        super().__init__()
        self.team = team
        self.backend_name = backend
        self.vocab_mode = vocab_mode
        self.backend = get_backend(backend)
        self.guesses_made = 0
        self.ranked = []


    def set_board(self, words):
        self.words = words

    def set_clue(self, clue, num):
        self.clue = clue
        self.num = int(num)
        self.guesses_made = 0
        cvec = self.backend["vec"](clue)
        remaining = [w for w in self.words if w[0] != "*"]
        scored = [(cosine_sim(cvec, self.backend["vec"](w)), w) for w in remaining]
        self.ranked = sorted(scored, reverse=True)
        self._rank_idx = 0

    def get_remaining_options(self):
        remaining_options = []
        for i in range(len(self.words)):
            if self.words[i][0] == '*':
                continue
            remaining_options.append(self.words[i])
        return remaining_options

    def get_answer(self):
        remaining = [w for w in self.words if w[0] != "*"]
        # re-filter ranked list in case the board changed since set_clue
        self.ranked = [(s, w) for s, w in self.ranked if w in remaining]
        if not self.ranked:
            return None
        _, guess = self.ranked[self._rank_idx] if self._rank_idx < len(self.ranked) else self.ranked[-1]
        self.guesses_made += 1
        print(f"{self.team} Guesser ({self.backend_name}/{self.vocab_mode}) guess:", guess)
        return guess

    def keep_guessing(self):
        self._rank_idx += 1
        if self.guesses_made >= self.num + 1:
            return False
        if self._rank_idx >= len(self.ranked):
            return False
        top_sim = self.ranked[0][0]
        next_sim = self.ranked[self._rank_idx][0]
        return (top_sim - next_sim) < 0.15

    def has(w):
            return w.lower() in glove_model.key_to_index or w.capitalize() in glove_model.key_to_index

    def vec(w):
            for cand in (w.lower(), w.capitalize(), w.upper()):
                if cand in glove_model.key_to_index:
                    return _l2_normalize(glove_model[cand])
            return None


"""# debug
doc_vec = nomic_model.encode("search_document: APPLE")
query_vec = nomic_model.encode("search_query: fruit")


#debug
for name, kwargs in [
    ("nomic-ai/nomic-embed-text-v1.5", {"trust_remote_code": True}),
]:
    m = SentenceTransformer(name, **kwargs)
    v = m.encode("APPLE")
    print(name, v.shape)"""