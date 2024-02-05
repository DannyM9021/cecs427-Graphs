# Daniel Moreno 
# CECS 427-01 Dynamic Networks
# Due Date: February 6, 2024

# Creating a global variable G, acting as "memory"
G = ""

def menu():
    print("MAIN MENU")
    print("1. Read a Graph")
    print("2. Save the Graph")
    print("3. Create a Random Graph")
    print("4. Shortest Path")
    print("5. Plot Graph")
    print("x. Exit\n")

def read_graph():
    print("Printing Graph:\n",G)

def save_graph():
    file_name = "File_name.txt"
    try:
        with open(file_name, 'w') as file:
            file.write(G)
            file.close()
    except FileNotFoundError:
        print("File not found!")

def create_graph(): 
    n = int(input("Please input an n value: "))
    c = float(input("Please input a c value: "))

def shortest_path():
    pass

def plot():
    pass

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

def main():
    option = '1'
    while (option != 'x'):
        menu()
        option = input("Please make a selection: ")
        selection(option)

main()
