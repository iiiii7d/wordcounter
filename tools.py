import difflib
import math
import re
import json
import time

def ms_to_time(ms):
    s = math.floor(ms / 1000)
    ms = round(ms % 1000, 2)
    m = math.floor(s / 60)
    s = s % 60
    h = math.floor(m / 60)
    m = m % 60
    d = math.floor(h / 24)
    h = h % 24
    res = ""
    if d != 0:
        res = res + str(d) + "d "
    if h != 0:
        res = res + str(h) + "h "
    if m != 0:
        res = res + str(m) + "min "
    if s != 0:
        res = res + str(s) + "s "
    if ms != 0:
        res = res + str(ms) + "ms "
    return res.strip()

def dedent(text):
    return re.sub('\n ', '\n', re.sub(' +', ' ', text))

def get_word_timing(word):
    with open("data/times.json", 'r+') as f:
        data = json.load(f)
        if word in data.keys(): return tuple(data[word])
        else: return None

def update_word_timing(word, id_):
    with open("data/times.json", 'r+') as f:
        data = json.load(f)
        data[word] = [int(time.time()), id_]
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

def tracked_add(id_, word, count):
    with open("data/tracked_words.json", 'r+') as f:
        data = json.load(f)
        if str(id_) not in data[word].keys(): data[word][str(id_)] = 0
        data[word][str(id_)] += count
        update_word_timing(word, id_)
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

def tracked_get_words():
    with open("data/tracked_words.json", 'r+') as f:
        data = json.load(f)
    return list(data.keys())

def tracked_user_stats(id_):
    res = {}
    with open("data/tracked_words.json", 'r+') as f:
        data = json.load(f)
        for word, counts in data.items():
            if str(id_) in counts.keys():
                res[word] = counts[str(id_)]
    return res

def tracked_word_stats(word):
    with open("data/tracked_words.json", 'r+') as f:
        data = json.load(f)
        if word in data.keys(): return data[word]
        else: return None

def tracked_add_word(word):
    with open("data/tracked_words.json", 'r+') as f:
        data = json.load(f)
        if word not in data.keys(): data[word] = {}
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

def tracked_remove_word(word):
    with open("data/tracked_words.json", 'r+') as f:
        data = json.load(f)
        if word in data.keys(): del data[word]
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

async def fullname_from_id(id_, client):
    user = await client.fetch_user(id_)
    return user.name+"#"+user.discriminator

def fullname_from_member(member):
    return member.name+"#"+member.discriminator

def scan_content_for_tracker(id_, text):
    text = text.lower()
    words = tracked_get_words()
    react = False
    for word in words:
        if count := text.count(word) > 0:
            tracked_add(id_, word, count)
            react = True

        def chunk(l, n):
            for i in range(0, len(l)):
                yield ' '.join(l[i:i + n])

        for text_word in chunk(text.split(), word.count(' ')+1):
            if (difflib.SequenceMatcher(None, text_word, word).ratio() > 0.75 or
               difflib.SequenceMatcher(None, word, text_word).ratio() > 0.75) and \
               text_word != word:
                tracked_add(id_, word, 1)
                react = True
    return react