# Daniel Moreno 
# CECS 427-01 Dynamic Networks
# Due Date: February 6, 2024

# Importing networkx and numpy as recommended by the documentation
import networkx as nx
import numpy as np


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
    except FileNotFoundError:
        print("File not found!\n")
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
    except FileNotFoundError:
        print("File not found!\n")
    return G

# Creates an Erdos-Reny graph using n nodes and a closeness coefficient provided by a user
def create_graph(G):
    n = int(input("Please input an n value (number of nodes): "))
    c = float(input("Please input a c value (closeness coefficient): "))
    p = c * (np.log(n)/n)
    G = nx.erdos_renyi_graph(n, p)
    mapping = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i',9:'j',10:'k',11:'l',12:'m',
               13:'n',14:'o',15:'p',16:'q',17:'r',18:'s',19:'t',20:'u',21:'v',22:'w',23:'x',24:'y',25:'z'}
    G = nx.relabel_nodes(G, mapping, copy=True)
    print("Graph successfully created and saved to memory!")
    return G

# Uses the shortest path algorithm using networkx's library
def shortest_path(G):
    return G

# Plots the graph G and highlights shortest path if it exists
def plot(G):
    return G

# Simple selction menu to handle user's input
def selection(selection: str, G) -> None:

    if (selection == '1'):
        print("Now reading graph\n")
        return read_graph(G)

    elif (selection == '2'):
        print("Now saving graph\n")
        return save_graph(G)

    elif (selection == '3'):
        print("Now creating graph\n")
        return create_graph(G)

    elif (selection == '4'):
        print("Now finding shortest path\n")
        return shortest_path(G)

    elif (selection == '5'):
        print("Now Plotting\n")
        return plot(G)

    elif (selection == 'x'):
        print("Now Exiting\n")

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
        G = selection(option, G)

main()
