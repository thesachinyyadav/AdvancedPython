def calculator():
    try:
        num1 = int(input('Enter numerator: '))
        num2 = int(input('Enter denominator: '))

        # Menu for operations
        print("\nChoose Operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            result = num1 + num2
            print(f"Result: {num1} + {num2} = {result}")

        elif choice == '2':
            result = num1 - num2
            print(f"Result: {num1} - {num2} = {result}")

        elif choice == '3':
            result = num1 * num2
            print(f"Result: {num1} * {num2} = {result}")

        elif choice == '4':
            try:
                result = num1 / num2
                print(f"Result: {num1} / {num2} = {result}")
            except ZeroDivisionError:
                print("Error: Division by zero is not allowed.")

        else:
            print("Invalid choice! Please select 1, 2, 3 or 4.")

    except ValueError:
        print("Invalid input! Please enter numeric values only.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the calculator
calculator()
