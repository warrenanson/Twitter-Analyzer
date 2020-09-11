
import sys
import threading
import re
import json
import time

Dictionary = {}

_sema = threading.Semaphore(1)
_wrote_count = 1
_thread_Queue = []
_All_OK = False

_timesema = threading.Semaphore(1)
_gb_time = 0
_timeout = False

def solve_Phrase(Phrase):

    if(len(Phrase) == 2):
        return Phrase

    Phrase[0] = Phrase[0] + '_' + Phrase[1]
    Phrase.pop(1)
    return solve_Phrase(Phrase)

def thread_Manager(fp):
    
    global _All_OK, _thread_Queue, _sema

    t = None
    while True:
        
        if(len(_thread_Queue) > 0):
            with _sema:
                t = _thread_Queue.pop(0)
                _sema.release()
        
            t.start()
            t.join()
        
        if _All_OK:
            fp.close()
            break

def write_Answer(Lines, fp): #寫答案
    
    global _wrote_count, Dictionary

    for line in Lines:
        
        score = 0
        for item in line:
            
            item = re.sub('[^a-zA-Z]', '', item)
            if(item == ''):
                continue

            #print(item)

            try:
                score += Dictionary[str.lower(item)]
                #print('Match: '+ item)
            except Exception:
                pass

        #print("mood score : %d" %score)
        print('Tweet {} = {}'.format(_wrote_count, score))
        fp.write('Tweet {} = {}\n'.format(_wrote_count, score))
        _wrote_count += 1

def generate_Dict(fp): #生成字典集
    
    global Dictionary
    
    keys = []
    values = []

    for line in fp:

        sep = line.strip()
        sep = re.split(r'[\s+\t]', sep)
        
        if(len(sep) > 2):
            sep = solve_Phrase(sep)

        keys.append(str.lower(sep[0]))
        values.append(int(sep[1]))

    Dictionary = dict(zip(keys,values)) 

def timer():
    
    global _gb_time, _timeout, _timesema

    while True:
        
        time.sleep(1)
        #print (_timeout)

        with _timesema:
            _gb_time = _gb_time + 1
            if(_gb_time > 1):
                _timeout = True
            _timesema.release()

        if _All_OK:
            break


def generate_Output(fp): #生成輸出

    global _timeout, _sema, _thread_Queue, _timesema, _All_OK

    Output_File = open('Prob_2', mode='a')
    OutputList = []
    threading.Thread(target = thread_Manager, args = [Output_File]).start()
    threading.Thread(target = timer).start()

    #讀檔
    for line in fp:
        
        json_data = json.loads(line)
        #print(line)
        if(len(OutputList) >= 5000 or _timeout == True):
            with _sema:
                _thread_Queue.append(threading.Thread(target = write_Answer, args=[OutputList, Output_File]))
                _sema.release()
                

        if json_data['full_text'] != '':
            
            sep = json_data['full_text'].split(' ')
            OutputList.append(sep)

        else:
            print('No Score')

        with _timesema:
            _gb_time = 0
            _timesema.release()

    _All_OK = True
    fp.close()

def main():
    
    sent_file = open(sys.argv[1]) #AFINN-111
    tweet_file = open(sys.argv[2]) #JsonData

    generate_Dict(sent_file)
    generate_Output(tweet_file)

if __name__ == '__main__':
    main()

