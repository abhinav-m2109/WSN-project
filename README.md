## Blockchain-Based Trust Management for Reliable and Secure Packet Routing in Wireless Sensor Networks  

Overview:  
Wireless Sensor Networks (WSNs) — used in environmental monitoring, smart infrastructure, and IoT systems — rely on multiple sensor nodes relaying data packets toward a destination. These networks face two core problems: 
1)Unreliable nodes that drop packets due to congestion or hardware limitations.

The solution: The system continuously monitors each node's forwarding behavior and computes a trust score based on successful vs. failed transmissions. These trust scores are stored on a lightweight, tamper-evident blockchain — so no node (not even a compromised one) can fake or alter its own trust history. The routing algorithm then picks paths using both distance and trust score, favoring reliable nodes and avoiding ones with a poor/malicious track record.  


Evaluation: Simulated comparison of trust-aware routing vs. conventional shortest-path routing, measured on packet delivery ratio, end-to-end latency, and how well the system detects/avoids compromised nodes over time.
