""" Tests to validate that the autocompleter functions correctly.
    We are evaluating how you write unit tests, so please demonstrate your ability at writing
    good tests.  Feel free to add more tests to validate your solution. """

import autocompleter
import time
import json
import pytest
from random import randrange
import numpy as np

DEFAULT_JSON_FILE = "tiny_sample.txt"
NUM_OF_SAMPLE_COMPLETIONS = 3 # how many sample prefixes and completions to generate
PREFIX_MAX_LENGTH = 10
DEFAULT_PREFIXES_COMPLETIONS_FILE = "prefixes_and_completions.txt"
IDEAL_RESPONSE_TIME_IN_MS = 50
NUM_OF_REQUESTS = 100

def test_generate_completions():
    auto_comp = autocompleter.Autocompleter()
    auto_comp.import_json("sample_conversations.json")
  
    print("Test each of the methods") # run "pytest -s" to see it
    # Write a tiny sample of conversations to a file then test read_json_file method
    conversations = {"NumTextMessages":8,"Issues":[\
        {"IssueId":1,"CompanyGroupId":1,"Messages":[\
            {"IsFromCustomer":True,"Text":"Hi! Can you help me find out where my package is?"},
            {"IsFromCustomer":False,"Text":"Sure. What's your order number?"}]},
        {"IssueId":2,"CompanyGroupId":1,"Messages":[\
            {"IsFromCustomer":True,"Text":"My battery exploded!"},
            {"IsFromCustomer":False,"Text":"Sorry about that. Have you taken care of it to avoid hazzard?"},
            {"IsFromCustomer":True,"Text":"Now it's safe"},
            {"IsFromCustomer":False,"Text":"Thank you. What's your account number"}]},
        {"IssueId":4,"CompanyGroupId":1,"Messages":[\
            {"IsFromCustomer":True,"Text":"I'm interested in upgrading my plan to Prime."},
            {"IsFromCustomer":False,"Text":"I can help with that. What's your account number?"}]} \
        ]}

    with open(DEFAULT_JSON_FILE, 'w') as f:
        json.dump(conversations, f)

    print("Test read_json_file")
    data = auto_comp.read_json_file(DEFAULT_JSON_FILE)
    assert len(data) == 2

    print("Test data_to_agent_text")
    agent_text = auto_comp.data_to_agent_text(data) 
    assert len(agent_text) == 4

    print("Test text_to_sentences")
    sentences = auto_comp.text_to_sentences(agent_text) 
    assert len(sentences) == 8

    print("Test sentences_to_trie")
    trie = auto_comp.sentences_to_trie(sentences) 
    assert len(trie) == 8
    assert trie["What's your account number?".lower()] == 1
    # The following should raise a KeyError exception
    with pytest.raises(Exception):
        trie["What's your hobby?".lower()]

    print("Test diff_more_than_punct")
    current_completions = ["What's your account number?", "What's your order number?"]
    completion1 = "What's your account number"
    assert auto_comp.diff_more_than_punct(current_completions, completion1) == False
    completion2 = "What's the product number?"
    assert auto_comp.diff_more_than_punct(current_completions, completion2) == True

    print("Test get_top_completions")
    comp_cnt_pair = [("What's your order numer", 10), ("What's your account number?", 5), 
        ("What's your phone number?", 3), ("What's your address?", 1)]
    for i in range(4):
        sorted_comp_cnt_pair = comp_cnt_pair[0:i]
        assert len(auto_comp.get_top_completions(sorted_comp_cnt_pair)) == \
            min(i, autocompleter.NUM_OF_COMPLETIONS)

    print("Test several simple cases (with different chat history data, their completions may be None)")
    assert len(auto_comp.generate_completions('how ca')) <= len(["How can we be of assistance to you?",\
        "How can we help you?","How can i help you?"])
    assert len(auto_comp.generate_completions('what is y')) <= len(["What is your account number?",\
        "What is your order number?","What is your phone number?"])
    assert len(auto_comp.generate_completions('when w')) <= \
        len(["When was the last time you changed your password?","When will it suite you?",\
        "When will you like to return home?"])

    print("Test corner cases, their completions are less important as long as there is no error")
    corner_case_prefix = ['', 'w', 'xyz', '!', '.', '?', ',', ':', '1', '0', 'o', '/', 'w1', \
        'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq']
    for p in corner_case_prefix:
        assert len(auto_comp.generate_completions(p)) <= 3
    
    print("For each sentence, generate a prefix of random length, do we get at least one completion?")
    data = auto_comp.read_json_file("sample_conversations.json")
    print("length of data", len(data))
    agent_text = auto_comp.data_to_agent_text(data)
    print("length of agent_text", len(agent_text))
    sentences = auto_comp.text_to_sentences(agent_text)
    print("length of sentences", len(sentences))
    
    shuffled_indices = np.random.permutation(len(sentences))
    indices = shuffled_indices[:NUM_OF_REQUESTS] # get a portion of the random indices
    t0 = time.time()
    for idx in indices:
        num_of_chars = randrange(PREFIX_MAX_LENGTH)
        prefix = sentences[idx][0:num_of_chars]
        completions = auto_comp.generate_completions(prefix)
        assert len(completions) >= 1
        # Check one completion, is it longer than or equal to the prefix?
        assert len(completions[0]) >= len(prefix)
    t1 = time.time()
    
    print("Test response time")
    interval = t1 - t0
    time_per_request = interval / NUM_OF_REQUESTS
    print("t0, t1, interval, NUM_OF_REQUESTS, time_per_request", \
        t0, t1, interval, NUM_OF_REQUESTS, time_per_request) 
    print("\nAverage response time in ms:", time_per_request * 1000) 
    # It would be nice if Autocomplete response time is under 50ms
    assert time_per_request * 1000 < IDEAL_RESPONSE_TIME_IN_MS

    print("\nGenerate some sample completions and save to file:", DEFAULT_PREFIXES_COMPLETIONS_FILE)
    num_of_sentences = len(sentences)
    prefix_comp_dict = {}
    for i in range(NUM_OF_SAMPLE_COMPLETIONS):
        idx = randrange(num_of_sentences) # randomly fetch a sentence
        num_of_chars = randrange(PREFIX_MAX_LENGTH) # randomly choose prefix length
        prefix = sentences[idx][0:num_of_chars]
        prefix_comp_dict[prefix] = auto_comp.generate_completions(prefix)
        print("\n", i, "PREFIX:", prefix, "\nCOMPLETIONS:", prefix_comp_dict[prefix])
    with open(DEFAULT_PREFIXES_COMPLETIONS_FILE, 'w') as f:
        json.dump(prefix_comp_dict, f)