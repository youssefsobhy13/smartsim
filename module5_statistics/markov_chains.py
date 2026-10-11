"""Markov chains: transition matrices and steady state."""

from typing import Sequence

import numpy as np


def transition_matrix(matrix: Sequence[Sequence[float]]) -> np.ndarray:
    """Validate a transition matrix (square, non-negative, rows sum to 1).

    Raises:
        ValueError: If the matrix is not a valid transition matrix.
    """
    p = np.asarray(matrix, dtype=float)
    if p.ndim != 2 or p.shape[0] != p.shape[1]:
        raise ValueError("matrix must be square")
    if (p < 0).any():
        raise ValueError("probabilities must be non-negative")
    if not np.allclose(p.sum(axis=1), 1.0):
        raise ValueError("each row must sum to 1")
    return p


def transition_matrix_from_sequence(states: Sequence[int], n_states: int) -> np.ndarray:
    """Estimate a transition matrix from an observed state sequence."""
    counts = np.zeros((n_states, n_states))
    for a, b in zip(states[:-1], states[1:]):
        counts[a, b] += 1
    rows = counts.sum(axis=1, keepdims=True)
    rows[rows == 0] = 1
    p = counts / rows
    # states never left: make them absorbing so rows still sum to 1
    for i in range(n_states):
        if counts[i].sum() == 0:
            p[i, i] = 1.0
    return p


def steady_state(matrix: Sequence[Sequence[float]]) -> np.ndarray:
    """Solve ``pi P = pi`` with ``sum(pi) = 1``.

    Example:
        >>> steady_state([[0.9, 0.1], [0.5, 0.5]]).round(4).tolist()
        [0.8333, 0.1667]
    """
    p = transition_matrix(matrix)
    n = p.shape[0]
    a = np.vstack([p.T - np.eye(n), np.ones(n)])
    b = np.zeros(n + 1)
    b[-1] = 1.0
    pi, *_ = np.linalg.lstsq(a, b, rcond=None)
    return pi
