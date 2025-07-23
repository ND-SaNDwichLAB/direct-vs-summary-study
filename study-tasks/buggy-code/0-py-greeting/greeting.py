def greet_user():
    name = input("Enter your name: ").strip()
    if not name:
        print("Hello, stranger!")
    else:
        print(f"Hello, {name}!")


if __name__ == "__main__":
    greet_user()
