"""Run ONE simulation and compare shortest-path vs trust-aware routing.
Examples:
  python run_demo.py
  python run_demo.py --malicious 0.3 --nodes 80 --rounds 300 --plot
"""
import argparse
from dataclasses import fields
from wsn_trust_sim import Config, simulate

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--nodes", type=int); ap.add_argument("--malicious", type=float, help="fraction, e.g. 0.2")
ap.add_argument("--rounds", type=int); ap.add_argument("--seed", type=int)
ap.add_argument("--alpha", type=float); ap.add_argument("--beta", type=float)
ap.add_argument("--drop", type=float, help="drop probability of malicious nodes")
ap.add_argument("--attack-start", type=int, help="round when attackers turn malicious (on/off attack)")
ap.add_argument("--plot", action="store_true", help="save results/demo.png")
a = ap.parse_args()
cfg = Config()
for k, v in dict(n_nodes=a.nodes, malicious_frac=a.malicious, rounds=a.rounds, seed=a.seed, alpha=a.alpha,
                 beta=a.beta, drop_prob=a.drop, attack_start=a.attack_start).items():
    if v is not None: setattr(cfg, k, v)

sp, tr = simulate(cfg, "shortest"), simulate(cfg, "trust")
print(f"\nNodes={cfg.n_nodes}  malicious={cfg.malicious_frac:.0%}  rounds={cfg.rounds}  "
      f"packets sent={sp['sent']}  alpha={cfg.alpha} beta={cfg.beta}\n")
rows = [("Packet delivery ratio (%)", "pdr"), ("Packet loss (%)", "loss"), ("Avg end-to-end delay (ms)", "delay_ms"),
        ("Routing overhead (%)", "overhead_pct"), ("Energy consumption (J)", "energy_J"),
        ("Hops handled by malicious nodes (%)", "mal_hop_share"), ("Malicious-node detection rate (%)", "detection"),
        ("False-positive rate (%)", "false_pos")]
print(f"{'Metric':40s}{'Shortest-path':>15s}{'Trust-aware':>14s}")
for name, k in rows:
    f = lambda r: "n/a" if r[k] is None else f"{r[k]:.2f}"
    print(f"{name:40s}{f(sp):>15s}{f(tr):>14s}")
ok, bad = tr["ledger"].verify()
print(f"\nLedger: {len(tr['ledger'].chain)} blocks, integrity check: {'PASSED' if ok else 'FAILED at block %s' % bad}")

if a.plot:
    import os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
    os.makedirs("results", exist_ok=True)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].bar(["Shortest-path", "Trust-aware"], [sp["pdr"], tr["pdr"]], color=["#e74c3c", "#2ecc71"])
    for i, v in enumerate([sp["pdr"], tr["pdr"]]): ax[0].text(i, v + 1, f"{v:.1f}%", ha="center")
    ax[0].set_ylim(0, 110); ax[0].set_ylabel("PDR (%)"); ax[0].set_title("Packet delivery ratio")
    obs = tr["S"] + tr["F"]; mal = tr["mal"]
    h = np.where(~mal)[0]; m = np.where(mal)[0]
    if len(h): ax[1].plot(tr["hist"][:, h[np.argmax(obs[h])]], color="#2ecc71", label="Honest node (most used)")
    if len(m): ax[1].plot(tr["hist"][:, m[np.argmax(obs[m])]], color="#e74c3c", label="Malicious node (most observed)")
    ax[1].set_ylim(0, 1.05); ax[1].set_xlabel("Round"); ax[1].set_ylabel("Trust T"); ax[1].legend()
    ax[1].set_title("Trust score evolution")
    plt.tight_layout(); plt.savefig("results/demo.png", dpi=150); print("Saved results/demo.png")
