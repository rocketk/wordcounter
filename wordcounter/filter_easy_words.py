import json


def filtrate(src_file="output/all_words_of_the_book.txt", des_file="output/filtered_words_of_the_book.txt"):
    words_db = read_wordcount_db_in_dict()
    new_words_list = []
    # load words from file
    with open(src_file, "r") as f:
        for line in f:
            word = line.split(",")[0]
            if words_db.has_key(unicode(word)):
                word_in_db = words_db[unicode(word)]
                if word_in_db['rank'] > 2000:
                    new_words_list.append(line)
    with open(des_file, "w") as f:
        for item in new_words_list:
            f.write(item)


def read_wordcount_db_in_dict(file="output/wordcount_db.txt"):
    with open(file, "r") as f:
        words_list = json.loads(f.read())
    words_dict = {}
    for word in words_list:
        # print word
        words_dict[word['word']] = word
    return words_dict


if __name__ == '__main__':
    filtrate()
