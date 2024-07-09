from collections import defaultdict
import re

__all__ = ['NativeFilter', 'BSFilter', 'DFAFilter']
__author__ = 'observer'
__update__ = 'obaby@mars https://www.h4ck.org.cn'
__update_date__ = '2019.11.27'


class NativeFilter():
    '''Filter Messages from keywords

    very simple filter implementation

    #>>> f = NaiveFilter()
    #>>> f.add("sexy")
    #>>> f.filter("hello sexy baby")
    hello **** baby
    '''

    def __init__(self):
        self.keywords = set([])

    def parse(self, path):
        with open(path, "r") as f:
            for keyword in f:
                keyword = keyword.strip()
                if not isinstance(keyword, str):
                    keyword = keyword.decode('utf-8')
                if keyword == '':
                    continue
                self.keywords.add(keyword.lower())

    def filter(self, message, repl="*"):
        message = message.lower()
        for kw in self.keywords:
            message = message.replace(kw, repl)
        return message


class BSFilter:
    '''Filter Messages from keywords

    Use Back Sorted Mapping to reduce replacement times

    #>>> f = BSFilter()
    #>>> f.add("sexy")
    #>>> f.filter("hello sexy baby")
    hello **** baby
    '''

    def __init__(self):
        self.keywords = []
        self.kwsets = set([])
        self.bsdict = defaultdict(set)
        self.pat_en = re.compile(r'^[0-9a-zA-Z]+$')  # english phrase or not

    def add(self, keyword):
        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')
        keyword = keyword.lower()
        if keyword not in self.kwsets:
            self.keywords.append(keyword)
            self.kwsets.add(keyword)
            index = len(self.keywords) - 1
            for word in keyword.split():
                if self.pat_en.search(word):
                    self.bsdict[word].add(index)
                else:
                    for char in word:
                        self.bsdict[char].add(index)

    def parse(self, path):
        with open(path, "r") as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):
        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        for word in message.split():
            if self.pat_en.search(word):
                for index in self.bsdict[word]:
                    message = message.replace(self.keywords[index], repl)
            else:
                for char in word:
                    for index in self.bsdict[char]:
                        message = message.replace(self.keywords[index], repl)
        return message


class DFAFilter():
    '''Filter Messages from keywords

    Use DFA to keep algorithm perform constantly

    #>>> f = DFAFilter()
    #>>> f.add("sexy")
    #>>> f.filter("hello sexy baby")
    hello **** baby
    '''

    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path, encoding='UTF-8') as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*") -> tuple:
        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        ret = []
        start = 0
        match_words_list = []
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            match_words = ''
            for char in message[start:]:
                if char in level:
                    match_words += char
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    match_words = ''
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1
            if match_words != '':
                match_words_list.append(match_words)

        return ''.join(ret), match_words_list

    def is_contain_sensi_key_word(self, message):
        repl = '_-__-'
        dest_string = self.filter(message=message, repl=repl)
        if repl in dest_string:
            return True
        return False


def test_first_character():
    gfw = DFAFilter()
    gfw.add("1989年")
    assert gfw.filter("1989", "*") == "1989"


