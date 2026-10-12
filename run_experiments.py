"""Sweep the percentage of malicious nodes (averaged over several random networks).
  python run_experiments.py            # saves results/sweep.png and results/sweep.csv
"""
import os, csv, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from wsn_trust_sim import Config, simulate

FRACS, SEEDS = [0, 0.1, 0.2, 0.3, 0.4], range(1, 11)
keys = ["pdr", "loss", "delay_ms", "overhead_pct", "energy_J", "detection"]
out = {m: {k: [] for k in keys} for m in ("shortest", "trust")}
for fr in FRACS:
    for m in out:
        runs = [simulate(Config(malicious_frac=fr, seed=s), m) for s in SEEDS]
        for k in keys:
            vals = [r[k] for r in runs if r[k] is not None]
            out[m][k].append(float(np.mean(vals)) if vals else float("nan"))
os.makedirs("results", exist_ok=True)
with open("results/sweep.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["malicious_%", "method"] + keys)
    for i, fr in enumerate(FRACS):
        for m in out: w.writerow([int(fr * 100), m] + [round(out[m][k][i], 3) for k in keys])
print(f"{'Mal%':>5}{'Method':>10}" + "".join(f"{k:>14}" for k in keys))
for i, fr in enumerate(FRACS):
    for m in out: print(f"{int(fr*100):>5}{m:>10}" + "".join(f"{out[m][k][i]:>14.2f}" for k in keys))
fig, ax = plt.subplots(2, 3, figsize=(14, 7)); x = [int(f * 100) for f in FRACS]
titles = ["PDR (%)", "Packet loss (%)", "End-to-end delay (ms)", "Routing overhead (%)", "Energy (J)", "Detection rate (%)"]
for a, k, t in zip(ax.ravel(), keys, titles):
    a.plot(x, out["shortest"][k], "o-", color="#e74c3c", label="Shortest-path")
    a.plot(x, out["trust"][k], "s-", color="#2ecc71", label="Trust-aware"); a.set_title(t)
    a.set_xlabel("Malicious nodes (%)"); a.grid(alpha=.3); a.legend()
plt.tight_layout(); plt.savefig("results/sweep.png", dpi=150); print("\nSaved results/sweep.png and results/sweep.csv")
