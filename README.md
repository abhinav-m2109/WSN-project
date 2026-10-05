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

## Sample Diagram:  
<img width="390" height="195" alt="Screenshot 2026-10-04 230115" src="https://github.com/user-attachments/assets/ef2271e0-b0ab-45a9-99ef-c48acd7b52c7" />  
<img width="804" height="679" alt="Screenshot 2026-10-04 225932" src="https://github.com/user-attachments/assets/851e287d-d9a6-46b0-ab6a-6dd664fb288c" />  





## Status:

 In progress.
- [ ] Trust score model for node reliability
- [ ] Blockchain ledger integration for trust records
- [ ] Simulation / routing protocol integration
