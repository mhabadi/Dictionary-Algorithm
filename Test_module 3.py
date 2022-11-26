from Brute_Force import Brute_Force
from Regular_Expression import Regular_Expression
from Search_Engine_3 import search as My_algorithm

#logging.basicConfig(filename='Detected_Pattern_Test.log',filemode='w',force=True)

database_name='test5.txt'
input_string_name='test5-input-2.txt'

RE_result=Regular_Expression(database_name,input_string_name)
#BR_result=Brute_Force(database_name,input_string_name)
My_result=My_algorithm(database_name,input_string_name)
#print(RE_result[0])
#print(My_result[0])
if RE_result[0] ==My_result[0]:
    print(RE_result[1])
    #print(BR_result[1])
    print(My_result[1])
    print ("Validation Done")
