#!/bin/python
# The purpose of this script is to take the *machine-readable* output of UMLS 
# MetaMap and convert it to something that looks like a sentence of UMLS CUIs, 
# if possible. Ideally there would be an option in MetaMap to do this, assuming
# it is sensible.

import re
import sys
utterance_re = re.compile('^utterance\(')
phrase_re = re.compile('^phrase\(')
mappings_re = re.compile('^mappings\(')
candidates_re = re.compile('^candidates\(')
EOU_re = re.compile('^\'EOU')

# --- define in/out paths --- #
# this is a file of sentences, fed into metamap
raw_data_path = ''
# this is the metamap output. YMMV
#   created by the command:
# metamap14 -q -Q 3 --word_sense_disambiguation raw_data_path metamap_output_path
metamap_output_path = ''
# this is the processed data path, the output of this script
proc_data_path = ''

# --- open files --- #
raw_data = open(raw_data_path, 'r')
metamap_output = open(metamap_output_path, 'r')
proc_data = open(proc_data_path, 'w')

# --- the relevant and important functions --- #
def parse_phrase(line):
    """
    Takes a phrase from machine-readable format, parses its mappings, returns
    a string of mapped terms (into CUIs, when possible).
    """
    # list of words in the phrase
    phrase = re.sub('\'','',re.sub('phrase\(','', line).split(',')[0])
    # get the candidates (and most importantly, their numbers)
    candidates = metamap_output.readline()
    assert candidates_re.match(candidates)
    TotalCandidateCount = int(re.sub('candidates\(','',candidates).split(',')[0])
    # get the mappings
    mappings = metamap_output.readline()
    assert mappings_re.match(mappings)
    if TotalCandidateCount == 0:
        # there were no mappings for this phrase
        parsed_phrase = phrase + ' '
    else:
        wordmap = dict()
        # accounted for by other words
        delwords = []
        parsed_phrase = ''
        # split the mappings up into 'ev's
        split_mappings = mappings.split('ev(')
        for mapping in split_mappings[1:]:
            CUI = mapping.split(',')[1].strip('\'')
            words = re.split('[\[\]]',','.join(mapping.split(',')[4:]))[1].split(',')
            wordmap[words[0]] = CUI
            delwords += words[1:]
        # we all do things we are not proud of
        for word in phrase.split():
            try:
                parsed_phrase += wordmap[word] + ' '
            except KeyError:
                if word in delwords:
                    continue
                else:
                    parsed_phrase += word + ' '
    return parsed_phrase


def parse_utterance():
    """
    Suck in an utterance from the machine-readable format, parse its mapping
    and then return a string of mapped terms (into CUIs).
    May not be the same length as the input sentence.
    """
    phrases = ''
    line = metamap_output.readline()
    while not EOU_re.match(line):
        if phrase_re.match(line):
            parsed_phrase = parse_phrase(line)
            phrases += parsed_phrase
        elif not EOU_re.match(line):
            print line
            sys.exit('ERROR: what', line)
        line = metamap_output.readline()
    return phrases

# --- run through the file --- #
n = 0
while True:
    line = metamap_output.readline()
    if not line: break
    if utterance_re.match(line):
        # we are now in an utterance!
        parsed_utterance = parse_utterance()
        print line,
        print '====>', parsed_utterance
        proc_data.write(parsed_utterance+'\n')
        n += 1
    else:
        # not interested in this line
        continue

proc_data.close()
print '\nWrote', n, 'sentences to', proc_data_path
