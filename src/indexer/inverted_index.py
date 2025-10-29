import os
import json
import re
from collections import defaultdict
from statistics import mean, pvariance
from .trie import TrieCompact

TOKEN_RE = re.compile(r'\w+', re.UNICODE)

def tokenize(text):
    return [t.lower() for t in TOKEN_RE.findall(text)]

class InvertedIndex:
    def __init__(self):
        self.index = {}          # term -> {doc_id: freq}
        self.doc_lengths = {}    # doc_id -> token count
        self.doc_ids = []        # ordered list of doc_ids (filenames)
        self.trie = TrieCompact()
        self.term_stats = {}     # term -> (mean, stddev)
        self.corpus_dir = None

    def build_from_corpus(self, corpus_dir):
        corpus_dir = os.path.abspath(corpus_dir)
        self.corpus_dir = corpus_dir
        if not os.path.isdir(corpus_dir):
            return

        files = sorted(f for f in os.listdir(corpus_dir) if os.path.isfile(os.path.join(corpus_dir, f)))
        self.doc_ids = files

        for fname in files:
            fpath = os.path.join(corpus_dir, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            except Exception:
                text = ""

            tokens = tokenize(text)
            self.doc_lengths[fname] = len(tokens)
            freqs = defaultdict(int)
            for t in tokens:
                freqs[t] += 1

            for term, freq in freqs.items():
                posting = self.index.setdefault(term, {})
                posting[fname] = posting.get(fname, 0) + freq
                self.trie.insert(term, fname, freq)

        self._compute_term_stats()

    def _compute_term_stats(self):
        n_docs = len(self.doc_ids)
        if n_docs == 0:
            return
        stats = {}
        for term, postings in self.index.items():
            freqs = [postings.get(doc_id, 0) for doc_id in self.doc_ids]
            mu = mean(freqs)
            var = pvariance(freqs)
            std = var ** 0.5
            stats[term] = (mu, std)
        self.term_stats = stats

    def save(self, path):
        data = {
            "index": self.index,
            "doc_lengths": self.doc_lengths,
            "doc_ids": self.doc_ids
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.index = {k: v for k, v in data.get("index", {}).items()}
        self.doc_lengths = data.get("doc_lengths", {})
        self.doc_ids = data.get("doc_ids", [])
        self.trie = TrieCompact()
        for term, postings in self.index.items():
            for doc_id, freq in postings.items():
                self.trie.insert(term, doc_id, freq)
        self._compute_term_stats()

    def load_or_build(self, index_path, corpus_dir):
        self.corpus_dir = corpus_dir
        if os.path.exists(index_path):
            try:
                self.load(index_path)
                return
            except Exception:
                pass
        self.build_from_corpus(corpus_dir)
        try:
            self.save(index_path)
        except Exception:
            pass

    def get_postings(self, term):
        return self.index.get(term, {})

    def get_doc_length(self, doc_id):
        return self.doc_lengths.get(doc_id, 0)

    def get_term_stats(self, term):
        return self.term_stats.get(term, (0.0, 0.0))

    def zscore_for(self, term, doc_id):
        mu, std = self.get_term_stats(term)
        freq = self.index.get(term, {}).get(doc_id, 0)
        if std == 0:
            return 0.0
        return (freq - mu) / std

    def snippet_for(self, doc_id, term, context=80):
        fpath = os.path.join(self.corpus_dir, doc_id) if self.corpus_dir else doc_id
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception:
            return ""

        lower = text.lower()
        t = term.lower()
        pos = lower.find(t)
        if pos == -1:
            start = 0
            snippet = text[start:start + context * 2]
            return snippet.replace('\n', ' ')
        start = max(0, pos - context)
        end = min(len(text), pos + len(term) + context)
        snippet = text[start:end].replace('\n', ' ')
        snippet_lower = snippet.lower()
        idx = snippet_lower.find(t)
        if idx != -1:
            before = snippet[:idx]
            matched = snippet[idx:idx+len(term)]
            after = snippet[idx+len(term):]
            return f"{before}<b>{matched}</b>{after}"
        return snippet