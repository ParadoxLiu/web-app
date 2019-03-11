from datetime import datetime
from app.bd_api import sentiment_classify
from elasticsearch import Elasticsearch
from app.zhaiyao import SummaryTxt
import jieba
import jieba.posseg as pseg
import codecs
import json
from gensim import corpora,models,similarities
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from flask import render_template,request,Flask,jsonify
app = Flask(__name__)
es = Elasticsearch(['192.168.68.156'], port=9200, timeout=120)
res = es.search(index="hiddenwebs", body={"query": {"match_all": {}}, "from": 0, "size": 100})
#print(res)
content = []
for hit in res["hits"]["hits"]:
    # print(hit["_source"]["content"])
    content.append(hit["_source"]["content"])

#将每条数据存放到字典中，方便后续的查询
dic = {}
for index in range(len(content)):
    dic[index] = content[index]

# 构建停用词表
stop_words = 'stop_words.txt'
stopwords = codecs.open(stop_words, 'r', encoding='GBK').readlines()
stopwords = [w.strip() for w in stopwords]
#print(stopwords)
#停用词性
stop_flag = ['x', 'u', 'p', 'r']


@app.route('/',methods=['GET'])
def home():
    return render_template('new_page.html')

@app.route('/content_analyze/login',methods=['GET','POST'])
def login():

    if request.form['u'] == 'admin' and request.form['p'] == 'password':
        return render_template('main.html')

    else:
        return render_template('new_page.html',message="用户名或密码错误，请重新输入！")


@app.route('/content_analyze/main_page',methods=['GET'])
def main_page():
    return render_template('main.html')

@app.route('/content_analyze/showresult',methods=['GET'])
def charts():
    return render_template('charts.html')

@app.route('/content_analyze/upload',methods=['GET'])
def upload():
    return render_template('upload.html')


@app.route('/content_analyze/sim_tuple',methods=['POST'])
def tuple():
    ct = request.values['content']
    # 对内容分词、去停用词
    def tokenization(list):
        result = []
        words = pseg.cut(list)
        for word, flag in words:
            if flag not in stop_flag and word not in stopwords:
                result.append(word)
        return result

    corpus = []
    for each in content:
        corpus.append(tokenization(each))
    # print(len(corpus))

    # 建立词袋模型
    dictionary = corpora.Dictionary(corpus)
    # print(dictionary)

    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    # print(len(doc_vectors))
    #print(doc_vectors)

    # 建立TF-IDF模型
    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]
    # print(len(tfidf_vectors))
    # print(len(tfidf_vectors[0]))

    # 构建一个与es查询返回的内容相关的文本，利用词袋模型的字典将其映射到向量空间
    ct_str = " ".join(ct)
    query = tokenization(ct_str)
    # print(query)
    query_bow = dictionary.doc2bow(query)
    # print(query_bow)
    # 生成索引
    index = similarities.MatrixSimilarity(tfidf_vectors)
    sims = index[query_bow]
    result = sorted(list(enumerate(sims)), key=lambda x: x[1], reverse=True)
    #创建两个列表用来存储文章的索引以及对应的相似度
    result1 = []
    result2 = []
    for i in range(8):
        result1.append(result[i][0]+1)

    for i in range(8):
        result2.append(result[i][1])

    return str(result1)+'|'+str(result2) + '|' + str(dic[1])

@app.route('/classify',methods=['POST'])
def classify():
    def jieba_tokenize(text):
        rst = []
        words = jieba.lcut(text)
        for word, flag in words:
            if flag not in stop_flag and word not in stopwords:
                        rst.append(word)
        return rst

    tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize,lowercase=False)
    tfidf_matrix = tfidf_vectorizer.fit_transform(content)

    num_cluster = 10
    km_cluster = KMeans(n_clusters=num_cluster,max_iter=300,n_init=1,init='k-means++',n_jobs=1)
    result = km_cluster.fit_predict(tfidf_matrix)
    return result

@app.route('/get_zhaiyao',methods=['GET'])
def get_zhaiyao():
    return render_template('zhaiyao.html')

@app.route('/zhaiyao',methods=['POST'])
def zhaiyao():
    obj = SummaryTxt('D:/app/stop_words')
    ct = request.values['content']
    return str(obj.summaryTopNtxt(ct)) + "|"

@app.route('/get_emotion',methods=['GET'])
def get_emotion():
    return render_template('emotion.html')

@app.route('/emotion',methods=['POST'])
def emotion():
    txt = request.values['content']
    dc = sentiment_classify(txt)
    return str(dc['items'][0]['positive_prob']) + '|' + str(dc['items'][0]['confidence']) + '|' + str(dc['items'][0]['negative_prob'])

if __name__ == '__main__':
    app.run(debug=True)






