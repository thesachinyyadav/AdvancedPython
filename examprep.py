try:
    num1 = int(input("numerator: "))
    num2 = int(input("denominator: "))
    result = num1 /num2

except ZeroDivisionError:
    print("error no zero denomiator")
except ValueError:
    print ("only numeric")
else:
    print(f"Result = {result}")

finally:
    print ("program exceution with exceptn" )