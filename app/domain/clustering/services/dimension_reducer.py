# dimension_reducer.py
import numpy as np

def build_keyword_counts(kw_per_paper_A, kw_per_paper_B):
    vocab_set = set()
    for s in kw_per_paper_A:
        vocab_set.update(s)
    for s in kw_per_paper_B:
        vocab_set.update(s)

    vocab = sorted(vocab_set)
    idx = {w: i for i, w in enumerate(vocab)}
    counts = np.zeros((len(vocab), 2), dtype=float)

    # count *papers* that contain the keyword (not raw token freq)
    for paper_set in kw_per_paper_A:
        for w in paper_set:
            counts[idx[w], 0] += 1.0
    for paper_set in kw_per_paper_B:
        for w in paper_set:
            counts[idx[w], 1] += 1.0

    return vocab, counts


def logratio_positions(counts, alpha=0.5):
    """Return 2D positions: x = log((A+α)/(B+α)), y = log(A+B+2α)."""
    A = counts[:, 0]
    B = counts[:, 1]
    x = np.log((A + alpha) / (B + alpha))
    y = np.log(A + B + 2 * alpha)
    coords = np.column_stack([x, y]).astype(float)
    basis = np.array([[1.0, -1.0], [1.0, 1.0]])  # purely informational
    return coords, basis
