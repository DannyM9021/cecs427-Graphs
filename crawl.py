# Daniel Moreno
# CECS 427 - 01 Dynamic Networks
# Due Data: April 26, 2024

# This program will parse the given document
# Then send parameters to the scrapy spider to get the nodes we want

# Importing spider to pass parameters
from network/network/spiders import www_spider 
# Parsing the file given
def file_parse():
    file_path = "crawlingFile" #input("Please input a file to read from: ")
    items = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                items.append(line.split("\n")[0])
            file.close()
            print(items)
    except Exception as e:
        print("Error:", e)

# Main function to call all the necessary functions
def main():
    file_parse()

# Main entrypoint the application
main()

