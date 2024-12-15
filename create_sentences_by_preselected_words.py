import random
import json
import re
from nltk.corpus import stopwords

import unicodedata

def remove_accents(palavra):  
  nfkd_form = unicodedata.normalize('NFKD', palavra)
  return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def kebab_case(string):
  return "-".join(word.lower() for word in string.split(" "))

def type_sentence(i):
    if i == 0:
        return 'val'
    elif i == -1:
        return 'val_x'
    else:
        return 'train'

def create_obj(noun, verb, adj, adv, index = 0, suffix = '', regular=True):

    duration_noun = noun
    duration_verb = verb
    duration_adj = adj
    duration_adv = adv

    d_noun = duration_noun.get('duration')
    d_verb = duration_verb.get('duration')
    d_adj = duration_adj.get('duration')
    d_adv = duration_adv.get('duration')
    
    duration = sum([d_noun, d_verb, d_adj, d_adv])
    full_sentence = remove_accents(noun.get('sign') + ' ' + adj.get('sign') + ' ' + verb.get('sign') + ' ' + adv.get('sign'))
    english_sentence = remove_accents(noun.get('english') + ' ' + adj.get('english') + ' ' + verb.get('english') + ' ' + adv.get('english'))

    return {
        "sentence": full_sentence,
        "sentence_english": english_sentence,
        "signs_words": [noun.get('sign'), adj.get('sign'), verb.get('sign'), adv.get('sign')],
        "signs_words_english": [noun.get('english'), adj.get('english'), verb.get('english'), adv.get('english')],
        "video_name": kebab_case(full_sentence) + suffix,
        "interpreter": index,
        "type_sentence": "n_adj_v_adv",
        "signs_times": [
            d_noun,
            d_noun + d_adj,
            d_noun + d_adj + d_verb,
            d_noun + d_adj + d_verb + d_adv,
        ],
        "signs_videos": [
            duration_noun.get('video'),
            duration_adj.get('video'),
            duration_verb.get('video'),
            duration_adv.get('video')
        ],
        "type": type_sentence(index) if regular else 'val_x',
        "begin":0,
        "end": duration,
        "duration": duration
    }


with open("./videos_words_times_final_2.json", "r", encoding="utf-8") as file:
    dados_sinais = json.load(file)


words = {}

palavras_selecionadas = open("./lista-palavras/50-selected-words.txt", "r", encoding="utf-8")
for palavra in palavras_selecionadas:
    p = remove_accents(palavra.lower().replace('\n', ''))    
    for i in range(3):
        palavra_selecionada, tipo = p.split(':')                
        key = str(i)+'-'+palavra_selecionada
        dados_sinais[key]['sign'] = dados_sinais[key]['word']
        dados_sinais[key]['english'] = dados_sinais[key]['word_english']
        dados_sinais[key]['classes'] = [tipo]
        words[key] = dados_sinais[key]

        for a in ['-upsample', '-downsample', '-horizontal-flip', '-horizontal-flip-downsample', '-horizontal-flip-upsample']:
            dados_sinais[key+a]['sign'] = dados_sinais[key+a]['word']
            dados_sinais[key+a]['english'] = dados_sinais[key+a]['word_english']
            dados_sinais[key+a]['classes'] = ['z']
            words[key+a] = dados_sinais[key+a]
    #print(p)
palavras_selecionadas.close()

sentences = []
mySentence = set()
created = set()

nouns0 = list(set(map(lambda x: x.split('-', 1)[1], filter(lambda x: "n" in words[x]['classes'], words))))
verbs0 = list(set(map(lambda x: x.split('-', 1)[1], filter(lambda x: "v" in words[x]['classes'], words))))
adj0 = list(set(map(lambda x: x.split('-', 1)[1], filter(lambda x: "a" in words[x]['classes'], words))))
adv0 = list(set(map(lambda x: x.split('-', 1)[1], filter(lambda x: "r" in words[x]['classes'], words))))


total_sentences = 955900
j = 0

while j <= total_sentences:
    key_noun = random.choice(nouns0)
    key_verb = random.choice(verbs0)
    key_adj  = random.choice(adj0)
    key_adv  = random.choice(adv0)
    
    keys =  [key_noun, key_verb, key_adj, key_adv]

    #random.shuffle(keys)        

    for i in range(3):

        noun = words[str(i) + '-' + keys[0]]
        verb = words[str(i) + '-' + keys[1]]
        adj  = words[str(i) + '-' + keys[2]]
        adv  = words[str(i) + '-' + keys[3]]

        regular = create_obj(
            noun=noun,
            verb=verb,
            adj=adj,
            adv=adv,
            index=i
        )

        full_sentence = regular.get('sentence')

        if full_sentence in created:
            break

        sentences.append(regular)       

        agumentations_types = ['-upsample', '-downsample', '-horizontal-flip', '-horizontal-flip-downsample', '-horizontal-flip-upsample']

        agumentations = random.sample(agumentations_types, 2)

        if i == 1 or i == 2:

            for x in agumentations:
                noun = words[str(i) + '-' + keys[0] + x]
                verb = words[str(i) + '-' + keys[1] + x]
                adj  = words[str(i) + '-' + keys[2]  + x]
                adv  = words[str(i) + '-' + keys[3]  + x]

                flip = create_obj(
                    noun=noun,
                    verb=verb,
                    adj=adj,
                    adv=adv,
                    index=i,
                    suffix=x
                )

                sentences.append(flip)
        
        
    j += 1
    created.add(full_sentence)


frases_validacao = open("./lista-palavras/76-frases.txt", "r", encoding="utf-8")
my_stop_words = stopwords.words('portuguese')
my_stop_words.remove('muito')
my_stop_words.remove('mais')
my_stop_words.remove('também')
my_stop_words.remove('não')

pattern = re.compile(r'\b(' + r'|'.join(my_stop_words) + r')\b\s*')

for frase in frases_validacao:    
    f = pattern.sub('', frase)
    f = remove_accents(f).lower().replace("\n", "").split()
    
    for i in range(0,1):    
        noun = words[str(i) + '-' + f[0]]
        adj  = words[str(i) + '-' + f[1]]
        verb = words[str(i) + '-' + f[2]]
        adv  = words[str(i) + '-' + f[3]]        

        regular = create_obj(
            noun=noun,
            verb=verb,
            adj=adj,
            adv=adv,
            index=i,
            regular=False
        )

        full_sentence = regular.get('sentence')

        if full_sentence in created:
            break

        sentences.append(regular)  

print(len(sentences), len(list(filter(lambda x: x['type'] == 'train', sentences))))
data = json.dumps(sentences)
file2write=open("dataset-sentences-features.json",'w')
file2write.write(data)
file2write.close()

print(len(words))
data = json.dumps(words)
file2write=open("words-selected-v-librasil.json",'w')
file2write.write(data)
file2write.close()
