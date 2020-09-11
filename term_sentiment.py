import sys
import re
import json

keys = []
values = []
all_term = []
all_term_value = {}
score_list = []

def solve_Phrase(Phrase):

    if(len(Phrase) == 2):
        return Phrase

    Phrase[0] = Phrase[0] + '_' + Phrase[1]
    Phrase.pop(1)
    return solve_Phrase(Phrase)

def main():
    
    sent_file = open(sys.argv[1]) #Dictionary
    tweet_file = open(sys.argv[2]) #JsonData

    line = sent_file.readline()
    while line != '':
        sep = line.strip()
        sep = re.split(r'[\s+\t]', sep)
        
        if(len(sep) >= 3):
            sep = solve_Phrase(sep)

        keys.append(str.lower(sep[0]))
        values.append(int(sep[1]))
        line = sent_file.readline()

    Dictionary = dict(zip(keys,values))

    for line in tweet_file:
        json_data = json.loads(line)

        if json_data['full_text'] != '':
            sep = json_data['full_text'].split(' ')

            score = 0.0
            count = 0
            for item in sep:
                
                item = re.sub('[^a-zA-Z0-9-\'\"\.?!~]', '', item)
                if(item == ''):
                    continue               

                try:
                    score += Dictionary[str.lower(item)]
                    #print('Match: '+ item)
                except Exception:
                    pass

                if item not in keys:
                    all_term.append(item)
                    count += 1

            for i in range(0,count):
                score_list.append(score)
            #print(score)

        else:
            print('No Score')
    
#    print(score_list)
    index = 0

    for term in all_term:
        try:
            all_term_value[term] = all_term_value[term] + score_list[index]
        except KeyError:
            all_term_value[term] = score_list[index]

        index += 1
                        
            

    #print(all_term)
    with open('term_sentiment_output.txt','w') as f: # output to json
        for term in all_term_value:
            f.write('{} {}'.format(term, all_term_value[term])+'\n')
            print('{} {}'.format(term, all_term_value[term]))

    

if __name__ == '__main__':
    main()
