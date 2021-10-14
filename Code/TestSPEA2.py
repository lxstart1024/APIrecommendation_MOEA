import emo.population as population
import emo.spea2 as spea2

import xlrd
import xlsxwriter
import re
import nltk
nltk.download('punkt')
nltk.download("stopwords")
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.models import word2vec
import numpy
import math


def sentence_split(str_centence):
    list_ret = list()
    for s_str in str_centence.split('.'):
        if '?' in s_str:
            list_ret.extend(s_str.split('?'))
        elif '!' in s_str:
            list_ret.extend(s_str.split('!'))
        else:
            list_ret.append(s_str)
    return list_ret

def sentenceFeatureExtract(sentence):

    words = nltk.word_tokenize(sentence)
    words = [i for i in words if i not in stopwords.words('english')]
    sentence_tags = nltk.pos_tag(words)
    feature_list = []

    for i in range(len(sentence_tags)):
        if len(sentence_tags) - i >= 4:
            if sentence_tags[i][1].startswith('VB') and sentence_tags[i + 1][1] == 'IN' and sentence_tags[i + 2][1].startswith('JJ') and sentence_tags[i + 3][1].startswith('NN'):
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 3][0]])
                i = i + 4
            elif sentence_tags[i][1].startswith('VB') and sentence_tags[i + 1][1] == 'JJ' and sentence_tags[i + 2][1].startswith('JJ') and sentence_tags[i + 3][1].startswith('NN'):
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 3][0]])
                i = i + 4
            elif sentence_tags[i][1].startswith('VB') and sentence_tags[i + 1][1] == 'NN' and sentence_tags[i + 2][1].startswith('IN') and sentence_tags[i + 3][1].startswith('NN'):
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 1][0]])
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 3][0]])
                i = i + 4
            elif sentence_tags[i][1].startswith('VB') and sentence_tags[i + 1][1].startswith('JJ') and sentence_tags[i + 2][1].startswith('NN') and sentence_tags[i + 3][1].startswith('NN'):
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 2][0]])
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 3][0]])
                i = i + 4
            elif sentence_tags[i][1].startswith('JJ') and sentence_tags[i + 1][1].startswith('NN') and sentence_tags[i + 2][1].startswith('NN') and sentence_tags[i + 3][1].startswith('NN'):
                feature_list.append(['', sentence_tags[i + 1][0]])
                feature_list.append(['', sentence_tags[i + 2][0]])
                feature_list.append(['', sentence_tags[i + 3][0]])
                i = i + 4
            elif sentence_tags[i][1].startswith('NN') and sentence_tags[i + 1][1].startswith('CC') and sentence_tags[i + 2][1].startswith('NN') and sentence_tags[i + 3][1].startswith('NN'):
                feature_list.append(['', sentence_tags[i][0]])
                feature_list.append(['', sentence_tags[i + 2][0]])
                feature_list.append(['', sentence_tags[i + 3][0]])
                i = i + 4
        if len(sentence_tags) - i >= 3:
            if sentence_tags[i][1].startswith('VB') and sentence_tags[i + 1][1].startswith('JJ') and sentence_tags[i + 2][1].startswith('NN'):
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 2][0]])
                i = i + 3
            elif sentence_tags[i][1].startswith('VB') and sentence_tags[i+1][1].startswith('NN') and sentence_tags[i+2][1].startswith('NN'):
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 1][0]])
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 2][0]])
                i = i + 3
            elif sentence_tags[i][1].startswith('VB') and sentence_tags[i + 1][1].startswith('IN') and sentence_tags[i + 2][1].startswith('NN'):
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 2][0]])
                i = i + 3
            elif sentence_tags[i][1].startswith('NN') and sentence_tags[i + 1][1].startswith('CC') and sentence_tags[i + 2][1].startswith('NN'):
                feature_list.append(['', sentence_tags[i][0]])
                feature_list.append(['', sentence_tags[i+2][0]])
                i = i + 3
            elif sentence_tags[i][1].startswith('JJ') and sentence_tags[i + 1][1].startswith('NN') and sentence_tags[i + 2][1].startswith('NN'):
                feature_list.append(['', sentence_tags[i+1][0]])
                feature_list.append(['', sentence_tags[i+2][0]])
                i = i + 3
            elif sentence_tags[i][1].startswith('NN') and sentence_tags[i + 1][1].startswith('NN') and sentence_tags[i + 2][1].startswith('NN'):
                feature_list.append(['', sentence_tags[i][0]])
                feature_list.append(['', sentence_tags[i + 1][0]])
                feature_list.append(['', sentence_tags[i + 2][0]])
                i = i + 3
            elif sentence_tags[i][1].startswith('VB') and sentence_tags[i + 1][1].startswith('PRP') and sentence_tags[i + 2][1].startswith('NN'):
                feature_list.append([sentence_tags[i][0], sentence_tags[i + 2][0]])
                i = i + 3
            elif sentence_tags[i][1].startswith('JJ') and sentence_tags[i + 1][1].startswith('JJ') and sentence_tags[i + 2][1].startswith('NN'):
                feature_list.append(['', sentence_tags[i + 2][0]])
                i = i + 3
            elif sentence_tags[i][1].startswith('NN') and sentence_tags[i + 1][1].startswith('IN') and sentence_tags[i + 2][1].startswith('NN'):
                feature_list.append(['', sentence_tags[i][0]])
                feature_list.append(['', sentence_tags[i + 2][0]])
                i = i + 3
        if len(sentence_tags) - i >= 2:
            if sentence_tags[i][1].startswith('VB') and sentence_tags[i + 1][1].startswith('NN'):
                feature_list.append([sentence_tags[i][0],sentence_tags[i+1][0]])
                i = i + 2
            elif sentence_tags[i][1].startswith('NN') and sentence_tags[i + 1][1].startswith('NN'):
                feature_list.append(['', sentence_tags[i][0]])
                feature_list.append(['', sentence_tags[i+1][0]])
                i = i + 2
            elif sentence_tags[i][1].startswith('JJ') and sentence_tags[i + 1][1].startswith('NN'):
                feature_list.append(['', sentence_tags[i + 1][0]])
                i = i + 2
        else:
            break
    return feature_list


