Commands:


Network: python3 network.py 10000 topology.dat

Nodes: python3 dvr.py 127.0.0.1 10000

***All Working As Expected***

**#1 4 Node Topology Setup:**

A B 1
A C 4
B C 2
B D 5
C D 1

Outputs:

log_A:

B:1:B C:4:C
B:1:B C:4:C
B:1:B C:4:C D:5:C
B:1:B C:3:B D:5:C
B:1:B C:3:B D:4:B

log_B:

A:1:A C:2:C D:5:D
A:1:A C:2:C D:5:D
A:1:A C:2:C D:5:D
A:1:A C:2:C D:3:C

log_C:

A:4:A B:2:B D:1:D
A:4:A B:2:B D:1:D
A:4:A B:2:B D:1:D
A:3:B B:2:B D:1:D

log_D:

B:5:B C:1:C
B:5:B C:1:C
B:5:B C:1:C A:6:B
B:3:C C:1:C A:5:C
B:3:C C:1:C A:4:C


**#2 3 Node Topology Setup:**

A B 2
B C 3
A C 5

Outputs:

log_A:

B:2:B C:5:C
B:2:B C:5:C
B:2:B C:5:C
B:2:B C:5:B

log_B:

A:2:A C:3:C
A:2:A C:3:C
A:2:A C:3:C
A:2:A C:3:C

log_C:

B:3:B A:5:A
B:3:B A:5:A
B:3:B A:5:A
B:3:B A:5:A



**#3 5 Node Topology Setup:**

A B 1
A C 4
B C 2
B D 7
C E 3
D E 1

Outputs:

log_A:

B:1:B C:4:C
B:1:B C:4:C
B:1:B C:3:B D:8:B
B:1:B C:3:B D:8:B E:7:C
B:1:B C:3:B D:8:B E:6:B
B:1:B C:3:B D:7:B E:6:B

log_B:

A:1:A C:2:C D:7:D
A:1:A C:2:C D:7:D
A:1:A C:2:C D:7:D
A:1:A C:2:C D:7:D E:5:C
A:1:A C:2:C D:7:D E:5:C
A:1:A C:2:C D:6:C E:5:C

log_C:

A:4:A B:2:B E:3:E
A:4:A B:2:B E:3:E
A:4:A B:2:B E:3:E
A:3:B B:2:B E:3:E D:9:B
A:3:B B:2:B E:3:E D:4:E
A:3:B B:2:B E:3:E D:4:E

log_D:

B:7:B E:1:E
B:7:B E:1:E
B:7:B E:1:E A:8:B C:9:B
B:7:B E:1:E A:8:B C:4:E
B:6:E E:1:E A:8:B C:4:E
B:6:E E:1:E A:8:B C:4:E
B:6:E E:1:E A:7:E C:4:E

log_E:

C:3:C D:1:D
C:3:C D:1:D
C:3:C D:1:D A:7:C B:5:C
C:3:C D:1:D A:7:C B:5:C
C:3:C D:1:D A:6:C B:5:C
