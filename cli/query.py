"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import warehouse1, warehouse2

# YOUR CODE STARTS HERE


# Get the user name
# Greet the user
# Show the menu and ask to pick a choice

name = input("What is your user name? ")
print("\n")

print(f"Hello, {name}!\nWhat would you like to do?\n1. List items by warehouse\n2. Search an item and place an order\n3. Quit")
operation = input("Type the number of the operation: ")

errorr = False
if operation == "1":
    print("Items in warehouse 1:")
    for item in warehouse1:
        print(f"- {item}")
    print("Items in warehouse 2:")
    for item in warehouse2:
        print(f"- {item}")
elif operation == "2":
    print("\n")
    itemname = input("What is the name of the item? ")
    howmany = warehouse1.count(itemname)
    howmany2 = warehouse2.count(itemname)

    both = howmany + howmany2

    print(f"Ammount available: {both}")
    if howmany > 0 and howmany2 > 0:
        print("Location: Both warehouses")
        if howmany >= howmany2:
            print(f"Maximum availability: {howmany} in Warehouse 1")
        else:
            print(f"Maximum availability: {howmany2} in Warehouse 2")

    elif howmany > 0 and howmany2 < 1:
        print("Location: Warehouse 1")
    elif howmany < 1 and howmany2 > 0:
        print("Location: warehouse 2")
    else: 
        errorr = True
        print("Location: Not in stock")
    

    print("\n")
    if errorr is not True:
        order = input("Would you like to order this item? (y/n) ")
        if order.lower() == "y":
            howmanyorder = int(input("How many would you like? "))
            if howmanyorder <= both and howmanyorder > 0:
                print(f"{howmanyorder} {itemname} have been ordered.\n")
            elif howmanyorder > both:
                print("********************************************")
                print(f"There are not this many available. The maximum amount that can be ordered is {both}")
                print("********************************************")
                ordermaximum = input("Would you like to order the maximum available? (y/n) ")
                if ordermaximum.lower() == "y":
                    print(f"{both} {itemname} have been ordered.\n")
elif operation == "3":
    pass
else:
    print("********************************************")
    print(f"{operation} is not a valid operation!")
    print("********************************************")





# Thank the user for the visit
print(f"\nThank you for your visit, {name}!")

