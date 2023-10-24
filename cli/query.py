from data import stock
from datetime import datetime
from collections import OrderedDict

name = input("What is your user name? ")
print("\n")

print(f"Hello, {name}!\nWhat would you like to do?\n1. List items by warehouse\n2. Search an item and place an order\n3. Browse by category\n4. Quit")
operation = input("Type the number of the operation: ")

errorr = False
if operation == "1":
    print("Items in warehouse 1:") 
    count = 0
    count2 = 0
    for i in range(len(stock)):
        if stock[i]["warehouse"] == 1:
            print(f"- {stock[i]['state']} {stock[i]['category']}")
            count+=1
    print("\nItems in warehouse 2:") 
    for i in range(len(stock)):
        if stock[i]["warehouse"] == 2:
            print(f"- {stock[i]['state']} {stock[i]['category']}")
            count2+=1
    print(f"\nTotal items in warehouse 1: {count}")
    print(f"Total items in warehouse 2: {count2}")

elif operation == "2":
    print("\n")
    itemname = input("What is the name of the item? ") ## taking item name lowered
    countm = 0
    full_answer = ""
    first_w = 0
    second_w = 0
    for i in range(len(stock)):
        fullname = stock[i]['state'] + " " + stock[i]['category']
        if fullname.lower() == itemname.lower():
            countm+=1
            if stock[i]['warehouse'] == 1:
                first_w += 1
            if stock[i]['warehouse'] == 2:
                second_w += 1  
            date_stock = datetime.strptime(stock[i]['date_of_stock'], '%Y-%m-%d %H:%M:%S')
            time_passed = str(datetime.now() - date_stock)
            days_passed = time_passed.split(",").pop(0)
            full_answer += f"- Warehouse {stock[i]['warehouse']} (in stock for {days_passed})\n"  

    if countm == 0:
        full_answer = "Not is stock"
        errorr = True
    print(f"Ammount available: {countm}")
    print("Location:")
    print(full_answer)
    if first_w > 0 and second_w > 0:
        max_awail = 0
        wareh = 0
        if first_w > second_w:
            wareh = 1
            max_awail = first_w
        elif first_w < second_w:
            wareh = 2
            max_awail = second_w
        elif first_w == second_w:
            wareh = 1
            max_awail = first_w
        print(f"Maximum availability: {max_awail} in Warehouse {wareh}")

    if errorr is not True:
        print("\n")
        order = input("Would you like to order this item? (y/n) ")
        if order.lower() == "y":
            both = first_w + second_w
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
        
        categories = OrderedDict()
        for item in stock:
            if item["category"] not in categories.keys():
                categories[item["category"]] = 0
            categories[item["category"]] += 1
      
        num = 1
        for category, amount in categories.items():
            print(f"{num}. {category} ({amount})")
            num += 1

        chosen_number = int(input("Type the number of the category to browse: "))
        category_list = list(categories.items())
        chosen_name = category_list[chosen_number - 1][0]
        print("\n")
        print(f"List of {chosen_name.lower()}'s available:")
        for item in stock:
            if item["category"] == chosen_name:
                full_name = f"{item['state']} {item['category'].lower()}"
                print(f"{full_name}, Warehouse {item['warehouse']}")

elif operation == "4":
    pass
else:
    print("*" * 40)
    print(f"{operation} is not a valid operation!")
    print("*" * 40)


# Thank the user for the visit
print(f"\nThank you for your visit, {name}!")