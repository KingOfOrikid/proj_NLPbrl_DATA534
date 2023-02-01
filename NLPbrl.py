from wordcloud import WordCloud
import pandas as pd
import altair as alt
from altair_saver import save
import numpy as np
import math
from collections import OrderedDict
from graphviz import Graph
from Data_ import Data


class NLPbrl():
    def __init__(self):
        self.api_data = Data()

    def __word_wash(self, text, stop_word='default'):
        #determine language
        if stop_word == 'default':
            try:
                lang = self.api_data.get_lang(text)
            except:
                print("Error with get language function")
            if lang == 'zho':
                stop_word = 'pacakge_data/cn_stopwords.txt'
            elif lang == 'eng':
                stop_word = 'pacakge_data/en_stopwords.txt'
            else:
                stop_word = 'pacakge_data/other_stopwords.txt'

        try:
            stop_file = open(stop_word, 'r', encoding='utf-8')
            stopwords = stop_file.read().split("\n")
            stop_file.close()
        except:
            print('{} is not exist, please check the file!'.format(stop_word))

        #check the characters limit
        text_lst = self.__check_limit(text)
        text_token = []
        try:
            for t in text_lst:
                text_token.extend(self.api_data.get_token(t))
        except:
            print("Error with get token function")

        washed_token = []
        for char in text_token:
            if char in stopwords:
                pass
            else:
                washed_token.append(char)
        return washed_token

    def cal_frequency(self, text, stop_word='default'):
        washed_token = self.__word_wash(text, self.api_data, stop_word)

        counts = {}
        for word in washed_token:
            counts[word] = counts.get(word, 0) + 1

        counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return counts

    def __check_limit(self, text):
        text = text.replace('\n', ' ')
        if len(text.replace(' ', '')) <= 5000:
            return [text]
        else:
            true_text = []
            if '.' in text:
                true_text = self.__check_limit_tool(text, '.')
            elif '。' in text:
                true_text = self.__check_limit_tool(text, '。')
            else:
                true_text = self.__check_limit_tool(text, '')
        return true_text


    def __check_limit_tool(text, symbol):
        temp = []
        string = ''
        if symbol != '':
            split_text = text.split(symbol)
        else:
            split_text = text
        for sen in split_text:
            temp_s = string + sen + symbol
            if len(temp_s.replace(' ', '')) > 5000:
                temp.append(string)
                string = sen + symbol
            else:
                string = string + sen + symbol

            if sen == split_text[-1]:
                temp.append(string)
        return temp

    def word_viz(self, text, file_loc, top_num, stop_word='default', cloud_set=WordCloud(font_path='pacakge_data/STKAITI.TTF')):
        washed_token = self.__word_wash(text, self.api_data, stop_word)
    
        cloud_set.generate(' '.join(washed_token))
        cloud_set.to_file(file_loc + 'cloud.png')

        counts = self.cal_frequency(text, self.api_data, stop_word)
        words = []
        count = []
        for i in counts:
            words.append(i[0])
            count.append(i[1])
        df = pd.DataFrame({'words': words, 'count': count})
        chart = (alt.Chart(df[:top_num]).mark_line().encode(
            x='words', y='count').properties(height=400, width=400))
        save(chart, "chart.html")

    #text: text which needs to be calculate tfidf
    #document: document_loc to train idf
    #topK, keywords for top x
    def key_extra_tfidf(self, text, document, stop_word='default'):
        text_wash_lst = []
        for doc in document:
            wash_token = self.__word_wash(doc, self.api_data, stop_word)
            text_wash_lst.append(wash_token)
        
        text_wash = self.__word_wash(text, self.api_data, stop_word)

        #word dictionary
        set_lst = []
        for i in text_wash_lst:
            set_lst.extend(i)
        wordSet = set(set_lst)

        wordDict_lst = []
        for wash_token in text_wash_lst:
            temp_dic = dict.fromkeys(wordSet, 0)
            for word in wash_token:
                temp_dic[word] += 1
            wordDict_lst.append(temp_dic)
        
        wordDict = dict.fromkeys(wordSet, 0)
        for word in text_wash:
            wordDict[word] += 1

        tfDict = self.__cal_TF(wordDict, text_wash)
        idfDict = self.__cal_IDF(wordDict_lst)

        tfidf = self.__cal_TFIDF(tfDict, idfDict)

        return tfidf

    def __cal_TF(self, wordDict, wash_token):
        tfDict = {}
        token_count = len(wash_token)
        for word, count in wordDict.items():
            tfDict[word] = count / token_count
        return tfDict

    def __cal_IDF(self, wordDict_lst):
        idfDict = dict.fromkeys(wordDict_lst[0], 0)
        N = len(wordDict_lst)
        for wordDict in wordDict_lst:
            for word, count in wordDict.items():
                if count > 0:
                    idfDict[word] += 1

        for word, ni in idfDict.items():
            idfDict[word] = math.log10(N / (ni + 1))

        return idfDict

    def __cal_TFIDF(self, tf, idf):
        tfidf = {}
        for word, tf_val in tf.items():
            tfidf[word] = tf_val * idf[word]
        return tfidf

    def cal_simi(self, text1, text2, size='sen', method='euc'):
        try:
            token_1 = self.api_data.get_token(text1)
            token_2 = self.api_data.get_token(text2)
        except:
            print("Error with get token function") 
        
        try:
            if size == 'sen':
                vec_1 = self.api_data.get_vec(text1)['documentEmbedding']
                vec_2 = self.api_data.get_vec(text2)['documentEmbedding']
            elif size == 'word':
                vec_1 = self.api_data.get_vec(text1)['tokenEmbeddings']
                vec_2 = self.api_data.get_vec(text2)['tokenEmbeddings']
        except:
            print("Error with get vector function") 
            #padding
            max_matrix_length = max(len(vec_1),len(vec_2))
            add = np.zeros(300)
            if max_matrix_length == len(vec_1):
                vec_2.extend([list(add)]* (max_matrix_length-len(vec_2)))
                vec_2 = np.array(vec_2).flatten()
                vec_1 = np.array(vec_1).flatten()
            else:
                vec_1.extend([list(add)]* (max_matrix_length-len(vec_1)))
                vec_1 = np.array(vec_1).flatten()
                vec_2 = np.array(vec_2).flatten()
        else:
            print('There is no size '.format(size))

        if method == 'euc':
            score = self.__simi_cal_euc(vec_1, vec_2, size)
        elif method == 'cos':
            score = self.__simi_cal_cos(vec_1, vec_2, size)
        elif method == 'jac':
            score = self.__simi_cal_jac(token_1, token_2, size)
        elif method == 'cheb':
            score = self.__simi_cal_cheb(vec_1, vec_2, size)
        elif method == 'mah':
            score = self.__simi_cal_mah(vec_1, vec_2, size)
        else:
            print('There is no method '.format(method))
        
        return score

    def __simi_cal_euc(self, vec1,vec2,size):
        if size=='word':
            pass
        else:
            vec1=np.array(vec1)
            vec2=np.array(vec2)
        return float(np.sqrt(np.sum(np.square(vec1-vec2))))
    
    def __simi_cal_cos(self, vec1,vec2,size):
        if size=='word':
            pass
        else:
            vec1=np.array(vec1)
            vec2=np.array(vec2)
        return float(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
    
    def __simi_cal_mah(self, vec1, vec2, size):
        if size=='word':
            pass
        else:
            vec1=np.array(vec1)
            vec2=np.array(vec2)
        return float(np.sum(np.abs(vec1-vec2)))

    def __simi_cal_jac(self, token_1, token_2, size):
        inter = len(list(set(token_1).intersection(token_2)))
        union = (len(token_1) + len(token_1)) - inter
        return float(inter) / union

    def __simi_cal_cheb(self,vec1, vec2, size):
        if size == 'word':
            pass
        else:
            vec1=np.mat(vec1)
            vec2=np.mat(vec2)
        return float(np.max(np.abs(vec1-vec2)))

    def cal_textRank(self, text, candidate_pos=['NOUN', 'PROPN', 'VERB'], top_k = 10, window_size=3, stop_word='default'):
        #damping coefficient
        damp = 0.85
        #convergence threshold
        min_conv = 1e-5
        iters = 10
        #keywords + weight
        key_weight = {}
    
        try:
            sentences = self.api_data.get_senTag(text)
        except:
            print("Error with get sentence tagging function")
    
        try:
            #filter pos tag
            pos_tag_lst = []
            for sen in sentences:
                pos_tag_lst.append(self.api_data.get_posTag(sen))
        except:
            print("Error with get pos tagging function")
    
        sen_filter_pos = []
        for pos_dic in pos_tag_lst:
            temp = []
            tokens = pos_dic['tokens']
            tags = pos_dic['posTags']
            for i in range(0,len(tags)):
                if tags[i] in candidate_pos:
                    temp.append(tokens[i])
            sen_filter_pos.append(temp)
    

        #determine language
        if stop_word == 'default':
            try:
                lang = self.api_data.get_lang(text)
            except:
                print("Error with get language function")
            if lang == 'zho':
                stop_word = 'pacakge_data/cn_stopwords.txt'
            elif lang == 'eng':
                stop_word = 'pacakge_data/en_stopwords.txt'
            else:
                stop_word = 'pacakge_data/other_stopwords.txt'

        try:
            stop_file = open(stop_word, 'r', encoding='utf-8')
            stopwords = stop_file.read().split("\n")
            stop_file.close()
        except:
            print('{} is not exist, please check the file!'.format(stop_word))

        washed_token = []
        for sen in sen_filter_pos:
            temp = []
            for char in sen:
                if char in stopwords:
                    pass
                else:
                    temp.append(char)
            washed_token.append(temp)
        
        vocab_dic = OrderedDict()
        count = 0
        for sen in washed_token:
            for token in sen:
                if token not in vocab_dic:
                    vocab_dic[token] = count
                    count += 1
                
        token_pair_lst = []
        for sen in washed_token:
            for i,word in enumerate(sen):
                for j in range(i+1,i+window_size):
                    if j>=len(sen):
                        break
                    if (word,sen[j]) not in token_pair_lst:
                        token_pair_lst.append((word,sen[j]))
                    
        #normalized matrix
        matrix_size = len(vocab_dic)
        matrix = np.zeros((matrix_size, matrix_size), dtype='float')
        for word_pair in token_pair_lst:
            word1 = vocab_dic[word_pair[0]]
            word2 = vocab_dic[word_pair[1]]
            matrix[word1][word2]=1
        
        #Symmeric matrix
        matrix = matrix +matrix.T-np.diag(matrix.diagonal())
    
        #normalize
        normalize = np.sum(matrix,axis=0)
        matrix_norm = np.divide(matrix,normalize,where=normalize!=0)
    
        #inital weight
        weight = np.array([1]*len(vocab_dic))
        pre_weight = 0
        for epoch in range(0,iters):
            weight = (1-damp)+damp*np.dot(matrix_norm,weight)
            if abs(pre_weight - sum(weight))  < min_conv:
                break
            else:
                pre_weight=sum(weight)
    
        for word,index in vocab_dic.items():
            key_weight[word]=weight[index]
        
        key_weight = OrderedDict(sorted(key_weight.items(), key=lambda t: t[1], reverse=True))
        count = 0
        keywords_lst = []
        for key in key_weight:
            keywords_lst.append((key,key_weight[key]))
            count += 1
            if count >= top_k:
                break
        return keywords_lst

    def relation_viz(self, text):
        text_lst = self.__check_limit(text)
        relations = []
        try:
            for t in text_lst:
                relations.extend(self.api_data.get_relation(t))
        except:
            print("Error with get relationship function")

        g = Graph('graph', filename='G', engine='neato')
        for relation_dic in relations:
            rela = relation_dic['predicate']
            arg1 = relation_dic['arg1']
            arg2 = relation_dic['arg2']
            g.node(arg1)
            g.node(arg2)
            g.edge(arg1,arg2, label=rela,len='1.50')
        
        g.view()
        return True

    def cal_classification(self, text, top_k = 3):
        try:
            classify = self.api_data.get_classification(text)
        except:
            print("Error with get classification function")
            
        if top_k > len(classify):
            print('The k exceed the number of categories')
            return False
        else:
            return classify[:top_k]