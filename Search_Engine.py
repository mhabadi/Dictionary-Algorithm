# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 09:34:53 2022

@author: MoAbadi
"""
import pickle
def search_engine(detect_vector,unified_group,pointer_vector,input_string):
    detect_vector=detect_vector
    pointer_vector=pointer_vector
    unified_group=unified_group
    max_length_pattern=len(pointer_vector)
    max_length_input=len(input_string)
    for i in range(0,max_length_input):
        pointer=pointer_vector[0].get(input_string[i],None)
        #print(i,pointer,"i, pointer before while")
        commulative_pointer=pointer
        counter=1
        while (pointer != None and counter < max_length_pattern and counter < (max_length_input-i)):
            #print(counter,"counter after while")
            #print(i+counter, 'i+counter')
            pointer=pointer_vector[counter].get(input_string[i+counter],None)
            #print(counter,'  counter----',pointer,'  pointer-----',commulative_pointer,'  commulative pointer')
            if pointer != None:
                commulative_pointer += pointer
                counter +=1
        #print(commulative_pointer,'commulative while end')
        #if i==11:
            #print('i=11 and commulative_pointer=',commulative_pointer)
            #print(unified_group)
        if commulative_pointer != None:
            pattern_pointer=unified_group[commulative_pointer][1]
            #print(pattern_pointer)
            #print(i,pattern_pointer,counter,'i,pattern pointer,counter')
            if pattern_pointer != None:
               leng=len(unified_group[commulative_pointer][0])
                
               #print (unified_group[commulative_pointer][0])
               #print (input_string[i:i+leng])
               if input_string[i:i+leng] == unified_group[commulative_pointer][0]:
                    #print(input_string[i:i+counter])
                    index_child_pattern=[]
                    for index,detect_value in enumerate(detect_vector[pattern_pointer]):
                        if detect_value ==1:
                            index_child_pattern.append(index)
                    #print(index_child_pattern)
                    for indexes in index_child_pattern:
                        print (f'malacious pattern detected {unified_group[commulative_pointer][0][0:indexes+1]}')
                    

        
    

def search(database,input_string):
    input_string_file=open(input_string,'r')
    input_string=tuple(input_string_file)[0]
    path_vector_file=open(f'{database[0:-4]}_path_directories.pickle','rb')
    path_vector=pickle.load(path_vector_file)
    path_vector_file.close()
    group_qty=path_vector[0]
    for i in range (2,group_qty+1):
        sub_group_pointer_file=open(path_vector[i][1],'rb')
        sub_group_pointer=pickle.load(sub_group_pointer_file)
        sub_group_pointer_file.close()
        print(sub_group_pointer)
        unified_sub_group_file=open(path_vector[i][0],'rb')
        unified_sub_group=pickle.load(unified_sub_group_file)
        unified_sub_group_file.close()
        print(unified_sub_group)
        #for index,element in enumerate(unified_sub_group):
        #    unified_sub_group[index]=element[1]
        #print(unified_sub_group)
        
        sub_detect_vector_file=open(path_vector[i][2],'rb')
        sub_detect_vector=pickle.load(sub_detect_vector_file)
        sub_detect_vector_file.close()
        print(sub_detect_vector)
        
        print(input_string)
        search_engine(sub_detect_vector,unified_sub_group,sub_group_pointer,input_string)
search('test3.txt','test3-input.txt')