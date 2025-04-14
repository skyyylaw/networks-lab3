**Columbia University - CSEE 4119 Computer Network**

**Assignment 3 - Distance Vector Routing**

**Sky Luo - tl3385**

The assignment code is structured into the provided NetworkInterface class, my helper functions, and the main Distance Vector algorithm logic in main().

I have designed the following helper functions (for each node):

- visualize_dv_table(): prints the full distance vector table with best paths for debugging
- log(): writes current shortest paths and next hops to a log file
- init_dv_table(init_costs): initializes the distance vector table from the initial network message
- serialize_dv_table(): converts the current distance vector to a formatted string for sending between neighbors
- update_dv_table(msg): updates the table using a neighbor’s advertised distance vector and returns whether any meaningful change occurred (whether an optimal path has changed in costs or next-hop)

Usage Example:

python3 dvr.py <network_ip> <network_port>

RUN: python3 dvr.py 127.0.0.1 10000
