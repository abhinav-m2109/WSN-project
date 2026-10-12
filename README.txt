## Setup (Windows / macOS / Linux)
```bash
python -m venv venv
# Windows:  venv\Scripts\activate        macOS/Linux:  source venv/bin/activate
pip install -r requirements.txt
```

## Run
| Command | What it does |
|---|---|
| `python run_demo.py --plot` | One run, side-by-side metrics table + `results/demo.png` |
| `python run_demo.py --malicious 0.3 --nodes 80 --rounds 300` | Try your own settings |
| `python run_demo.py --attack-start 60` | Attackers behave honestly until round 60, then turn malicious |
| `python run_experiments.py` | Sweeps 0-40% malicious nodes, 10 networks each; saves `results/sweep.png` and `.csv` |
| `python tamper_demo.py` | Edits a stored trust value and shows the ledger check failing |

`run_demo.py` options: `--nodes --malicious --rounds --seed --alpha --beta --drop --attack-start --plot`.
Other settings (radio energy, ranges, block size) are in the `Config` class in `wsn_trust_sim.py`.

## Metrics printed
Packet delivery ratio, packet loss, average end-to-end delay, routing overhead (ledger bytes
vs data bytes), energy, share of hops handled by malicious nodes, malicious-node detection rate,
and false-positive rate.

## Model assumptions (read before quoting numbers)
- Each hop must move closer to the base station; a node with no closer neighbour drops the packet.
- Malicious nodes drop forwarded packets with probability `drop_prob` (default 0.7); every hop also has a small random link loss, which counts against the forwarder's trust.
- Forwarding is observed perfectly (a watchdog); real networks have noisy observation.
- Trust is committed to the ledger every `block_every` rounds, and routing reads trust from the ledger.
- The ledger is a hash chain with no consensus protocol, and is not a full blockchain.
- Energy uses the standard first-order radio model; the ledger broadcast is counted as one relay per node.
- **Detection rate** counts only nodes observed at least `min_obs` times. Trust-aware routing avoids bad nodes early, so they are observed less, and the detection rate can look low even when avoidance works. The "hops handled by malicious nodes" row is the better indicator of avoidance.

## Expected behaviour
As the share of malicious nodes grows, trust-aware routing keeps a higher PDR than shortest-path
routing. It costs slightly more delay, energy and routing overhead (longer, safer paths plus ledger updates).

## Files
```
wsn_trust_sim.py     core simulation (network, ledger, routing, metrics)
run_demo.py          single comparison run
run_experiments.py   malicious-percentage sweep and charts
tamper_demo.py       ledger tamper-evidence demo
requirements.txt     numpy, matplotlib
results/             generated charts and CSV
```
