# Daniel Moreno 
# CECS 427-01 Dynamic Networks
# Due Date: March 19, 2024

# Importing networkx and numpy as recommended by the documentation
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
# importing for balancing graph
import dimod as di
import dwave_networkx as dnx

# Making a global variable for shortest path
short = []

# Making global variable Digraph to store digraph
digraph_storage = nx.empty_graph()

# Printing a CLI menu so user knows the options
def menu():
    print("MAIN MENU")
    print("1. Read a Graph")
    print("2. Save the Graph")
    print("3. Create a Graph")
    print("4. Algorithms")
    print("5. Plot Graph")
    print("6. Assign and Validate Attributes")
    print("7. Read a DiGraph")
    print("x. Exit\n")

# As part of new assignment, submenu for some of the new features
def sub_menu(selection:str):
    if (selection == '3'):
        print("1. Random Erdos-Reny Graph")
        print("2. Karate-Club Graph\n")
    elif (selection == '4'):
        print("1. Shortest Path")
        print("2. Partition G\n")
    elif (selection == '5'):
        print("1. The Shortest Path")
        print("2. Cluster Coefficients")
        print("3. Neighborhood Overlaps\n")
    elif (selection == '6'):
        print("1. Homophily")
        print("2. Balanced Graph")

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

# Assignment 3: Read a digraph
def read_digraph(G):
    digraph = []
    temp = []
    File_name = input("Please input a file to read from: ")
    try:
        with open(File_name, 'r') as file:
            # Going through each line of file to parse informaiton in format:
            # source, destination, a, b
            for line in file:
                # File will have spaces separating the terms
                temp_line = line.split(" ")
                # Only getting the first 3 as no special case
                for i in range(3):
                    temp.append(temp_line[i])
                # On last term, remove "\n" escape character
                temp.append(temp_line[3].split("\n")[0])
                # Adding to digraph storage
                digraph.append(temp)
                # Re-initializing list
                temp = []
            file.close()
            # Accessing Global Digraph Graph storage
            global digraph_storage
            digraph_storage = digraph
            print("Digraph read and saved to memory!\n")
            return G
    # Handling exception if no file exists
    except FileNotFoundError:
        print("File not found!\n")
        return G

# Saves a graph from memory to the external file provided by the user's input
def save_graph(G):
    File_name = input("Please input a file to save to: ")
    try:
        # If graph is directed will save accordingly
        if (nx.is_directed(G)):
            print("DIRECTED")
            return G
        # Saves UNDIRECTED GRAPH, Assignment 1
        with open(File_name, 'w') as file:
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
    # Re-initializing shortest path to non-existant
    global short
    short = []
    G.graph["short_path"] = []
    n = int(input("Please input an n value (number of nodes): "))
    c = float(input("Please input a c value (closeness coefficient): "))
    # Equation to calculate probability of edges being connected
    p = c * (np.log(n)/n)
    # Using builtin function as well as adding randomness using numpy library
    G = nx.erdos_renyi_graph(n, p, seed=np.random)
    # Fixes the issue with shortest path right after creating
    G = nx.relabel_nodes(G, {node:str(node) for node in G.nodes()})
    # Initializing now so it can be used in cluster enabling and disabling
    G.graph["cluster_enable"] = False
    G.graph["cluster_node_sizes"] = []
    G.graph["cluster_node_colors"] = []
    # Initializing now so it can be used in neighborhood enbaling and disabling
    G.graph["neighbor_enable"] = False
    G.graph["neighbor_edge_colors"] = {}

    print("Graph successfully created and saved to memory!\n")
    return G

# Creates Karate-Club Graph provided by networkx
def karate_club(G):
    G = nx.karate_club_graph()
    # Fixes the issue with shortest path right after creating (from Erdos-Renyi Function)
    G = nx.relabel_nodes(G, {node:str(node) for node in G.nodes()})
    # Initializing now so it can be used later in shortest path
    G.graph["short_path"] = []
    # Initializing now so it can be used in cluster enabling and disabling
    G.graph["cluster_enable"] = False
    G.graph["cluster_node_sizes"] = []
    G.graph["cluster_node_colors"] = []
    # Initializing now so it can be used in neighborhood enbaling and disabling
    G.graph["neighbor_enable"] = False
    G.graph["neighbor_edge_colors"] = {}

    print("Karate Graph successfully created and saved to memory\n")
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

        G.graph["short_path"] = short_path
        # Printing shortest path on the console
        string = ""
        for i in range(len(short_path)):
            string = string+short_path[i] + "->"
        string = string[:-2]
        print(string)
        print()
        return G
    # Handling Exceptions
    except nx.NodeNotFound:
        print("Node(s) not found in graph G!\n")
        return G
    except nx.NetworkXNoPath:
        print(f"No path between {source} and {target} was found\n")
        return G

