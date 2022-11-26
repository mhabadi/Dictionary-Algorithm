import logging
import re
from Search_Engine_3 import search
import time
#logging.basicConfig(filename='Detected_Pattern_Test.log',filemode='w',force=True)
detected_patterns={}
database_name='test5.txt'
input_string_name='test5-input.txt'

ti_1=time.time()
with open(database_name,'r') as f:
    malacious_pattern=[line.strip('\n') for line in f]
with open(input_string_name,'r') as g:
    input_string=g.read()
for pattern in malacious_pattern:
    if pattern in input_string:
        detected_patterns[pattern]=[m.start() for m in re.finditer(pattern, input_string)]
to_1=time.time()

result=search(database_name,input_string_name)
to_2=time.time()

process_time_python=to_1-ti_1
process_time_my_algorithm=to_2-to_1

print(process_time_python)

print(process_time_my_algorithm)

if result == detected_patterns:
    print ("Validation Done")
