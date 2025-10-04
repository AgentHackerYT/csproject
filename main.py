import csv
import datetime
import json
import os
from collections import defaultdict

def firsttime():
    print("Hey welcome to the first step of becoming healthier")

    print("Let's start by asking you some questions")

    name=input("So what is your name?: ")
    print(f"{name} that's a great name there!")
    gender=""
    while True:
        gender=input("What is your gender?(M/F/O): ")
        if gender not in "MFO":
            print("Not A Valid Gender, must be M: Male\nF:Female\nO:Other\nLet's try that again")
            continue
        else:
            break
    age = int(input("What is your age?: "))
    height = int(input("Your Height (in cm): "))
    weight = int(input("Your Weight (in kg): "))
    activitylevel = float(input("Your Activity Level on scale from 1.2 to 1.9, 1.2 being sedentary and 1.9 being extra active\nYour choice: "))
    
    if gender == "M":
        tdee = (10*weight)+(6.25*height)-(5*age)+5
    elif gender == "F":
        tdee = (10*weight)+(6.25*height)-(5*age)-161
    else:
        tdee = (10*weight)+(6.25*height)-(5*age)-50
    tdee *= activitylevel

    data = {
        "name": name,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "tdee": round(tdee, 2)
    }

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"Your profile is all set, wish you best of luck {name} see you healthier ;)")

def load_user_data():
    if not os.path.exists("data.json") or os.stat("data.json").st_size == 0:
        firsttime()
    with open("data.json", "r") as f:
        return json.load(f)

def log_meal(user):
    meal = input("Enter meal name (e.g., Breakfast/Lunch/Dinner/Snack): ")
    calories = float(input("Enter calories for this meal: "))
    date = datetime.date.today().strftime("%Y-%m-%d")

    with open("meals.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0: 
            writer.writerow(["Date", "Name", "Meal", "Calories"])
        writer.writerow([date, user["name"], meal, calories])

    print(f"Logged {calories} calories for {meal} on {date}.")

def get_daily_total(user, date=None):
    """Return total calories for a given date"""
    if date is None:
        date = datetime.date.today().strftime("%Y-%m-%d")
    total = 0
    try:
        with open("meals.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Date"] == date and row["Name"] == user["name"]:
                    total += float(row["Calories"])
    except FileNotFoundError:
        pass
    return total

def view_daily_log(user):
    """View today's calorie intake vs TDEE"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    total = get_daily_total(user, today)
    print(f"\n📅 {today} | {user['name']}")
    print(f"Calories logged today: {total}")
    print(f"Your TDEE: {user['tdee']}")

    if total < user['tdee'] - 100:
        print("➡ You are in a CALORIE DEFICIT 🔻")
    elif total > user['tdee'] + 100:
        print("➡ You are in a CALORIE SURPLUS 🔺")
    else:
        print("➡ You are around MAINTENANCE ⚖️")

def view_analytics(user):
    calories_by_date = defaultdict(float)
    try:
        with open("meals.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Name"] == user["name"]:
                    calories_by_date[row["Date"]] += float(row["Calories"])
    except FileNotFoundError:
        print("No meal logs yet.")
        return

    today = datetime.date.today()
    print("\n📊 Weekly Analytics (last 7 days):")
    weekly_total = 0
    for i in range(7):
        day = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        cals = calories_by_date.get(day, 0)
        weekly_total += cals
        print(f"{day}: {cals} cal")
    print(f"Average daily intake: {round(weekly_total/7,2)} cal")
    print("\n📊 Monthly Analytics (last 30 days):")
    monthly_total = 0
    for i in range(30):
        day = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        monthly_total += calories_by_date.get(day, 0)
    print(f"Total in last 30 days: {monthly_total} cal")
    print(f"Average daily intake: {round(monthly_total/30,2)} cal")

def main():
    user = load_user_data()
    while True:
        print("\n===== Main Menu =====")
        print("1) Log a meal")
        print("2) View today's calorie log (compare with TDEE)")
        print("3) View analytics (weekly & monthly)")
        print("4) Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            log_meal(user)
        elif choice == "2":
            view_daily_log(user)
        elif choice == "3":
            view_analytics(user)
        elif choice == "4":
            print("Goodbye! Stay healthy!")
            break
        else:
            print("Invalid choice. Please try again.")
main()
