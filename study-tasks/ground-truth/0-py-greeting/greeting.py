def greet_user(times=3):
    count = 0
    while count < times:
        name = input("Enter your name: ").strip()
        if not name:
            print("Name is empty, please enter again.")
        else:
            print(f"Hello, {name}!")
            count += 1


if __name__ == "__main__":
    greet_user()
