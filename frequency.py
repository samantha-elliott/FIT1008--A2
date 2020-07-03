__Student__ = 'Samantha Elliott 30119057'

from hash_table import LinearProbeHashTable
from dictionary import Dictionary
from list import ArrayList
import string
from enum import Enum
import sys


class Rarity(Enum):

    """Best and Worst Case Time Complexity: O(1)
    enum class for rarity method"""
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    MISSPELT = 3


class Frequency(Dictionary, LinearProbeHashTable):
    def __init__(self) -> None:
        """Best and Worst Case Time Complexity: O(1)
        initialise a hash table, create an instance of the Dictionary called dictionary and read english large"""
        hash_base = 27183
        table_size = 402221
        self.dictionary = Dictionary(hash_base, table_size)
        self.dictionary.load_dictionary("english_large.txt")
        self.hash_table = LinearProbeHashTable(hash_base, table_size)
        self.max_word = 0

    def add_file(self, filename: str) -> None:
        """Best and Worst Case Time Complexity: O(n^2)
        reads each word from the file into the hash table (only if it exists in the dictionary),
        in such a way that the data associated to the word is its “occurrence count”,
        The class (and its methods) must keep track of the word which has the most occurrences"""
        f = open(filename, encoding="UTF-8")
        file = f.read()
        max_value = 0
        word_value = 0
        maxlist = []
        #strip text
        for line in file.split():
            line = line.strip("\n")
            for word in line.split():
                word = word.lower()
                word = word.strip(string.punctuation)
                if self.dictionary.find_word(word):
                    if word in self.hash_table:
                        # if the word is already in hash_table increase the count by one
                        word_value = self.hash_table.__getitem__(word) + 1
                        self.hash_table.__setitem__(word, word_value)
                    else:
                        # if it is a new word count = 1
                        self.hash_table.__setitem__(word, 1)
                    # if the frequency of the current word is higher than max set mac frequency to current and set max word to word
                    if len(maxlist) == 0:
                        if word_value > max_value:
                            max_value = word_value
                            maxlist.append(word)
                            maxlist.append(max_value)
                    else:
                        if word_value > max_value:
                            max_value = word_value
                            maxlist[0] = word
                            maxlist[1] = max_value
                    self.max_word = tuple(maxlist)


    def rarity(self, word: str) -> Rarity:
        """Best and Worst Case Time Complexity: O(n)
        given a word, returns the rairty score as enum value"""
        if not self.hash_table.__contains__(word):
            return Rarity.MISSPELT

        if self.hash_table.__contains__(word):
            occurrence_count = self.hash_table.__getitem__(word)
            max_word_value = self.max_word[1]
            if occurrence_count >= max_word_value / 100:
                # print("This is a common word")
                return Rarity.COMMON
            elif occurrence_count < max_word_value / 1000:
                # print("This is a rare word")
                return Rarity.RARE
            elif max_word_value / 100 > occurrence_count >= max_word_value / 1000:
                # print("This is a uncommon word")
                return Rarity.UNCOMMON


    def ranking(self) -> ArrayList[tuple]:
        """Best Case Time Complexity: O(nlog(n)) and worst case = O(n^2)
        returns list of words and frequencys orderd by frequency count in descending order,
        Copy all non empty tuples from hash table and insert them to ArrayList sort using quicksort, return the sorted list"""
        sys.setrecursionlimit(50000)
        array_length = self.hash_table.__len__()
        my_array = ArrayList(array_length)
        for item in self.hash_table.table:
            if item is not None:
                if type(item) != str:
                    str(item)
                    (key, value) = item
                    my_array.append(item)
                else:
                    (key, value) = item
                    my_array.append(item)

        sorted_array = self.quick_sort(my_array)
        return sorted_array

    def swap(self, array, i, j):
        """Best and Worst Case Time Complexity: O(1)"""
        array[i], array[j] = array[j], array[i]

    def quick_sort(self, array: ArrayList):
        """Best and Worst Case Time Complexity: O(n^2)"""
        start = 0
        end = len(array) - 1
        Frequency.quick_sort_aux(self, array, start, end)
        return array

    def quick_sort_aux(self, array: ArrayList, start: int, end: int):
        """Best and Worst Case Time Complexity: O(n^2)"""
        if start < end:
            boundary = Frequency.partition(self, array, start, end)
            Frequency.quick_sort_aux(self, array, start, boundary - 1)
            Frequency.quick_sort_aux(self, array, boundary + 1, end)
        return array

    def partition(self, array: ArrayList, start: int, end: int) -> int:
        """Best and Worst Case Time Complexity: O(nlog(n))"""
        mid = (start + end) // 2
        pivot = array[mid][1]
        Frequency.swap(self, array, start, mid)
        boundary = start
        for k in range(start + 1, end + 1):
            if array[k][1] > pivot:
                boundary += 1
                Frequency.swap(self, array, k, boundary)
        Frequency.swap(self, array, start, boundary)
        return boundary


def frequency_analysis() -> None:
    """Best and Worst Case Time Complexity: O(n)
    creates Frequency instance, adds single file, generates ranking list. Prompts user to input number of rankings to show. Check valid input,
    OUTPUT: ranking, word, frequency and rarity.  call function from main"""
    freq = Frequency()
    freq.add_file("84-0.txt")
    print()
    while True:
        no_of_words = input("How many words would you like to see? ")
        try:
            no_of_words = int(no_of_words)
            break;
        except ValueError:
            print("Input must be a number. Please try again")


    sorted_array = freq.ranking()
    for item in sorted_array[:no_of_words]:
        print("Ranking: ", (sorted_array.index(item)+1))
        i = sorted_array.index(item)
        print("Word: ", sorted_array[i][0])
        print("Frequency: ", sorted_array[i][1])
        print("Rarity : ", freq.rarity(sorted_array[i][0]))
        print("\n")


if __name__ == '__main__':
    f = Frequency()
    filename = ("1342-0.txt", "2600-0.txt", "98-0.txt")
    for file in filename:
        f.add_file(file)
    frequency_analysis()
