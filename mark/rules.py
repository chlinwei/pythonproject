#_*_coding=utf-8_*_
class Rule:
    def action(self,block,handler):
        """
        所有规则的基类
        """
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    """
    标题占一行,最多70个字符,并且不是以冒号结尾
    """
    type = 'heading'
    def condition(self,block):
        return not '\n' in block and len(block) <=70 and not block[-1] == ':'

class TitleRule(HeadingRule):
    """
    题目是文档的第一个块,但前提是它是个大标题
    first是个类成员变量,主要是用来判断第一个块是否是题目,后面的block判断时,first始终为False
    """
    type = 'title'
    first = True
    def condition(self,block):
        if not self.first:return  False
        self.first = False
        return HeadingRule.condition(self,block)

class ListItemRule(Rule):
    """
    列表项是以连字符开始的段落,作为格式化的一部分,要移除连字符
    重写基类的action函数,因为连字符是不需要的
    """
    type = 'listitem'
    def condition(self,block):
        return block[0] == '-'

    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return  True

class ListRule(ListItemRule):
    """
    列表从不是列表项的块和随后的列表项之间,在最后一个连续的列表项之后结束
    重写action函数
    """
    type = 'list'
    inside = False
    def condition(self,block):
        return  True
    def action(self,block,handler):
        if not self.inside and ListItemRule.condition(self,block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not  ListItemRule.condition(self,block):
            handler.end(self.type)
            self.inside = False
        return False

class ParagraphRule(Rule):
    """
    段落只是其他规则没有覆盖到的块
    """
    type = 'paragraph'
    def condition(self,block):
        return  True


