""""
Columbia University - CSEE 4119 Computer Network
Assignment 3 - Distance Vector Routing

dvr.py - the Distance Vector Routing (DVR) program announces its distance vector to its neighbors and 
updates its routing table based on the received routing vectors from its neighbors

RUN: python3 dvr.py 127.0.0.1 10000

"""
import sys
import socket
import time
from collections import defaultdict

class NetworkInterface():
    """
    DO NOT EDIT.
    
    Provided interface to the network. In addition to typical send/recv methods,
    it also provides a method to receive an initial message from the network, which
    contains the costs to neighbors. 
    """
    def __init__(self, network_port, network_ip):
        """
        Constructor for the NetworkInterface class.

        Parameters:
            network_port : int
                The port the network is listening on.
            network_ip : str
                The IP address of the network.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((network_ip, network_port))
        self.init_msg = self.sock.recv(4096).decode() # receive the initial message from the network
        
    def initial_costs(self): 
        """
        Return the initial message received from the network in following format:
        <node_id>. <neighbor_1>:<cost_1>,...,<neighbor_n>:<cost_n>

        node_id is the unique identifier for this node, i.e., dvr.py instance. 
        Neighbor_i is the unique identifier for direct neighbor nodes. All identifiers
        and costs are specified in the topology file.
        """
        return self.init_msg
    
    def send(self, message):
        """
        Send a message to all direct neigbors.

        Parameters:
            message : bytes
                The message to send.
        
        Returns:
            None
        """
        message_len = len(message)
        packet = message_len.to_bytes(4, byteorder='big') + message
        self.sock.sendall(packet)
    
    def recv(self, length):
        """
        Receive a message from neighbors. Behaves exactly like socket.recv()

        Parameters:
            length : int
                The length of the message to receive.
        
        Returns:
            bytes
                The received message.
        """
        return self.sock.recv(length)
    
    def close(self):
        """
        Close the socket connection with the network.
        """
        self.sock.close()


CONVERGENCE_THRESHOLD = 500
MSG_LENGTH = 1024 * 4
node_id = None
dv_table = defaultdict(lambda: defaultdict(lambda: float('inf'))) # usage: dv_table[destination node_id][via node_id] = cost
prev_best_path = defaultdict(lambda: (float('inf'), "")) # usage: prev_best_path[destination node_id] = (cost, via/ next hop)
file = None

def visualize_dv_table():
    for dest, via_table in dv_table.items():
        print(f"{dest}:")
        for via, cost in via_table.items():
            print(f"  via {via}: {cost}")
        min_cost, via = min((cost, via) for via, cost in via_table.items())
        print(f"  best via {via}:{min_cost}")

"""
Write the message to the log file. Use flush to ensure the message is written to the file immediately
<node_1>:<cost_1>:<next_hop_1> ... <node_n>:<cost_n>:<next_hop_n>
"""
def log():
    for destination, via_table in dv_table.items():
        min_cost, via = min((cost, via) for via, cost in via_table.items())
        file.write(f"{destination}:{min_cost}:{via} ")
    file.write("\n")
    file.flush() # IMPORTANT

"""
get the initial costs to your neighbors to help initialize your vector and table. Format is:
<node_id>. <neighbor_1>:<cost_1>,...,<neighbor_n>:<cost_n>
"""
def init_dv_table(init_costs):
    # <node_id>. <neighbor_1>:<cost_1>,...,<neighbor_n>:<cost_n>
    this_node_id, neighbors_part =  init_costs.split(". ")
    for pair in neighbors_part.split(","):
        neighbor, cost = pair.split(":")
        dv_table[neighbor][neighbor] = int(cost)
    return this_node_id

"""
return dv_table into optimal path to destination costs for broadcasting
in the following format:
<node_id>. <destination_1>:<cost_1>,...,<destination_n>:<cost_n>
"""
def serialize_dv_table():
    res = f"{node_id}. "
    for destination, via_table in dv_table.items():
        res += f"{destination}:{min(via_table.values())},"
    # remove the last comma
    res = res[:-1]
    # add a '|' to separate msgs
    res += "|"
    return res

"""
update dv_table given the msg from neighbor
return True if updated. False otherwise.
<node_id>. <neighbor_1>:<cost_1>,<neighbor_n>:<cost_n>
"""
def update_dv_table(msg):
    is_updated = False
    neighbor_node_id, other = msg.split(". ")
    for pair in other.split(","):
        # update the total cost to destination thru this neighbor
        destination, advertised_cost = pair.split(":")
        # do not record the cost it this node itself
        if destination == node_id:
            continue
        # update the new cost to destination via this neighbor
        cost_to_neighbor = dv_table[neighbor_node_id][neighbor_node_id]
        new_total_cost_to_dest = int(advertised_cost) + cost_to_neighbor        
        dv_table[destination][neighbor_node_id] = new_total_cost_to_dest
        
        # check if the optimal path & cost has been updated
        via, min_cost = min(dv_table[destination].items(), key=lambda x: x[1])
        if prev_best_path[destination] != (min_cost, via):
            # the optimal path & cost to a destination has been updated 
            # update the new optimal next hop & cost
            prev_best_path[destination] = (min_cost, via)
            is_updated = True
    return is_updated



if __name__ == '__main__':
    network_ip = sys.argv[1] # the IP address of the network
    network_port = int(sys.argv[2]) # the port the network is listening on
 
    net_interface = NetworkInterface(network_port, network_ip) # initialize the network interface

    # obtain & record init costs
    init_costs = net_interface.initial_costs() 
    node_id = init_dv_table(init_costs)
    # print(init_costs)

    # Create a log file & log initial state
    file = open(f"log_{node_id}.txt", "w")
    log()

    is_updated = True
    no_update = 0
    while no_update < CONVERGENCE_THRESHOLD:
        # broadcast to neighbor dv_table because recv is blocking
        net_interface.send(serialize_dv_table().encode())
        
        if is_updated:
            log()
            no_update = 0
        else:
            no_update += 1
        
        is_updated = False

        raw_msg = net_interface.recv(MSG_LENGTH)
        msgs = raw_msg.decode().split("|")
        for msg in msgs:
            if msg.strip():
                is_updated = is_updated or update_dv_table(msg)

    # print the dv_table to verify convergence
    visualize_dv_table()

    net_interface.close()
    file.close()