if __name__ == "__main__":
    keyword_path = 'keywords'
    native_filter = NativeFilter()
    native_filter.parse(keyword_path)

    # gfw = BSFilter()
    dfa_fitler = DFAFilter()
    dfa_fitler.parse(keyword_path)

    # print(gfw.filter("法轮功 我操操操", "*"))
    # print(gfw.filter("针孔摄像机 我操操操", "*"))
    # print(gfw.filter("售假人民币 我操操操", "*"))
    # print(gfw.filter("传世私服 我操操操", "*"))

    need_check_content = '<p>今年6月，中国汽车市场折扣率达到近3年新高，降价促销力度的加强让各大车企的销量也因此达到年内高峰。</p><p>今年6月，整体乘用车销量继续环比向上。乘用车产量为213.4万辆，同比降低2.8%，环比增长6.9%；乘用车零售销量为176.7万辆，同比降低6.7%，但是环比增长3.2%。</p><p>新能源汽车的销量则呈现同比和环比双增长的态势，新能源汽车渗透率也再次临近50%大关。</p><p><img src="https://wpimg-wscn.awtmt.com/79d992fe-c2ee-47c3-a677-99f7cf4ef40d.png" alt="" title="" data-wscntype="image" data-wscnsize="461045" data-wscnh="533" data-wscnw="865" class="wscnph"/></p><p>6月，新能源汽车产量达到93.3万辆，同比增长26.6%，环比增长5.8%；销量为85.6万辆，同比增长28.6%，环比增长6.4%。新能源汽车市场渗透率维持在高位，达到48.4%，同比增长13.5个百分点。</p><h2>1、6月汽车市场折扣率中位数创3年新高，价格战未有停歇</h2><p>年初至今，汽车行业价格战就一直保持高烈度，并在 “618大促”助攻下达到最高潮，市场平均折扣率中位数创近3年新高。</p><p>通过提供折扣、现金回馈、置换奖励和优惠金融方案等等措施，无论是以油车为主的车企如宝马、丰田、本田和长安福特等，还是新能源车企如极氪、理想、零跑和小鹏等都给出了不同程度的降价优惠，幅度在2-7万元不等。</p><p>具体来看，今年6月汽车市场的平均车型折扣率中位数达到5.9%，同比增长1.6个百分点；折扣金额高达7695 元，较去年同期增加1672 元。</p><p><img src="https://wpimg-wscn.awtmt.com/1e934ace-483e-4b4c-9202-07f9fbcef4e1.png" alt="" title="" data-wscntype="image" data-wscnsize="381160" data-wscnh="520" data-wscnw="733" class="wscnph"/></p><p>华尔街见闻·见智研究认为，经过半年的发酵，纯粹的价格下探带来的成交转化效果有所趋弱，但是在如今车型配置同质化严重，未有新的技术或设备突破的情况下，降价换量依然还是车企手上为数不多有用的策略，此次参与降价活动的众多新能源车企都因此创下历史交付量新高。</p><p>此外，临近今年上半年的销量任务考核节点，大部分的汽车经销商的库存水平却还维持在高位，今年6月中国汽车经销商库存预警指数为62.3%，同比上升8.3个百分点，环比上升4.1个百分点。为了实现上半年的销量任务目标，汽车经销商选择降价冲量也就不难理解。</p><h2>2、新能源汽车出口热度有所降温</h2><p>此前，海外市场一直是作为中国新能源汽车销量的第二增长点，2022年开始中国新能源汽车出口量就持续保持着高增长态势。不过受累于海外多个国家的电动汽车关税调整，今年二季度开始，中国新能源汽车出口量环比持续转负，并在6月呈现出口量年内新低。</p><p>具体来看，今年6月，中国整体乘用车出口量达到37.8万辆，同比增长28%，环比持平，其中，新能源汽车出口量为8万辆，环比下滑15.2%，占总出口量的比例较同期下降3个百分点至21%。</p><p><img src="https://wpimg-wscn.awtmt.com/3b4afd23-a95c-4e97-ba03-d56a401b9ad9.png" alt="" title="" data-wscntype="image" data-wscnsize="413930" data-wscnh="530" data-wscnw="781" class="wscnph"/></p><p>今年二季度开始，欧盟委员会（对中国进口电动汽车征收17.4%～38.1%的临时反补贴税）、巴西（对电动汽车的关税提升至18%-25%）和美国（对中国电动汽车征收100%关税）等都调整了对中国电动汽车的进口关税。</p><p>尽管，中国新能源车企不会因此而放缓对海外市场的开拓，但短时间内关税翻倍增长还是会对出口造成干扰。</p><p>随着关税变化，中国新能源汽车出口结构或将迎来变化，后续插电混动车型的出口量占比有望得到提升，6月纯电动车型出口占比已经降至72.6%。</p><p>以头部新能源车企比亚迪为例，最先打入日本、泰国和巴西等国家的车型均是纯电动车型——海豹、海豚和元PLUS。而今年，比亚迪力推的出口车型则换成插电混动车型——宋 PLUS DMI，以及海外特供版鲨鱼插混皮卡。</p><h2>3、6月各大新能源车企创销量新高，但年度销量目标完成率不高</h2><p>今年6月，无论是头部新能源车企比亚迪，还是造车新势力们如小米、蔚来、极氪和零跑等都创下销量历史新高。即使未能如愿突破销量纪录的车企如理想和小鹏等，也至少是年内新高，保持着销量高增长状态。</p><p><img src="https://wpimg-wscn.awtmt.com/9b950d65-b4f2-4772-9e4d-03ea38ee46c4.png" alt="" title="" data-wscntype="image" data-wscnsize="223170" data-wscnh="258" data-wscnw="865" class="wscnph"/></p><p>不过，尽管新能源车企们上半年的收官之战打得很好，但是从上半年整体的年度销量目标完成率来看，大部分新能源车企的表现并不尽如人意。</p><p>年度销量目标完成率真正过半的新能源车企却寥寥无几。</p><p>其中，屡创销量新高的比亚迪，超水平完成上半年销量目标，截止今年6月底，比亚迪的年度销量目标完成率高达44.7%。</p><p>就算在下半年销售旺季中，比亚迪的月销量不再环比增长，维持在6月的34.2万辆，比亚迪也有望超越360万辆的年销售目标。</p><p><img src="https://wpimg-wscn.awtmt.com/16b755fd-5b99-4cb9-b63a-a6363e0787e7.png" alt="" title="" data-wscntype="image" data-wscnsize="195488" data-wscnh="298" data-wscnw="656" class="wscnph"/></p><p>反观造车新势力们，它们的全年销量目标跨度较大，普遍完成率并不理想。只有极氪汽车、蔚来和理想的完成率保持在30%以上。哪吒汽车和小鹏，销量完成率都在20%以下。</p><p>各大车企6月的收官之战效果超预期，一定程度上挽回了上半年的销量颓势，但厂商之间的差距仍然十分明显。</p>'

    import time
    t = time.process_time()
    print(native_filter.filter(need_check_content))
    print('native_filter cost is %6.6f' % (time.process_time() - t))

    t = time.process_time()
    print(dfa_fitler.filter(need_check_content))
    print('dfa_fitler cost is %6.6f' % (time.process_time() - t))

    #print(gfw.is_contain_sensi_key_word('习大大'))
    #test_first_character()