from data import stock, personnel
from datetime import datetime
from collections import OrderedDict


parameters = {
    "is_authenticated": False,
    "user_name": None,
    "password": None,
    "how_much_entries": 0
}
summary = []
def get_user_name():
    return input("What is your user name? ")

def greet_user():
    print(f"Hello, {parameters['user_name']}!")


def selecting_operation():
    print(f"What would you like to do?\n1. List items by warehouse\n2. Search an item and place an order\n3. Browse by category\n4. Quit")
    return input("Type the number of the operation: ")


def list_items_on_all_warehouses():
    other_warehouses = {} #new dict to write other warehouses if they exist

    print("Items in warehouse 1:")
    count = 0
    for item in stock:
        if item['warehouse'] == 1:
            count+=1
            print(f"- {item['state']} {item['category']}")
        else:
            warehouse_id = str(item['warehouse'])
            if warehouse_id not in other_warehouses:
                other_warehouses[warehouse_id] = []
            other_warehouses[warehouse_id].append(item)

    for warehouse_id, items in other_warehouses.items():
        print(f"Items in warehouse {warehouse_id}:")
        for item in items:
            print(f"- {item['state']} {item['category']}")

    print()
    print("Total items in warehouse 1:", count)
    total = count
    total_warehouses = 1
    for warehouse_id, items in other_warehouses.items():
        total_warehouse = len(items)
        total = total + total_warehouse
        total_warehouses+=1
        print(f"Total items in warehouse {warehouse_id}:", total_warehouse)
    summary.append(f"Listed {total} items in {total_warehouses} warehouses")
    parameters['how_much_entries'] +=1

def print_warehouse_list(warehouse):
    for item in warehouse:
        date_of_stock = datetime.strptime(item['date_of_stock'], '%Y-%m-%d %H:%M:%S')
        time_passed = str(datetime.now() - date_of_stock)
        days_passed = time_passed.split(",").pop(0)
        stock_text = f"in stock for {days_passed}"
        print(f"- Warehouse {item['warehouse']} ({stock_text})")

def print_results(**warehouses):

    totals = [len(items) for items in warehouses.values()]
    total_amount = sum(totals)

    print("Amount available:", total_amount)
    if total_amount:
        print("Location:")
        for items in warehouses.values():
            print_warehouse_list(items)

        if len(warehouses) > 1:
            max_availability = max(*totals)
            max_warehouse = next(iter([id for id, items in warehouses.items()
                                       if len(items) == max_availability]), None)
            print(f"Maximum availability: {max_availability} in Warehouse {max_warehouse}")
    else:
        print("Location: Not in stock")


def only_for_users(func):
    def inner(*args, **kwargs):
        if parameters["is_authenticated"]:
            func(*args, **kwargs)
        else:
            password = input("Please, type your employee password: ")
            userr = None
            for user in personnel:
                if user["user_name"] == parameters["user_name"] and user["password"] == password:
                    userr = user
            if userr:
                parameters["is_authenticated"] = True
                print()
                func(*args, **kwargs)
            else:
                again = input("There is no user with these credentials.\n"
                              "Would you like to try again?(y/n) ")
                if again.lower() in ["y", "yes"]:
                    parameters["user_name"] = get_user_name()
                    inner(*args, **kwargs)
    return inner

def order_an_item(searched_item, **warehouses):
    totals = [len(items) for items in warehouses.values()]
    total_amount = sum(totals)

    if total_amount:
        print()
        order = input("Would you like to order this item?(y/n) ")
        if order == "y":
            place_an_order(searched_item, total_amount)

@only_for_users
def place_an_order(searched_item, total_amount):
    amount = int(input("How many would you like? "))
    if amount > total_amount:
        print("*" * 50)
        print("There are not this many available.",
              "The maximum amount that can be ordered is", total_amount)
        print("*" * 50)
        accept_available = input("Would you like to order the maximum available?(y/n) ")
        if accept_available == "y":
            amount = total_amount
    if amount <= total_amount:
        print(amount, searched_item, "have been ordered.")

    summary.append(f"Ordered {amount} {searched_item}")
    parameters["how_much_entries"] += 1

def search_item(searched_item):
    results = {}
    for item in stock:
        full_name = f"{item['state']} {item['category'].lower()}"
        if full_name.lower() == searched_item.lower():
            warehouse_id = str(item["warehouse"])
            if str(warehouse_id) not in results:
                results[warehouse_id] = []
            results[warehouse_id].append(item)
    return results

def search_and_order_item():
    searched_item = input("What is the name of the item? ")
    search_results = search_item(searched_item)

    print_results(**search_results)

    summary.append(f"Searched for item {searched_item}")
    order_an_item(searched_item=searched_item, **search_results)

    parameters['how_much_entries'] +=1

def ordered_dict():
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
    summary.append(f"Searched in category {category}")

def main(operation):

    #operation = selecting_operation()
    stop = False
    if operation == "1":
        list_items_on_all_warehouses()

    elif operation == "2":
        search_and_order_item()

    elif operation == "3":
        ordered_dict()
    elif operation == "4":
        stop = True
        pass
    else:
        print("*" * 40)
        print(f"{operation} is not a valid operation!")
        print("*" * 40)

    if stop is False and parameters['how_much_entries'] < 4:
        go_again = input("\nWould you like to perform another operation?(y/n) ")
        if go_again.lower() in ["y", "yes"]:
            main(selecting_operation()) 


parameters['user_name'] = get_user_name()
greet_user()
print("\n")

main(selecting_operation())


print(f"\nThank you for your visit, {parameters['user_name']}!")
if parameters['how_much_entries'] > 0:
    print("\nSession summary: ")
    for n, summ in enumerate(summary):
        print(f"\t{n+1}. {summ}")
