# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:27:55 2022

@author: MoAbadi
"""

class dictionary_search():
    
    def __init__(self,source):
        fin=open(source,'r')
        self.database={}
        for line in fin:
            pattern=line.strip("\n")
            self.database[len(pattern)]=self.database.get(len(pattern),[])+['1'+pattern]            
        fin.close()
        
        for key,value in self.dict_database.items():
            self.database[key].sort()
        
        #print(self.dict_database,'\n')
        
    def dict_pointer(self,length):
        
        self.dict_database={}
        for items in length:
            self.dict_database[items]=self.database[items]
        
        self.dict_pointers={}
        for key,value in self.dict_database.items():
            
            #print(key,value,'key,value\n')
            pointer=[None]*key
            #print(pointer[4],'pointer#######')
            for length in range(key,1,-1):
                #print(length,'length')
                patterns=self.dict_database[key]
                parent_child={}
                for pattern in patterns:
                    #print(pattern,'pattern')
                    parent=pattern[1:length]
                    #print(parent,'parent')
                    child=pattern[length]
                    #print(child,'child')
                    parent_child[parent]=parent_child.get(parent,'')+child
                    #print(parent_child,'parent_child $$$$$$$$$$$$$$$$')
                    current_pointer=parent_child[parent].index(child)
                    #if length ==2:
                    #    print(current_pointer,'current_pointer'
                    #print(pointer,'first condition')
                    if pointer[length-1]==None:
                        pointer[length-1]={child:current_pointer}
                    else:
                        if child not in pointer[length-1]:
                            pointer[length-1][child]=current_pointer
                        elif current_pointer > pointer[length-1][child]:
                            pointer[length-1][child]= current_pointer
                        #print(pointer,'second condition')
                #if length ==4:
                #    print(parent_child,'parent_child')
                #    print(pointer,'pointer###################')
                self.dict_database[key]=[]
                self.dict_pointers[key]=pointer
                temp_pattern_gen=(pattern for pattern in patterns)
                for par,chil in parent_child.items():
                    #print(par,'-----------',chil)
                    max_pointer=0
                    for i in chil:
                        total_length=pointer[length-1][i]+chil.count(i)
                        max_pointer=total_length if total_length > max_pointer else max_pointer
                        

                 
                    #print(max_pointer,'max_pointer')
                    temp_memory=['0'+par]*(max_pointer)
                    #if length ==4:
                    #    print(max_pointer,temp_memory,'temp memoryyyyyyyyyyyyyyy')
                    #    print (chil,'childssssssssssss')
                    offset=0
                    
                    for j,ch in enumerate(chil):
                        if j < 1:
                            temp_pointer=pointer[length-1][ch]
                        else:
                            if ch==chil[j-1]:
                                offset += 1
                            else:
                                offset=0
                            temp_pointer=pointer[length-1][ch]+offset
                        #if length==4:
                         #   print(max_pointer,temp_pointer,'MAXXXXXXXXXXXXXXXX')
                        temp_memory[temp_pointer]=next(temp_pattern_gen)
                    #if length ==4:
                     #   print(temp_memory,'tempppppppppppppppppppppppppppppppp')
                    self.dict_database[key].extend(temp_memory)
                
                    #print(self.dict_database,'dict******************************************************')
                    
                    

        
            


test=dictionary_search('word.txt')
#print(test.dict)

#for i in test.dict_database[5]:
#    print (test.dict[i])
#print(test.dict_database)
#print(test.dict_database.items())
#print(test.len_vector)

test.dict_pointer()
print(test.dict_database[5])
print(test.dict_pointers[5])

    