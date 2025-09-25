import re 
string = 'hello 123 world 4567'
pattern = '\d+'
result = re.findall(pattern, string)
print(result)

import re 
pattern = '^a...s$'
test_string = 'abjhj'
result = re.match(pattern, test_string)
if result:
    print("Search successful")
else:
    print("Search unsuccessful")