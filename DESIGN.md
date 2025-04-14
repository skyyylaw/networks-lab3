**Distance Vector Routing - Protocol Design and Implementation**

**Overview:**

Implements the Distance Vector Routing protocol. Each node maintains shortest path costs to all destinations, broadcasts its dv table to neighbors, and updates its routing table based on the broadcast from neighbor until convergence.

**Algorithm:**

*-	Bellman-Ford Algorithm*

*- 	Equation*

***
    Dₓ(y) = min [ c(x, v) + Dᵥ(y) ] for all neighbors v of x***

*
    Where:*

 *`Dₓ(y)`: estimated cost at node `x` to destination `y`*

`c(x, v)`: cost from `x` to neighbor `v`*

*`Dᵥ(y)`: cost reported by neighbor `v` to destination `y`*

*Steps*

1. *Initialize all distances to ∞, except the source which is 0.*
2. *Repeat V − 1 times:*
   - *For each edge (u, v) with weight w:*
     - *If `dist[u] + w < dist[v]`, update `dist[v] = dist[u] + w`*
3. *Optionally check for negative-weight cycles.*

**Protocol Logic:**

* Each node sends its distance vector to neighbors over a socket.
* Upon receiving updates, it recalculates shortest paths.
* Stops after CONVERGENCE_THRESHOLD number of consecutive loops without any meaningful changes (where an optimal path has changed in costs or next-hop)
* Logs best paths to file after each update.

**Global Variables:**

* CONVERGENCE_THRESHOLD specifies the number of no-change loops to assume convergence from one node's perspective
* MSG_LENGTH specifies the length of the msg to take from the socket
* dv_table: nested dict storing cost to each destination via each neighbor. **Format: dv_table[destination][via next hop] = cost**
* prev_best_path: tracks best known cost and next hop for each destination. **Format: prev_best_path[destination] = (cost, via next hop)**
* node_id: ID of the current node.
* file: the log file object

**Neighbor Communication - Packet Structure:**

Messages are strings in the following format:

- `<sender>`. `<dest1>`:`<cost1>`,`<dest2>`:`<cost2>`,...,`<destN>`:`<costN>`|
- Note that each message ends with "|" to separate messages from different neighbors

**Functions:**

* init_dv_table(init_costs): parses initial costs and sets up this node's dv_table.
* serialize_dv_table(): formats this node's dv_table as a string message to be send to neighbors.
* update_dv_table(msg): updates this node's dv_table by parsing the neighbor message.
* log(): parse this node's dv_table and logs this node's current best paths to all other reachable nodes.
* visualize_dv_table(): nicely visualize prints final table for debugging.

**Convergence:**

Detected after CONVERGENCE_THRESHOLD number of rounds with no routing changes. Then, final table is printed and the node exits.