def cal_sim_singleapi(apino):
    queryfeature = ['get', 'image']
    feature_apino = []

    workbook1 = xlrd.open_workbook("E:/APIDescriptionFiltered.xlsx")
    worksheet1 = workbook1.sheet_by_index(0)
    nrows = worksheet1.nrows
    description_apino = sentence_split(worksheet1.cell_value((apino-1), 1))
    if description_apino[len(description_apino)-1] == '':
        description_apino.pop()
    for i in range(len(description_apino)):
        feature_apino.append(sentenceFeatureExtract(description_apino[i]))

    sentences = word2vec.Text8Corpus(u"E:/paper2/demo/DemoAPIDescription6.txt")
    model = word2vec.Word2Vec(sentences, size=100, min_count=1)
    maxsim_noun = 0
    maxsim_verb = 0
    for i in range(len(feature_apino)):
        maxsim_noun_temp = 0
        maxsim_verb_temp = 0
        
        for j in range(len(feature_apino[i])):
            if feature_apino[i][j][0] != '':
                if maxsim_verb_temp < model.similarity(queryfeature[0].lower(), feature_apino[i][j][0].lower()):
                    maxsim_verb_temp = model.similarity(queryfeature[0].lower(), feature_apino[i][j][0].lower())
            if feature_apino[i][j][1] != '':
                if maxsim_noun_temp < model.similarity(queryfeature[1].lower(), feature_apino[i][j][1].lower()):
                    maxsim_noun_temp = model.similarity(queryfeature[1].lower(), feature_apino[i][j][1].lower())
        if maxsim_verb < maxsim_verb_temp:
            maxsim_verb = maxsim_verb_temp
        if maxsim_noun < maxsim_noun_temp:
            maxsim_noun = maxsim_noun_temp
    return maxsim_verb*0.5+maxsim_noun*0.5


def fun0(APIpattern):
    semantic_sim_APIpattern = 0
    for apino in APIpattern:
        semantic_sim_APIpattern = semantic_sim_APIpattern+cal_sim_singleapi(apino)
    return semantic_sim_APIpattern/len(APIpattern)


def cal_euclid(vec1, vec2):
    sum = 0
    for i in range(len(vec1)):
        if isinstance(vec1[i], str):
            print(vec1[i].strip())
            vec1[i] = float(vec1[i].strip())
            print(vec1[i])
        if isinstance(vec2[i], str):
            print(vec2[i].strip())
            vec2[i] = float(vec2[i].strip())
            print(vec1[i])
        sum = sum+math.pow((vec1[i] - vec2[i]), 2)
    dist = math.sqrt(sum)
    return dist


def fun1(APIpattern):
    workbook1 = xlrd.open_workbook("E:/APIEmbedding.xlsx")
    worksheet1 = workbook1.sheet_by_index(0)
    nrows = worksheet1.nrows
    vec_list = []
    for apino in APIpattern:
        temp_list = []
        for i in range(2, 130):
            temp_list.append(worksheet1.cell_value(apino-1, i))
        vec_list.append(temp_list)

    dist_sum = 0
    count = 0
    for i in range(0, (len(vec_list)-1)):
        j = i+1
        while j<len(vec_list):
            dist_sum = dist_sum+cal_euclid(vec_list[i], vec_list[j])
            j = j+1
            count = count+1
    return 1000 - (dist_sum/count)

if __name__ == "__main__":
    testmop = population.MOP([fun0], 'max')
    P = spea2.spea2(mop=testmop, populationsize=10, archivesize=10,
                    propertynum=6, min=1, max=208, maxiter=100)
    print('final')
    print(population.printpopulation(P))


