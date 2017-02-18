#_*_coding=utf-8_*_
class Handler:
    """
    这个解析器会在每个块的开始调用start()和end()方法,使用合适的块名作为参数
    """
    def callback(self,prefix,name,*args):
        method = getattr(self,prefix + name,None)
        if callable(method):return method(*args)
    def start(self,name):
        self.callback('start_',name)
    def end(self,name):
        self.callback('end_',name)
    def sub(self,name):
        """
        根据markup.py文件中的addFilter函数中的re.sub(pattern,handler.sub(name),None)
        可以向handler.sub(name)函数(即substitution())传递匹配对象(match)
        这里闭包很明显是因为我们不知道匹配对象,只有根据文档才能得出匹配对象.

        返回值:返回一个经过经过处理了得block
        """
        def substitution(match):
            result = self.callback('sub_',name,match)
            if result is None: result = match.group(0)
            return result
        return substitution


class HTMLRenderer(Handler):
    def start_document(self):
        print  '<html><head><title>...</title></head<body>'
    def end_document(self):
        print '</body></html>'
    def start_paragraph(self):
        print '<p>'
    def end_paragraph(self):
        print '</p>'
    def start_heading(self):
        print '<h2>'
    def end_heading(self):
        print '</h2>'
    def start_list(self):
        print '<ul>'
    def end_list(self):
        print '</ul>'
    def start_listitem(self):
        print '<li>'
    def end_listitem(self):
        print '</li>'
    def start_title(self):
        print '<h1>'
    def end_title(self):
        print '</h1>'
    def sub_emphasis(self,match):
        return '<em>%s<em>' % match.group(1)
    def sub_url(self,match):
        return '<a href="%s">%s</a> ' %(match.group(1),match.group(1))
    def sub_mail(self,match):
        return '<a href="mailto:%s">%s</a>' %(match.group(1),match.group(1))
    def feed(self,data):
        print data

