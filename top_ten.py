import json
import re
import sys

def PrintResult():

    file = sys.argv[1]
    hash_tags = {}

    with open(file) as f:

        for line in f.readlines():

            #print(line)
            
            json_data = json.loads(line)
            if json_data['entities']['hashtags'] != '':
                tags = json_data['entities']['hashtags']['text']

                for tag in tags:
                    try:
                        hash_tags[tag] = hash_tags[tag] + 1
                    except KeyError:
                        hash_tags[tag] = 1  

                 
    for tag in hash_tags:
        print(tag)
                
PrintResult()
