# Daniel Moreno 
# CECS 427-01 Dynamic Networks
# Due Date: April 28, 2024

# Importing networkx and numpy as recommended by the documentation
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import math
# importing for balancing graph
import dimod as di
import dwave_networkx as dnx
# In case needed for bipartite algorithms
# https://networkx.org/documentation/stable/reference/algorithms/bipartite.html
from networkx.algorithms import bipartite
import json

# Making a global variable for shortest path
short = []

# Making global variable Digraph to store digraph, initializing to empty list
digraph_storage = []

# Making global variable to store Bigraph for assignment 4
bigraph_storage = []
market_graph_storage = []

# Making global variable graph for page rank
web_page_graph = []

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
        print("2. Karate-Club Graph")
        print("3. Bipartite Graph")
        print("4. Market Clearing\n")
    elif (selection == '4'):
        print("1. Shortest Path")
        print("2. Partition G")
        print("3. Travel Equilibrium and Social Optimal")
        print("4. Perfect Matching")
        print("5. Market Clearance Algorithm")
        print("6. Page Rank Algorithm\n")
    elif (selection == '5'):
        print("1. The Shortest Path")
        print("2. Cluster Coefficients")
        print("3. Neighborhood Overlaps")
        print("4. Bipartite Graph")
        print("5. Preferred-Seller Graph")
        print("6. Page Rank of Web Graph")
        print("7. Loglog Graph\n")
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
    selection = int(input("\n1. Unidirectional Graph\n2. Directional Graph\nWhich type of graph do you want to save?: "))
    File_name = input("Please input a file to save to: ")
    try:
        # If graph is directed will save accordingly
        if (selection == 2):
            digraph_string = ""
            global digraph_storage
            for row in digraph_storage:
                for index in range(len(row)):
                    digraph_string += str(row[index]) + " "
                digraph_string += '\n'
            print(digraph_string)
            # Now saving from global to file
            with open(File_name, 'w') as file:
                file.write(digraph_string)
                file.close()
                print("Directed Graph saved into file!\n")
                return G
        # Saves UNDIRECTED GRAPH, Assignment 1
        with open(File_name, 'w') as file:
            nx.write_adjlist(G, File_name)
            file.close()
            print("Undirected Graph saved into file!\n")
            return G
    # Handles exception if no file exists
    except FileNotFoundError:
        print("File not found!\n")
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

# Creates Bigraph for assignment 4
def create_bigraph(G):
    nodes_A = int(input("How many nodes in set A?: "))
    nodes_B = int(input("How many nodes in set B?: "))
    prob_p = float(input("Probability that edge (u,v) is created: "))
    # Creating Random Bipartite Graph given user input
    # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.generators.random_graph.html
    global bigraph_storage
    bigraph_storage = nx.bipartite.random_graph(nodes_A,nodes_B, prob_p)
    print("Bigraph created successfully!\n")
    return G

# Market CLearing Graph for assignment 4 (using file provided by professor)
def market_clearing(G):
    # Reading file path provided by user
    # Parsing through file to get necessary information
    temp = []
    buyer_pref = []
    file_path = input("Please input file path for market clearing: ")
    try:
        with open(file_path, 'r') as file:
            for line in file:
                temp.append(line.strip())
            file.close()
        # Parsing and assigning values
        num_houses = int(temp[0][0])
        start_prices = temp[0][2:7].split(',')
        for i in range(len(start_prices)):
            start_prices[i] = int(start_prices[i])
        # Starting at 1, since index 0 has num houses and start prices
        for i in range(1,len(temp)):
            buyer_pref.append(temp[i].split(','))
        for i in range(len(buyer_pref)):
            for j in range(len(buyer_pref[i])):
                buyer_pref[i][j] = int(buyer_pref[i][j])

        # Assigning bipartite graph
        global market_graph_storage
        market_graph_storage = nx.Graph()
        # Assigning Seller's start prices
        for i in range(0, int(num_houses)):
            seller_id = str(i+1)
            market_graph_storage.add_node(seller_id, bipartite=0, type="seller",start_price=start_prices[i])

        # Assigning buyers preference list
        for i, buyer_pref in enumerate(buyer_pref, start=int(num_houses)):
            buyer_id = str(i+1)
            market_graph_storage.add_node(buyer_id, bipartite=1, type = "buyer",preference = buyer_pref)
        print(market_graph_storage)
        for node, data in market_graph_storage.nodes(data=True):
            print(f"Node: {node}, Attributes: {data}")
        print("Disconnected Market Graph Created\n")
        return G
    # In case of error, exits without crashing
    except Exception as e:
        print("Market Clearing Error:", e)
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

