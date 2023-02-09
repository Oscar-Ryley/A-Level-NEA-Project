from general_functions import open_file, mergesort
from string import punctuation

def find_frequency(words: list):
    """Function: find_frequency
    @params
    words: list of all words from an extract

    Returns a frequency dictionary created by iterating through a list of words.
    If the word already exists in the dictionary, its value is added to.
    If it doesn't, a new entry is added to the dictionary.
    """
    frequency = {}
    for word in words:
        if word.lower() in frequency:
            frequency[word.lower()] += 1
        else:
            frequency[word.lower()] = 1
    return frequency

def create_frequency_dictionary(file: str):
    """Function: create_frequency_dictionary
    @params
    file: file name for the text extract input

    Returns a frequency dictionary given an extract of text.
    This is the main frequency dictionary function.
    """
    lines = open_file(file)
    full_text = "\n".join(lines)
    full_text = full_text.translate(str.maketrans("", "", punctuation))
    words_list = full_text.split()
    freq_dict = find_frequency(words_list)
    freq_values = mergesort(list(freq_dict.values())) #to get the dictionary in order to find the most frequent words
    temp_dict = {}
    for i in freq_values:
        for j in freq_dict.keys():
            if freq_dict[j] == i:
                temp_dict[j] = freq_dict[j]
    freq_dict = temp_dict
    return freq_dict

def create_frequency_list(file: str):
    """Function: create_frequency_list
    @params
    frequency_dictionary: a frequency dictionary (as created by the function create_frequency_dictionary)

    Returns a frequency list created using a frequency dictionary produced using the create_frequency_dictionary function.
    """
    frequency_dictionary = create_frequency_dictionary(file)
    common_nonwords = open_file("Data/nonwords.txt")
    frequency_list = []
    i = -1
    try:
        while True:
            i += 1
            if list(frequency_dictionary.keys())[i] not in common_nonwords:
                frequency_list.append([list(frequency_dictionary.values())[i], list(frequency_dictionary.keys())[i]])    
            max_length = int(len(frequency_dictionary)*0.025)
            if max_length > 40:
                max_length = 40
            if max_length < 10:
                max_length = 10
            if len(frequency_list) == max_length:
                break

        for i in frequency_list:
            for j in frequency_list:
                if str(i[1]) == str(j[1])+"s":
                    if j[0] > i[0]:
                        j[0] += int(i[0])
                        frequency_list.remove(i)
                    else:
                        i[0] += int(j[0])
                        frequency_list.remove(j)
    except:
        frequency_list = ["No Summary Available"]
    frequency_list = mergesort(frequency_list)
    return frequency_list

def find_nouns(freq_list: list):
    """Function: find_nouns
    @params
    freq_list: a frequency list (as created by the function create_frequency_list)

    Returns a list of all of the nouns from a frequency list.
    """
    nouns = []
    nouns_list = open_file("Data/nouns.txt")
    for i in freq_list:
        if i[1] in nouns_list:
            nouns.append(i)
    return nouns

def list_to_summary(slist: list):
    """Function: list_to_summary
    @params
    slist: an inputted frequency list

    Returns a formulaic text summary given a frequency list.
    """
    if len(slist) <= 1:
        return slist[0]
    summary = "Word Frequency: " + str(slist[0][1]) + " (with "+ str(slist[0][0]) + " instances)"
    for i in slist:
        if i == slist[0]:
            pass
        else:
            summary = summary + ", " + str(i[1]) + " (" + str(i[0]) + ")"
    return summary + "."
