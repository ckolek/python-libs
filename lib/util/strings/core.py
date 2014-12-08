__author__ = 'ckolek'


def split_lines(string, line_separator='\n', line_length=-1, word_connector=None):
    lines = []

    while len(string) > 0:
        split_index = string.find(line_separator)

        if 0 < split_index < line_length:
            lines.append(string[0:split_index])
            string = string[split_index + 1:]
        elif 0 < line_length < len(string):
            last_char = string[line_length - 1]
            next_char = string[line_length]

            if not (last_char.isspace() and next_char.isspace()):
                if word_connector is not None:
                    lines.append(string[0:line_length - 1] + word_connector)
                    string = string[line_length - 1:]
                else:
                    space_index = None
                    for i in xrange(line_length - 1, -1, -1):
                        if string[i].isspace():
                            space_index = i
                            break

                    if space_index is not None:
                        lines.append(string[0:space_index])
                        string = string[space_index + 1:]
                    else:
                        lines.append(string[0:line_length])
                        string = string[line_length:]
            else:
                lines.append(string[0:line_length])
                string = string[line_length:]
        else:
            lines.append(string)
            string = ''

    return lines