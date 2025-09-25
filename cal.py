def calculator():
    print("Simple Calculator")
    print("Operations: +  -  *  /")

    try:
        num1 = float(input("Enter the first number: "))
        op = input("Enter an operator (+, -, *, /): ")
        num2 = float(input("Enter the second number: "))

        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            if num2 == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            result = num1 / num2
        else:
            raise ValueError("Invalid operator. Please use +, -, *, or /.")

        print("Result:", result)

    except ValueError as ve:
        print("Value Error:", ve)

    except ZeroDivisionError as zde:
        print("Math Error:", zde)

    except Exception as e:
        print("An unexpected error occurred:", e)

calculator()
