import numpy as np
import copy


class HuffNode(object):
    """
    定义一个HuffNode虚类，里面包含两个虚方法：
    1. 获取节点的权重函数
    2. 获取此节点是否是叶节点的函数
    """

    def get_wieght(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'get_wieght'")

    def isleaf(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'isleaf'")


class LeafNode(HuffNode):
    """
    树叶节点类
    """

    def __init__(
            self,
            value=0,
            freq=0,
    ):
        """
        初始化 树节点 需要初始化的对象参数有 ：value及其出现的频率freq
        """
        super(LeafNode, self).__init__()
        # 节点的值
        self.value = value
        self.wieght = freq

    def isleaf(self):
        """
        基类的方法，返回True，代表是叶节点
        """
        return True

    def get_wieght(self):
        """
        基类的方法，返回对象属性 weight，表示对象的权重
        """
        return self.wieght

    def get_value(self):
        """
        获取叶子节点的 字符 的值
        """
        return self.value


class IntlNode(HuffNode):
    """
    中间节点类
    """

    def __init__(self, left_child=None, right_child=None):
        """
        初始化 中间节点 需要初始化的对象参数有 ：left_child, right_chiled, weight
        """
        super(IntlNode, self).__init__()

        # 节点的值
        self.wieght = left_child.get_wieght() + right_child.get_wieght()
        # 节点的左右子节点
        self.left_child = left_child
        self.right_child = right_child

    def isleaf(self):
        """
        基类的方法，返回False，代表是中间节点
        """
        return False

    def get_wieght(self):
        """
        基类的方法，返回对象属性 weight，表示对象的权重
        """
        return self.wieght

    def get_left(self):
        """
        获取左孩子
        """
        return self.left_child

    def get_right(self):
        """
        获取右孩子
        """
        return self.right_child


class HuffTree(object):
    """
    huffTree
    """

    def __init__(self, flag, value=0, freq=0, left_tree=None, right_tree=None):

        super(HuffTree, self).__init__()

        if flag == 0:
            self.root = LeafNode(value, freq)
        else:
            self.root = IntlNode(left_tree.get_root(), right_tree.get_root())

    def get_root(self):
        """
        获取huffman tree 的根节点
        """
        return self.root

    def get_wieght(self):
        """
        获取这个huffman树的根节点的权重
        """
        return self.root.get_wieght()

    def traverse_huffman_tree(self, root, code, char_freq):
        """
        利用递归的方法遍历huffman_tree，并且以此方式得到每个 字符 对应的huffman编码
        保存在字典 char_freq中
        """
        if root.isleaf():
            char_freq[root.get_value()] = code
            return None
        else:
            self.traverse_huffman_tree(root.get_left(), code + '0', char_freq)
            self.traverse_huffman_tree(root.get_right(), code + '1', char_freq)


def buildHuffmanTree(list_hufftrees):
    """
    构造huffman树
    """
    while len(list_hufftrees) > 1:

        # 1. 按照weight 对huffman树进行从小到大的排序
        list_hufftrees.sort(key=lambda x: x.get_wieght())

        # 2. 跳出weight 最小的两个huffman编码树
        temp1 = list_hufftrees[0]
        temp2 = list_hufftrees[1]
        list_hufftrees = list_hufftrees[2:]

        # 3. 构造一个新的huffman树
        newed_hufftree = HuffTree(1, 0, 0, temp1, temp2)

        # 4. 放入到数组当中
        list_hufftrees.append(newed_hufftree)

    # last.  数组中最后剩下来的那棵树，就是构造的Huffman编码树
    return list_hufftrees[0]


def compress(filedata):

    filesize = filedata.size

    # 保存在字典 char_freq中
    char_freq = {}
    for x in range(filesize):
        tem = filedata[x]  # python3.0 version
        if tem in char_freq.keys():
            char_freq[tem] = char_freq[tem] + 1
        else:
            char_freq[tem] = 1

    # 3. 开始构造原始的huffman编码树 数组，用于构造Huffman编码树
    list_hufftrees = []
    for x in char_freq.keys():
        # 使用 HuffTree的构造函数 定义一棵只包含一个叶节点的Huffman树
        tem = HuffTree(0, x, char_freq[x], None, None)
        # 将其添加到数组 list_hufftrees 当中
        list_hufftrees.append(tem)

    # 5. 构造huffman编码树，并且获取到每个字符对应的 编码
    char_freq1 = copy.deepcopy(char_freq)
    tem = buildHuffmanTree(list_hufftrees)
    tem.traverse_huffman_tree(tem.get_root(), '', char_freq1)

    # 6. 开始对文件进行压缩
    code = []
    for i in range(filesize):
        # key = six.byte2int(filedata[i]) #python2.7 version
        key = filedata[i]  #python3 version
        code.append(char_freq1[key])

    strcode = ''.join(code)
    return char_freq, strcode


def decompress(char_freq, strcode):

    # 3. 重建huffman 编码树，和压缩文件中建立Huffman编码树的方法一致
    list_hufftrees = []
    for x in char_freq.keys():
        tem = HuffTree(0, x, char_freq[x], None, None)
        list_hufftrees.append(tem)

    tem = buildHuffmanTree(list_hufftrees)
    tem.traverse_huffman_tree(tem.get_root(), '', char_freq)

    tempOutput = []
    currnode = tem.get_root()
    while len(strcode) > 0:
        if strcode[0] == '1':
            currnode = currnode.get_right()
        else:
            currnode = currnode.get_left()
        if currnode.isleaf():
            tempOutput.append(currnode.get_value())
            currnode = tem.get_root()
        strcode = strcode[1:]
    return np.array(tempOutput, dtype=float)
