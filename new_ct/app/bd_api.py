# coding=gbk
import urllib
import urllib.request
import json
def get_access_token():
    """
    ��ȡ�ٶ�AIƽ̨��Access Token
    """
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=uIIR9NvBBSnwy9pYkd6BsjUB&client_secret=Comyn1XxH7Iy8O2wczOcFIW4FVwkWn8F'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content.split(",")[3].split(":")[1]



txt = u'ʮ�˴����������꣬�ǵ��͹��ҷ�չ�����м���ƽ�������ꡣ������羭�ø��շ������ֲ���ͻ�Ͷ���Ƶ����ȫ��������Ӿ���ⲿ����������ҹ����÷�չ�����³�̬��һϵ����̱仯�����Ǽ��������������ܻ�����ӭ�Ѷ��ϣ����ؽ�ȡ��ȡ���˸ĸ￪�ź���������ִ����������ʷ�Գɾ͡�Ϊ�᳹ʮ�˴��񣬵������ٿ��ߴ�ȫ�ᣬ�ֱ�����������ĸ��ְ��ת�䡢ȫ����ĸȫ���ƽ������ι����ƶ���ʮ���塱�滮��ȫ������ε����ش��������������Ͳ���������������ͳ���ƽ�����λһ�塱���岼�֡�Э���ƽ����ĸ�ȫ�桱ս�Բ��֣���ʮ���塱�滮ʤ����ɣ���ʮ���塱�滮˳��ʵʩ�����͹�����ҵȫ�濪���¾��澭�ý���ȡ���ش�ɾ͡��ᶨ���ƹ᳹�·�չ������������չ���ת�䷢չ��ʽ����չ������Ч�治�����������ñ����и�����������������Ҫ����������ǰé������������ֵ����ʮ������Ԫ��������ʮ����Ԫ���Ⱦ�����ڶ��������羭�����������ʳ����ٷ�֮��ʮ��������ṹ�Ըĸ������ƽ������ýṹ�����Ż������־��õ����˲�ҵ���չ����������·���������ۿڡ������Ȼ�����ʩ��������ƽ���ũҵ�ִ����Ȳ��ƽ�����ʳ���������ﵽһ���ǧ�ڽ������������һ������ٷֵ㣬��ǧ����ũҵת���˿ڳ�Ϊ�����������չЭ������ǿ����һ��һ·�����衢����Эͬ��չ���������ô���չ��Ч����������������չս�Դ���ʵʩ�������͹��ҽ���ɹ���˶���칬�����������ۡ���ա�ī�ӡ���ɻ����ش�Ƽ��ɹ�����������Ϻ�������������ƽ��������;����������𲽽�ȫ������ó�ס�����Ͷ�ʡ���㴢���Ⱦ�����ǰ�С�ȫ����ĸ�ȡ���ش�ͻ�ơ��㼲�����ƽ�ȫ����ĸ����Ƴ����������ƻ��Ʊ׶ˡ��ĸ�ȫ�淢�������ͻ�ơ������ƽ���������ǿ�ĸ�ϵͳ�ԡ������ԡ�Эͬ�ԣ�ѹ����չ�ĸ��Ⱥ���ȣ��Ƴ�һǧ��ٶ���ĸ�ٴ룬��Ҫ����͹ؼ����ڸĸ�ȡ��ͻ���Խ�չ����Ҫ����ĸ������ܻ���ȷ�����й���ɫ��������ƶȸ������ƣ�����������ϵ�����������ִ���ˮƽ������ߣ�ȫ��ᷢչ�����ʹ��»���������ǿ��'
def sentiment_classify(text):
    """
    ��ȡ�ı��ĸ���ƫ������ or ���� or ������
    ������
    text:str ����
    """
    raw = {"text":"����"}
    raw['text'] = text
    data = json.dumps(raw).encode('utf-8')
    AT = get_access_token()
    host = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token="+AT
    request = urllib.request.Request(url=host,data=data)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    rdata = json.loads(content)
    return rdata

# if __name__ == '__main__':
#     print(sentiment_classify(txt))


