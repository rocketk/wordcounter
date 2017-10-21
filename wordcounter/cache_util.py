import codecs
import json


def tranform_file_from_list_to_dict():
    with codecs.open("cache/translations_in_list.json", 'r', "utf-8") as f:
        translations_list = json.loads(f.read())
    print "read {0} words".format(len(translations_list))
    translations_dict = {}
    for word_dict in translations_list:
        if 'rq' in word_dict:
            translations_dict[word_dict['rq']] = word_dict
    with codecs.open("cache/translations_in_dict.json", 'w', "utf-8") as f:
        f.write(json.dumps(translations_dict, indent=4, ensure_ascii=False))
    print "write {0} words".format(len(translations_dict))


def transform_file_from_dict_to_list():
    with codecs.open("cache/translations_in_dict.json", 'r', "utf-8") as f:
        translations_dict = json.loads(f.read())
    print "read {0} words".format(len(translations_dict))
    translations_list = []
    for key in translations_dict:
        translations_list.append(translations_dict[key])
    with codecs.open("cache/translations_in_list.txt", 'w', "utf-8") as f:
        for one in translations_list:
            f.write(json.dumps(one, ensure_ascii=False) + "\n")


def remove_duplicate_by_oq():
    translations_dict = {}
    lines_length = 0
    with codecs.open("cache/translations_in_list.txt", 'r', "utf-8") as f:
        for line in f:
            one_dict = json.loads(line, encoding="utf-8")
            if one_dict and 'oq' in one_dict:
                translations_dict[one_dict['oq']] = one_dict
                lines_length += 1
    with codecs.open("cache/translations_in_list.txt", 'w', "utf-8") as f:
        for key in translations_dict:
            f.write(json.dumps(translations_dict[key], ensure_ascii=False, encoding="utf-8") + "\n")
    print "before remove duplicate: ", lines_length
    print "after: ", len(translations_dict)


if __name__ == '__main__':
    remove_duplicate_by_oq()
