from bitarray import bitarray

import mmh3

class BloomFilter(set):
    def __init__(self,size,hash_count):
        super(BloomFilter,self).__init__()
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.size = size
        self.hash_count = hash_count

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.bit_array)

    def add(self,item):
        for ii in range(self.hash_count):
            index = mmh3.hash(item,ii) % self.size
            self.bit_array[index] = 1

        return self

    def __contains__(self, item):
        out = True
        for ii in range(self.hash_count):
            index = mmh3.hash(item,ii) % self.size
            if self.bit_array[index] == 0:
                out = False
        return out


if __name__ == '__main__':
    bloom = BloomFilter(100,10)
    urls = ['www.baidu.com', 'www.sohu.com', 'www.163.com', 'www.1234.com', 'www.alibaba.com', 'www.tisor.com', 'www.wudi.com',
               'www.haha.com', 'www.hehe.com', 'www.123.com', 'www.csdn.com', 'www.stack.com', 'www.anaconda.com', 'www.python.com'
            ]

    #先将animals添加进bloom filter里
    for url in urls:
        bloom.add(url)


    for url in urls:
        if url in bloom:
            print("{} is in the bloom!".format(url))
        else:
            print("Something went wrong!")

    other_animals = ['www.baidu.com/haha','www.baidu.com/1a','www.baidu.com/2b','www.baidu.com/3c']
    for other_animal in other_animals:
        if other_animal.split('/')[0] in bloom:
            print("{} is also in the bloom".format(other_animal))
        else:
            print("AAAAAAAAAAAA")


