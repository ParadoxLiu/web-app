# coding=gbk
import nltk
import numpy
import jieba
import codecs
import os

class SummaryTxt:
    def __init__(self,stopwordspath):
        # ��������
        self.N = 100
        # ���ʼ�ľ���
        self.CLUSTER_THRESHOLD = 5
        # ���ص�top n����
        self.TOP_SENTENCES = 5
        self.stopwrods = {}
        #����ͣ�ô�
        if os.path.exists(stopwordspath):
            stoplist = [line.strip() for line in codecs.open(stopwordspath, 'r', encoding='utf8').readlines()]
            self.stopwrods = {}.fromkeys(stoplist)


    def _split_sentences(self,texts):
        '''
        ��texts��ֳɵ������ӣ��������б����棬�ԣ�.!?����������Щ�����Ϊ��ֵ������
        :param texts: �ı���Ϣ
        :return:
        '''
        splitstr = '.!?������'
        start = 0
        index = 0  # ÿ���ַ���λ��
        sentences = []
        for text in texts:
            # ����������һ���ַ��Ƿ��Ǳ��
            if text in splitstr:
                sentences.append(texts[start:index + 1])  # ��ǰ������λ��
                start = index + 1  # start��ǵ���һ��Ŀ�ͷ
            index += 1
        if start < len(texts):
            sentences.append(texts[start:])  # ����Ϊ�˴����ı�ĩβû�б��

        return sentences

    def _score_sentences(self,sentences, topn_words):
        '''
        ����ǰN���ؼ��ָ����Ӵ��
        :param sentences: �����б�
        :param topn_words: �ؼ����б�
        :return:
        '''
        scores = []
        sentence_idx = -1
        for s in [list(jieba.cut(s)) for s in sentences]:
            sentence_idx += 1
            word_idx = []
            for w in topn_words:
                try:
                    word_idx.append(s.index(w))  # �ؼ��ʳ����ڸþ����е�����λ��
                except ValueError:  # w���ھ�����
                    pass
            word_idx.sort()
            if len(word_idx) == 0:
                continue
            # �������������ĵ��ʣ����õ���λ��������ͨ�����뷧ֵ������
            clusters = []
            cluster = [word_idx[0]]
            i = 1
            while i < len(word_idx):
                if word_idx[i] - word_idx[i - 1] < self.CLUSTER_THRESHOLD:
                    cluster.append(word_idx[i])
                else:
                    clusters.append(cluster[:])
                    cluster = [word_idx[i]]
                i += 1
            clusters.append(cluster)
            # ��ÿ�����֣�ÿ��������������ǶԾ��ӵĴ��
            max_cluster_score = 0
            for c in clusters:
                significant_words_in_cluster = len(c)
                total_words_in_cluster = c[-1] - c[0] + 1
                score = 1.0 * significant_words_in_cluster * significant_words_in_cluster / total_words_in_cluster
                if score > max_cluster_score:
                    max_cluster_score = score
            scores.append((sentence_idx, max_cluster_score))
        return scores

    def summaryScoredtxt(self,text):
        # �����·ֳɾ���
        sentences = self._split_sentences(text)

        # ���ɷִ�
        words = [w for sentence in sentences for w in jieba.cut(sentence) if w not in self.stopwrods if
                 len(w) > 1 and w != '\t']
        # words = []
        # for sentence in sentences:
        #     for w in jieba.cut(sentence):
        #         if w not in stopwords and len(w) > 1 and w != '\t':
        #             words.append(w)

        # ͳ�ƴ�Ƶ
        wordfre = nltk.FreqDist(words)

        # ��ȡ��Ƶ��ߵ�ǰN����
        topn_words = [w[0] for w in sorted(wordfre.items(), key=lambda d: d[1], reverse=True)][:self.N]

        # ������ߵ�n���ؼ��ʣ������Ӵ��
        scored_sentences = self._score_sentences(sentences, topn_words)

        # ���þ�ֵ�ͱ�׼����˷���Ҫ����
        avg = numpy.mean([s[1] for s in scored_sentences])  # ��ֵ
        std = numpy.std([s[1] for s in scored_sentences])  # ��׼��
        summarySentences = []
        for (sent_idx, score) in scored_sentences:
            if score > (avg + 0.5 * std):
                summarySentences.append(sentences[sent_idx])
                print(sentences[sent_idx])
        return summarySentences

    def summaryTopNtxt(self,text):
        # �����·ֳɾ���
        sentences = self._split_sentences(text)

        # ���ݾ����б����ɷִ��б�
        words = [w for sentence in sentences for w in jieba.cut(sentence) if w not in self.stopwrods if
                 len(w) > 1 and w != '\t']
        # words = []
        # for sentence in sentences:
        #     for w in jieba.cut(sentence):
        #         if w not in stopwords and len(w) > 1 and w != '\t':
        #             words.append(w)

        # ͳ�ƴ�Ƶ
        wordfre = nltk.FreqDist(words)

        # ��ȡ��Ƶ��ߵ�ǰN����
        topn_words = [w[0] for w in sorted(wordfre.items(), key=lambda d: d[1], reverse=True)][:self.N]

        # ������ߵ�n���ؼ��ʣ������Ӵ��
        scored_sentences = self._score_sentences(sentences, topn_words)

        top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-self.TOP_SENTENCES:]
        top_n_scored = sorted(top_n_scored, key=lambda s: s[0])
        summarySentences = []
        for (idx, score) in top_n_scored:
            #print(sentences[idx])
            summarySentences.append(sentences[idx])

        return summarySentences



