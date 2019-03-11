from elasticsearch import Elasticsearch
import jieba
import jieba.posseg as pseg
import codecs
from gensim import corpora,models,similarities
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

es = Elasticsearch(['192.168.68.156'], port=9200, timeout=120)
res = es.search(index="hiddenwebs", body={"query": {"match_all": {}}, "from": 0, "size": 100})
#print(res)
content = []
for hit in res["hits"]["hits"]:
    # print(hit["_source"]["content"])
    content.append(hit["_source"]["content"])

dic = {}
for index in range(len(content)):
    dic[index] = content[index]

# 构建停用词表
stop_words = 'stop_words.txt'
stopwords = codecs.open(stop_words, 'r', encoding='GBK').readlines()
stopwords = [w.strip() for w in stopwords]
print(stopwords)
#停用词性
stop_flag = ['x', 'u', 'p', 'r']


def analyze(ct):
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
    result1 = []
    result2 = []
    for i in range(8):
        result1.append(result[i][0])

    for i in range(8):
        result2.append(result[i][1])

    rst = [result1,result2]
    return rst
    # print(dic[0])



#聚类
def cluster():
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

if __name__ == '__main__':
    print(cluster())
    print(content[0])