class HTML:
    def __init__(self, output):
        self.output = output
        self.items = []
    def __iadd__(self, other):
        self.items.append(other)
        return self
    def __str__(self):
        child = ""
        for item in self.items:
            child += str(item)
        html = "<html>\n{}</html>".format(child)
        return html
    def __enter__(self):
        return self
    def __exit__(self, *args, **kwargs):
        print(str(self))
        with open(self.output, "w") as file:
            file.write(str(self))
class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.items = []
    def __str__(self):
        child = ""
        for item in self.items:
            child += str(item)
        tagtext = "<{tag}>{child}</{tag}>\n".format(tag=self.tag, child=child) #add==================
        return tagtext
    def __enter__(self):
        return self
    def __exit__(self, *args, **kwargs):
        pass
    def __iadd__(self, other):
        self.items.append(other)
        return self
class Tag:
    def __init__(self, tag, is_single=None, klass = None, **otherattrs):
        self.tag = tag
        self.is_single = is_single
        self.items = []
        self.klass = ""
        self.otherattrs = ""
        self.text = ""
        if klass is not None: #записываем содержимое klass в строку
            attrib = {}
            attrib["class"] = " ".join(klass)
            for key, value in attrib.items():
                self.klass = ' {} = "{}"'.format(key, value)
        for key, value in otherattrs.items(): #именованные аргументы записываем в строку
            self.otherattrs += ' {} = "{}"'.format(key, value)
    def __enter__(self):
        return self
    def __exit__(self, *args, **kwargs):
        pass
    def __str__(self):
        if self.is_single:
            return "    <{}{}{}>".format(self.tag, self.klass, self.otherattrs)
        else:
            if self.text:
                text = "{}".format(self.text)
            else:
                text = ""
            for item in self.items:
                    text += str(item)
            return "\n    <{}{}{}>{}</{}>\n".format(self.tag,self.klass, self.otherattrs, text, self.tag)
    def __iadd__(self, other):
        self.items.append(other)
        return self
if __name__ == '__main__':
    with HTML(output="test.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "Hello, world"
                head += title
            doc += head
        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "Another text"
                    div += paragraph
                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img
                body += div
            doc += body