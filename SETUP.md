# Setup Guide

Follow these steps to run the WSN trust-aware routing simulation on your own computer.
It works on Windows, macOS and Linux, needs no special hardware, and each run takes only a few seconds.

## 1. What you need
- **Python 3.8 or newer.** Check with `python --version`. On macOS/Linux you may need `python3 --version`.
- **pip**, which comes with Python.
- **Git** (optional). You can also download the project as a ZIP.

If you don't have Python, install it from https://www.python.org/downloads/.
**Windows:** during installation, tick **"Add Python to PATH"**.

## 2. Get the code
**Option A: with Git**
```bash
git clone https://github.com/YOUR-USERNAME/wsn-blockchain-trust-routing.git
cd wsn-blockchain-trust-routing
```
**Option B: without Git**
On the GitHub page click **Code > Download ZIP**, extract it, and open a terminal inside the extracted folder.

## 3. Create a virtual environment (recommended)
This keeps the project's libraries separate from the rest of your system.

**Windows (Command Prompt or PowerShell)**
```bash
python -m venv venv
venv\Scripts\activate
```
**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```
You should now see `(venv)` at the start of your terminal line.

## 4. Install the requirements
```bash
pip install -r requirements.txt
```
This installs `numpy` and `matplotlib`.

## 5. Run the simulation
| Goal | Command |
|---|---|
| Quick comparison with a chart | `python run_demo.py --plot` |
| Your own settings | `python run_demo.py --malicious 0.3 --nodes 80 --rounds 300` |
| Attackers that turn bad after round 60 | `python run_demo.py --attack-start 60` |
| Full sweep, 0-40% malicious nodes | `python run_experiments.py` |
| Ledger tamper-evidence demo | `python tamper_demo.py` |

(On macOS/Linux use `python3` if `python` isn't found.)

Charts and tables are saved in the `results/` folder:
- `demo.png`: PDR comparison and trust score evolution
- `sweep.png` and `sweep.csv`: metrics versus percentage of malicious nodes

## 6. What you should see
Running `python run_demo.py` prints a table like this (exact numbers depend on the settings):

```
Metric                                    Shortest-path   Trust-aware
Packet delivery ratio (%)                         59.90         66.80
Packet loss (%)                                   40.10         33.20
Avg end-to-end delay (ms)                         12.27         13.99
Routing overhead (%)                               0.00          7.44
Energy consumption (J)                             2.50          3.33
Hops handled by malicious nodes (%)               35.47         18.18
...
Ledger: 41 blocks, integrity check: PASSED
```
Trust-aware routing should deliver more packets and send fewer packets through malicious nodes.
It costs a little extra delay, energy and overhead.

## 7. Try changing things
| Option | Meaning | Try |
|---|---|---|
| `--malicious` | Fraction of malicious nodes | `0.1`, `0.3`, `0.4` |
| `--nodes` | Number of sensor nodes | `40`, `100` |
| `--drop` | How often a malicious node drops packets | `0.3`, `0.9` |
| `--alpha`, `--beta` | Weight of distance vs trust in route cost | `--alpha 0.8 --beta 0.2` |
| `--seed` | Different random network | `--seed 7` |
| `--attack-start` | Round at which attackers turn malicious | `50` |

Advanced settings (radio energy, ranges, block size) are in the `Config` class in `wsn_trust_sim.py`.

## 8. No installation: Google Colab
1. Open https://colab.research.google.com and create a new notebook.
2. Upload the project ZIP using the folder icon on the left.
3. Run these cells:
```python
!unzip -q wsn-trust-routing-sim.zip
%cd wsn-trust-routing-sim
!python run_demo.py --plot
```
4. To view the chart:
```python
from IPython.display import Image
Image("results/demo.png")
```
(`numpy` and `matplotlib` are already installed on Colab.)

## 9. Troubleshooting
| Problem | Fix |
|---|---|
| `'python' is not recognized` (Windows) | Reinstall Python and tick "Add Python to PATH", or try `py` instead of `python` |
| `python: command not found` (macOS/Linux) | Use `python3` instead |
| `No module named numpy` or `matplotlib` | Activate the virtual environment, then run `pip install -r requirements.txt` again |
| PowerShell says "running scripts is disabled" | Use Command Prompt instead, or run `Set-ExecutionPolicy -Scope Process RemoteSigned` and activate again |
| `pip` not found | Use `python -m pip install -r requirements.txt` |
| Chart window doesn't open | Expected. Charts are saved as image files in `results/` |
| Results differ from the README | Normal. Results change with settings and `--seed` |

## 10. When you're done
```bash
deactivate
```
This leaves the virtual environment. To remove the project, delete its folder.

## Notes
- This is a simplified teaching model of the proposed method. Its numbers are illustrative and are not the final results of the research paper.
- See `README.md` for how the model works and its assumptions.
