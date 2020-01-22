import pickle


class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = []
        """
        ["1st_line", "2nd_line", "3rd_line", ...]
        Example:
        "How are you?\nI am fine.\n" will be stored as
        ["How are you?", "I am fine." ]
        """

        self.index = {}
        """
        {word1: [line_number_of_1st_occurrence,
                 line_number_of_2nd_occurrence,
                 ...]
         word2: [line_number_of_1st_occurrence,
                  line_number_of_2nd_occurrence,
                  ...]
         ...
        }
        """

        self.total_msgs = 0
        self.total_words = 0

    def get_total_words(self):
        return self.total_words

    def get_msg_size(self):
        return self.total_msgs

    def get_msg(self, n):
        return self.msgs[n]

    def add_msg(self, m):
        """
        m: the message to add

        updates self.msgs and self.total_msgs
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        # update list and increment counter
        # must right-stripe the return char
        self.msgs.append(m.rstrip("\n"))
        self.total_msgs += 1

        # ---- end of your code --- #
        return

    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    def indexing(self, m, l):
        """
        updates self.total_words and self.index
        m: message, l: current line number
        """

        # IMPLEMENTATION
        # ---- start your code ---- #
        # must first right stripe the return char
        m = m.rstrip("\n")
        # Split msg by space
        for word in m.split(" "):
            self.total_words += 1
            if word in self.index.keys():
                # word already exists, append line number to the list
                self.index[word].append(l)
            else:
                # word doesn't exist, create new list
                self.index[word] = [l]

        # ---- end of your code --- #
        return

    # implement: query interface

    def search(self, term):
        """
        return a list of tupple.
        Example:
        if index the first sonnet (p1.txt),
        then search('thy') will return the following:
        [(7, " Feed'st thy light's flame with self-substantial fuel,"),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (12, ' Within thine own bud buriest thy content,')]
        """
        msgs = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        # check if term exists in keys
        if term in self.index.keys():
            # iterate all the index
            for l in self.index[term]:
                msgs.append((l, self.msgs[l]))

        # ---- end of your code --- #
        return msgs


class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()

    def load_poems(self):
        """
        open the file for read, then call
        the base class's add_msg_and_index()
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        file = open("AllSonnets.txt", "r")

        # iterate all the lines and call parent function
        for line in file:
            super().add_msg_and_index(line)
        # release resource
        file.close()

        # ---- end of your code --- #
        return

    def get_poem(self, p):
        """
        p is an integer, get_poem(1) returns a list,
        each item is one line of the 1st sonnet

        Example:
        get_poem(1) should return:
        ['I.', '', 'From fairest creatures we desire increase,',
         " That thereby beauty's rose might never die,",
         ' But as the riper should by time decease,',
         ' His tender heir might bear his memory:',
         ' But thou contracted to thine own bright eyes,',
         " Feed'st thy light's flame with self-substantial fuel,",
         ' Making a famine where abundance lies,',
         ' Thy self thy foe, to thy sweet self too cruel:',
         " Thou that art now the world's fresh ornament,",
         ' And only herald to the gaudy spring,',
         ' Within thine own bud buriest thy content,',
         " And, tender churl, mak'st waste in niggarding:",
         ' Pity the world, or else this glutton be,',
         " To eat the world's due, by the grave and thee.",
         '', '', '']
        """
        poem = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        # call function to load all sonnets
        self.load_poems()

        # get the line number of the start line
        line_start = super().search(str(self.int2roman[p]) + ".")[0][0]

        # the first line of the next sonnet (if exists)
        next_roman = str(self.int2roman[p + 1]) + "."

        # continue to read line from the start line
        # until the end or the next sonnet
        cursor = line_start
        # here with the short-circuit logic,
        # there won't be index-out-of-range exception
        while cursor < len(self.msgs) and self.msgs[cursor] != next_roman:
            poem.append(self.msgs[cursor])
            cursor += 1

        # ---- end of your code --- #
        return poem
'''
More improvement:

1\  when indexing the word, left-strip and right-strip all the punctuation
    when searching, not using the index dict, but to iterate every line
    and check if the line is equal to "IIX\n"

2\  list(set(msg)), then the duplicates are removed

3\  search the first word in the phrases,
    and then iterate them to check if the word next to them is
    the same as the second word in the phrase,
    then the third one, the forth one, and so on
'''

if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    # the next two lines are just for testing
    p3 = sonnets.get_poem(3)
    print(p3)
    s_love = sonnets.search("love")
    print(s_love)
