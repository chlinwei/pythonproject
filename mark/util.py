#_*_coding=utf-8 _*_

def lines(file):
    for line in file:
        yield  line
    yield  '\n'

def blocks(file):
    """
    文本块生成器
    """
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip() #去除block前后的空格
            block = []

