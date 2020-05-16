import json
import pickle
import re
import string
from patricia import trie
from collections import defaultdict 
from pandas import json_normalize

DEFAULT_FILENAME = "autocompleter.pkl"

class Autocompleter:
    def __init__(self, agent_trie = None):
        self.agent_trie = agent_trie
        self.cache = {}

    def read_json_file(self, conversation_file):
        """ read data from json file """
        f = open(conversation_file,) 
        data = json.load(f)  
        f.close() 
        return data

    def data_to_agent_text(self, data):
        """ flatten json data, keep text from agents (exclude text from customers) """
        df = json_normalize(data['Issues'], 'Messages')
        agent_only = df[(df.IsFromCustomer == False)]
        agent_text = agent_only.Text
        return agent_text.values.tolist()

    def text_to_sentences(self, text):
        """ preprocessing: replace no-break space, end-of-line; split text on sentence delimiters... """
        sentences = []
        for i in range(len(text)):
            s = text[i].replace(u'\xa0', u' ').replace(u'\n', u' ')
            s = re.sub(' +', ' ', s).strip().lower() # reduce multiple spaces into one space
            sentences += re.split('(?<=[.!?]) +', s) #split with '.!?' but keep the delimiters
        return sentences

    def sentences_to_trie(self, sentences):
        """ store sentences to patria trie. refer to: https://pypi.org/project/patricia-trie/ """
        sentence_dict = defaultdict(int)
        for a in sentences:
            sentence_dict[a] += 1
        return trie(**sentence_dict) 

    def import_json(self, json_filename):
        """ from json file to patricia trie data structure in memory """
        data = self.read_json_file(json_filename)
        agent_text = self.data_to_agent_text(data)
        sentences = self.text_to_sentences(agent_text)
        self.agent_trie = self.sentences_to_trie(sentences)
    
    def diff_more_than_punct(self, current_suggestions, new_suggestion): 
        """ compare with existing suggestions. The follwoing two sentences:
        How can I help you?
        How can I help you
        differ only in punctuation and are basically same (this function will return False)
        """
        new_suggestion = new_suggestion.translate(str.maketrans('', '', string.punctuation))
        for a in current_suggestions:
            if new_suggestion == a.translate(str.maketrans('', '', string.punctuation)):
                return False
        return True

    def get_top_suggestions(self, num_of_sugg, ranked_sugg_cnt):
        """ fetch the top suggestions which are different (not just different in punctuation) """
        top_sugg = [] 
        for a in ranked_sugg_cnt:
            if self.diff_more_than_punct(top_sugg, a[0]):
                top_sugg.append(a[0])
                if (len(top_sugg) == num_of_sugg):
                    return top_sugg
        return top_sugg

    def generate_completions(self, prefix_string):
        """ For a prefix, return top 3 suggestions based on frequency cnt. Fetch from cache, trie """
        if prefix_string == None or not isinstance(prefix_string, str):
            return []
        prefix = prefix_string.lower()
        if prefix in self.cache:  # start with checking the cache
            return self.cache[prefix] 

        suggestions = list(self.agent_trie.iter(prefix))

        # for each suggestion, what's the frequency? we display suggestions with the most frequency
        sugg_cnt = defaultdict(int)
        for sugg in suggestions:
            cnt = self.agent_trie.value(sugg)
            if isinstance(cnt, int):
                sugg_cnt[sugg] += int(cnt) 
        ranked_sugg_cnt = sorted(sugg_cnt.items(), key=lambda x: x[1], reverse=True) #sort on freq cnt
        top_sugg = self.get_top_suggestions(3, ranked_sugg_cnt)
        result = [r.capitalize() for r in top_sugg] # capitalize the first letter
        self.cache[prefix] = result # save to cache
        return result

    def save(self, filename=DEFAULT_FILENAME):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename=DEFAULT_FILENAME):
        with open(filename, "rb") as f:
            return pickle.load(f)