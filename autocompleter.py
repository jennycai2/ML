import json
import pickle
import re
import string
from patricia import trie
from collections import defaultdict 
from pandas import json_normalize

DEFAULT_FILENAME = "autocompleter.pkl"
NUM_OF_COMPLETIONS = 3

class Autocompleter:
    def __init__(self, agent_trie = None):
        self.agent_trie = agent_trie
        self.cache = {}

    def read_json_file(self, conversation_file):
        """ use the json module to read data from a json file """
        try:
            with open(conversation_file, 'r') as f:
                return json.load(f)
        except IOError:
            print("Failed to open file:", conversation_file)
            return None

    def data_to_agent_text(self, data):
        """ flatten json data, keep text from agents (exclude text from customers) """
        if (not data):
            return None
        df = json_normalize(data['Issues'], 'Messages')
        agent_only = df[(df.IsFromCustomer == False)]
        agent_text = agent_only.Text
        return agent_text.values.tolist()

    def text_to_sentences(self, text):
        """ preprocessing: replace no-break space, end-of-line; split text on sentence delimiters... """
        if (not text):
            return None
        sentences = []
        for i in range(len(text)):
            s = text[i].replace(u'\xa0', u' ').replace(u'\n', u' ')
            s = re.sub(' +', ' ', s).strip().lower() # reduce multiple spaces into one space
            sentences += re.split('(?<=[.!?]) +', s) #split with '.!?' but keep the delimiters
        return sentences

    def sentences_to_trie(self, sentences):
        """ store sentences to patria trie. refer to: https://pypi.org/project/patricia-trie/ """
        if (not sentences):
            return None
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
    
    def diff_more_than_punct(self, current_completions, new_completion): 
        """ compare with existing completions. The follwoing two sentences:
        How can I help you?
        How can I help you
        differ only in punctuation and are basically same (this function will return False)
        """
        new_completion = new_completion.translate(str.maketrans('', '', string.punctuation))
        for a in current_completions:
            if new_completion == a.translate(str.maketrans('', '', string.punctuation)):
                return False
        return True

    def get_top_completions(self, sorted_comp_cnt_pair):
        """ fetch the top completions which are different (not just different in punctuation) """
        top_comp = [] 
        for a in sorted_comp_cnt_pair:
            if self.diff_more_than_punct(top_comp, a[0]):
                top_comp.append(a[0])
                if (len(top_comp) == NUM_OF_COMPLETIONS):
                    return top_comp
        return top_comp

    def generate_completions(self, prefix_string):
        """ For a prefix, return top completions based on frequency cnt. Fetch from cache, trie """
        if prefix_string == None or not isinstance(prefix_string, str):
            return []
        if (not self.agent_trie):
            return []
        prefix = prefix_string.lower()
        if prefix in self.cache:  # start with checking the cache
            return self.cache[prefix] 

        completions = list(self.agent_trie.iter(prefix))

        # for each completions, what's the frequency? we display completions with the most frequency
        comp_cnt_pair = defaultdict(int)
        for comp in completions:
            cnt = self.agent_trie.value(comp)
            if isinstance(cnt, int):
                comp_cnt_pair[comp] += int(cnt) 
        sorted_comp_cnt_pair = sorted(comp_cnt_pair.items(), key=lambda x: x[1], reverse=True) #sort on freq cnt
        top_comp = self.get_top_completions(sorted_comp_cnt_pair)
        result = [r.capitalize() for r in top_comp] # capitalize the first letter
        self.cache[prefix] = result # save to cache
        return result

    def save(self, filename=DEFAULT_FILENAME):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename=DEFAULT_FILENAME):
        with open(filename, "rb") as f:
            return pickle.load(f)