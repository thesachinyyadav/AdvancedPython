import numpy as np

arr = np.array([str(i) for i in range(1, 51)])

print("Array of strings:")
print(arr)

num_arr = arr.astype(int)

print("\nArithmetic Operations on Array:")
print("Addition (+5):", num_arr + 5)
print("Subtraction (-3):", num_arr - 3)
print("Multiplication (*2):", num_arr * 2)
print("Division (/2):", num_arr / 2)

print("\nShape of array:", arr.shape)
print("Type of array:", arr.dtype)
