# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:27:55 2022

@author: MoAbadi
"""
import os
import pickle
import copy

class dictionary_search():
    
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
                vector=[0]*(leng)
                for i in prefix_vector:
                    vector[i]=1
                prefix_vector=[]
                self.detect_vector.append(vector)

            elif pattern == next_pattern[0:leng]:
                prefix_vector.append(leng-1)
        #self.len_vector=list(self.len_vector)
        
    def group_creation(self,qty=1):
        ''' Segregate patterns into the user defined number of groups (default number=1), each group will be
        written into a subfolder with the correspodning detect vector, the path to each 
        folder will be return to be used with other functions'''
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
                self.path_sub_group[i]='%s/sub_group_%d.pickle'%(paths[-1],i)
                self.path_sub_detect_vector[i]='%s/sub_detect_vector_%d.pickle'%(paths[-1],i)
                #self.path_sub_len_vector[i]='%s/sub_len_vector_%d.txt'%(paths[-1],i)
                sub_group_file[i]=open(self.path_sub_group[i],'wb')
                sub_detect_vector_file[i]=open(self.path_sub_detect_vector[i],'wb')
                #sub_len_vector_file[i]=open(self.path_sub_len_vector[i],'wb')
                sub_group[i]=[]
                sub_detect_vector[i]=[]
                #sub_len_vector[i]=[]
            
        #print(paths)
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

    def dict_pointer(self,sub_group):
        '''implement dictionary algorithm over the given sub_group in order to
        unify the pointer table for each character at each level, return the new dictionary
        along with the pointer table'''
        dict_database_length={}
        #detection_vector=detect_vector
        len_vector=[]
        dict_database=[]
        #print(sub_group,'\n\n')
        for pattern in sub_group:
            pat_len=len(pattern[0])
            len_vector=set(list(len_vector)+[pat_len])
            dict_database_length[pat_len]=dict_database_length.get(pat_len,[])+[pattern]
        print(dict_database_length,'\n')
        len_vector=list(len_vector)
        len_vector.sort(reverse=True)
        #print(len_vector)
        dict_pointer=[None]*(max(len_vector))
        #print(len_vector,'\n\n')
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
                child_parent_rest={}
                #print(length)
                for pattern in patterns:
            
                    #print (pattern)
                    parent=pattern[0][0:length-1]
                    child=pattern[0][length-1]
                    rest=pattern[0][length:]
                    pattern_index=pattern[1]
                    #print(parent,'----',child,'----',rest,'----,',pattern_index)
                    #parent_child[parent]=parent_child.get(parent,'')+child
                    if child not in child_parent_rest:
                        child_parent_rest[child]=[[parent],[rest],[pattern_index]]
                    else:
                        child_parent_rest[child][0].extend([parent])
                        child_parent_rest[child][1].extend([rest])
                        child_parent_rest[child][2].extend([pattern_index])
                    #print(child_parent_rest)
                    #if max_len_child < len(parent_child[parent]):
                    #    max_len_child=max_len_child                    
                    
                    
                #reverse_parent_child={}
                #parent_childs_rests={}
                level_pointer={}
                dict_database=[]
                temp_parent_childs_rests={}
                #print(child_parent_rest)
                for child,parents_rests in child_parent_rest.items():
                    #print(length,child,'length and child')
                    parents=parents_rests[0]
                    rests=parents_rests[1]
                    pat_index=parents_rests[2]
                    max_pointer=0
                    temp_pointer=0
                    for index,parent in enumerate(parents):
                        #print(temp_parent_childs_rests)
                        if parent not in temp_parent_childs_rests:
                            temp_parent_childs_rests[parent]=[[child],[rests[index]],[pat_index[index]]]
                        else:
                            temp_parent_childs_rests[parent][0].extend([child])
                            temp_parent_childs_rests[parent][1].extend([rests[index]])
                            temp_parent_childs_rests[parent][2].extend([pat_index[index]])
                        #print(temp_parent_childs_rests)
                        temp_pointer=temp_parent_childs_rests[parent][0].index(child)
                        #print(temp_pointer,'temp_pointer')
                        max_pointer=temp_pointer if temp_pointer >max_pointer else max_pointer

                    
                    level_pointer[child]=max_pointer
                    for index,parent in enumerate(parents):
                        
                        offset=max_pointer-temp_parent_childs_rests[parent][0].index(child)
                        if offset <0:
                            print("trap- something is wrong")
                        for i in range (offset):
                            dict_database.append((parent,None))
                        pattern_reconstruct=(parent+child+rests[index],pat_index[index])
                        dict_database.append(pattern_reconstruct)
                        
                dict_pointer[length-1]=copy.deepcopy(level_pointer)
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
    test=dictionary_search(source)
    path_sub_group,path_detect_vector,root_path=test.group_creation(qty)  
    
               
    path_directories=[qty]
    for index,group in enumerate (root_path):
        #print(index,group)
        path_directories.append((f'{group}/unified_sub_group_{index}.pickle',f'{group}/sub_group_pointer{index}.pickle',path_detect_vector[index]))
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
    
preprocessing('test3.txt',2)
    
    
    
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


    
    
    
        
    
    

    