from typing import Set, Optional, Dict

# from matplotlib import pyplot as plt # Unused import commented out

class Node:
    # Type annotation preamble to make Node a concrete (not generic) class
    _children: Set[Optional[int]]
    _count: int
    kmer: str
    visited: bool
    depth: int
    max_depth_child: Optional[int]

    def __init__(self, kmer):
        self._children = set()
        self._count = 0
        self.kmer = kmer
        self.visited = False
        self.depth = 0
        self.max_depth_child = None

    def add_child(self, child_idx):
        self._children.add(child_idx)

    def add_count(self, count=1):
        self._count += count


class DBG:
    def __init__(self, k, data_list):
        self.k = k
        # Explicitly type the dictionaries
        self.nodes: Dict[int, Node] = {}
        self.kmer2idx: Dict[str, int] = {}
        self.kmer_count = 0
        # build
        self._check(data_list)
        self._build(data_list)

    def _check(self, data_list):
        for data in data_list:
            if len(data) < self.k:
                raise ValueError("data length should be larger than k")

    def _build(self, data_list):
        for data in data_list:
            for i in range(len(data) - self.k + 1):
                kmer = data[i:i + self.k]
                if kmer not in self.kmer2idx:
                    self.kmer2idx[kmer] = self.kmer_count
                    self.nodes[self.kmer_count] = Node(kmer)
                    self.kmer_count += 1
                self.nodes[self.kmer2idx[kmer]].add_count()

        for kmer in self.kmer2idx:
            for i in range(4):
                next_kmer = kmer[1:] + 'ACGT'[i]
                if next_kmer in self.kmer2idx:
                    self.nodes[self.kmer2idx[kmer]].add_child(
                        self.kmer2idx[next_kmer])

    def _get_depth(self, node_idx):
        if self.nodes[node_idx].visited:
            return self.nodes[node_idx].depth

        self.nodes[node_idx].visited = True
        max_depth = 0
        max_depth_child = None
        for child in self.nodes[node_idx]._children:
            depth = self._get_depth(child)
            if depth > max_depth:
                max_depth = depth
                max_depth_child = child
        self.nodes[node_idx].depth = max_depth + self.nodes[node_idx]._count
        self.nodes[node_idx].max_depth_child = max_depth_child
        return self.nodes[node_idx].depth

    def get_contigs(self):
        for node_idx in self.nodes:
            self._get_depth(node_idx)

        contigs = []
        for node_idx in sorted(self.nodes.keys()):
            if self.nodes[node_idx].depth > 0:
                contig = ""
                cur_idx = Optional(node_idx)
                while cur_idx is not None:
                    contig += self.nodes[cur_idx].kmer[-1]
                    self.nodes[cur_idx].depth = 0
                    cur_idx = self.nodes[cur_idx].max_depth_child
                contigs.append(self.nodes[node_idx].kmer[:-1] + contig)
        return contigs
