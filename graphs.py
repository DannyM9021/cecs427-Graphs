# Daniel Moreno 
# CECS 427-01 Dynamic Networks
# Due Date: February 6, 2024

# Importing networkx and numpy as recommended by the documentation
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Making a global variable for shortest path
short = []

# Printing a CLI menu so user knows the options
def menu():
    print("MAIN MENU")
    print("1. Read a Graph")
    print("2. Save the Graph")
    print("3. Create a Random Graph")
    print("4. Shortest Path")
    print("5. Plot Graph")
    print("x. Exit\n")

# Reads a graph provided by user's input and saved to memory G
def read_graph(G):
    File_name = input("Please input a file to read from: ")
    try:
        with open(File_name, 'r') as file:
            G = nx.read_adjlist(File_name)
            file.close()
            print("File read and saved to memory!\n")
    # Handling exception if no file exists
    except FileNotFoundError:
        print("File not found!\n")
        return G
    return G

# Saves a graph from memory to the external file provided by the user's input
def save_graph(G):
    File_name = input("Please input a file to save to: ")
    try:
        with open(File_name, 'w') as file:
            print(G)
            nx.write_adjlist(G, File_name)
            file.close()
            print("Graph saved into file!\n")
    # Handles exception if no file exists
    except FileNotFoundError:
        print("File not found!\n")
        return G
    return G

# Creates an Erdos-Reny graph using n nodes and a closeness coefficient provided by a user
def create_graph(G):
    global short
    short = []
    n = int(input("Please input an n value (number of nodes): "))
    c = float(input("Please input a c value (closeness coefficient): "))
    # Equation to calculate probability of edges being connected
    p = c * (np.log(n)/n)
    G = nx.erdos_renyi_graph(n, p, seed=np.random)
    # Remapping node numbers to a corresponding letter since erdos_renyi_graph function uses integers
    mapping = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i',9:'j',10:'k',11:'l',12:'m',
               13:'n',14:'o',15:'p',16:'q',17:'r',18:'s',19:'t',20:'u',21:'v',22:'w',23:'x',24:'y',25:'z'}
    G = nx.relabel_nodes(G, mapping, copy=True)
    print("Graph successfully created and saved to memory!\n")
    return G

# Uses the shortest path algorithm using networkx's library
def shortest_path(G):
    source = input("Please enter a source node: ")
    target = input("Please enter a target node: ")
    try:
        # Using built-in networkx method to find shortest path
        short_path = nx.shortest_path(G, source, target)
        global short
        short = short_path
        # Printing shortest path on the console
        string = ""
        for i in range(len(short_path)):
            string = string+short_path[i] + "->"
        string = string[:-2]
        print(string)
        print()
    # Handling Exceptions
    except nx.NodeNotFound:
        print("Source not found in graph G!\n")
        return G
    except nx.NetworkXNoPath:
        print(f"No path between {source} and {target} was found\n")
        return G
    return G

# Plots the graph G and highlights shortest path if it exists
# used https://stackoverflow.com/questions/24024411/highlighting-the-shortest-path-in-a-networkx-graph as a resource
def plot(G):
    global short
    # Helps set position of graph for node and edges
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos)
    # Plots shortest path ONLY if it exists
    if short != []:
        short_path_edges = list(zip(short, short[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=short, node_color='b')
        nx.draw_networkx_edges(G, pos, edgelist=short_path_edges, edge_color='b', width=5)
    # Plotting the graph with equal axis
    plt.axis('equal')
    plt.show()
    return G

# Simple selction menu to handle user's input
def selection(selection: str, G) -> None:

    if (selection == '1'):
        print("Now reading graph...\n")
        return read_graph(G)

    elif (selection == '2'):
        print("Now saving graph...\n")
        return save_graph(G)

    elif (selection == '3'):
        print("Now creating graph...\n")
        return create_graph(G)

    elif (selection == '4'):
        print("Now finding shortest path...\n")
        return shortest_path(G)

    elif (selection == '5'):
        print("Now Plotting...\n")
        return plot(G)

    elif (selection == 'x'):
        print("Now Exiting...\n")

    else:
        print("Not a valid selection\n")

# main function of the program
def main():
    # Creating a gloabal G, acting as memory
    G = nx.empty_graph()
    
    option = '1'
    while (option != 'x'):
        menu()
        option = input("Please make a selection: ")
        # Reusing G as volatile memory
        G = selection(option, G)

main()
