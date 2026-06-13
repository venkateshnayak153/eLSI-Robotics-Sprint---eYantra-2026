# Task 0 Bonus: Square Path Challenge

## Problem Statement
Make the bot in CoppeliaSim trace a perfect square path, starting and stopping at the same spot such that the robot traces a square and ends where it began.

## Approach

### The Bridge Problem
The organizers provided two bridge binaries:
- `bridge.exe` — Windows only
- `bridge` — Linux (x86-64) only

Neither works on **macOS Apple Silicon (M-series)** because:
- The `bridge` binary is an ELF x86-64 Linux executable
- Mac M-series uses ARM64 architecture
- Running it gives: `zsh: exec format error: ./bridge`

### What the Bridge Does
The bridge acts as a middleman between `task0.py` and CoppeliaSim:
```
task0.py → (TCP socket port 50002) → bridge → (ZMQ port 23000) → CoppeliaSim
```
It translates simple TCP socket commands (`L:2.0;R:2.0`) into ZMQ protocol that CoppeliaSim understands.

### Our Workaround — Direct ZMQ Connection
Since CoppeliaSim exposes a ZMQ Remote API on port 23000, we connected directly using the `coppeliasim-zmqremoteapi-client` Python package — skipping the bridge entirely:

```
task0.py → (ZMQ port 23000) → CoppeliaSim
```

This is cleaner, faster, and works natively on Mac.

### Why This Works
CoppeliaSim's ZMQ Remote API allows direct Python control of any object in the simulation. We get the motor joint handles directly and set their velocities:

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')
left  = sim.getObject('/LineTracer/DynamicLeftJoint')
right = sim.getObject('/LineTracer/DynamicRightJoint')
sim.setJointTargetVelocity(left, 2.0)
sim.setJointTargetVelocity(right, 2.0)
```

## Solution

### Logic
The robot uses open-loop timed motor control (no sensors):
1. Drive both wheels forward for `SIDE_DURATION` seconds → moves one side
2. Stop briefly
3. Spin left wheel backward, right wheel forward for `TURN_DURATION` seconds → turns 90°
4. Stop briefly
5. Repeat 4 times → completes the square

### Tuned Values
| Parameter | Value | Description |
|-----------|-------|-------------|
| `SIDE_DURATION` | `18.2s` | Time to cover one side of the square |
| `TURN_DURATION` | `2.28s` | Time to turn exactly 90° |
| Forward speed | `2.0` | Both motors forward |
| Turn speed | `1.5` | Left backward, right forward |

## Setup

### Prerequisites
```bash
conda create -n elsi_sprint python=3.10 -y
conda activate elsi_sprint
pip install pyzmq coppeliasim-zmqremoteapi-client
```

### Run
1. Open CoppeliaSim and load `task0_simulation.ttt`
2. Hit ▶️ Play
3. Run:
```bash
conda activate elsi_sprint
python task0.py
```

## Platform
- macOS Apple Silicon (M-series)
- Python 3.10 (elsi_sprint conda env)
- CoppeliaSim Edu V4.10.0

## Team ID
[ XXX ]