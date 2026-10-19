# Blockchain-Based Trust Management for Reliable and Secure Packet Routing in Wireless Sensor Networks (WSN)

## Overview
Wireless Sensor Networks (WSNs), used in environmental monitoring, smart infrastructure
and IoT systems, rely on many sensor nodes relaying data packets towards a base station.
They face two core problems:

- **Unreliable nodes** that drop packets because of congestion or hardware limits.
- **Malicious nodes** that intentionally drop, alter or misroute packets.

## Problem
Routing usually picks paths by distance, hop count or energy. It does not consider which
nodes are actually trustworthy, so sensor networks lose data and are open to exploitation.

## Solution
A trust-scoring system backed by a lightweight, tamper-evident blockchain ledger. Each node's
trust is computed from its observed forwarding behaviour (successful vs failed forwards) and
recorded on the ledger. Routing then combines trust with distance, so it can detect and avoid
unreliable or malicious nodes instead of blindly following the shortest path.

## Impact (Beta simulation)
In simulation, trust-aware routing improved packet delivery over standard shortest-path routing:
about 6 to 17 percentage points of PDR with 10-40% malicious nodes, and a smaller gain
(about 3-4 points) when nodes only started misbehaving partway through operation.
The cost is slightly higher delay, energy use and routing overhead.
Numbers come from a simplified simulation, not from the final experiments.

## Status: In progress
- [x] Trust score model for node reliability (Beta)
- [x] Hash-chained ledger for trust records (Beta)
- [x] Simulation of shortest-path vs trust-aware routing (Beta)
- [ ] Final experiments and evaluation

## Try it
The uploaded files are a **beta version** of the model, meant to show how the project works.  
They are not the final project. See [SETUP.md](SETUP.md) for step-by-step instructions to run the simulation on your own device, and [README](README.md) for how the model works.

