# Daniel Moreno 
# CECS 427-01 Dynamic Networks
# Due Date: February 6, 2024

# Importing networkx as recommended by the documentation
import networkx as nx

# Creating a global variable G, acting as "memory"
G = ""

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
def read_graph():
    File_name = input("Please input a file to read from: ")
    try:
        with open(File_name, 'r') as file:
            G = file.read()
            file.close()
            print("File read and saved to memory!\n")
        except FileNotFoundError:
            print("File not found!\n")

# Saves a graph from memory to the external file provided by the user's input
def save_graph():
    File_name = input("Please input a file to save to: ")
    try:
        with open(File_name, 'w') as file:
            file.write(G)
            file.close()
            print("Graph saved into file!\n")
    except FileNotFoundError:
        print("File not found!\n")

# Creates an Erdos-Reny graph using n nodes and a closeness coefficient provided by a user
def create_graph():
    n = int(input("Please input an n value: "))
    c = float(input("Please input a c value: "))

# Uses the shortest path algorithm using networkx's library
def shortest_path():
    pass

# Plots the graph G and highlights shortest path if it exists
def plot():
    pass

# Simple selction menu to handle user's input
def selection(selection: str) -> None:
    if (selection == '1'):
        print("Now reading graph\n")
        read_graph()

    elif (selection == '2'):
        print("Now saving graph\n")
        save_graph()

    elif (selection == '3'):
        print("Now creating graph\n")
        create_graph()

    elif (selection == '4'):
        print("Now finding shortest path\n")
        shortest_path()

    elif (selection == '5'):
        print("Now Plotting\n")
        plot()

    elif (selection == 'x'):
        print("Now Exiting\n")

    else:
        print("Not a valid selection\n")

# main function of the program
def main():
    option = '1'
    while (option != 'x'):
        menu()
        option = input("Please make a selection: ")
        selection(option)

main()
