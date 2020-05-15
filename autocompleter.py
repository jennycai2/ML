import json
import pickle
import re
import string
from patricia import trie
from collections import defaultdict 
from pandas import json_normalize

DEFAULT_FILENAME = "autocompleter.pkl"


class Autocompleter:
    def __init__(self):
        pass

    def get_agent_text(self, conversation_file):
        f = open(conversation_file,) 
        data = json.load(f)  
        f.close() 

        df = json_normalize(data['Issues'], 'Messages')
        agent_only = df[(df.IsFromCustomer == False)]
        agent_text = agent_only.Text
        return agent_text.values.tolist()
        
    def process_data(self, sentences):
        phrases = []
        for i in range(len(sentences)):
            s = sentences[i].replace(u'\xa0', u' ').replace(u'\n', u' ')
            s = re.sub(' +', ' ', s) # reduce multiple spaces into one space
            phrases += re.split('(?<=[.!?]) +', s.lower()) #split with '.!?' but keep the delimiters
        return phrases

    def import_json(self, json_filename):
        agent_data = self.get_agent_text(json_filename)
        phrases = self.process_data(agent_data)
        phrase_dict = defaultdict(int)
        for a in phrases:
            phrase_dict[a] += 1
        self.agent_trie = trie(**phrase_dict)

    def not_a_duplicate(self, non_dup_str, s): # compare with a list of strings
        s = s.translate(str.maketrans('', '', string.punctuation))
        for a in non_dup_str:
            if s == a.translate(str.maketrans('', '', string.punctuation)):
                return False
        return True

    def generate_completions(self, prefix_string):
        suggestions = list(self.agent_trie.iter(prefix_string.lower())) # change to lower case
        #return suggestions[0:3]
        sugg_cnt = defaultdict(int)
        for sugg in suggestions:
            k, cnt = self.agent_trie.item(sugg)
            print(type(cnt), cnt, type(sugg_cnt[sugg]))
            sugg_cnt[sugg] += int(cnt) # get frequency cnt

        ranked_sugg_cnt = sorted(sugg_cnt.items(), key=lambda x: x[1], reverse=True)

        #get top 3 non duplicated results
        #what about result is 0, 1, 2?
        top_3 = []
        for a in ranked_sugg_cnt:
            if self.not_a_duplicate(top_3, a[0]):
                top_3.append(a[0])
                if (len(top_3) == 3):
                    print(top_3)
                    break

        sugg_without_dup = top_3
        return [r.capitalize() for r in sugg_without_dup[0:3]] # capitalize the first letter

    def save(self, filename=DEFAULT_FILENAME):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename=DEFAULT_FILENAME):
        with open(filename, "rb") as f:
            return pickle.load(f)
