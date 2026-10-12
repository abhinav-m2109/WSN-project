"""
wsn_trust_sim.py
Lightweight blockchain-based trust-aware routing for Wireless Sensor Networks (simulation).

Model (simplified, for learning/demo):
  * Nodes are placed randomly; a base station (BS) sits in the field.
  * Packets travel hop by hop towards the BS (each hop must get closer to the BS).
  * Malicious nodes drop packets; every node also has a small random link loss.
  * Trust:      T_i = S_i / (S_i + F_i)            (S/F = successful/failed forwards)
  * Route cost: C_i = alpha * D_i + beta * (1 - T_i) (D_i = distance of candidate to BS, normalised)
  * Trust values are committed to a tiny hash-chained ledger (a "lightweight blockchain").
Two routers are compared on the SAME network: 'shortest' (greedy, trust-unaware) and 'trust'.
"""
import hashlib, json
from dataclasses import dataclass
import numpy as np


@dataclass
class Config:
    n_nodes: int = 60
    area: float = 100.0
    comm_range: float = 25.0
    bs: tuple = (50.0, 50.0)
    malicious_frac: float = 0.2
    drop_prob: float = 0.7          # chance a malicious node drops a packet it should forward
    link_loss: float = 0.02         # random loss per hop (affects every node)
    rounds: int = 200
    packets_per_round: int = 15
    alpha: float = 0.4              # weight of distance in route cost
    beta: float = 0.6               # weight of (1 - trust) in route cost
    init_trust: float = 0.5         # trust before any observation
    trust_threshold: float = 0.4    # candidates below this are skipped if alternatives exist
    flag_threshold: float = 0.5     # a node is "detected" if trust < this ...
    min_obs: int = 5                # ... after at least this many observations
    attack_start: int = 0           # round when malicious nodes start dropping (>0 = on/off attacker)
    block_every: int = 5            # rounds per ledger block
    seed: int = 1
    # radio / size model (first-order radio model)
    packet_bits: int = 4000
    e_elec: float = 50e-9
    e_amp: float = 100e-12
    hop_delay_ms: float = 5.0
    data_packet_bytes: int = 500
    record_bytes: int = 4           # id (2 B) + trust (2 B)
    block_header_bytes: int = 40    # previous hash + index/round


class Ledger:
    """Tiny hash-chained ledger: every block stores only (node_id, trust) records."""

    def __init__(self):
        self.chain = []
        self.trust = {}
        self._append(0, [])  # genesis block

    @staticmethod
    def _hash(index, rnd, prev, records):
        data = json.dumps([index, rnd, prev, records]).encode()
        return hashlib.sha256(data).hexdigest()

    def _append(self, rnd, records):
        prev = self.chain[-1]["hash"] if self.chain else "0" * 64
        idx = len(self.chain)
        self.chain.append({"index": idx, "round": rnd, "prev": prev, "records": records,
                           "hash": self._hash(idx, rnd, prev, records)})

    def add_block(self, rnd, records):
        """records: list of [node_id, trust]"""
        self._append(rnd, records)
        for node, t in records:
            self.trust[node] = t

    def verify(self):
        """Return (ok, index_of_first_bad_block)."""
        for i, b in enumerate(self.chain):
            prev = self.chain[i - 1]["hash"] if i else "0" * 64
            if b["prev"] != prev or b["hash"] != self._hash(b["index"], b["round"], b["prev"], b["records"]):
                return False, i
        return True, None

    def rebuild_trust(self, upto=None):
        self.trust = {}
        for b in self.chain[:upto]:
            for node, t in b["records"]:
                self.trust[node] = t


def build_network(cfg):
    rng = np.random.default_rng(cfg.seed)
    pos = rng.uniform(0, cfg.area, (cfg.n_nodes, 2))
    mal = np.zeros(cfg.n_nodes, bool)
    mal[rng.choice(cfg.n_nodes, int(round(cfg.malicious_frac * cfg.n_nodes)), replace=False)] = True
    return pos, mal