# Partition of Graph
def parition_graph(G):
    # Getting the amount of components a user wants
    requested_components = int(input("Please enter the of components you wish to be connected: "))
    connected_comp = 0

    # In a try/exception block to prevent program from crashing
    try:
        # Loops until requested connected compnents have been met
        while connected_comp < requested_components:
            # Using Networkx built-in betweeness function (attached for reference)
            # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.edge_betweenness_centrality.html
            betweeness = nx.edge_betweenness_centrality(G)

            # Getting the largest edge with betweeness using python's max function, since edge_betweenness_centrality is a dictionary, we can user
            # key = betweeness.get to get the edge with the highest betweeness
            biggest_betweeness = max(betweeness, key=betweeness.get)

            # Removing that edge from the saved Graph
            # https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.remove_edge.html
            # used as reference: G.remove_edge(*e)  # unpacks e from an edge tuple
            G.remove_edge(*biggest_betweeness)

            # Checks the connected components at the moment after removing the edge
            # Used Networkx Connected Component function
            # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.number_connected_components.html
            connected_comp = nx.number_connected_components(G)

    # Not sure what kind of exception might happen, so catching any exception that could happen
    except Exception as e:
        print("Exception:", e,"; Partition failed!\n")

    return G

# Plots the graph G and highlights shortest path if it exists
# used https://stackoverflow.com/questions/24024411/highlighting-the-shortest-path-in-a-networkx-graph as a resource
def plot_shortest(G):
    global short
    
    print("1. Enable\Disable Shortest Path\n2. Continue\n")
    enable_disable = input("Do you want to Enable/Disable Shortest Path or continue?")
    if (enable_disable == '1'):
        print("1. Enable\n2. Disable")
        switch = input("Please Make a choice: ")

        if (switch == '1'):
            if (G.graph["short_path"] == []):
                G.graph["short_path"] == short
                print("ENABLE\n")
            else:
                print("Already Enabled, returning to main menu...\n")
                return G
        elif (switch == '2'):
            if (G.graph["short_path"] == short):
                G.graph["short_path"] = []
                print("DISABLED\n")
            else:
                print("Already Disabled, returning to main menu...\n")
                return G
        else:
            print("OPTION NOT VALID\n")
            return G

    try:
        # Helps set position of graph for node and edges
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos)
        # Plots shortest path ONLY if it exists
        if G.graph["short_path"] != []:
            print("IN HERE")
            short_path_edges = list(zip(short, short[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=short, node_color='r')
            nx.draw_networkx_edges(G, pos, edgelist=short_path_edges, edge_color='r', width=5)
    except Exception as e:
        print("Something went wrong:",e)
    # Plotting the graph with equal axis
    plt.axis('equal')
    plt.show()
    return G

# Plotting of the cluster coefficient
def plot_cluster(G):
    # Similar to Shortest Path Plotting for enabling and disabling
    print("1. Enable\Disable Cluster Coefficient\n2. Continue\n")
    enable_disable = input("Do you want to Enable/Disable Cluster Coefficient or continue? ")
    if (enable_disable == '1'):
        print("1. Enable\n2. Disable")
        switch = input("Please Make a choice: ")

        if (switch == '1'):
            if (G.graph["cluster_enable"] == False):
                G.graph["cluster_enable"] = True
                print("ENABLE\n")
            else:
                print("Already Enabled, returning to main menu...\n")
                return G
        elif (switch == '2'):
            if (G.graph["cluster_enable"] == True):
                G.graph["cluster_enable"] = False
                G.graph["cluster_node_sizes"] = []
                G.graph["cluster_node_colors"] = []
                print("DISABLED\n")
            else:
                print("Already Disabled, returning to main menu...\n")
                return G
        else:
            print("OPTION NOT VALID\n")
            return G

    # If clustering is enabled, it will actually find the sizes and colors for nodes
    if (G.graph["cluster_enable"] == True):
        # Computes the clustering coefficient of the nodes in graph G
        # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.clustering.html#networkx.algorithms.cluster.clustering
        clustering_coefficients = nx.clustering(G)

        # Using Python's min and max functions to find the max and min
        # coefficient values in the dictionary generated by nx.clustering function
        minimum_coeff = min(clustering_coefficients.values()) + 0.00000001 # Adding a super small constant to prevent divide by 0
        maximum_coeff = max(clustering_coefficients.values())

        # Defined max and min nodes as 500 and 1000 pixels
        MIN_PIXEL = 300
        MAX_PIXEL = 2000

        # Saving node's sizes and RGB value to lists to graph later
        sizes = []
        colors = []

        try:
            # Looping through all of the nodes and assigning their color and size
            for nodev, coeff in clustering_coefficients.items():
                # Calculating the proportional coefficient using formula given from instructions
                pv = (coeff - minimum_coeff)/(maximum_coeff- minimum_coeff)

                # Calculating the size of the node using the proportional coefficient and 
                # formula from instructions
                nodev_size = MIN_PIXEL + pv * (MAX_PIXEL - MIN_PIXEL)
                sizes.append(nodev_size)

                # RGB Color where R = pv * 254, G = 254, B = 0 (according to instructions)
                # Dividing by 255 to normalize, since matplotlib requires them to be in the range between 0 and 1
                # https://matplotlib.org/stable/users/explain/colors/colors.html
                RGB = (abs(int(pv * 254))/255,254/255,0) # type casting int(R) since may be int
                colors.append(RGB)
            G.graph["cluster_node_sizes"] = sizes
            G.graph["cluster_node_colors"] = colors

        except Exception as e:
            print("Exception:", e,"; Graphing Cluster Failed!\n")

    # Time to plot graph
    pos = nx.spring_layout(G) # Same as shortest path, to define position of all nodes

    # Drawing the graph using nx's graphing function
    # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw.html 
    if (G.graph["cluster_enable"] == True):
        nx.draw(G, pos, with_labels=True, node_size=G.graph["cluster_node_sizes"], node_color=G.graph["cluster_node_colors"])
    # If disabled will just print without sizes nor colors
    else:
        nx.draw(G, pos, with_labels=True)

    # Displaying the graph using matplotlib
    plt.show()
    
    
    return G

# Neighborhood overlap mapping
def neighborhood_overlap(G):
    # Similar to Shortest Path Plotting and Cluster Coefficient for enabling and disabling
    print("1. Enable\Disable Neighborhood Overlap\n2. Continue\n")
    enable_disable = input("Do you want to Enable/Disable Neighborhood Overlap or continue? ")
    if (enable_disable == '1'):
        print("1. Enable\n2. Disable")
        switch = input("Please Make a choice: ")

        if (switch == '1'):
            if (G.graph["neighbor_enable"] == False):
                G.graph["neighbor_enable"] = True
                print("ENABLE\n")
            else:
                print("Already Enabled, returning to main menu...\n")
                return G
        elif (switch == '2'):
            if (G.graph["neighbor_enable"] == True):
                G.graph["neighbor_enable"] = False
                G.graph["neighbor_edge_colors"] = {}
                print("DISABLED\n")
            else:
                print("Already Disabled, returning to main menu...\n")
                return G
        else:
            print("OPTION NOT VALID\n")
            return G

    # Making a dictionary to store (u,v) pairs with common neighbors generated using
    # networkx's common_neighbors function
    # https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.common_neighbors.html
    common_neighbors = {}

    # From CLuster Coefficient Function
    clustering_coefficients = nx.clustering(G)
    minimum_coeff = min(clustering_coefficients.values()) + 0.00000001 # Adding a super small constant to prevent divide by 0
    maximum_coeff = max(clustering_coefficients.values())

    colors = {}


    try:
        # From Cluster Coefficient Function
        for nodev, coeff in clustering_coefficients.items():
            # Calculating the proportional coefficient using formula given from instructions
            pv = (coeff - minimum_coeff)/(maximum_coeff- minimum_coeff)

            # RGB Color where R = pv * 254, G = 254, B = 0 (according to instructions)
            # Dividing by 255 to normalize, since matplotlib requires them to be in the range between 0 and 1
            # https://matplotlib.org/stable/users/explain/colors/colors.html
            RGB = (abs(int(pv * 254))/255,254/255,0) # type casting int(R) since may be int
            colors.update({nodev:RGB})

        # Nodes is a tuple of u,v edges saved as (u,v) as a key
        # the value is an generator iterable object returned by networkx's common neighbors method
        # which can be accessed through a for loop as shown below
        for nodes in G.edges():
            common_neighbors.update({nodes:nx.common_neighbors(G,nodes[0],nodes[1])})

        # Graph plotting!
        # Determining position of each node (used in other graphs)
        pos = nx.spring_layout(G)
        # Drawing the main graph
        nx.draw(G, pos, with_labels=True)
        if (G.graph["neighbor_enable"] == True):
            # Getting the nodes and common neighbors of those nodes (where nodes u,v are in a tuple (u,v))
            # and common neighbors seem to be a tuple (in documentation says that its an iterator as the return type)
            # from documentation: return (w for w in G[u] if w in G[v] and w not in (u, v))
            # https://networkx.org/documentation/networkx-1.9.1/_modules/networkx/classes/function.html
            for nodes, common_neigh in common_neighbors.items():
                # Goes through all the neighbor nodes between nodes u and v, and colors them based on the colors defined above
                # same as the coefficient cluster colors
                for common in common_neigh:
                    # nodes[0] represents node u, nodes[1] represents node v, and common is the neighbor of both of them,
                    # so those edges are colored the same
                    nx.draw_networkx_edges(G, pos, edgelist = [(nodes[0],common),(nodes[1],common)], edge_color = colors[nodes[0]])
        plt.show()

    # Catching any unwanted exception
    except Exception as e:
        print("Exception:",e,"Graphing Neighborhood Overlap Failed!\n")

    return G

# Homophily of a graph
def homophily(G):
    # Random p value will be generated using python's random module
    probability_p = float(input("Please enter a p value between 0 and 1: "))

    # Validating whether p is in range of 0 and 1
    if (probability_p > 1) or (probability_p < 0):
        print("Not within range of 0 and 1. Now exiting...")
        return G

    try:
        # Going through all the nodes in the Graph and assigning either red or blue
        # depending on more random events
        for graph_node in G.nodes():
            random_number = random.uniform(0,1) 
            if random_number < probability_p:
                G.nodes[graph_node]["homophily_color"] = "red"
            else:
                G.nodes[graph_node]["homophily_color"] = "blue"
        # Using Networkx's assortativiy coefficient function, giving homophily_color
        # as a parameter to use it and find homophily
        homophily = nx.attribute_assortativity_coefficient(G,"homophily_color")
        print("\nAccording to Networkx Assortativity Function, coefficient is:", homophily,"\n")

        cross_colored = 0
        red_nodes = 0
        blue_nodes = 0
        total_edges_n = 0
        # Going through all of the edges and checking if the next node is a different color
        for graph_edge in G.edges():
            total_edges_n += 1
            node1 = graph_edge[0]
            node2 = graph_edge[1]
            if (G.nodes[node1]["homophily_color"] != G.nodes[node2]["homophily_color"]):
                cross_colored += 1

        i = 0
        for graph_node in G.nodes():
            if (G.nodes[graph_node]["homophily_color"] == "red"):
                red_nodes += 1
            else:
                blue_nodes += 1
        # To check the "tolerance", (1/number_edges)^2
        homophily_tolerance = (1/total_edges_n)**2

        twoTimespTimesq = 2 * (red_nodes/total_edges_n) * (blue_nodes/total_edges_n)

        cross_dividedby_total = cross_colored/total_edges_n

        if (twoTimespTimesq + homophily_tolerance) < cross_dividedby_total:
            print("THERE IS EVIDENCE OF HOMOPHILY!")
            print("2*p*q:",twoTimespTimesq,"+ (1/n)^2",homophily_tolerance,"=",twoTimespTimesq+homophily_tolerance)
            print("IS LESS THAN")
            print("Cross Colored Edges Divided by Total Edges:",cross_dividedby_total,"\n")
        else:
            print("NO EVIDENCE OF HOMOPHILY")
            print("2*p*q:",twoTimespTimesq,"+ (1/n)^2",homophily_tolerance,"=",twoTimespTimesq+homophily_tolerance)
            print("IS GREATER THAN")
            print("Cross Colored Edges Divided by Total Edges:",cross_dividedby_total,"\n")

        # Outputting the Homophily Graph
        pos = nx.spring_layout(G) # Defines position of all nodes

        # Temporary color list for the nodes
        colors = []
        for graph_node in G.nodes():
            colors.append(G.nodes[graph_node]["homophily_color"])
        # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw.html 
        nx.draw(G, pos, with_labels=True, node_color=colors)
    except Exception as e:
        print("Something went wrong:",e)

    # Plotting the graph
    plt.show()
    return G

# Adding "+" or "-" to each edge
def balanced_graph(G):
    G.graph["balance"] = {}
    p = float(input("Please enter a p value between 0 and 1: "))

    # Validating whether p is in range of 0 and 1
    if (p > 1) or (p < 0):
        print("Not within range of 0 and 1. Now exiting...\n")
        return G

    try:
        sampler = di.ExactSolver()
        # Added this dictionary so I can use to determine if 
        # there are any "frustrated" nodes
        weighted_nodes = {}
        for nodes in G.edges():
            random_num = random.uniform(0,1)
            if random_num < p:
                G.graph["balance"].update({nodes:"+"})
                weighted_nodes.update({nodes:int(1)})
            else:
                G.graph["balance"].update({nodes:"-"})
                weighted_nodes.update({nodes:int(-1)})

        # Adding the weight of the nodes using networkx's set_edge_attribute function
        # https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.set_edge_attributes.html
        nx.set_edge_attributes(G,weighted_nodes,"sign")

        # Using DWave's example as a reference to find an inbalance, finding "frustrated edges"
        # https://docs.ocean.dwavesys.com/en/stable/docs_dnx/reference/algorithms/generated/dwave_networkx.algorithms.social.structural_imbalance.html
        frustration, node_colors = dnx.structural_imbalance(G,sampler)
        print("FRUSTRATION",frustration)

        # Determininig if the Graph is balanced
        # If there are no frustrated nodes, then graph should be balanced
        # If frustration dictionary is empty, then graph is balanced, using method from stackoverflow to check if empty
        # https://stackoverflow.com/questions/23177439/how-to-check-if-a-dictionary-is-empty
        if (not frustration):
            print("Graph IS Balanced!")
        else:
            print("Graph IS NOT Balanced")
    except Exception as e:
        print("Something went wrong:",e)

    
    # Plotting the graph now!
    # Defining position of the nodes
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True,node_size=500)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=G.graph["balance"], font_size=20, font_color="red")

    
    # Plotting the graph
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
        sub_menu(selection)
        new = input("Please make a choice: ")
        if (new == '1'):
            print("Now creating graph...\n")
            return create_graph(G)

        elif (new == '2'):
            print("Now creating Karate Club Graph...\n")
            return karate_club(G)

        else:
            print("Invalid Option\n")

    elif (selection == '4'):
        sub_menu(selection)
        new = input("Please make a choice: ")
        if (new == '1'):
            print("Now finding shortest path...\n")
            return shortest_path(G)
        elif (new =='2'):
            print("Now Partitioning Graph...\n")
            return parition_graph(G)
        else:
            print("Invalid Option\n")

    elif (selection == '5'):
        sub_menu(selection)
        new = input("Please make a choice: ")
        if (new == '1'):
            print("Now Plotting Shortest Path...\n")
            return plot_shortest(G)
        elif (new == '2'):
            print("Now Plotting Coefficient Cluster...\n")
            return plot_cluster(G)
        elif (new == '3'):
            print("Now Plotting Neighborhood Overlap...\n")
            return neighborhood_overlap(G)
        else:
            print("Invalid Option\n")

    elif (selection == '6'):
        sub_menu(selection)
        new = input("Please make a choice: ")
        if (new == '1'):
            print("Now Assigning Homophily...\n")
            return homophily(G)
        elif (new == '2'):
            print("Now Assigning Balance to Graph...\n")
            return balanced_graph(G)
        else:
            print("Invalid Option\n")

    elif (selection == '7'):
        print("Now Reading a Digraph...\n")
        return read_digraph(G)

    elif (selection == 'x'):
        print("Now Exiting...\n")

    else:
        print("Not a valid selection\n")

# main function of the program
def main():
    # Creating a gloabal G, acting as memory
    G = nx.empty_graph()
    # Initializing now so it can be used later in shortest path
    G.graph["short_path"] = []
    # Initializing now so it can be used in cluster enabling and disabling
    G.graph["cluster_enable"] = False
    G.graph["cluster_node_sizes"] = []
    G.graph["cluster_node_colors"] = []
    # Initializing now so it can be used in neighborhood enbaling and disabling
    G.graph["neighbor_enable"] = False
    G.graph["neighbor_edge_colors"] = {}

    option = '1'
    while (option != 'x'):
        menu()
        option = input("Please make a selection: ")
        # Reusing G as volatile memory
        G = selection(option, G)

main()
