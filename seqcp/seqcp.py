# coding: utf-8
import io
import json
import os
from pathlib import PurePath

import fire
import matplotlib.pyplot as plt
import numpy as np
from seaborn import heatmap


def load(filename):
    replacement_matrix = {}
    with open(filename) as f:
        key_names = f.readline().strip().split()
        for line in f:
            key_values = line.strip().split()
            key, values = key_values[0], key_values[1:]
            assert len(key_names) == len(values), "\nkeys(%d): %s\nvalues(%d):%s" % (
                len(key_names), key_names, len(values), values
            )
            for cmp_key, value in zip(key_names, values):
                if key not in replacement_matrix:
                    replacement_matrix[key] = {}
                replacement_matrix[key][cmp_key] = int(value)
    return replacement_matrix


class BLOSUM(object):
    def __init__(self, matrix_type='62'):
        self.matrix = load(os.path.join(PurePath(__file__).parents[1], ("meta/BLOSUM%s" % matrix_type)))

    def __call__(self, key, cmp_key):
        return self.matrix[key][cmp_key]

    def __str__(self):
        matrix = [[""] * len(self.matrix) for _ in range(len(self.matrix))]
        sorted_keys = sorted(self.matrix.keys())
        for i, key in enumerate(sorted_keys):
            for j, cmp_key in enumerate(sorted_keys):
                matrix[i][j] = "%2s" % str(self(key, cmp_key))

        ret = []
        ret.append("\t".join([" "] + ["%2s" % key for key in sorted_keys]))
        for i, key in enumerate(sorted_keys):
            ret.append("\t".join([key] + matrix[i]))
        return "\n".join(ret)

    def __repr__(self):
        return str(self)


class SequenceComparePlayer(object):
    def __init__(self, matrix_type="62"):
        self.blosum = BLOSUM(matrix_type)

    def __call__(self, seq1: str, seq2: str) -> int:
        assert len(seq1) == len(seq2)
        score = 0
        if seq1 == seq2:
            seq1 = seq1.replace("-", "")
            seq2 = seq2.replace("-", "")
        for key1, key2 in zip(seq1, seq2):
            if key1 == "-" or key2 == "-":
                score += 11
            else:
                score += self.blosum(key1, key2)
        return score


def run(src, tar=None, itar=None, viz=True):
    seqs = []
    with open(src) as f:
        for line in f:
            line = line.strip()
            if line:
                seqs.append(line)

    result = [[0] * len(seqs) for _ in range(len(seqs))]

    scp = SequenceComparePlayer()

    for i, seq1 in enumerate(seqs):
        for j, seq2 in enumerate(seqs):
            result[i][j] = scp(seq1, seq2)

    if viz or itar:
        viz_result = np.array(result)
        plt.clf()
        heatmap(viz_result)
        if itar:
            plt.savefig(itar)
        if viz:
            plt.show()

    if tar:
        with io.open(tar, "w") as wf:
            json.dump(result, wf)


if __name__ == '__main__':
    fire.Fire(run)
