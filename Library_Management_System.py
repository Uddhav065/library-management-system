from datetime import datetime, timedelta

# -----------------------------
# Data Storage
# -----------------------------

books = {}
movies = {}
users = {}
memberships = {}
issued_records = {}

# Default admin
users["admin"] = {
    "password": "admin123",
    "role": "admin"
}

# -----------------------------
# Utility Functions
# -----------------------------

def get_today():
    return datetime.now().date()


def authenticate(username, password):
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None


# -----------------------------
# Login System
# -----------------------------

def login_system():
    print("\n=== Library Management System ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    role = authenticate(username, password)

    if role:
        print("Login successful.")
        return role
    else:
        print("Invalid credentials.")
        return None


# -----------------------------
# Maintenance Module
# -----------------------------

def add_item():
    print("\n--- Add New Item ---")
    print("1. Book (default)")
    print("2. Movie")

    choice = input("Select type: ")

    if choice == "" or choice == "1":
        item_type = "book"
    elif choice == "2":
        item_type = "movie"
    else:
        print("Invalid selection.")
        return

    item_id = input("Enter ID: ").strip()
    title = input("Enter Title: ").strip()
    creator = input("Enter Author/Director: ").strip()

    if not item_id or not title or not creator:
        print("All fields are required.")
        return

    if item_type == "book":
        if item_id in books:
            print("Book ID already exists.")
            return
        books[item_id] = {
            "title": title,
            "author": creator,
            "available": True
        }
    else:
        if item_id in movies:
            print("Movie ID already exists.")
            return
        movies[item_id] = {
            "title": title,
            "director": creator,
            "available": True
        }

    print(f"{item_type.capitalize()} added successfully.")


def update_item():
    print("\n--- Update Item ---")
    print("1. Book (default)")
    print("2. Movie")

    choice = input("Select type: ")

    if choice == "" or choice == "1":
        item_type = "book"
        collection = books
        field = "author"
    elif choice == "2":
        item_type = "movie"
        collection = movies
        field = "director"
    else:
        print("Invalid selection.")
        return

    item_id = input("Enter ID to update: ").strip()

    if item_id not in collection:
        print("Item not found.")
        return

    print("Leave field empty to keep existing value.")

    new_title = input("New Title: ").strip()
    new_creator = input("New Author/Director: ").strip()

    if new_title:
        collection[item_id]["title"] = new_title
    if new_creator:
        collection[item_id][field] = new_creator

    print("Item updated successfully.")


def user_management():
    while True:
        print("\n--- User Management ---")
        print("1. Add User")
        print("2. Update User")
        print("3. Back")

        choice = input("Select option: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            update_user()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")


def add_user():
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    print("1. User (default)")
    print("2. Admin")
    role_choice = input("Select role: ")

    role = "user"
    if role_choice == "2":
        role = "admin"

    if not username or not password:
        print("Username and password required.")
        return

    if username in users:
        print("User already exists.")
        return

    users[username] = {
        "password": password,
        "role": role
    }

    print("User added successfully.")


def update_user():
    username = input("Enter Username to update: ").strip()

    if username not in users:
        print("User not found.")
        return

    new_password = input("New Password (leave empty to keep): ").strip()

    print("1. User")
    print("2. Admin")
    print("Press Enter to keep role")

    role_choice = input("Select new role: ")

    if new_password:
        users[username]["password"] = new_password

    if role_choice == "1":
        users[username]["role"] = "user"
    elif role_choice == "2":
        users[username]["role"] = "admin"

    print("User updated successfully.")


def membership_management():
    while True:
        print("\n--- Membership Management ---")
        print("1. Add Membership")
        print("2. Update Membership")
        print("3. Back")

        choice = input("Select option: ")

        if choice == "1":
            add_membership()
        elif choice == "2":
            update_membership()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")


def add_membership():
    username = input("Enter Username: ").strip()

    if username not in users:
        print("User does not exist.")
        return

    if username in memberships:
        print("Membership already exists.")
        return

    print("1. 6 Months (default)")
    print("2. 1 Year")
    print("3. 2 Years")

    choice = input("Select duration: ")

    months = 6
    if choice == "2":
        months = 12
    elif choice == "3":
        months = 24

    start = get_today()
    end = start + timedelta(days=30 * months)

    memberships[username] = {
        "start_date": start,
        "end_date": end
    }

    print("Membership added successfully.")


def update_membership():
    username = input("Enter Username: ").strip()

    if username not in memberships:
        print("Membership not found.")
        return

    print("1. 6 Months")
    print("2. 1 Year")
    print("3. 2 Years")

    choice = input("Select new duration: ")

    months = 6
    if choice == "2":
        months = 12
    elif choice == "3":
        months = 24

    start = get_today()
    end = start + timedelta(days=30 * months)

    memberships[username]["start_date"] = start
    memberships[username]["end_date"] = end

    print("Membership updated.")


def master_list_view():
    print("\n--- Books ---")
    for k, v in books.items():
        status = "Available" if v["available"] else "Issued"
        print(k, "|", v["title"], "|", status)

    print("\n--- Movies ---")
    for k, v in movies.items():
        status = "Available" if v["available"] else "Issued"
        print(k, "|", v["title"], "|", status)

    print("\n--- Users ---")
    for k, v in users.items():
        print(k, "|", v["role"])

    print("\n--- Memberships ---")
    for k, v in memberships.items():
        status = "Active" if v["end_date"] >= get_today() else "Expired"
        print(k, "|", status)


# -----------------------------
# Transactions Module
# -----------------------------

def search_available():
    print("\n--- Available Items ---")
    for k, v in books.items():
        if v["available"]:
            print("Book:", k, "-", v["title"])
    for k, v in movies.items():
        if v["available"]:
            print("Movie:", k, "-", v["title"])


def issue_item():
    username = input("Enter Username: ").strip()

    if username not in users:
        print("User not found.")
        return

    if username not in memberships:
        print("User has no membership.")
        return

    if memberships[username]["end_date"] < get_today():
        print("Membership expired.")
        return

    # Limit 3 items per user
    count = sum(1 for r in issued_records.values() if r["username"] == username)
    if count >= 3:
        print("User cannot issue more than 3 items.")
        return

    item_id = input("Enter Item ID: ").strip()

    if item_id in books:
        collection = books
        item_type = "book"
    elif item_id in movies:
        collection = movies
        item_type = "movie"
    else:
        print("Item not found.")
        return

    if not collection[item_id]["available"]:
        print("Item already issued.")
        return

    issue_date = get_today()
    return_date = issue_date + timedelta(days=15)

    issued_records[item_id] = {
        "username": username,
        "issue_date": issue_date,
        "return_date": return_date,
        "item_type": item_type
    }

    collection[item_id]["available"] = False
    print("Item issued successfully.")


def return_item():
    item_id = input("Enter Item ID: ").strip()

    if item_id not in issued_records:
        print("Item not issued.")
        return

    record = issued_records[item_id]
    today_date = get_today()
    fine = 0

    if today_date > record["return_date"]:
        days = (today_date - record["return_date"]).days
        fine = days * 10

    print("Fine Amount:", fine)

    if fine > 0:
        paid = input("Fine paid? (yes/no): ").strip().lower()
        if paid != "yes":
            print("Return cancelled.")
            return

    if record["item_type"] == "book":
        books[item_id]["available"] = True
    else:
        movies[item_id]["available"] = True

    del issued_records[item_id]
    print("Item returned successfully.")


# -----------------------------
# Reports Module
# -----------------------------

def issued_report():
    print("\n--- Issued Items ---")
    for k, v in issued_records.items():
        print(k, "|", v["username"], "|", v["return_date"])


def overdue_report():
    print("\n--- Overdue Items ---")
    today_date = get_today()
    for k, v in issued_records.items():
        if today_date > v["return_date"]:
            print(k, "|", v["username"])


def membership_report():
    print("\n--- Membership Report ---")
    for k, v in memberships.items():
        status = "Active" if v["end_date"] >= get_today() else "Expired"
        print(k, "|", status)


# -----------------------------
# Navigation
# -----------------------------

def maintenance_menu():
    while True:
        print("\n1. Add Item")
        print("2. Update Item")
        print("3. User Management")
        print("4. Membership Management")
        print("5. Master List")
        print("6. Back")

        choice = input("Select: ")

        if choice == "1":
            add_item()
        elif choice == "2":
            update_item()
        elif choice == "3":
            user_management()
        elif choice == "4":
            membership_management()
        elif choice == "5":
            master_list_view()
        elif choice == "6":
            break


def transactions_menu():
    while True:
        print("\n1. Search")
        print("2. Issue")
        print("3. Return")
        print("4. Back")

        choice = input("Select: ")

        if choice == "1":
            search_available()
        elif choice == "2":
            issue_item()
        elif choice == "3":
            return_item()
        elif choice == "4":
            break


def reports_menu():
    while True:
        print("\n1. Issued Report")
        print("2. Overdue Report")
        print("3. Membership Report")
        print("4. Back")

        choice = input("Select: ")

        if choice == "1":
            issued_report()
        elif choice == "2":
            overdue_report()
        elif choice == "3":
            membership_report()
        elif choice == "4":
            break


def admin_home():
    while True:
        print("\n--- Admin Home ---")
        print("1. Maintenance")
        print("2. Transactions")
        print("3. Reports")
        print("4. Logout")

        choice = input("Select: ")

        if choice == "1":
            maintenance_menu()
        elif choice == "2":
            transactions_menu()
        elif choice == "3":
            reports_menu()
        elif choice == "4":
            break


def user_home():
    while True:
        print("\n--- User Home ---")
        print("1. Transactions")
        print("2. Reports")
        print("3. Logout")

        choice = input("Select: ")

        if choice == "1":
            transactions_menu()
        elif choice == "2":
            reports_menu()
        elif choice == "3":
            break


# -----------------------------
# Main
# -----------------------------

def main():
    role = login_system()

    if role == "admin":
        admin_home()
    elif role == "user":
        user_home()


if __name__ == "__main__":
    main()