# if __name__=='__main__':
#     obj =SummaryTxt('stop_words.txt')
#
#     txt=u'ʮ�˴����������꣬�ǵ��͹��ҷ�չ�����м���ƽ�������ꡣ������羭�ø��շ������ֲ���ͻ�Ͷ���Ƶ����ȫ��������Ӿ���ⲿ����������ҹ����÷�չ�����³�̬��һϵ����̱仯�����Ǽ��������������ܻ�����ӭ�Ѷ��ϣ����ؽ�ȡ��ȡ���˸ĸ￪�ź���������ִ����������ʷ�Գɾ͡�' \
#         u'Ϊ�᳹ʮ�˴��񣬵������ٿ��ߴ�ȫ�ᣬ�ֱ�����������ĸ��ְ��ת�䡢ȫ����ĸȫ���ƽ������ι����ƶ���ʮ���塱�滮��ȫ������ε����ش��������������Ͳ���������������ͳ���ƽ�����λһ�塱���岼�֡�Э���ƽ����ĸ�ȫ�桱ս�Բ��֣���ʮ���塱�滮ʤ����ɣ���ʮ���塱�滮˳��ʵʩ�����͹�����ҵȫ�濪���¾��档' \
#         u'���ý���ȡ���ش�ɾ͡��ᶨ���ƹ᳹�·�չ������������չ���ת�䷢չ��ʽ����չ������Ч�治�����������ñ����и�����������������Ҫ����������ǰé������������ֵ����ʮ������Ԫ��������ʮ����Ԫ���Ⱦ�����ڶ��������羭�����������ʳ����ٷ�֮��ʮ��������ṹ�Ըĸ������ƽ������ýṹ�����Ż������־��õ����˲�ҵ���չ����������·���������ۿڡ������Ȼ�����ʩ��������ƽ���ũҵ�ִ����Ȳ��ƽ�����ʳ���������ﵽһ���ǧ�ڽ������������һ������ٷֵ㣬��ǧ����ũҵת���˿ڳ�Ϊ�����������չЭ������ǿ����һ��һ·�����衢����Эͬ��չ���������ô���չ��Ч����������������չս�Դ���ʵʩ�������͹��ҽ���ɹ���˶���칬�����������ۡ���ա�ī�ӡ���ɻ����ش�Ƽ��ɹ�����������Ϻ�������������ƽ��������;����������𲽽�ȫ������ó�ס�����Ͷ�ʡ���㴢���Ⱦ�����ǰ�С�' \
#         u'ȫ����ĸ�ȡ���ش�ͻ�ơ��㼲�����ƽ�ȫ����ĸ����Ƴ����������ƻ��Ʊ׶ˡ��ĸ�ȫ�淢�������ͻ�ơ������ƽ���������ǿ�ĸ�ϵͳ�ԡ������ԡ�Эͬ�ԣ�ѹ����չ�ĸ��Ⱥ���ȣ��Ƴ�һǧ��ٶ���ĸ�ٴ룬��Ҫ����͹ؼ����ڸĸ�ȡ��ͻ���Խ�չ����Ҫ����ĸ������ܻ���ȷ�����й���ɫ��������ƶȸ������ƣ�����������ϵ�����������ִ���ˮƽ������ߣ�ȫ��ᷢչ�����ʹ��»���������ǿ��'
#
#     t1 = u'��ҳ��̳��ҳ�ϴη����� 2018��-4��-15�� 09:19���ڵ�ʱ���� 2018��-4��-16�� 16:32����̳���Ϊ�Ѷ��г������������������������¹�����Ʒ������[����: ������Ʒ��Ϣ����, ����ý�飺���ر�, ���׹������: 2018.04.14 ][ע:����Ͷ����, �����ʽ������Ͷ��������Ͷ��, �ſ���ҳ���վ]�������˵����������鿴.��Ϣ���������������ע�۸���������, Ͷ�����ޣ�������Ϊ��թ,ɾ���˺�����: 33 ����6 �������������� 1721903095�鿴��������2018��-4��-15�� 22:22������Ʒ������[����: ������Ʒ��Ϣ����, ����ý�飺���ر�, ���׹������: 2018.04.14 ] [ע:����Ͷ����, �����ʽ������Ͷ��������Ͷ��, �ſ���ҳ���վ]�������˵����������鿴.��Ϣ���������������ע�۸���������, Ͷ�����ޣ�������Ϊ��թ,ɾ���˺�����: 4545 ����310 �������������� hanhanmoney�鿴��������2018��-4��-16�� 14:17��վ����������������������²��Է�������վ����˽����Ϣ����,�ܶ����û�����Ϥ,�������������ֵ���Υ���涨���߷�������Ϣ�ᱻ��ָ��������ⷢ��,�������. �������ݶ������,������������: 3333 ����60 �������������� vivi100�鿴��������2018��-4��-15�� 23:20����֪ʶ������վ�Ļ���ʹ�ó���֪ʶ����: 66 ����6 �������������� almvdkg6�鿴��������2018��-3��-05�� 12:38������Ϣ��������������������˽�˺�����Ϣ��Ŀ̽��,Ѱ�Һ���,Ѱ�Ҽ���,�ҳ�ı���߱�����Ŀ���Բ������ۣ��ž���������������û����ѵ���ͣ���Ҫ�����쿪.�����ʴ�:��û���޷�������׬��Ǯ,�����򵥵�ҵ��?���ƻ����벻Ҫ���뱾��,�ʹ�����:����˽�����۷���,����ʾ������ظ�֮��Ի�����: 638638 ����3406 �������������� densefog245536�鿴��������2018��-4��-16�� 14:34˽������������Ʒ����,������������,����Ѱ���Ͷ�����Դ������Ŀ���Բ������ۣ��ž���������������û����ѵ���ͣ���Ҫ�����쿪.�����ʴ�:��û���޷�������׬��Ǯ,�����򵥵�ҵ��?���ƻ����벻Ҫ���뱾��,�ʹ�����:����˽�����۷���,����ʾ������ظ�֮��Ի�����: 10061006 ����5369 �������������� loveoccean�鿴��������2018��-4��-16�� 16:26������������������������������ɢ�����������Ļ���,��������,��Ϣ����������������,���ƹ��Ʒ����վ��,�������ִ�����Ϣ��Ϊ�������.������Ϣ����,����������Ϣ�����˿ɼ�,��ע�Ᵽ����.������Ŀ���Բ������ۣ��ž���������������û����ѵ���ͣ���Ҫ�����쿪.����: 465465 ����2775 �������������� guxing�鿴��������2018��-4��-16�� 16:29������ƭ��¶�����޷�׷��ע���û����,����Է�������թ,û�н���İ취������թ,��Ǯ����·��,���ڴ˽�¶,�Ƕ�����թ�߳��干ͬά�����׷�Χ.��������ߵı�վ���ر�ͨ��,����ϵ����Ա,���ڶԷ���ҳ�վǰ��������: 3434 ����247 �������������� almvdkg6�鿴��������2018��-4��-16�� 14:57����ɫ������������Ϣ,�߼�����,ɫ����Ϣ���ڰ�����Ҫ����10�����ϼ�������ת������,��ͼƬ.��Ƶ����Ч������ͨӦ�ڶ��û�Ҫ��,�ؿ�����,���������״�����н�����Ϣ,���˼������: 7474 ����1341 �������������� wy666666�鿴��������2018��-4��-16�� 13:12CardingCarding�߼�����ר��,����������,������:TiTiTiTi����: 66 ����38 �������������� anxiaoxin�鿴��������2018��-4��-15�� 01:07ͳ����Ϣ�������� 22056 ? �������� 4409 ? �û����� 16275 ? ����ע����û���nh453245��ҳ��̳��ҳ������ʾ��ʱ���� UTC+08:00ɾ��ȫ����̳ cookie�� phpBB? Forum Software ? phpBB Limited �ṩ֧�� | SE Square Left by PhpBB3 BBCodes�������������� David Yin ά��'
#
#     print(txt)
#     print("--")
#     obj.summaryScoredtxt(t1)
#
#     print("----")
#     obj.summaryTopNtxt(t1)