# Assignment 3 Finding Travel Equilibrium and Social Optimality
def equilibrium_and_optima(G):
    global digraph_storage
    total_drivers = int(input("Number of Drivers: "))
    source = digraph_storage[0][0] # Start node is 1st row, 1st entry
    destination = digraph_storage[-1][1] # Destination node is last row, 2nd entry

    # Social Optimal
    top_route = math.ceil(total_drivers/2)
    bottom_route = math.floor(total_drivers/2)
    top_eq1 = int(digraph_storage[0][2]) * total_drivers + int(digraph_storage[0][3]) # Gets weights from digraph memory (3rd and 4th positions)
    top_eq2 = int(digraph_storage[1][2]) * total_drivers + int(digraph_storage[1][3]) # Gets weights from digraph memory (3rd and 4th positions)
    bottom_eq1 = int(digraph_storage[3][2]) * total_drivers + int(digraph_storage[3][3]) # Gets weights from digraph memory (3rd and 4th positions)
    bottom_eq2 = int(digraph_storage[4][2]) * total_drivers + int(digraph_storage[4][3]) # Gets weights from digraph memory (3rd and 4th positions)
    total_top = top_eq1 + top_eq2
    total_bottom = bottom_eq1 + bottom_eq2
    social_optimal = total_top + total_bottom
    print("Social Optimal:",social_optimal)

    # Nash Equilibrium
    nash_equilibrium = int(digraph_storage[0][2]) * total_drivers + int(digraph_storage[0][3]) * 2 # Nash Equilibrium when all drivers go same route: top, middle, bottom
    true_cost = nash_equilibrium * total_drivers/2
    print("Nash Equilibrium",true_cost)
    print()

    try:
        # Plotting 
        social_nash_graph = nx.DiGraph()
        social_nash_graph.add_node(0, pos=(0,0))
        social_nash_graph.add_node(1, pos=(1,1))
        social_nash_graph.add_node(2, pos=(1,-1))
        social_nash_graph.add_node(3, pos=(2,0))
        social_nash_graph.add_weighted_edges_from([(0, 1, str(digraph_storage[0][2]+'x + '+digraph_storage[0][3])), (0, 2, str(digraph_storage[1][2]+'x + '+digraph_storage[1][3])), (1, 2,  str(digraph_storage[2][2]+'x + '+digraph_storage[2][3])), (1, 3,  str(digraph_storage[3][2]+'x + '+digraph_storage[3][3])), (2,3,  str(digraph_storage[4][2]+'x + '+digraph_storage[4][3]))])
        pos = nx.get_node_attributes(social_nash_graph,'pos')
        edge_weights = nx.get_edge_attributes(social_nash_graph,'weight')
        nx.draw_networkx_edge_labels(social_nash_graph,pos,edge_labels=edge_weights)
        nx.draw_networkx(social_nash_graph, pos)
        plt.axis('equal')
        plt.title("Social Optimal and Nash Equilibrium Digraph")
        plt.text(0.1,0.9, "Number of Drivers: "+str(total_drivers), fontsize=15, transform=plt.gca().transAxes)
        plt.text(0.1,0.85, "Social Optimal: "+str(social_optimal), fontsize=15, transform=plt.gca().transAxes)
        plt.text(0.1,0.8, "Nash Equilibrium: "+str(int(true_cost)), fontsize=15, transform=plt.gca().transAxes)
        plt.show()
    except Exception as e:
        print(e)
    return G

# Perfect Matching Algorithm for assignment 4
def perfect_match(G):
    try:
        global bigraph_storage
        # Making sure a bigraph exists
        if (bigraph_storage == []):
            print("Create a Bipartite Graph first please!\n")
            return G
        # Creating two sets, to be able to match, between "buyers and sellers"
        buyers = set()
        sellers = set()
        # Separates nodes based on if they are in the sellers or buyer's part of the graph
        for node, data in bigraph_storage.nodes(data=True):
            if data['bipartite'] == 0:
                sellers.add(node)
            else:
                buyers.add(node)
        # Used for existing algorithm in Networkx for Matching
        # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.matching.hopcroft_karp_matching.html
        perfect_matching = nx.bipartite.matching.hopcroft_karp_matching(bigraph_storage, top_nodes=sellers)
        for seller, buyer in perfect_matching.items():
            print("Seller:",seller, "Matches with Buyer", buyer)
        print()
        return G
    # Returns any exception without crashing program
    except Exception as e:
        print(e)
        return G

