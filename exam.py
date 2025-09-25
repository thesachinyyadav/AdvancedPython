import re
text = "christ university is located in bangalore!"
match = re.search(r"hema",text)
if match:
    print("match found!")
if not match:
    print ("match not found!")
num = re.findall(r"\d+" , text)
print(num)
if not num:
    print("num not found!")