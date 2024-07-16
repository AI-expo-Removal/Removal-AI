def masking(timeline):
    n = 0
    for i in timeline:
        f = open('./v2/rmbd/badlist.txt', 'r', encoding='UTF8')
        bad_list = f.read().split(', ')
        data = i['text'].split()

        new_text = []
        for inp in data:
            result = [p for p in inp]
            for bad in bad_list:
                if bad in inp:
                    idx = inp.find(bad)
                    for i in range(idx, len(bad)+idx):
                        result[i] = '*'
            new_text.append(''.join(result))
        timeline[n]['text'] = (' '.join(new_text))
    return timeline