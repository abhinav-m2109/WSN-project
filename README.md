## Blockchain-Based Trust Management for Reliable and Secure Packet Routing in Wireless Sensor Networks  

## Overview:  
Wireless Sensor Networks (WSNs) — used in environmental monitoring, smart infrastructure, and IoT systems — rely on multiple sensor nodes relaying data packets toward a destination. These networks face two core problems:  

* Unreliable nodes that drop packets due to congestion or hardware limitations.  
* Malicious nodes that intentionally drop, alter, or misroute packets.  
  
## Problem:  
Sensor networks lose data and are vulnerable to exploitation because routing decisions don't account for which nodes are actually trustworthy.  

## Solution:  
A trust-scoring system backed by a tamper-proof blockchain, so routing can dynamically detect and avoid unreliable or malicious nodes — instead of blindly trusting the shortest path.  
## Impact:  
In simulation, trust-aware routing improved packet delivery and made the network resilient against nodes that started misbehaving mid-operation — compared to standard shortest-path routing, which had no way to detect or avoid them.  
## Status:

 In progress.
- [ ] Trust score model for node reliability
- [ ] Blockchain ledger integration for trust records
- [ ] Simulation / routing protocol integration
