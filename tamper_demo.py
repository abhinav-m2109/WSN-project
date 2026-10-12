"""Show why the ledger is tamper-evident: edit a stored trust value and watch verification fail."""
import copy
from wsn_trust_sim import Config, simulate

res = simulate(Config(malicious_frac=0.3), "trust")
led = res["ledger"]; mal = [int(i) for i in range(len(res["mal"])) if res["mal"][i]]
print(f"Blocks in ledger: {len(led.chain)}  | integrity: {led.verify()}")
target = next(i for i, b in enumerate(led.chain) if any(r[0] in mal for r in b["records"]))
blk = led.chain[target]; rec = next(r for r in blk["records"] if r[0] in mal)
print(f"\nAttacker edits block {target}: node {rec[0]} (malicious) trust {rec[1]} -> 0.99")
rec[1] = 0.99
ok, bad = led.verify()
print(f"Integrity check: {'PASSED' if ok else 'FAILED'} (first bad block = {bad})")
led.chain = led.chain[:bad]; led.rebuild_trust()
print(f"Recovery: ledger truncated to the last valid block ({len(led.chain)} blocks); trust rebuilt from verified data.")
