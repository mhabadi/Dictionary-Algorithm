# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:27:55 2022

@author: MoAbadi
"""
import os
import pickle

class dictionary_search():
    
    def __init__(self,source):
        self.name=source
        fin=open(source,'r')
        temp_dict=list(fin)
        temp_dict.sort()
        self.database=[]
        self.detect_vector=[]
        self.len_vector=[]
        prefix_vector=[]
        fin.close()
        for index,pattern in enumerate(temp_dict):            
            pattern=pattern.strip('\n')
            leng=len(pattern)
            next_pattern=(temp_dict[index+1].strip('\n')) if index < len(temp_dict)-1 else ""
            if pattern != next_pattern[0:leng]:
                self.len_vector=set(list(self.len_vector)+[leng])
                self.database.append(pattern)
                prefix_vector.append(leng-1)
                vector=[None]*(leng)
                for i in prefix_vector:
                    vector[i]=pattern[i]
                prefix_vector=[]
                self.detect_vector.append(vector)

            elif pattern == next_pattern[0:leng]:
                prefix_vector.append(leng-1)
        self.len_vector=list(self.len_vector)
        
    def group_creation(self,qty=1):
        sub_group_file=[None]*qty
        sub_detect_vector_file=[None]*qty
        sub_group=[[None]]*qty
        sub_detect_vector=[[None]]*qty
        paths=[]
        
#        try:
        for i in range (0,qty):
                paths.append('%s_sub_%d'%(self.name,i))
                os.mkdir(paths[-1])
                sub_group_file[i]=open('%s/sub_dict_%d.txt'%(paths[-1],i),'wb')
                sub_detect_vector_file[i]=open('%s/sub_detect_vector_%d.txt'%(paths[-1],i),'wb')
                sub_group[i]=[]
                sub_detect_vector[i]=[]
            
        for i in range(0,len(self.database)):
                index=i%qty
                sub_group[index].append((self.database[i],len(sub_group[index])))
                sub_detect_vector[index].append(self.detect_vector[i])
        
        for i in range (0,qty):
                pickle.dump(sub_group[i],sub_group_file[i])
                pickle.dump(sub_detect_vector[i],sub_detect_vector_file[i])
                sub_group_file[i].close()
                sub_detect_vector_file[i].close()
        
        for i,path in enumerate(paths):
            sub_group_file[i]=open('%s/sub_dict_%d.txt'%(path,i),'rb')
            sub_detect_vector_file[i]=open('%s/sub_detect_vector_%d.txt'%(path,i),'rb')
            list1=pickle.load(sub_group_file[i])
            list2=pickle.load(sub_detect_vector_file[i])
            sub_group_file[i].close()
            sub_detect_vector_file[i].close()
            print(list1,'group_%d'%i,'\n')
            print(list2,'group_detect vector_%d'%i,'\n')
            
        
#        except:
#            print('Sub directories are already exist for %s'%self.name)        

    def dict_pointer(self,database,detection_vector,len_vector,le):
        dict_database=database
        detection_vector=detection_vector
        dict_pointers=[]
        pointer=[None]
        for length in range(le,0,-1):
            patterns=dict_database
            parent_child={}

            for pattern in patterns:
                parent=pattern[0:length-1]
                child=pattern[length-1]
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
            detect_vector_gen=(vector for vector in detect_vector)
            detect_vector=[]            
            
            for par,chil in parent_child.items():
                max_pointer=0
                for i in chil:
                    total_length=pointer[length-1][i]+chil.count(i)
                    max_pointer=total_length if total_length > max_pointer else max_pointer
                        
                temp_memory=[par]*(max_pointer)
                temp_detect_vector=[[0]*le]*max_pointer
                
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
                    temp_detect_vector[temp_pointer]=next(detect_vector_gen)

                dict_database.extend(temp_memory)
                detect_vector.extend(temp_detect_vector)
                
        return (dict_database,dict_pointers,detect_vector)

                    
                    

        
            


test=dictionary_search('test3.txt')
print(test.database)
print(test.detect_vector,'\n\n')

print(len(test.database))
print(len(test.detect_vector),'\n\n')
#print(test.len_vector)


test.group_creation(2)
#print(test.dict_pointer(5))

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


    
    
    
        
    
    

    