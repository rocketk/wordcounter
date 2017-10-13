import urllib2
import json

import re

totalWords = 0


def doFetch(rank_of_requested=0):
    words = []
    url = "http://www.wordcount.org/dbquery.php?toFind={0}&method=SEARCH%5FBY%5FINDEX".format(rank_of_requested)
    response = urllib2.urlopen(url)
    content = response.read()
    content_dict = {}
    words_count_in_response = 0  # how many words in the response
    for one in content.split("&"):
        if not one:
            continue
        split = one.split("=")  # key=value
        if not split:
            continue
        content_dict[split[0]] = split[1]
        if re.match(r"word\d+", split[0]):
            words_count_in_response += 1
    if totalWords == 0:
        global totalWords
        totalWords = int(content_dict['totalWords'])
    # rank_of_requested = content_dict['rankOfRequested']
    # if rank_of_requested!=index:
    #     raise Exception("rankOfRequested not equals index")
    for i in range(0, words_count_in_response):
        word_dict = {
            'rank': int(rank_of_requested) + i + 1,
            'word': content_dict["word" + str(i)],
            'freq': content_dict["freq" + str(i)]
        }
        words.append(word_dict)
    return words


def fetch_all():
    words_list = []
    rank_of_requested = 0
    global totalWords
    while True:
        print "fetching ", rank_of_requested
        words_list_part = doFetch(rank_of_requested=rank_of_requested)
        words_list.extend(words_list_part)
        rank_of_requested += len(words_list_part)
        if rank_of_requested >= totalWords:
            break
    return words_list


def write_to_file(words_list):
    with open("target/wordcount_db.txt", "w") as f:
        for item in words_list:
            f.write(json.dumps(item) + "\n")


if __name__ == '__main__':
    all_words_list = fetch_all()
    print "fetched successfully, ", len(all_words_list)
    write_to_file(all_words_list)