# Market Clearance Algorithm for assignment 4
def market_clearance_algorithm(G):
    try:
        global market_graph_storage
        # Checking if a market graph has been created
        if (market_graph_storage == []):
            print("Please Create a Market Graph first!\n")
            return G
        # Getting information from graph to perform Market Clearance algorithm
        house_prices = []
        preference = []
        for node, data in market_graph_storage.nodes(data=True):
            if data['type'] == 'seller':
                house_prices.append([node, data['start_price']])
            elif data['type'] == 'buyer':
                preference.append([node, data['preference']])

        # Figuring out payoffs for each of the buyers
        # Recording which house gives the best payoff for each buyer's preference
        matched_nodes = []
        max_preference = []
        matched = False
        market_cleared = []

        while matched == False:
            for node in preference:
                for index in range(len(node[1])):
                    max_preference.append([house_prices[index][0],node[1][index] - house_prices[index][1]])
                # Getting max value based on the profit of each house
                # Used lambda function to use value rather than node as the max argument
                # https://docs.python.org/3/reference/expressions.html
                max_node = max(max_preference, key = lambda price: price[1])
                matched_nodes.append(max_node)
                market_cleared.append([node[0],max_node[0]])
                max_preference = []
            
            # Checking if there is a constricted set
            counter = []
            for x in range(len(house_prices)):
                counter.append(0)
            for m in matched_nodes:
                counter[int(m[0])-1] += 1
            # If constriction, subtract 1, at the end, i should equal number of houses
            i = 0
            # Increasing the price of the house with constriction
            for c in range(len(counter)):
                if (counter[c] > 1):
                    house_prices[c][1] += 1
                    matched_nodes = []
                    market_cleared = []
                    i -= 1
                i += 1
            # If no constricted sets, while loop terminated and results are obtained
            if i == len(counter):
                matched = True
                print("RESULTS!!!")
                print("Final House Prices in [node, price] format:",house_prices)
                # print(matched_nodes)
                print("Preference Match in [buyer,seller] format:",market_cleared)
                print()
                break
        # Adding final prices to each of the house
        for node in house_prices:
            market_graph_storage.nodes[node[0]]["final_price"] = node[1]
        # Connecting buyer to seller nodes based on algorithm
        for pair in market_cleared:
            market_graph_storage.add_edge(pair[0],pair[1])
        return G
    except Exception as e:
        print(e)
        return G

# Page rank algorithm for assignment 5
def page_rank_algo(G):
    global web_page_graph

    # If graph already exists, just do page rank
    if web_page_graph != []:
        return G
    # If graph doesn't exist, graph will first be created
    try:
        nodes = []
        file = input("Please enter file you want to use: ")
        with open(file, 'r') as f:
            data = json.load(f)
            for value in data:
                #dictionary = json.loads(value)
                nodes.append(value)
            # Creating the directed graph
            web_page_graph = nx.DiGraph()
            for list_item in range(100):
                for key, value in nodes[list_item].items():
                    web_page_graph.add_nodes_from([key,value])
                    web_page_graph.add_edge(key,value)
            web_page_graph.graph["page_rank"] = nx.pagerank(web_page_graph)
            print("Page Rank saved")
            return G
    except Exception as e:
        print("Error: ", e)
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

# Plotting Bigraph Assignment 4
def plot_bigraph(G):
    # Separating nodes from left and right (bipartit 0 or 1)
    global bigraph_storage
    left_nodes = []
    right_nodes = []
    for node,data in bigraph_storage.nodes(data=True):
        if data['bipartite'] == 0:
            left_nodes.append(node)
        else:
            right_nodes.append(node)
    print(left_nodes)
    print(right_nodes)

    # Defines positioning for bipartite graph
    # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.bipartite_layout.html
    pos = nx.bipartite_layout(bigraph_storage, left_nodes)

    # Drawing nodes (left and right side)
    nx.draw_networkx_nodes(bigraph_storage, pos, nodelist = left_nodes, node_color = 'red', label="Sellers")
    nx.draw_networkx_nodes(bigraph_storage, pos, nodelist = right_nodes, node_color = 'blue', label="Buyers")

    # Drawing the pre-made edges generated by networkx library
    nx.draw_networkx_edges(bigraph_storage, pos)

    # Labeling the graph
    labels = {}
    # Using same key as value since node 1 corresponds to node 1 from node_list
    for node in bigraph_storage.nodes():
        labels.update({node: node})
    print(labels)
    nx.draw_networkx_labels(bigraph_storage, pos, labels=labels)

    # Displaying Bipratite Graph Legend
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
    plt.legend(loc='upper center')

    # Actually Displaying
    # Turning off x and y axis to plot on a "blank page"
    plt.axis("off")
    plt.show()
    return G

