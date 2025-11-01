from functools import lru_cache
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

MODEL_NAME = "allenai-specter"
NGRAM_RANGE = (1, 3)
TOPN_EACH = 50
TARGET_COUNT = 10
USE_MMR = True
DIVERSITY = 0.5
STOP_WORDS = "english"


@lru_cache(maxsize=1)
def _get_kw_model():
    emb = SentenceTransformer(MODEL_NAME)
    return KeyBERT(emb)


def _norm(s):
    return " ".join((s or "").lower().split())


def _select_keywords(title_kws, abstract_kws, k=TARGET_COUNT):
    tmap = {_norm(p): (p, s) for p, s in title_kws}
    amap = {_norm(p): (p, s) for p, s in abstract_kws}

    inter = []
    for key in set(tmap) & set(amap):
        pt, st = tmap[key]
        pa, sa = amap[key]
        disp = pt if len(pt) >= len(pa) else pa
        inter.append((disp, st + sa))
    inter.sort(key=lambda x: -x[1])
    selected = [p for p, _ in inter[:k]]

    if len(selected) >= k:
        return selected[:k]

    selected_norm = {_norm(p) for p in selected}
    pool = {}
    for p, s in list(tmap.values()) + list(amap.values()):
        key = _norm(p)
        pool[key] = max(pool.get(key, 0.0), s)

    for key in list(pool.keys()):
        if key in selected_norm:
            pool.pop(key, None)

    fillers = []
    for key, score in pool.items():
        disp = (tmap.get(key) or amap.get(key))[0]
        fillers.append((disp, score))
    fillers.sort(key=lambda x: -x[1])

    need = k - len(selected)
    selected.extend([p for p, _ in fillers[:need]])
    return selected


def keywords_for_paper(title, abstract, top_k=TARGET_COUNT):
    kwm = _get_kw_model()
    title_kws = kwm.extract_keywords(
        (title or "").strip(),
        keyphrase_ngram_range=NGRAM_RANGE,
        stop_words=STOP_WORDS,
        use_mmr=USE_MMR,
        diversity=DIVERSITY,
        top_n=TOPN_EACH,
    ) if title else []

    abstract_kws = kwm.extract_keywords(
        (abstract or "").strip(),
        keyphrase_ngram_range=NGRAM_RANGE,
        stop_words=STOP_WORDS,
        use_mmr=USE_MMR,
        diversity=DIVERSITY,
        top_n=TOPN_EACH,
    ) if abstract else []

    chosen = _select_keywords(title_kws, abstract_kws, k=top_k)
    return {_norm(p) for p in chosen if p}


def extract_keywords_for_papers(papers, top_k_per_paper=TARGET_COUNT):
    return [keywords_for_paper(t, a, top_k_per_paper) for (t, a) in papers]
