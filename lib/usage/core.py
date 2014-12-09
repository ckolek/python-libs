__author__ = 'ckolek'

import os
from .exceptions import IllegalUsageError, InvalidInputError, OptionError
from cwk.util.strings.stringBuilder import StringBuilder
from cwk.util.strings.tableMaker import TableMaker


class Usage:
    def __init__(self, path, description=None, simple_path=False):
        if simple_path:
            self.path = os.path.basename(path)
        else:
            self.path = path

        self.description = description
        self.options = list()
        self.options_by_flag = dict()
        self.arguments = list()
        self.__required_arg_count = 0
        self.__optional_arg_count = 0

    def option(self, flags, name=None, description=None, value_type=str,
               default=None, count=1):
        option = Option(flags, name, description, value_type, default, count)

        self.options.append(option)

        self.register_option(flags, option)

    def register_option(self, flags, option):
        for flag in flags:
            self.options_by_flag[flag] = option

    def get_option(self, flag):
        option = self.options_by_flag[flag]

        if isinstance(option, OptionGroup):
            option = option.get_option(flag)

        return option

    def is_option(self, flag):
        return self.options_by_flag.has_key(flag)

    def get_option_value(self, arguments, flag, index=0):
        try:
            flag_indices = arguments.get_flag_indices(flag)
        except IndexError:
            raise OptionError('flag "' + flag + '" not specified')

        option = self.options_by_flag[flag]

        if isinstance(option, OptionGroup):
            option = option.get_option(flag)

        value = arguments.values[flag_indices[index] + 1]

        try:
            return option.value_type(value)
        except:
            raise InvalidInputError('Invalid value "' + value + '" for flag "' +
                                    flag + '"')

    def option_group(self, required=False, exclusive=False, count=1):
        group = OptionGroup(self, required, exclusive, count)

        self.options.append(group)

        return group

    def argument(self, name, description=None, value_type=str, required=True,
                 count=1):
        arg_count = len(self.arguments)

        if arg_count > 0:
            prev_arg = self.arguments[arg_count - 1]

            if required and not prev_arg.required:
                raise IllegalUsageError('required argument "' + name +
                                        '" must not follow optional argument "'
                                        + prev_arg.name + '"')
            if prev_arg.count < 0:
                raise IllegalUsageError('argument "' + name + '" must not ' +
                                        'follow variable count argument "' +
                                        + prev_arg.name + '"')

        if required:
            self.__required_arg_count += count if count > 0 else 1
        else:
            self.__optional_arg_count += count if count > 0 else 1

        argument = Argument(name, description, value_type, required, count)

        self.arguments.append(argument)

    def get_argument(self, index):
        return self.arguments[index]

    def get_required_argument_count(self):
        return self.__required_arg_count

    def get_optional_argument_count(self):
        return self.__optional_arg_count

    def get_argument_value(self, arguments, i, count=1):
        argument_index = -1

        for x in range(i):
            argument = self.arguments[x]

            if argument.count > 0:
                argument_index += argument.count
            else:
                argument_index += 1

        # TODO: finish this

    def parse(self, values):
        return Arguments(self, values)

    def __str__(self):
        string = StringBuilder()

        if self.description is not None:
            string.appendf('{!s}\n', self.description)

        summary = string.branch()
        summary.join_string = ' '
        summary.appendf('usage: {!s}', self.path)

        string.append('\n\n')

        details = string.branch()

        if len(self.options) > 0:
            details.append('options:\n')

            options_table = TableMaker(3)
            options_table.width = 80
            options_table.column_weights[1] = 0.2
            options_table.column_weights[2] = 0.8

            for option in self.options:
                summary.append(option.get_summary_part())

                if isinstance(option, UsageElement):
                    options_table.append(('  ',) + option.get_detail_parts())
                else:
                    for sub_option in option.elements:
                        options_table.append(('  ',) +
                                             sub_option.get_detail_parts())

            details.append(options_table)

        if len(self.arguments) > 0:
            if len(details) > 0:
                details.append('\n')

            details.append('arguments:\n')

            arguments_table = TableMaker(3)
            arguments_table.width = 80
            arguments_table.column_weights[1] = 0.2
            arguments_table.column_weights[2] = 0.8

            for argument in self.arguments:
                summary.append(argument.get_summary_part())

                arguments_table.append(('  ',) + argument.get_detail_parts())

            details.append(arguments_table)

        return str(string)


