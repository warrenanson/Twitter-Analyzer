l= []
import json
with open('data.json') as f:
    studentDict = json.load(f)
    
    print(studentDict['entities']['hashtags'])

