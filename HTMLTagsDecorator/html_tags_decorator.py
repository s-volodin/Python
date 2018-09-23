def add_html_tag(tag_name):
    def html_tags_decorator(func):
        def wrapper(text):
            text = '<' + tag_name + '>' + func(text) + '</' + tag_name + '>'
            return text
        return wrapper
    return html_tags_decorator


@add_html_tag('html')
@add_html_tag('div')
@add_html_tag('h1')
def text(text):
    return text


def main():
    string = '1234567890'
    result  = text(string)
    print(result)


if __name__ == "__main__":
    main()