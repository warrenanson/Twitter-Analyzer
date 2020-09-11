import json
import re
import sys
from collections import Counter 

def PrintResult():

    file = sys.argv[1]
    hash_tags = {}
    tags = []

    with open(file) as f:

        for line in f.readlines():

            #print(line)
            
            json_data = json.loads(line)
            if json_data['entities']['hashtags'] != '': # make sure data exists
                n = len(json_data['entities']['hashtags'])
                for i in range(0,n):
                    tag = json_data['entities']['hashtags'][i]['text']
                    tags.append(tag)

        for tag in tags:
            try:
                hash_tags[tag] = hash_tags[tag] + 1 # count
            except KeyError:
                hash_tags[tag] = 1  

    #print(hash_tags) 

    k = Counter(hash_tags) 
    top_ten = k.most_common(10) # finding top ten value of key

    with open('top_ten_output.txt','w') as f:
        for i in top_ten: 
            f.write("{} {} ".format(i[0],i[1])+'\n')
            print(i[0],' ',i[1]) 

    #for tag in hash_tags:
    #    print(tag)
                
PrintResult()