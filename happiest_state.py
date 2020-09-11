import sys
import re
import json


def solve_Phrase(Phrase):

    if(len(Phrase) == 2):
        return Phrase

    Phrase[0] = Phrase[0] + '_' + Phrase[1]
    Phrase.pop(1)
    return solve_Phrase(Phrase)


def main():

    keys = []
    values = []

    sent_file = open(sys.argv[1])  # Dictionary
    tweet_file = open(sys.argv[2])  # JsonData

    line = sent_file.readline()
    while line != '':
        sep = line.strip()
        sep = re.split(r'[\s+\t]', sep)

        if(len(sep) >= 3):
            sep = solve_Phrase(sep)

        keys.append(str.lower(sep[0]))
        values.append(int(sep[1]))
        line = sent_file.readline()

    Dictionary = dict(zip(keys, values))

    # 第五題的變數
    Place_hash = {}
    To_Simply = {
        'ALASKA': 'AK',
        'ALABAMA': 'AL',
        'ARIZONA': 'AZ',
        'ARKANSAS': 'AR',
        'CALIFORNIA': 'CA',
        'COLORADO': 'CO',
        'CONNECTICUT': 'CT',
        'DELAWARE': 'DE',
        'DISTRICT OF COLUMBIA': 'DC',
        'FLORIDA': "FL",
        'GEORGIA': 'GA',
        'HAWAII': 'HI',
        'IDAHO': 'ID',
        'ILLINOIS': 'IL',
        'INDIANA': 'IN',
        'IOWA': 'IA',
        'KANSAS': 'KS',
        'KENTUCKY': 'KY',
        'LOUISIANA': 'LA'
,        'MAINE': 'ME'
,        'MARYLAND': 'MD'
,        'MASSACHUSETTS': 'MA'
,        'MICHIGAN': 'MI'
,        'MINNESOTA': 'MN'
,        'MISSISSIPPI': 'MS'
,        'MISSOURI': 'MO'
,        'MONTANA': 'MT'
,        'NEBRASKA': 'NB'
,        'NEVADA': 'NV'
,        'NEW HAMPSHIRE': 'NH'
,        'NEW JERSEY': 'NJ'
,        'NEW MEXICO': 'NM'
,        'NEW YORK': 'NY'
,        'NORTH CAROLINA': 'NC'
,        'NORTH DAKOTA': 'ND'
,        'OHIO': 'OH'
,        'OKLAHOMA': 'OK'
,        'OREGON': 'OR'
,        'PENNSYLVANIA': 'PA'
,        'PUERTO RICO': 'PR'
,        'RHODE ISLAND': 'RI'
,        'SOUTH CAROLINA': 'SC'
,        'SOUTH DAKOTA': 'SD'
,        'TENNESSEE': 'TN'
,        'TEXAS': 'TX'
,        'UTAH': 'UT'
,        'VERMONT': 'VT'
,        'VIRGINIA': 'VA'
,        'VIRGIA ISLAND': 'VI'
,        'WASHINGTON': 'WA'
,        'WEST VIRGINIA': 'WV'
,        'WISCONSIN': 'WI'
,        'WYOMING': 'WY'
,    }
    # >...

    for line in tweet_file:
        json_data = json.loads(line)

        score = 0
        simply_Done = False
        Place_key_Error = False
        if(json_data['place'] and json_data['place']['full_name']):

            if json_data['full_text'] != '':
                sep = json_data['full_text'].split(' ')

                for item in sep:

                    item = re.sub('[^a-zA-Z]', '', item)
                    if(item == ''):
                        continue

                    try:
                        score += Dictionary[str.lower(item)]
                    except Exception:
                        pass

            else:
                print('No Score')

            Place = json_data['place']['full_name'].split(',')
            if(len(Place) < 2):
                continue
            Simply = ''
            
            try : 
                Simply = To_Simply[Place[0]]
                simply_Done = True
            except KeyError:
                pass
            
            if simply_Done == False:
                Simply = re.sub('[^a-zA-Z]', '', Place[1])

            try:
                Place_hash[Simply] = Place_hash[Simply] + score
            except KeyError:
                Place_hash[Simply] = score
    
    max = -77777
    state = ''
    for key, value in Place_hash.items():
        print(key, value, max, state)
        if(max < value):
            max = value
            state = key

    print(state)
    with open('Prob_5', mode='w') as f:
        f.write(state)
    
    """
    SortPlace = sorted(Place_hash.items(), key=lambda x: x[1], reverse=True)
    i = 1
    for key, value in SortPlace:
        print('HappiestState Top {} : {} | Score : {}'.format(i, key, value))
        i = i + 1
        if(i > 10):
            break
    """
    

if __name__ == '__main__':
    main()