class UsageElement:
    def __init__(self, required, count):
        self.required = required
        self.count = count

    def get_summary_part(self):
        if self.required:
            summary = self._get_summary_part()
        else:
            summary = '[' + self._get_summary_part() + ']'

        if self.count > 0:
            summary = ' '.join([summary] * self.count)
        elif self.count < 0:
            summary += ' ...'

        return summary

    def _get_summary_part(self):
        pass

    def get_detail_parts(self):
        pass


class UsageElementGroup:
    def __init__(self, required, exclusive, count):
        self.required = required
        self.exclusive = exclusive
        self.count = count
        self.elements = []

    def get_summary_part(self):
        sep = ' | ' if self.exclusive else ' '
        summary = sep.join(map(lambda e: e._get_summary_part(), self.elements))

        if self.required:
            summary = '(' + summary + ')'
        else:
            summary = '[' + summary + ']'

        if self.count > 0:
            summary = ' '.join([summary] * self.count)
        elif self.count < 0:
            summary += ' ...'

        return summary

    def get_detail_parts(self, i):
        return self.elements[i].get_detail_parts()

    def __len__(self):
        return len(self.elements)


class NamedValueUsageElement(UsageElement):
    def __init__(self, required, count, name, description, value_type):
        UsageElement.__init__(self, required, count)

        self.name = name
        self.description = description
        self.value_type = value_type

class OptionGroup(UsageElementGroup):
    def __init__(self, usage, required, exclusive, count):
        UsageElementGroup.__init__(self, required, exclusive, count)

        self.usage = usage
        self.__option_indices = dict()

    def option(self, flags, name=None, description=None, value_type=str,
               default=None, count=1):
        option = Option(flags, name, description, value_type, default, count)

        index = len(self)

        for flag in flags:
            self.__option_indices[flag] = index

        self.elements.append(option)
        self.usage.register_option(flags, self)

    def get_option(self, flag):
        return self.elements[self.__option_indices[flag]]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Option(NamedValueUsageElement):
    def __init__(self, flags, name, description, value_type, default, count):
        NamedValueUsageElement.__init__(self, False, count, name, description,
                                        value_type)

        self.flags = flags
        self.default = default

    def _get_summary_part(self):
        if self.name is not None:
            return self.flags[0] + ' ' + self.name
        else:
            return self.flags[0]

    def get_detail_parts(self):
        if self.name is not None:
            part1 = '{!s} {!s}'.format(', '.join(self.flags), self.name)
        else:
            part1 = ', '.join(self.flags)

        if self.description is not None:
            part2 = self.description
        else:
            part2 = ''

        return part1, part2


class Argument(NamedValueUsageElement):
    def __init__(self, name, description, value_type, required, count):
        NamedValueUsageElement.__init__(self, required, count, name,
                                        description, value_type)

    def _get_summary_part(self):
        return self.name

    def get_detail_parts(self):
        part1 = self.name

        if self.description is not None:
            part2 = self.description
        else:
            part2 = ''

        return part1, part2


class Arguments:
    def __init__(self, usage, values):
        self.usage = usage
        self.values = values
        self.__flag_indices = dict()
        self.args = list()

        skip = False

        for i, value in enumerate(values):
            if skip:
                skip = False
                continue

            if value[0] == '-':
                if not usage.is_option(value):
                    raise InvalidInputError('Illegal option: ' + value)

                option = usage.get_option(value)

                if option.name is not None:
                    skip = True

                if self.__flag_indices.has_key(value):
                    self.__flag_indices[value].append(i)
                else:
                    self.__flag_indices[value] = [i]
            else:
                self.args.append(value)

        arg_count = len(self.args)

        if arg_count < usage.get_required_argument_count():
            required_argument = usage.get_argument(arg_count)

            raise InvalidInputError('Missing required argument: ' +
                                    required_argument.name)
        if arg_count > usage.get_required_argument_count() +\
                usage.get_optional_argument_count():
            raise InvalidInputError('Invalid argument "' +
                                    self.args[arg_count - 1] + '"')

    def get_flags(self):
        flags = []

        for flag, indices in self.__flag_indices.items():
            flags.extend(map(lambda i: flag, indices))

        return flags

    def get_unique_flags(self):
        return self.__flag_indices.keys()

    def get_flag_indices(self, flag):
        return self.__flag_indices[flag]

    def get_option(self, flag, index=0):
        return self.usage.get_option_value(self, flag, index)

    def has_flag(self, *flags):
        for flag in flags:
            if self.__flag_indices.has_key(flag):
                return True

        return False

    def get_arguments(self):
        return self.args

    def get_argument(self, i, count=1):
        return self.usage.get_argument_value(self, i, count)
