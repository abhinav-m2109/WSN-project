## Blockchain-Based Trust Management for Reliable and Secure Packet Routing in Wireless Sensor Networks

The problem: Wireless Sensor Networks (WSNs) — used in environmental monitoring, smart infrastructure, IoT systems — relay data packets through multiple intermediate nodes. Some nodes are unreliable (drop packets due to congestion/hardware issues), and some are malicious (deliberately drop, alter, or misroute packets). Standard routing just picks the shortest path, ignoring whether nodes are trustworthy — so it can route straight through a bad node.  


The solution: The system continuously monitors each node's forwarding behavior and computes a trust score based on successful vs. failed transmissions. These trust scores are stored on a lightweight, tamper-evident blockchain — so no node (not even a compromised one) can fake or alter its own trust history. The routing algorithm then picks paths using both distance and trust score, favoring reliable nodes and avoiding ones with a poor/malicious track record.  


Evaluation: Simulated comparison of trust-aware routing vs. conventional shortest-path routing, measured on packet delivery ratio, end-to-end latency, and how well the system detects/avoids compromised nodes over time.
