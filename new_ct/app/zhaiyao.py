# coding=gbk
import nltk
import numpy
import jieba
import codecs
import os

class SummaryTxt:
    def __init__(self,stopwordspath):
        # 单词数量
        self.N = 100
        # 单词间的距离
        self.CLUSTER_THRESHOLD = 5
        # 返回的top n句子
        self.TOP_SENTENCES = 5
        self.stopwrods = {}
        #加载停用词
        if os.path.exists(stopwordspath):
            stoplist = [line.strip() for line in codecs.open(stopwordspath, 'r', encoding='utf8').readlines()]
            self.stopwrods = {}.fromkeys(stoplist)


    def _split_sentences(self,texts):
        '''
        把texts拆分成单个句子，保存在列表里面，以（.!?。！？）这些标点作为拆分的意见，
        :param texts: 文本信息
        :return:
        '''
        splitstr = '.!?。！？'
        start = 0
        index = 0  # 每个字符的位置
        sentences = []
        for text in texts:
            # 检查标点符号下一个字符是否还是标点
            if text in splitstr:
                sentences.append(texts[start:index + 1])  # 当前标点符号位置
                start = index + 1  # start标记到下一句的开头
            index += 1
        if start < len(texts):
            sentences.append(texts[start:])  # 这是为了处理文本末尾没有标点

        return sentences

    def _score_sentences(self,sentences, topn_words):
        '''
        利用前N个关键字给句子打分
        :param sentences: 句子列表
        :param topn_words: 关键字列表
        :return:
        '''
        scores = []
        sentence_idx = -1
        for s in [list(jieba.cut(s)) for s in sentences]:
            sentence_idx += 1
            word_idx = []
            for w in topn_words:
                try:
                    word_idx.append(s.index(w))  # 关键词出现在该句子中的索引位置
                except ValueError:  # w不在句子中
                    pass
            word_idx.sort()
            if len(word_idx) == 0:
                continue
            # 对于两个连续的单词，利用单词位置索引，通过距离阀值计算族
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
            # 对每个族打分，每个族类的最大分数是对句子的打分
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
        # 将文章分成句子
        sentences = self._split_sentences(text)

        # 生成分词
        words = [w for sentence in sentences for w in jieba.cut(sentence) if w not in self.stopwrods if
                 len(w) > 1 and w != '\t']
        # words = []
        # for sentence in sentences:
        #     for w in jieba.cut(sentence):
        #         if w not in stopwords and len(w) > 1 and w != '\t':
        #             words.append(w)

        # 统计词频
        wordfre = nltk.FreqDist(words)

        # 获取词频最高的前N个词
        topn_words = [w[0] for w in sorted(wordfre.items(), key=lambda d: d[1], reverse=True)][:self.N]

        # 根据最高的n个关键词，给句子打分
        scored_sentences = self._score_sentences(sentences, topn_words)

        # 利用均值和标准差过滤非重要句子
        avg = numpy.mean([s[1] for s in scored_sentences])  # 均值
        std = numpy.std([s[1] for s in scored_sentences])  # 标准差
        summarySentences = []
        for (sent_idx, score) in scored_sentences:
            if score > (avg + 0.5 * std):
                summarySentences.append(sentences[sent_idx])
                print(sentences[sent_idx])
        return summarySentences

    def summaryTopNtxt(self,text):
        # 将文章分成句子
        sentences = self._split_sentences(text)

        # 根据句子列表生成分词列表
        words = [w for sentence in sentences for w in jieba.cut(sentence) if w not in self.stopwrods if
                 len(w) > 1 and w != '\t']
        # words = []
        # for sentence in sentences:
        #     for w in jieba.cut(sentence):
        #         if w not in stopwords and len(w) > 1 and w != '\t':
        #             words.append(w)

        # 统计词频
        wordfre = nltk.FreqDist(words)

        # 获取词频最高的前N个词
        topn_words = [w[0] for w in sorted(wordfre.items(), key=lambda d: d[1], reverse=True)][:self.N]

        # 根据最高的n个关键词，给句子打分
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
#     txt=u'十八大以来的五年，是党和国家发展进程中极不平凡的五年。面对世界经济复苏乏力、局部冲突和动荡频发、全球性问题加剧的外部环境，面对我国经济发展进入新常态等一系列深刻变化，我们坚持稳中求进工作总基调，迎难而上，开拓进取，取得了改革开放和社会主义现代化建设的历史性成就。' \
#         u'为贯彻十八大精神，党中央召开七次全会，分别就政府机构改革和职能转变、全面深化改革、全面推进依法治国、制定“十三五”规划、全面从严治党等重大问题作出决定和部署。五年来，我们统筹推进“五位一体”总体布局、协调推进“四个全面”战略布局，“十二五”规划胜利完成，“十三五”规划顺利实施，党和国家事业全面开创新局面。' \
#         u'经济建设取得重大成就。坚定不移贯彻新发展理念，坚决端正发展观念、转变发展方式，发展质量和效益不断提升。经济保持中高速增长，在世界主要国家中名列前茅，国内生产总值从五十四万亿元增长到八十万亿元，稳居世界第二，对世界经济增长贡献率超过百分之三十。供给侧结构性改革深入推进，经济结构不断优化，数字经济等新兴产业蓬勃发展，高铁、公路、桥梁、港口、机场等基础设施建设快速推进。农业现代化稳步推进，粮食生产能力达到一万二千亿斤。城镇化率年均提高一点二个百分点，八千多万农业转移人口成为城镇居民。区域发展协调性增强，“一带一路”建设、京津冀协同发展、长江经济带发展成效显著。创新驱动发展战略大力实施，创新型国家建设成果丰硕，天宫、蛟龙、天眼、悟空、墨子、大飞机等重大科技成果相继问世。南海岛礁建设积极推进。开放型经济新体制逐步健全，对外贸易、对外投资、外汇储备稳居世界前列。' \
#         u'全面深化改革取得重大突破。蹄疾步稳推进全面深化改革，坚决破除各方面体制机制弊端。改革全面发力、多点突破、纵深推进，着力增强改革系统性、整体性、协同性，压茬拓展改革广度和深度，推出一千五百多项改革举措，重要领域和关键环节改革取得突破性进展，主要领域改革主体框架基本确立。中国特色社会主义制度更加完善，国家治理体系和治理能力现代化水平明显提高，全社会发展活力和创新活力明显增强。'
#
#     t1 = u'首页论坛首页上次访问是 2018年-4月-15日 09:19现在的时间是 2018年-4月-16日 16:32将论坛标记为已读市场交易区域主题帖子最新文章购买物品发布区[功能: 购买物品信息发布, 交易媒介：比特币, 交易规则更新: 2018.04.14 ][注:增设投诉期, 卖家资金必须在投诉期内无投诉, 才可提币出网站]更多规则说明请进本区查看.信息发布后必须立即标注价格，买卖数量, 投诉期限，否则视为欺诈,删除账号主题: 33 主题6 帖子最新文章由 1721903095查看最新帖子2018年-4月-15日 22:22出售物品发布区[功能: 出售物品信息发布, 交易媒介：比特币, 交易规则更新: 2018.04.14 ] [注:增设投诉期, 卖家资金必须在投诉期内无投诉, 才可提币出网站]更多规则说明请进本区查看.信息发布后必须立即标注价格，买卖数量, 投诉期限，否则视为欺诈,删除账号主题: 4545 主题310 帖子最新文章由 hanhanmoney查看最新帖子2018年-4月-16日 14:17网站入口区域主题帖子最新文章测试发帖区域本站采用私密信息交流,很多新用户不熟悉,到其它区域发帖又担心违反规定或者发无用信息会被人指责此区随意发布,随意测试. 本区内容定期清空,不做保留主题: 3333 主题60 帖子最新文章由 vivi100查看最新帖子2018年-4月-15日 23:20基本知识方法网站的基本使用常用知识主题: 66 主题6 帖子最新文章由 almvdkg6查看最新帖子2018年-3月-05日 12:38个人信息发布主题帖子最新文章私人合作信息项目探讨,寻找合作,寻找技术,找出谋划策必须有目的性参与讨论，杜绝无意义的言语。暗网没有免费的午餐，不要异想天开.典型问答:有没有无风险又能赚大钱,操作简单的业务?类似话题请不要进入本区,就此作答:死滚私密讨论分区,仅显示发帖与回复之间对话主题: 638638 主题3406 帖子最新文章由 densefog245536查看最新帖子2018年-4月-16日 14:34私人买卖交易物品买卖,技术出售与求购,付费寻找劳动力资源必须有目的性参与讨论，杜绝无意义的言语。暗网没有免费的午餐，不要异想天开.典型问答:有没有无风险又能赚大钱,操作简单的业务?类似话题请不要进入本区,就此作答:死滚私密讨论分区,仅显示发帖与回复之间对话主题: 10061006 主题5369 帖子最新文章由 loveoccean查看最新帖子2018年-4月-16日 16:26其它内容区域主题帖子最新文章闲散话题聊天闲聊话题,自由讨论,信息公开禁交易买卖帖,禁推广产品、网站帖,此区出现此类信息视为垃圾广告.此区信息公开,发帖回帖信息其他人可见,请注意保密性.必须有目的性参与讨论，杜绝无意义的言语。暗网没有免费的午餐，不要异想天开.主题: 465465 主题2775 帖子最新文章由 guxing查看最新帖子2018年-4月-16日 16:29暗网欺骗揭露暗网无法追查注册用户身份,如果对方恶意欺诈,没有解决的办法若遇欺诈,拿钱就跑路等,请在此揭露,非恶意欺诈者澄清共同维护交易氛围.如果交易走的本站比特币通道,请联系管理员,可在对方提币出站前冻结主题: 3434 主题247 帖子最新文章由 almvdkg6查看最新帖子2018年-4月-16日 14:57暗网色情娱乐娱乐信息,高级游玩,色情信息由于暗网需要经过10层以上加密网络转发数据,故图片.视频传播效果不畅通应众多用户要求,特开此区,请根据网络状况自行交流信息,无人监管主题: 7474 主题1341 帖子最新文章由 wy666666查看最新帖子2018年-4月-16日 13:12CardingCarding高级技术专区,纯技术区域,负责人:TiTiTiTi主题: 66 主题38 帖子最新文章由 anxiaoxin查看最新帖子2018年-4月-15日 01:07统计信息帖子总数 22056 ? 主题总数 4409 ? 用户总数 16275 ? 最新注册的用户：nh453245首页论坛首页所有显示的时间是 UTC+08:00删除全部论坛 cookie由 phpBB? Forum Software ? phpBB Limited 提供支持 | SE Square Left by PhpBB3 BBCodes简体中文语言由 David Yin 维护'
#
#     print(txt)
#     print("--")
#     obj.summaryScoredtxt(t1)
#
#     print("----")
#     obj.summaryTopNtxt(t1)