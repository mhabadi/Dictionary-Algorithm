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
        
        for key,value in self.database.items():
            self.database[key].sort()
        
        #print(self.dict_database,'\n')
        
    def dict_pointer(self,le):
        dict_database=self.database[le] 
        dict_pointers=[]
        pointer=[None]*le
        for length in range(le,0,-1):
            patterns=dict_database
            parent_child={}
            for pattern in patterns:
                parent=pattern[1:length]
                child=pattern[length]
                parent_child[parent]=parent_child.get(parent,'')+child
                current_pointer=parent_child[parent].index(child)
                if pointer[length-1]==None:
                   pointer[length-1]={child:current_pointer}
                else:
                   if child not in pointer[length-1]:
                      pointer[length-1][child]=current_pointer
                   elif current_pointer > pointer[length-1][child]:
                      pointer[length-1][child]= current_pointer

            dict_database=[]
            dict_pointers=pointer
            temp_pattern_gen=(pattern for pattern in patterns)
            
            for par,chil in parent_child.items():
                max_pointer=0
                for i in chil:
                    total_length=pointer[length-1][i]+chil.count(i)
                    max_pointer=total_length if total_length > max_pointer else max_pointer
                        
                temp_memory=['0'+par]*(max_pointer)
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
                   
                    temp_memory[temp_pointer]=next(temp_pattern_gen)

                dict_database.extend(temp_memory)
                
        return (dict_database,dict_pointers)

                    
                    

        
            


test=dictionary_search('word.txt')
#print(test.dict)

#for i in test.dict_database[5]:
#    print (test.dict[i])
#print(test.dict_database)
#print(test.dict_database.items())
#print(test.len_vector)
import os

def classification(source,qty=1):
    fin=open(source,'r')
    fout=[None]*qty
    paths=[]
    try:
        
        for i in range (0,qty):
            paths.append('%s_sub_%d'%(source,i))
            os.mkdir(paths[-1])
            fout[i]=open('%s/dict_group_%d.txt'%(paths[-1],i),'w')
        
        counter=0
        for line in fin:
            index=counter%qty
            fout[index].write(line)
            counter +=1

        for i in range (0,qty):
            fout[i].close()
    except:
        print('Sub directories are already exist for %s'%source)
#classification('word.txt',3)
    
    
    
        
    
    

    