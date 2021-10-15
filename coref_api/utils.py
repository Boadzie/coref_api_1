pronoun_list = ["he", "she", "it", "they", "them", "him", "her", "his", "hers", "its", "we", "us"]

# Given an index eg: 8 and a list ['Scientists ', 'know ', 'many ', 'things ', 'about ', 'the ', 'Sun', '. ', 'They ', 'know ', 'how ', 'old ', 'it ', 'is', '. ', 'The ', 'Sun ', 'is ', 'more ', 'than ', '4½ ', 'billion ', 'years ', 'old', '. ', 'It ', 'is ', 'also ', 'a ', 'star', '. ', 'They ', 'also ', 'know ', 'the ', 'Sun', '’s ', 'size', '.']
# Retrieve the sentence corresponding to that index as a list. Eg: ['They ', 'know ', 'how ', 'old ', 'it ', 'is', '. ']
def get_sentence_for_index(index, resolved_list):
    end_of_sentence_punctuation = [".", "!", "?"]
    beginning_index = index
    ending_index = index
    while beginning_index >= 0:
        val = resolved_list[beginning_index].strip()
        if val in end_of_sentence_punctuation:
            break
        else:
            beginning_index = beginning_index - 1
    while ending_index <= (len(resolved_list) - 1):
        val = resolved_list[ending_index].strip()
        if val in end_of_sentence_punctuation:
            break
        else:
            ending_index = ending_index + 1
    return resolved_list[beginning_index + 1 : ending_index + 1], beginning_index + 1


def get_resolved(doc, clusters):
    """ Return a list of utterrances text where the coref are resolved to the most representative mention"""
    resolved = list(tok.text_with_ws for tok in doc)
    questions = []
    for cluster in clusters:
        for coref in cluster:
            coref_text = coref.text.lower()
            cluster_main_text = cluster.main.text.lower()
            if len(coref_text.split()) == 1 and coref_text != cluster_main_text and coref_text in pronoun_list:
                get_sentence, start_index = get_sentence_for_index(coref.start, resolved)
                get_sentence_string = "".join(get_sentence).lower()
                cluster_main_string = " ".join(cluster_main_text.strip().split())
                if cluster_main_string not in get_sentence_string:
                    resolved[coref.start] = cluster.main.text + doc[coref.end - 1].whitespace_
                    if start_index == coref.start:
                        resolved[coref.start] = resolved[coref.start].capitalize()
                    final_sentence = "".join(get_sentence)
                    # Leave out very short sentences to frame questions.
                    if len(final_sentence) > 20:
                        questions.append([final_sentence, coref.text, resolved[coref.start]])

    return "".join(resolved), questions

