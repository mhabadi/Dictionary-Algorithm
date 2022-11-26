import time
def Brute_Force(database_name,input_string_name):
    detected_patterns={}
    with open(database_name,'r') as f:
        malacious_pattern=[line.strip('\n') for line in f]
    with open(input_string_name,'r') as g:
        input_string=g.read()
    ti=time.time()
    for pattern in malacious_pattern:
        counter=0
        while counter < len(input_string):
            detected_index=input_string.find(pattern,counter)
            if detected_index != -1:
                detected_patterns[pattern]=detected_patterns.get(pattern,[])+[detected_index]
                counter=detected_index+1
            else:
                counter+=1
    to=time.time()
    process_time=to-ti
    return (detected_patterns,process_time)