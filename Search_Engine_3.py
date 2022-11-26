# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 09:34:53 2022

@author: MoAbadi
"""
import time
import pickle
import logging
logging.basicConfig(filename='Detected_Pattern.log',filemode='w',force=True)
detected_patterns={}
def search_engine(unified_group,pointer_vector,input_string):
    global detected_patterns
    pointer_vector=pointer_vector
    unified_group=unified_group
    max_length_pattern=len(pointer_vector)
    max_length_input=len(input_string)
    for i in range(0,max_length_input):
        pointer=0
        commulative_pointer=0
        #print(i,pointer,"i, pointer before while")
        counter=0
        #print(i,counter,'i and counter')
        while (pointer != None and counter < max_length_pattern and counter < (max_length_input-i) and commulative_pointer < len(unified_group)):
            #print(i,counter,'i and counter')
            pointer=pointer_vector[counter].get(input_string[i+counter],None)
            #print(pointer,'pointer')
            if pointer != None:
                commulative_pointer += pointer
                if commulative_pointer < len(unified_group):
                #print(unified_group[commulative_pointer])
                #print(i)
                    leng=len(unified_group[commulative_pointer][0])
                    min_value=min(counter,leng)
                    if input_string[i:i+min_value] == unified_group[commulative_pointer][0][0:min_value]:
                        vector=unified_group[commulative_pointer][1]
                        if vector != None:
                            if len(vector) > counter:
                                if vector[counter] == 1:
                                    detected_pattern=unified_group[commulative_pointer][0][0:counter+1]
                                    #logging.critical(f'malacious pattern detected {unified_group[commulative_pointer][0][0:counter+1]}')
                                    detected_patterns[detected_pattern]=list(set(detected_patterns.get(detected_pattern,[])+[i]))
                    else:
                        pointer = None    
            #print(counter,'  counter----',pointer,'  pointer-----',commulative_pointer,'  commulative pointer')
                    counter +=1
    return(detected_patterns)

def search(database,input_string):
    input_string_file=open(input_string,'r')
    input_string=tuple(input_string_file)[0]
    path_vector_file=open(f'{database[0:-4]}_path_directories.pickle','rb')
    path_vector=pickle.load(path_vector_file)
    path_vector_file.close()
    group_qty=path_vector[0]
    for i in range (1,group_qty+1):
        sub_group_pointer_file=open(path_vector[i][1],'rb')
        sub_group_pointer=pickle.load(sub_group_pointer_file)
        sub_group_pointer_file.close()
        #print(sub_group_pointer)
        unified_sub_group_file=open(path_vector[i][0],'rb')
        unified_sub_group=pickle.load(unified_sub_group_file)
        unified_sub_group_file.close()
        #print(unified_sub_group)
        ti=time.time()
        search_engine(unified_sub_group,sub_group_pointer,input_string)
        to=time.time()
        process_time=to-ti
    for detected in detected_patterns:
        detected_patterns[detected].sort()
    return(detected_patterns,process_time)
    logging.shutdown()

if __name__ == '__main__':
    search('test5.txt','test5-input.txt')

