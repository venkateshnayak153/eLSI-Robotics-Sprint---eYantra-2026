"""
===================================================
    eLSI Sprint 1- [eLSI 2026-27]
===================================================

This script is intended to be a Boilerplate for
Bonus Task 0 of eLSI Sprint 1- [eLSI 2026-27]

Filename:        task0.py
Created:         29/05/2026
Last Modified:   29/05/2026
Author:          e-Yantra Team
Team ID:         [ XXX ]
This software is made available on an "AS IS WHERE IS BASIS".
Licensee/end user indemnifies and will keep e-Yantra indemnified from
any and all claim(s) that emanate from the use of the Software or
breach of the terms of this agreement.

e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*****************************************************************************************
"""
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
client = RemoteAPIClient()
sim = client.require('sim')
left = sim.getObject('/LineTracer/DynamicLeftJoint')
right = sim.getObject('/LineTracer/DynamicRightJoint')
def set_motor(l, r):
    sim.setJointTargetVelocity(left, l)
    sim.setJointTargetVelocity(right, r)
time.sleep(1.0)
for side in range(4):
    print('Side', side+1, 'forward')
    set_motor(2.0, 2.0)
    time.sleep(18.2)
    set_motor(0.0, 0.0)
    time.sleep(0.3)
    print('Side', side+1, 'turning')
    set_motor(-1.5, 1.5)
    time.sleep(2.28)
    set_motor(0.0, 0.0)
    time.sleep(0.3)
print('Done!')
set_motor(0.0, 0.0)