# Plotting Preferred Seller Graph Assignment 4
# Very similar to Plot Bigraph Function
def plot_seller_graph(G):
    try:
        global market_graph_storage
        left_nodes = []
        right_nodes = []
        for node,data in market_graph_storage.nodes(data=True):
            if data['bipartite'] == 0:
                left_nodes.append(node)
            else:
                right_nodes.append(node)
        # Defines positioning for bipartite graph
        # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.bipartite_layout.html
        pos = nx.bipartite_layout(market_graph_storage, left_nodes)

        # Placing nodes on the "canvas"
        nx.draw_networkx_nodes(market_graph_storage, pos, nodelist=left_nodes, node_color='b', label='Sellers')
        nx.draw_networkx_nodes(market_graph_storage, pos, nodelist=right_nodes, node_color='r', label='Buyers')

        # Drawing the edges created by market clearance
        nx.draw_networkx_edges(market_graph_storage, pos)

        # Labeling the graph
        labels = {}
        # Using same key as value since node 1 corresponds to node 1 from node_list
        for node,data in market_graph_storage.nodes(data=True):
            if data['bipartite'] == 0:
                labels.update({node: 'S'+str(node)})
            else:
                labels.update({node: 'B'+str(int(node) % 4 + 1)})

        # Adding information for each node
        for node, (x, y) in pos.items():
            if market_graph_storage.nodes[node]['bipartite'] == 0:
                plt.text(x - 0.2, y, market_graph_storage.nodes[node]['final_price'], fontsize=10, color='black')
            else:
                plt.text(x + 0.1, y, market_graph_storage.nodes[node]['preference'], fontsize=10, color='black')
        nx.draw_networkx_labels(market_graph_storage, pos, labels=labels)

        # Displaying Bipratite Graph Legend
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
        plt.legend(loc='upper center')

        # Adding a title
        plt.title("Seller Preference Graph")

        # Actually Displaying
        # Turning off x and y axis to plot on a "blank page"
        plt.axis("off")
        plt.show()
        return G
    except Exception as e:
        print(e)
        return G

# Plotting the Page Rank Graph 5
def page_rank_graph(G):
    global web_page_graph

    if web_page_graph == []:
        print("Please do Page Rank Algorithm first")
        return G
    try:
        pos = nx.spring_layout(web_page_graph)
        nx.draw(web_page_graph, pos, with_labels=True, arrows=True)
        page_ranks = web_page_graph.graph["page_rank"]
        label_position = {}
        for node, (x,y) in pos.items():
            label_position.update({node: (x, y + 0.07)})
        nx.draw_networkx_labels(web_page_graph, label_position, labels=page_ranks)
        plt.show()
        return G
    except Exception as e:
        print("Error", e)
        return G

# Plotting LogLog Graph for assignment 5
def loglog(G):
    print("LOGLOG")

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

        elif (new == '3'):
            print("Now Creating Bipartite graph...")
            return create_bigraph(G)

        elif (new == '4'):
            print("Now creating Market Clearing Graph")
            return market_clearing(G)

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
        elif (new == '3'):
            return equilibrium_and_optima(G)
        elif (new == '4'):
            print("Now finding perfect match...")
            return perfect_match(G)
        elif (new == '5'):
            print("Now computing market clearance algorithm...")
            return market_clearance_algorithm(G)
        elif (new == '6'):
            print("Now computing Page Rank...")
            return page_rank_algo(G)
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
        elif (new == '4'):
            print("Now Plotting Bipartite Graph...")
            return plot_bigraph(G)
        elif (new == '5'):
            print("Now Plotting Preferred-Seller Graph...")
            return plot_seller_graph(G)
        elif (new == '6'):
            print("Now Plotting Page Rank Graph...")
            return page_rank_graph(G)
        elif (new == '7'):
            print("Now Plotting Loglog Graph...")
            return loglog(G)
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
