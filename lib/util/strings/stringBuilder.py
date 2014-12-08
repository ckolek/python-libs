__author__ = 'ckolek'


class StringBuilder:
    def __init__(self):
        self.parts = []
        self.join_string = ''

    def append(self, element):
        if isinstance(element, StringBuilderElement):
            element.append_to(self)
        else:
            self.parts.append(element)

        return self

    def appendf(self, fmt, *args, **kwargs):
        self.parts.append(fmt.format(*args, **kwargs))

        return self

    def branch(self):
        part = StringBuilder()

        self.parts.append(part)

        return part

    def __str__(self):
        return self.join_string.join(self.flatten())

    def flatten(self):
        return self.flatten_on(list())

    def flatten_on(self, flat_list):
        for part in self.parts:
            if isinstance(part, StringBuilder):
                if part.join_string == self.join_string:
                    part.flatten_on(flat_list)
                else:
                    flat_list.append(str(part))
            elif type(part) != str:
                flat_list.append(str(part))
            else:
                flat_list.append(part)

        return flat_list

    def __len__(self):
        return len(self.parts)


class StringBuilderElement:
    def __init__(self):
        pass

    def __str__(self):
        return self.append_to(StringBuilder()).__str__()

    def append_to(self, builder):
        return builder