"""Caixas conservadoras e distancias para a triagem de movimento R54."""
import itertools
import numpy as np

# IDs conferidos por label e hierarquia do snapshot R54; nao sao medidas reais.
FIXED_ENVELOPES = ['Peca088'] + ['Peca%03d'%i for i in range(113,122)] + [
    'Peca131','Peca132','Peca134','Peca138','Peca139','Peca140','Peca141',
    'Peca152','Peca154','Peca155','Peca156']
RIGID_MIRRORS = ['EspelhoAplicadoR12','EspelhoAplicadoR001']


def transformed_box(box, matrix):
    corners = np.array(list(itertools.product(*zip(box[:3], box[3:]))))
    points = np.c_[corners, np.ones(8)] @ matrix.T
    return np.r_[points[:, :3].min(axis=0), points[:, :3].max(axis=0)]


def distances(a, b):
    gap = np.maximum(np.maximum(a[:, None, :3] - b[None, :, 3:],
                                b[None, :, :3] - a[:, None, 3:]), 0)
    return np.linalg.norm(gap, axis=2)
