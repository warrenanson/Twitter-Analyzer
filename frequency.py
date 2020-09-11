
import json
import re
import sys



def PrintResult():

    total = 0   # num of occurrences of all terms in all tweets
    d = {} # dict of term  
    file = sys.argv[1]
    
    with open(file) as f:

        for line in f.readlines():

            #print(line)
            
            json_data = json.loads(line)
            if json_data['full_text'] != '':    # make sure data is exist
                sep = json_data['full_text'].split(' ')

                
                for word in sep:

                    word = re.sub(r'[^a-zA-Z0-9\'\"-\.?!~]', '', word) # filter non-english words

                    if(word == ''):
                        continue

                    '''
                    if not(word.encode( 'UTF-8' ).isalpha()):
                        continue
                    #print(word)
                    '''

                    try:
                        d[word] = d[word] + 1   # count 
                    except KeyError:
                        d[word] = 1
                        
                total += len(sep)         
                #sum = 0
        print(total)

    with open('frequency_output.txt','w') as f: # output to json
        for word in d:
            f.write("{} {} ".format(word, d[word]/total)+'\n')
            print(word,' ',d[word]/total)

PrintResult()