def simulate(cfg, mode):
    """mode: 'shortest' (trust-unaware greedy) or 'trust' (blockchain trust-aware)."""
    assert mode in ("shortest", "trust")
    pos, mal = build_network(cfg)
    rng = np.random.default_rng(cfg.seed + 1000)          # same packet randomness for both modes
    n = cfg.n_nodes
    bs = np.array(cfg.bs)
    d_bs = np.linalg.norm(pos - bs, axis=1)
    dist = np.linalg.norm(pos[:, None] - pos[None], axis=2)
    dmax = d_bs.max()
    idx = np.arange(n)
    S, F = np.zeros(n), np.zeros(n)
    trust = np.full(n, cfg.init_trust)                    # trust as read from the ledger
    ledger, pending = Ledger(), set()
    hist = np.zeros((cfg.rounds, n))
    sent = delivered = tx_count = mal_hops = hops_total = 0
    energy = ctrl_bytes = delay_sum = 0.0
    tx_e = lambda d: cfg.packet_bits * (cfg.e_elec + cfg.e_amp * d * d)
    rx_e = cfg.packet_bits * cfg.e_elec

    for rnd in range(cfg.rounds):
        attacking = rnd >= cfg.attack_start
        for s in rng.integers(0, n, cfg.packets_per_round):
            sent += 1
            cur, hops, ok = s, 0, False
            while True:
                if d_bs[cur] <= cfg.comm_range:                       # BS in range: last hop
                    energy += tx_e(d_bs[cur]); tx_count += 1; hops += 1
                    ok = rng.random() >= cfg.link_loss
                    break
                cand = idx[(dist[cur] <= cfg.comm_range) & (d_bs < d_bs[cur])]
                if cand.size == 0:                                    # routing void
                    break
                if mode == "shortest":
                    nxt = cand[np.argmin(d_bs[cand])]
                else:
                    pool = cand[trust[cand] >= cfg.trust_threshold]
                    pool = pool if pool.size else cand
                    cost = cfg.alpha * d_bs[pool] / dmax + cfg.beta * (1 - trust[pool])
                    nxt = pool[np.argmin(cost)]
                energy += tx_e(dist[cur, nxt]) + rx_e; tx_count += 1; hops += 1
                mal_hops += bool(mal[nxt]); hops_total += 1
                bad = (mal[nxt] and attacking and rng.random() < cfg.drop_prob) or rng.random() < cfg.link_loss
                if bad:
                    F[nxt] += 1; pending.add(nxt); break
                S[nxt] += 1; pending.add(nxt); cur = nxt
            if ok:
                delivered += 1
                delay_sum += hops * cfg.hop_delay_ms + rng.uniform(0, 2, hops).sum()
        # commit trust to the ledger every block_every rounds (trust mode only)
        last = rnd == cfg.rounds - 1
        if mode == "trust" and pending and ((rnd + 1) % cfg.block_every == 0 or last):
            recs = [[int(i), round(float(S[i] / (S[i] + F[i])), 4)] for i in sorted(pending)]
            ledger.add_block(rnd, recs)
            for i, t in recs:
                trust[i] = t
            blk = cfg.block_header_bytes + cfg.record_bytes * len(recs)
            ctrl_bytes += blk * n                                     # every node relays the block once
            energy += n * blk * 8 * (cfg.e_elec + cfg.e_amp * cfg.comm_range ** 2)
            pending = set()
        hist[rnd] = trust

    res = dict(mode=mode, sent=sent, delivered=delivered, pdr=100 * delivered / sent,
               loss=100 * (1 - delivered / sent), delay_ms=delay_sum / max(delivered, 1),
               overhead_pct=100 * ctrl_bytes / (tx_count * cfg.data_packet_bytes),
               energy_J=energy, mal_hop_share=100 * mal_hops / max(hops_total, 1),
               hist=hist, mal=mal, S=S, F=F, ledger=ledger, detection=None, false_pos=None)
    if mode == "trust":
        obs = (S + F) >= cfg.min_obs
        flagged = obs & (trust < cfg.flag_threshold)
        res["detection"] = 100 * (flagged & mal).sum() / max(mal.sum(), 1)
        res["false_pos"] = 100 * (flagged & ~mal).sum() / max((~mal).sum(), 1)
    return res
