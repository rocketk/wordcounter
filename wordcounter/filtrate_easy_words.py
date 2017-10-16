import json, ConfigParser


def filtrate(src_file="all_words_of_the_book.txt", des_file="filtered_words_of_the_book.txt", output_path="output/",
             top_rank=2000):
    words_db = read_wordcount_db_in_dict()
    new_words_list = []
    # load words from file
    total = 0
    with open(output_path + src_file, "r") as f:
        for line in f:
            word = line.split(",")[0]
            if word:
                total += 1
                if unicode(word) in words_db:
                    word_in_db = words_db[unicode(word)]
                    if word_in_db['rank'] > top_rank:
                        new_words_list.append(line)
    with open(output_path + des_file, "w") as f:
        for item in new_words_list:
            f.write(item)
    print "total words: {0}, deleted: {1}, rest: {2}".format(total, total - len(new_words_list), len(new_words_list))


def read_wordcount_db_in_dict(file="cache/wordcount_db.json"):
    with open(file, "r") as f:
        words_list = json.loads(f.read())
    words_dict = {}
    for word in words_list:
        # print word
        words_dict[word['word']] = word
    return words_dict


if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.read('config.properties')
    book_name = config.get("default", "book_name")
    output_path = config.get("default", "output_path")
    top_rank = config.getint("default", "filtrate_top_rank")
    filtrate(output_path=output_path, top_rank=top_rank)
