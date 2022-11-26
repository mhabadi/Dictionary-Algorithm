
import re
import time
def Regular_Expression(database_name,input_string_name):
    detected_patterns={}
    
    with open(database_name,'r') as f:
        malacious_pattern=[line.strip('\n') for line in f]
    with open(input_string_name,'r') as g:
        input_string=g.read()
    
    ti=time.time()
    for pattern in malacious_pattern:
        if pattern in input_string:
            detected_patterns[pattern]=[m.start() for m in re.finditer(pattern, input_string)]
    to=time.time()
    process_time=to-ti
    return (detected_patterns,process_time)