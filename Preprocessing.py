# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:27:55 2022

@author: MoAbadi
"""

class dictionary_search():
    
    def __init__(self,source):
        fin=open(source,'r')
        temp_dict=list(fin)
        temp_dict.sort()
        self.dict=[]
        self.len_vector=[]
        self.dict_database={}
        self.detect_vector=[]
        fin.close()
        for index,pattern in enumerate(temp_dict):            
            pattern=pattern.strip('\n')
            length=len(pattern)
            next_pattern=(temp_dict[index+1].strip('\n')) if index < len(temp_dict)-1 else ""
            if pattern != next_pattern[0:length]:
                self.len_vector=set(list(self.len_vector)+[length])
                self.dict.append(pattern)
                self.dict_database[length]=self.dict_database.get(length,[])+[len(self.dict)-1]
                if len(self.dict) > len(self.detect_vector):
                    self.detect_vector.append(("0"*(length-1))+"1")
                else:
                    self.detect_vector[-1]=self.detect_vector[-1][0:-1]+"1"
            elif pattern == next_pattern[0:length]:
                if len(self.detect_vector) <= len(self.dict):
                    self.detect_vector.append(("0"*(length-1))+"1"+"0"*(len(next_pattern)-length))
                else:
                    self.detect_vector[-1]=self.detect_vector[-1][0:-1]+"1"+"0"*(len(next_pattern)-length)

            self.len_vector=list(self.len_vector)       
                
    def Pointer_vector(self):
        self.len_vector.sort(reverse=True)
        print (self.len_vector)
        self.pointers=[{}]*self.len_vector[0]
        self.len_database={}
        
        for index,length in enumerate(self.len_vector):
            for i in range (0,index+1):
                self.len_database[length]=self.len_database.get(length,[])+(self.dict_database[self.len_vector[i]])
        
        for lengths in self.len_vector:
            for index,location in enumerate(self.len_database[lengths]):
                parent_pattern=self.dict[location][0:lengths-1]
                child_character=self.dict[location][lengths-1]
                self.pointer[lengths][child_character]=0
                pointer=0
                if (len(self.len_database[lengths])-index) >= 3:
                    parent_duplicate=0
                    for next_indexes in range(index+1,len(self.len_database[lengths])):
                        first_next_parent_pattern=self.dict[self.len_database[lengths][index+1]][0:lengths-1]
                        first_next_child=self.dict[self.len_database[lengths][index+1]][lengths-1]
                        second_next_parent_pattern=self.dict[self.len_database[lengths][index+2]][0:lengths-1]
                        second_next_child=self.dict[self.len_database[lengths][index+2]][lengths-1]
                        if parent_pattern == first_next_parent_pattern and child_character != next_child_character:
                            pointer +=1
                        if 
                    
                    if parent_pattern ==first_next_pattern:
                        parrent_duplicate += 1
                    else:
                        parrent_duplicate = 0
                                        
                    second_next_location=self.dict[self.len_database[length][index+2]]              
                    for next_location in range (index+1,len(self.len_database[lengths])):
                        next_parent_pattern=self.dict[next_location][0:lengths-1]
                        next_child_character=self.dict[next_location][lengths-1]
                        if (parent_pattern,child_character) == (next_parent_pattern,next_child_character):
                        self.synchronizer()
            
            
    
    
#    def synchronizer(self,index):
        
           
            
test=dictionary_search('test.txt')
#print(test.dict)

#for i in test.dict_database[5]:
#    print (test.dict[i])
print (test.dict)
print(test.dict_database)
#print(test.len_vector)
test.Pointer_vector()
print(test.len_database)



