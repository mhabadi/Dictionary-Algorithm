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
        #self.len_vector=[]
        prefix_vector=[]
        fin.close()
        for index,pattern in enumerate(temp_dict):            
            pattern=pattern.strip('\n')
            leng=len(pattern)
            next_pattern=(temp_dict[index+1].strip('\n')) if index < len(temp_dict)-1 else ""
            if pattern != next_pattern[0:leng]:
                #self.len_vector=set(list(self.len_vector)+[leng])
                self.database.append(pattern)
                prefix_vector.append(leng-1)
                vector=[None]*(leng)
                for i in prefix_vector:
                    vector[i]=pattern[i]
                prefix_vector=[]
                self.detect_vector.append(vector)

            elif pattern == next_pattern[0:leng]:
                prefix_vector.append(leng-1)
        #self.len_vector=list(self.len_vector)
        
    def group_creation(self,qty=1):
        sub_group_file=[None]*qty
        sub_detect_vector_file=[None]*qty
        #sub_len_vector_file=[None]*qty
        sub_group=[[None]]*qty
        sub_detect_vector=[[None]]*qty
        #sub_len_vector=[[None]]*qty
        self.path_sub_group=[None]*qty
        self.path_sub_detect_vector=[None]*qty
        #self.path_sub_len_vector=[None]*qty
        
        paths=[]
#        try:
        for i in range (0,qty):
                paths.append('%s_sub_%d'%(self.name[0:-4],i))
                if not os.path.exists(paths[-1]):
                    os.mkdir(paths[-1])
                self.path_sub_group[i]='%s/sub_group_%d.txt'%(paths[-1],i)
                self.path_sub_detect_vector[i]='%s/sub_detect_vector_%d.txt'%(paths[-1],i)
                #self.path_sub_len_vector[i]='%s/sub_len_vector_%d.txt'%(paths[-1],i)
                sub_group_file[i]=open(self.path_sub_group[i],'wb')
                sub_detect_vector_file[i]=open(self.path_sub_detect_vector[i],'wb')
                #sub_len_vector_file[i]=open(self.path_sub_len_vector[i],'wb')
                sub_group[i]=[]
                sub_detect_vector[i]=[]
                #sub_len_vector[i]=[]
            
        print(paths)
        for i in range(0,len(self.database)):
                index=i%qty
                
                sub_group[index].append((self.database[i],len(sub_group[index])))
                sub_detect_vector[index].append(self.detect_vector[i])
               # sub_len_vector[index]=set(list(sub_len_vector[index])+[len(self.database[i])])
              
        for i in range (0,qty):
                pickle.dump(sub_group[i],sub_group_file[i])
                pickle.dump(sub_detect_vector[i],sub_detect_vector_file[i])
                #pickle.dump(list(sub_len_vector[i]),sub_len_vector_file[i])
                sub_group_file[i].close()
                sub_detect_vector_file[i].close()
                #sub_len_vector_file[i].close()
        
        return (self.path_sub_group,self.path_sub_detect_vector,paths)
        
#        except:
#            print('Sub directories are already exist for %s'%self.name)        

    def dict_pointer(self,sub_group,detect_vector):
        dict_database_length={}
        detection_vector=detect_vector
        len_vector=[]
        dict_database=[]
        print(sub_group,'\n\n')
        for pattern in sub_group:
            pat_len=len(pattern[0])
            len_vector=set(list(len_vector)+[pat_len])
            dict_database_length[pat_len]=dict_database_length.get(pat_len,[])+[pattern]
        print(dict_database_length,'\n\n')
        len_vector=list(len_vector)
        len_vector.sort(reverse=True)
        dict_pointers=[]
        pointer=[None]*(max(len_vector))
        #print(len_vector,'\n\n')
        
        for le in len_vector:
            #print(le)
            dict_database.extend(dict_database_length[le])
            #print(dict_database,'\n\n')
            dict_database.sort(key=lambda dict_database : dict_database[0])
            #print(dict_database,'\n\n')
            
            for length in range(le,0,-1):
                patterns=dict_database
                
                parent_child={}

                for pattern in patterns:
                    parent=pattern[0][0:length-1]
                    child=pattern[0][length-1]
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
                        
                    temp_memory=[(par,None)]*(max_pointer)
                
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

                    
                    

        
            



#print(test.database)
#print(test.detect_vector,'\n\n')

#print(len(test.database))
#print(len(test.detect_vector),'\n\n')
#print(test.len_vector)

#print(test.dict_pointer(5))

#for i in test.dict_database[5]:
#    print (test.dict[i])
#print(test.dict_database)
#print(test.dict_database.items())
#print(test.len_vector)
import os

def preprocessing(source,qty=1):
    test=dictionary_search(source)
    path=test.group_creation(2)
    
    print(path[0][0])
    x=open(path[0][0],'rb')
    y=open(path[1][0],'rb')
    list1=pickle.load(x)
    list2=pickle.load(y)
    print(list1)
    x.close()
    y.close()
    print(test.dict_pointer(list1,list2))
    
preprocessing('test3.txt')
    
    
    
#        for  path_sub_group,path_detect_vector,path_len_vector in zip(self.path_sub_group,self.path_sub_detect_vector):
#            x=open(path_sub_group,'rb')
#            y=open(path_detect_vector,'rb')
#            #z=open(path_len_vector,'rb')
#            list1=pickle.load(x)
#            list2=pickle.load(y)
            #list3=pickle.load(z)
#            x.close()
#            y.close()
#            #z.close()
#            print(list1,'group_%d'%i,'\n')
#            print(list2,'group_detect vector_%d'%i,'\n')
#            #print(list3,'len_vector_%d \n'%i)


    
    
    
        
    
    

    