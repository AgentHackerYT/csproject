import csv
import random
from datetime import datetime, timedelta
import time
import os
import ast

def place_order():
    order = []
    orderid = random.randint(1000000000000000, 9999999999999999)  # Generate a unique order ID
    estimated_delivery = datetime.now() + timedelta(days=random.randint(3, 5))  # Random delivery in 3-5 days
    
    # Open the stock file once outside the loop
    with open("stock.csv", "r") as f:
        reader = list(csv.reader(f))  # Read all rows into memory
        
        while True:
            item = []
            found = False
            item_id = input("Enter Item number: ")
            
            # Search for the item in the stock list
            for i in reader:
                if i[0] == item_id:
                    found = True
                    item = i
                    if int(i[2]) == 0:  # Check if the item is out of stock
                        print("🔴 Out of Stock!")
                        break  # Stop searching if item is out of stock
                    print("🟢 Item Found")
                    print(f"Name: {i[1]}\nStock Left: {i[2]}\nPrice: {i[3]}")
                    break  # Stop looping through items once found
            
            if not found:
                print("🔴 Product Not Found")
                continue  # Prompt for another item if not found
            
            # Ask for the quantity and handle invalid input
            while True:
                try:
                    q = int(input("Enter Quantity: "))
                    if q <= 0:
                        print("❌ Quantity must be a positive number.")
                    elif q > int(item[2]):  # Check stock availability
                        print(f"🟠 Only {item[2]} left in stock. Please choose a valid quantity.")
                    else:
                        break  # Exit the loop if the quantity is valid
                except ValueError:
                    print("❌ Please enter a valid quantity.")
            
            # Calculate the price for this item
            price = float(item[3]) * q
            print(f"Successfully added {item[1]} x {q} | ${price}")
            
            # Add the item to the order
            order.append([item[0], item[1], q, price])
            
            # Subtract purchased quantity from stock
            item[2] = str(int(item[2]) - q)
            #print(f"Updated Stock for {item[1]}: {item[2]} left.")

            # Ask if they want to continue shopping
            c = input("Do you want to shop more? (y/n): ").strip().lower()
            if c != 'y':
                break  # Exit the loop if they don’t want to shop more

    # Display Final Confirmation of Order
    print("\n--- Order Summary ---")
    for item in order:
        print(f"Item: {item[1]} | Quantity: {item[2]} | Price: ${item[3]:.2f}")
    
    total_amount = sum(item[3] for item in order)
    print(f"Grand Total: ${total_amount:.2f}")
    
    confirm = input("\nDo you want to confirm and place the order? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Order canceled.")
        return
    
    # Deduct stock after confirmation
    with open("stock.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(reader)  # Write the updated stock back into the file
    
    # Generate a random tracking number
    tracking_number = random.randint(1000000000, 9999999999)
    
    # Estimate delivery date and display the shipping info
    print("\n--- Order Confirmation ---")
    print(f"Order ID: {orderid}")
    print(f"Order Status: Confirmed")
    print(f"Shipped via: FedEx")
    print(f"Estimated Delivery Date: {estimated_delivery.strftime('%A, %B %d, %Y')}")
    print(f"Tracking Number: {tracking_number}")
    print(f"Total Amount: ${total_amount:.2f}")
    print("\nYour order has been placed successfully!")

    # Save the order details to order.csv
    with open("order.csv", "a", newline="") as f:
        writer = csv.writer(f)
        # Write the order details (Order ID, Item, Quantity, Price, Total Amount, Tracking Number, Delivery Date)
        writer.writerow([orderid, "Confirmed",order, sum(item[3] for item in order),tracking_number, estimated_delivery.strftime('%A, %B %d, %Y')])

    print(f"\nOrder details have been saved to 'order.csv'.")

# Call the place_order function to run the program
def view_order():
    oid = int(input("Enter Order ID: "))  # Request the user to input the order ID
    with open("order.csv", "r") as f:
        found = False
        r = csv.reader(f)
        for i in r:
            if int(i[0]) == oid:  # Check if the Order ID matches
                print("🟢 Order Found")
                
                # Extracting the order details from the row
                order_id = i[0]
                status = i[1]
                items_list_str = i[2]  # String representation of the list of items
                total_amount = float(i[3])
                tracking_number = i[4]
                delivery_date = i[5]
                
                # Convert the string to a list using ast.literal_eval (safe eval)
                items_list = eval(items_list_str)
                
                print(f"\n--- Order Details ---")
                print(f"Order ID: {order_id}")
                print(f"Order Status: {status}")
                print(f"Total Amount: ${total_amount:.2f}")
                print(f"Tracking Number: {tracking_number}")
                print(f"Estimated Delivery Date: {delivery_date}")
                
                print("\nItems Ordered:")
                for item in items_list:
                    item_id, item_name, qty, item_price = item
                    print(f"Item ID: {item_id} | Name: {item_name} | Quantity: {qty} | Price: ${item_price:.2f}")

                found = True
                break  # Stop searching once the order is found
        
        if not found:
            print(f"🔴 Order ID {oid} Not Found")  # If no order with that ID is found
def view_items():
    # Open the stock file and read the items
    with open("stock.csv", "r") as f:
        reader = list(csv.reader(f))
        
        # If the file is empty
        if not reader:
            print("❌ No items available in the stock.")
            return
        
        # Header for the product list
        print("\n✨ Welcome to the Product List ✨")
        print("-" * 50)
        print(f"{'ID':<5} {'Name':<25} {'Stock':<10} {'Price':<10}")
        print("-" * 50)
        
        # Print each product with formatting
        for item in reader:
            # You can add colors using ANSI escape codes for more beauty
            print(f"{item[0]:<5} {item[1]:<25} {item[2]:<10} ${float(item[3]):<10.2f}")
        
        print("-" * 50)
        print("\n✨ Thank you for viewing our products! ✨\n")
def customer_menu():
    while True:
        print("="*40)
        print("🔷 Welcome to Online Store (Customer) 🔷")
        print("="*40)
        print("Select from the options below")
        print()
        print('1️⃣  Buy')
        print('2️⃣  Items')
        print('3️⃣  Track')
        print('4️⃣  Main Menu')
        print()

        try:
            c = int(input("🟢 Choose your option: "))
        except ValueError:
            os.system("cls" if os.name == "nt" else "clear")
            print("*"*40)
            print("🔴 Invalid input, please enter a number 🙏")
            print("*"*40)
            time.sleep(2)
            continue

        if c == 1:
            os.system("cls" if os.name == "nt" else "clear")
            print("🔷 You chose: Buy 🛒")
            place_order()
            # Add the logic for buying items

        elif c == 2:
            os.system("cls" if os.name == "nt" else "clear")
            print("🔷 You chose: Items 📦")
            view_items()
            # Show the list of items or handle items-related actions
        elif c == 3:
            os.system("cls" if os.name == "nt" else "clear")
            print("🔷 You chose: Track your order 📍")
            view_order()
            # Implement tracking functionality
        elif c == 4:
            os.system("cls" if os.name == "nt" else "clear")
            return  # Exit customer menu and return to main menu
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print("*"*40)
            print("🔴 No such option, Please try again 🙏")
            print("*"*40)
            time.sleep(2)

def view_orders():
    print("🔷 View Orders")

    # Read the orders from 'order.csv' (assuming it contains order details)
    print(f"{'Order ID':<20} {'Status':<12} {'Total Price':<12} {'Items'}")
    print("-" * 60)

    with open('order.csv', 'r') as file:
        reader = csv.reader(file)
        #next(reader)  # Skip header row if necessary
        for row in reader:
            order_id = row[0]
            order_status = row[1]
            items = ast.literal_eval(row[2])  # Convert string to list of items
            total_price = row[3]
            print(f"{order_id:<20} {order_status:<12} ${total_price:<12} {items}")
    input("Press Enter to exit....")
    print("Returning to Employee Menu...\n")
    time.sleep(1)
def add_item_to_stock():
    print("🔷 Add Item to Stock")
    time.sleep(1)

    # Input item details
    item_id = input("Enter Product ID (unique): ")
    item_name = input("Enter Product Name: ")
    try:
        item_stock = int(input("Enter Stock Quantity: "))
        item_price = float(input("Enter Product Price: $"))
    except ValueError:
        print("🔴 Invalid input. Please enter valid numerical values for stock and price.")
        return  # Exit the function if the input is invalid

    # Read current stock data
    rows = []
    with open('stock.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Check if item already exists in the stock
    for row in rows:
        if row[0] == item_id:
            print("🔴 Item with this ID already exists in stock!")
            return

    # Add new item to the stock
    rows.append([item_id, item_name, str(item_stock), f"{item_price:.2f}"])

    # Write the updated stock back to the file
    with open('stock.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"🟢 Item '{item_name}' added to stock successfully.")
def update_order_status():
    print("🔷 Update Order Status")
    time.sleep(1)

    order_id = input("Enter Order ID to update: ")
    new_status = input("Enter new status (e.g., 'Confirmed', 'Shipped', 'Delivered'): ")

    updated = False
    rows = []

    # Read the orders from the CSV file and update the selected order's status
    with open('order.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)  # Read all rows into a list

        for row in rows:
            if row[0] == order_id:
                row[1] = new_status  # Update the status
                updated = True
                print(f"Order {order_id} status updated to '{new_status}'")
                break

    # Write the updated rows back to the file
    if updated:
        with open('order.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    if not updated:
        print(f"Order ID {order_id} not found.")
    
    print("Returning to Employee Menu...\n")
    time.sleep(1)

def manage_orders():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # Clear screen on each menu refresh
        print("=" * 40)
        print("🔷 Manage Orders")
        print("=" * 40)
        print("1️⃣  View Orders")
        print("2️⃣  Update Order Status")
        print("3️⃣  Employee Menu")
        print()

        try:
            order_choice = int(input("🟢 Choose your option: "))
        except ValueError:
            print("*" * 40)
            print("🔴 Invalid input, please enter a number 🙏")
            print("*" * 40)
            time.sleep(1)
            continue  # Restart the loop if input is invalid

        if order_choice == 1:
            view_orders()  # Call the function to view orders
        elif order_choice == 2:
            update_order_status()  # Call the function to update the order status
        elif order_choice == 3:
            print("Returning to Employee Menu...\n")
            time.sleep(1)
            employee_menu()
            break  # Exit the manage orders menu and return to the employee menu
        else:
            print("*" * 40)
            print("🔴 Invalid option, Please try again 🙏")
            print("*" * 40)
            time.sleep(1)


def manage_stock():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # Clear screen on each menu refresh
        print("="*40)
        print("🔷 Manage Stock")
        print("="*40)
        print("1️⃣  View Stock")
        print('2️⃣  Add Item to Stock')
        print('3️⃣  Add/Subtract Stock')
        print('4️⃣  Employee Menu')
        print()

        try:
            stock_choice = int(input("🟢 Choose your option: "))
        except ValueError:
            print("*"*40)
            print("🔴 Invalid input, please enter a number 🙏")
            print("*"*40)
            time.sleep(2)
            return  # Restart the menu if input is invalid

        if stock_choice == 1:
            print("🔷 Viewing Stock Levels...")
            with open('stock.csv', 'r') as file:
                reader = csv.reader(file)
                print(f"{'ID':<5} {'Product Name':<25} {'Stock':<10} {'Price':<10}")
                for row in reader:
                    print(f"{row[0]:<5} {row[1]:<25} {row[2]:<10} ${row[3]:<10}")
            input("Press enter to exit....")
            print("Returning to Employee Menu...\n")
            time.sleep(1)

        elif stock_choice == 2:
            add_item_to_stock()  # Call the function to add a new item
            print("Returning to Employee Menu...\n")
            time.sleep(1)

        elif stock_choice == 3:
            print("🔷 Add/Subtract Stock...")
            product_id = input("Enter Product ID to update: ")
            quantity_change = int(input("Enter the quantity to add or subtract (e.g., -5 to subtract): "))
            
            updated = False
            rows = []
            
            with open('stock.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)  # Read all rows into a list
                
                for row in rows:
                    if row[0] == product_id:
                        stock = int(row[2])
                        row[2] = str(stock + quantity_change)  # Update the stock value
                        updated = True
                        print(f"Updated Stock for {row[1]}: {stock} -> {stock + quantity_change}")
                        break
            
            # Write the updated rows back to the file
            if updated:
                with open('stock.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
            
            time.sleep(2)
            print("Returning to Employee Menu...\n")
            time.sleep(1)
        
        elif stock_choice == 4:
            print("Returning to Employee Menu...\n")
            employee_menu()
            time.sleep(1)

        else:
            print("*"*40)
            print("🔴 Invalid option, Please try again 🙏")
            print("*"*40)
            time.sleep(2)


def analytics():
    # Initialize variables to store analytics data
    total_sales = 0
    total_items_sold = 0
    item_sales = {}  # To track sales for each item
    total_orders = 0

    # Read the orders from 'order.csv'
    with open('order.csv', 'r') as file:
        reader = csv.reader(file)
        #next(reader)  # Skip header row if necessary

        for row in reader:
            order_id = row[0]  # Order ID
            order_status = row[1]  # Order status
            items = ast.literal_eval(row[2])  # Convert string to list of items
            total_price = float(row[3])  # Total price of the order
            customer_id = row[4]  # Customer ID (if needed)
            order_date = row[5]  # Order date

            total_orders += 1
            total_sales += total_price

            # Count total items sold and individual item sales
            for item in items:
                item_id, item_name, quantity, price = item
                total_items_sold += quantity
                if item_name in item_sales:
                    item_sales[item_name] += quantity
                else:
                    item_sales[item_name] = quantity

    # Print the analytics data
    print("=" * 40)
    print("🔷 Online Store Analytics 🔷")
    print("=" * 40)
    print(f"Total Orders: {total_orders}")
    print(f"Total Sales: ${total_sales:.2f}")
    print(f"Total Items Sold: {total_items_sold}")
    print("\nMost Popular Items:")
    for item, quantity in item_sales.items():
        print(f"{item}: {quantity} sold")
    print("=" * 40)
    input("Press Enter to exit....")
    # Add some delay before returning to employee menu
    time.sleep(1)


def employee_menu(log=False):
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # Clear screen on each menu refresh
        print("="*40)
        print("🔷 Welcome to Online Store (Employee) 🔷")
        print("="*40)
        print("Select from the options below")
        print()
        print("1️⃣  Manage Orders")
        print("2️⃣  Manage Stock")
        print("3️⃣  Analytics")
        print("4️⃣  Main Menu")
        print()
        if log == True:
            with open("log.csv", "a", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["🟢 LOG IN" , str(datetime.today())])
        try:
            choice = int(input("🟢 Choose your option: "))
        except ValueError:
            print("*"*40)
            print("🔴 Invalid input, please enter a number 🙏")
            print("*"*40)
            time.sleep(2)
            continue  # Restart the loop if the input is invalid
        
        if choice == 1:
            manage_orders()  # Call the manage orders function
        elif choice == 2:
            manage_stock()  # Call the manage stock function
        elif choice == 3:
            analytics()  # Call the analytics function
        elif choice == 4:
            print("Returning to Main Menu...\n")
            with open("log.csv", "a", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["🔴 LOG OUT",str(datetime.today())])
            time.sleep(1)
            main_menu()
            break  # Exit the employee menu and return to the main menu
        else:
            print("*"*40)
            print("🔴 Invalid option, Please try again 🙏")
            print("*"*40)
            time.sleep(2)

def main_menu():
    while True:
        print("="*40)
        print("🔷 Welcome to Online Store 🔷")
        print("="*40)
        print("Select from the options below")
        print()
        print("1️⃣  Customer 👨‍👩‍👧‍👦")
        print("2️⃣  Employee 👨‍💼")
        print("3️⃣  Exit 🔚")
        print()

        try:
            c = int(input("🟢 Choose your option: "))
        except ValueError:
            print("*"*40)
            print("🔴 Invalid input, please enter a number 🙏")
            print("*"*40)
            time.sleep(2)
            continue

        if c == 1:
            os.system("cls" if os.name == "nt" else "clear")
            customer_menu()  # Go to customer menu
        elif c == 2:
            os.system("cls" if os.name == "nt" else "clear")
            employee_menu(True)
            time.sleep(2)
        elif c == 3:
            for i in range(6):
                print("="*40)
                print("Saving Data")
                print("="*40)
                time.sleep(0.2)
                os.system("cls" if os.name == "nt" else "clear")
                print("="*40)
                print("Saving Data.")
                print("="*40)
                time.sleep(0.2)
                os.system("cls" if os.name == "nt" else "clear")
                print("="*40)
                print("Saving Data..")
                print("="*40)
                time.sleep(0.2)
                os.system("cls" if os.name == "nt" else "clear")
                print("="*40)
                print("Saving Data...")
                print("="*40)
                time.sleep(0.2)
                os.system("cls" if os.name == "nt" else "clear")
            print("Online Store Customer and Employee Experience Software")
            time.sleep(0.3)
            print("Made by Jenil Dobaria")
            time.sleep(0.3)
            print("XII B")
            time.sleep(0.3)
            print("Goodbye! 👋")
            time.sleep(0.3)
            os.abort()
            break  # Exit the main menu and stop the program
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print("*"*40)
            print("🔴 No such option, Please try again 🙏")
            print("*"*40)
            time.sleep(2)

print("""
░██████╗████████╗░█████╗░██████╗░███████╗███╗░░░███╗░█████╗░███╗░░██╗░█████╗░░██████╗░███████╗██████╗░
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝████╗░████║██╔══██╗████╗░██║██╔══██╗██╔════╝░██╔════╝██╔══██╗
╚█████╗░░░░██║░░░██║░░██║██████╔╝█████╗░░██╔████╔██║███████║██╔██╗██║███████║██║░░██╗░█████╗░░██████╔╝
░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██╔══╝░░██║╚██╔╝██║██╔══██║██║╚████║██╔══██║██║░░╚██╗██╔══╝░░██╔══██╗
██████╔╝░░░██║░░░╚█████╔╝██║░░██║███████╗██║░╚═╝░██║██║░░██║██║░╚███║██║░░██║╚██████╔╝███████╗██║░░██║
╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░╚═════╝░╚══════╝╚═╝░░╚═╝""")
main_menu()
