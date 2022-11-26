# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:27:55 2022

@author: MoAbadi
"""
import os
import pickle
import copy
import logging
logging.basicConfig(filename='Debug.log',filemode='w',force=True,level=logging.DEBUG)

class Dictionary_search():
    
    def __init__(self,source):
        '''source is the input file of malacious patterns. The source file 
        is processed for inital sort and creating detect_vector in order to
        remove duplicate pattern where a pattern is the prefix
        of other. The detect vector is a list of values corrosppodning to each 
        pattern in the dictionary and consists of 0,1 equal to the length of value
        with 0 means as no mtach and 1 means as a match. Eg: ['001001'] correspond to pattern['abcdef'] 
        means that 'abc'and 'abcdef' are malcious patterns '''
        self.name=source
        fin=open(source,'r')
        temp_dict=list(fin)
        temp_dict.sort()
        self.database=[None]
        prefix_vector=[]
        fin.close()
        for index,pattern in enumerate(temp_dict):            
            pattern=pattern.strip('\n')
            leng=len(pattern)
            next_pattern=(temp_dict[index+1].strip('\n')) if index < len(temp_dict)-1 else ""
            previous_pattern=self.database[-1]
            if pattern != next_pattern[0:leng]:
                prefix_vector.append(leng-1)
                vector=[0]*(leng)
                for i in prefix_vector:
                    vector[i]=1
                self.database.append((pattern,vector))
                if previous_pattern != None:
                    min_len=min(leng,len(previous_pattern[0]))
                    for prefix_len in range (1,min_len+1):
                        if self.database[-1][0][0:prefix_len]==previous_pattern[0][0:prefix_len]:
                            self.database[-1][1][0:prefix_len]=previous_pattern[1][0:prefix_len]
                prefix_vector=[]

            elif pattern == next_pattern[0:leng]:
                prefix_vector.append(leng-1)
        self.database.pop(0)

        
    def group_creation(self,qty=1):
        ''' Segregate patterns into the user defined number of groups (default number=1), each group will be
        written into a subfolder with the correspodning detect vector, the path to each 
        folder will be return to be used with other functions'''
        sub_group_file=[None]*qty
        sub_group=[[None]]*qty
        self.path_sub_group=[None]*qty
        
        paths=[]
#        try:
        for i in range (0,qty):
                paths.append('%s_sub_%d'%(self.name[0:-4],i))
                if not os.path.exists(paths[-1]):
                    os.mkdir(paths[-1])
                self.path_sub_group[i]='%s/sub_group_%d.pickle'%(paths[-1],i)
                sub_group_file[i]=open(self.path_sub_group[i],'wb')
                sub_group[i]=[]
            
        #print(paths)
        for i in range(0,len(self.database)):
                index=i%qty
              
                sub_group[index].append((self.database[i]))
 
        for i in range (0,qty):
                pickle.dump(sub_group[i],sub_group_file[i])
                sub_group_file[i].close()

        return (self.path_sub_group,paths)
        
#        except:
#            print('Sub directories are already exist for %s'%self.name)        

    def dict_pointer(self,sub_group):
        '''implement dictionary algorithm over the given sub_group in order to
        unify the pointer table for each character at each level, return the new dictionary
        along with the pointer table'''
        #print(sub_group)
        dict_database_length={}
        len_vector=[]
        dict_database=[]
        #print(sub_group,'\n\n')
        for pattern in sub_group:
            pat_len=len(pattern[0])
            len_vector=set(list(len_vector)+[pat_len])
            dict_database_length[pat_len]=dict_database_length.get(pat_len,[])+[pattern]
        #print(dict_database_length,'---------------------------\n')
        len_vector=list(len_vector)
        len_vector.sort(reverse=True)
        #print(len_vector)
        dict_pointer=[None]*(max(len_vector))
        #print(dict_pointer,'\n\n')
        #print(len_vector)
        for n,le in enumerate(len_vector):
            #print(le,'le')
            next_len=len_vector[n+1] if n != (len(len_vector)-1) else 0
            #print(le)
            dict_database.extend(dict_database_length[le])
            #print(dict_database,'\n\n')
            #dict_database.sort(key=lambda dict_database : dict_database[0])
            #print(le,dict_database,'le and database\n')  
            for length in range(le,next_len,-1):
                patterns=dict_database
                #max_len_child=0
                parent_child_rest={}
                child_vector=[]
                #print(length)
                for pattern in patterns:
                    parent=pattern[0][0:length-1]
                    child=pattern[0][length-1]
                    rest=pattern[0][length:]
                    detect_vector=pattern[1]
                    child_vector.append(child)
                    #detect_vector=self.detect_vector[pattern_index] if pattern_index != None else ([0]*len(parent))
                    #print(parent,'----',child,'----',rest,'----,',pattern_index)
                    #parent_child[parent]=parent_child.get(parent,'')+child
                    if parent not in parent_child_rest:
                        parent_child_rest[parent]=[[child],[rest],[detect_vector]]
                    else:
                        parent_child_rest[parent][0].extend([child])
                        parent_child_rest[parent][1].extend([rest])
                        parent_child_rest[parent][2].extend([detect_vector])
                    #print(child_parent_rest)
                    #if max_len_child < len(parent_child[parent]):
                    #    max_len_child=max_len_child                    
                child_vector=list(set(child_vector))
                child_vector.sort()
                level_pointer={}
                for child in child_vector:
                    change_flag=False
                    for parent,child_rest in parent_child_rest.items():
                        child_vector=child_rest[0]
                        if child in child_vector:
                            current_pointer=child_vector.index(child)
                            if child not in level_pointer:
                                level_pointer[child]=current_pointer
                            else:
                                if current_pointer > level_pointer[child]:
                                    change_flag=True
                                    level_pointer[child]=current_pointer
                                elif current_pointer < level_pointer[child]:
                                    change_flag=True
                                else:
                                    pass
                    if change_flag == True:
                        for parent,child_rest in parent_child_rest.items():
                            child_vector=child_rest[0]
                            if child in child_vector:
                                current_position=child_vector.index(child)
                                offset=level_pointer[child]-current_position
                                if offset < 0 :
                                    raise ValueError("Error- Something is wrong")
                                elif offset > 0:
                                    if parent_child_rest[parent][2][current_position] != None:
                                        if 1 in parent_child_rest[parent][2][current_position][0:length]:
                                            current_position_vector=parent_child_rest[parent][2][current_position][0:length]
                                            parent_child_rest[parent][2][current_position][0:length]=[0]*length
                                        else:
                                            current_position_vector=None
                                    else:
                                        current_position_vector=None
                                    for counter in range(offset):
                                        parent_child_rest[parent][0].insert(current_position,'')
                                        parent_child_rest[parent][1].insert(current_position,'')
                                        if counter == offset-1:
                                            parent_child_rest[parent][2].insert(current_position,current_position_vector)
                                        else:
                                            parent_child_rest[parent][2].insert(current_position,None)
                                else:
                                    pass
                dict_pointer[length-1]=copy.deepcopy(level_pointer)    
                dict_database=[]
                for parent,child_rest in parent_child_rest.items():
                    for index,child in enumerate(child_rest[0]):
                        rest=child_rest[1][index]
                        detect_vector=child_rest[2][index]
                        pattern_reconstruct=(parent+child+rest,detect_vector)
                        dict_database.append(pattern_reconstruct)  
        return(dict_database,dict_pointer)
                            
                    
                        
                        
                        
                    
                    
                    
                    

                    

        
            



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
    test=Dictionary_search(source)
    path_sub_group,root_path=test.group_creation(qty)  
    
               
    path_directories=[qty]
    for index,group in enumerate (root_path):
        #print(index,group)
        path_directories.append((f'{group}/unified_sub_group_{index}.pickle',f'{group}/sub_group_pointer{index}.pickle'))
        unified_sub_group_file=open(path_directories[-1][0],'wb')
        sub_group_pointer_file=open(path_directories[-1][1],'wb')
        sub_group_file=open(path_sub_group[index],'rb')
        sub_group=pickle.load(sub_group_file)
        unified_sub_group,sub_group_pointer=test.dict_pointer(sub_group)
        print(unified_sub_group,'\n\n')
        print(sub_group_pointer)
        pickle.dump(unified_sub_group,unified_sub_group_file)
        pickle.dump(sub_group_pointer,sub_group_pointer_file)
        unified_sub_group_file.close()
        sub_group_pointer_file.close()
        sub_group_file.close()
    
    #print(path_directories)
    path_directories_file=open(f'{source[0:-4]}_path_directories.pickle','wb')
    pickle.dump(path_directories,path_directories_file)
    path_directories_file.close()
    

        
        
        
#    x=open(path[0][0],'rb')
#    y=open(path[1][0],'rb')
#    list1=pickle.load(x)
#    list2=pickle.load(y)
#    print(list1)
#    x.close()
#    y.close()
#    print(test.dict_pointer(list1,list2))
    
preprocessing('test5.txt',1)
    
    
    
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


    
    
    
        
    
    

    