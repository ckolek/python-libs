__author__ = 'ckolek'

from core import *
from stringBuilder import StringBuilder


class TableMaker:
    def __init__(self, columns):
        self.columns = columns
        self.rows = 0
        self.data = tuple(map(lambda i: list(), range(columns)))
        self.data_lens = [0] * columns
        self.column_weights = [0] * columns
        self.width = -1

    def append(self, row):
        assert(len(row) == self.columns)

        for i, datum in enumerate(row):
            if type(datum) != str:
                datum = str(datum)

            self.data[i].append(datum)

            datum_len = len(datum)

            if datum_len > self.data_lens[i]:
                self.data_lens[i] = datum_len

        self.rows += 1

    def __str__(self):
        column_widths = self.get_column_widths()
        columns = range(self.columns)

        string = StringBuilder()

        for j in range(self.rows):
            row = map(lambda i: split_lines(self.data[i][j],
                                            line_length=column_widths[i]),
                       columns)
            row_heights = map(lambda d: len(d), row)

            for jj in range(max(row_heights)):
                for i in columns:
                    text = row[i][jj] if jj < row_heights[i] else ' '

                    if i < self.columns - 1:
                        string.append(text.ljust(column_widths[i]))
                    else:
                        string.append(text)

            string.append('\n')

        return str(string)

    def get_column_widths(self):
        if self.width <= 0:
            return self.data_lens
        else:
            weight_sum = sum(self.column_weights)
            weights = map(lambda w: float(w) / weight_sum, self.column_weights)

            columns = range(self.columns)

            width = self.width - sum(map(lambda i:
                                         self.data_lens[i]
                                         if weights[i] == 0 else 0,
                                         columns))
            widths = map(lambda i:
                         int(weights[i] * width)
                         if weights[i] > 0 else self.data_lens[i],
                         columns)

            return widths