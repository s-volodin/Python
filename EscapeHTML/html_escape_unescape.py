def replace_reserved_chars(mode):
    def html_chars_decorator(func):
        reserved_chars = {
            '&': '&amp;',
            '"': '&quot;',
            '<': '&lt;',
            '>': '&gt;'
        }
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            for key, value in reserved_chars.items():
                if mode == 'escape':
                    text = text.replace(key, value)
                elif mode == 'unescape':
                    text = text.replace(value, key)
            return text
        return wrapper
    return html_chars_decorator


@replace_reserved_chars('unescape')
def escaped_html_text(text):
    return text


@replace_reserved_chars('escape')
def html_text(text):
    return text


def main():
    not_escaped_text = ('<html><body><h2>Size Attributes</h2><p>Images in HTML have a set of "size" attributes, '
                        'which "specifies" the width & height of the image:</p><h1>Hello & Welcome</h1>')
                        
    escaped_text = ('&lt;html&gt;&lt;body&gt;&lt;h2&gt;Size Attributes&lt;/h2&gt;&lt;p&gt;Images in '
                    'HTML have a set of &quot;size&quot; attributes, which &quot;specifies&quot; ' 
                    'the width &amp; height of the image:&lt;/p&gt;&lt;h1&gt;Hello &amp; Welcome&lt;/h1&gt;')
    
    print(html_text(not_escaped_text))
    print(escaped_html_text(escaped_text))


if __name__ == '__main__':
    main()