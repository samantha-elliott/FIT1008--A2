"""Unit Testing for Task 1 and 2"""
__author__ = 'Brendon Taylor'
__docformat__ = 'reStructuredText'
__modified__ = '30/05/2020'
__since__ = '22/05/2020'
__Student__ ='Samantha Elliott 30119057'

import unittest
from hash_table import LinearProbeHashTable
from dictionary import Statistics, Dictionary


def file_len(filename: str) -> int:
    """Calculates the number of lines in a given file"""
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


class TestDictionary(unittest.TestCase):
    DEFAULT_TABLE_SIZE = 250727
    DEFAULT_HASH_BASE = 31
    DEFAULT_TIMEOUT = 10
    FILENAMES = ['english_small.txt', "english_large.txt", "french.txt"]
    RANDOM_STR = 'FIT1008 is the best subject!'

    def setUp(self) -> None:
        """ Used by our test cases """
        self.dictionary = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)

    def test_init(self) -> None:
        """ Testing type of our table and the length is 0 """
        #TO DO: ADD 2 MORE TESTS
        self.assertEqual(type(self.dictionary.hash_table), LinearProbeHashTable)
        self.assertEqual(len(self.dictionary.hash_table), 0)

    def test_load_dictionary_statistics(self) -> None:
        """ For each file, doing some basic testing on the statistics generated """
        statistics = Statistics()
        for filename in TestDictionary.FILENAMES:
            words, time, collision_count, probe_total, probe_max, rehash_count = statistics.load_statistics(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE * 2, filename, TestDictionary.DEFAULT_TIMEOUT)
            self.assertGreater(words, 0)
            self.assertLess(time, TestDictionary.DEFAULT_TIMEOUT)

        # the probe total should be greater than the probe max
        result = statistics.load_statistics(31, 10, 'english_small.txt', 10)
        self.assertGreater(result[3], result[4])

        #test to see if more word added with more time, the shorter time out limit should read less words
        long_time = statistics.load_statistics(31, 10, 'english_small.txt', 10)
        short_time = statistics.load_statistics(31, 10, 'english_small.txt', 3)
        self.assertLess(short_time[0], long_time[0])




    def test_load_dictionary(self) -> None:
        """ Reading a dictionary and ensuring the number of lines matches the number of words
            Also testing the various exceptions are raised correctly """
        for filename in TestDictionary.FILENAMES:
            self.dictionary = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)
            words = self.dictionary.load_dictionary(filename)
            lines = file_len(filename)
            self.assertEqual(words, lines, "Number of words should match number of lines")

        # tests timeout error
        with self.assertRaises(TimeoutError):
            self.dictionary.load_dictionary("english_large.txt", 1)

        # test that even with time out still saving the amount of lines counted
        self.assertNotEqual(self.dictionary.timeout_line_count, 0,
                            "Even with time out error lines counted still recorded ")

    def test_add_word(self) -> None:
        """ Testing the ability to add words """
        self.dictionary.load_dictionary('english_small.txt')
        table_size = len(self.dictionary.hash_table)
        #test if the word "samanthaelliott" is added
        self.dictionary.add_word("samanthaelliott")
        self.assertTrue(self.dictionary.find_word("samanthaelliott"))

        #test is the length is correctly updated
        self.assertEqual(len(self.dictionary.hash_table), table_size + 1)

        #test if "ppppp" is added
        self.dictionary.load_dictionary('english_small.txt')
        self.dictionary.add_word("ppppp")
        self.assertTrue(self.dictionary.find_word("ppppp"))


    def test_find_word(self) -> None:
        """ Ensuring both valid and invalid words """
        self.dictionary.load_dictionary('english_small.txt')
        #test provided random strin - should be false
        self.assertFalse(self.dictionary.find_word(TestDictionary.RANDOM_STR))
        #test "hello" - should retrun true
        self.assertTrue(self.dictionary.find_word("hello"))
        #test "the" should return true
        self.assertTrue(self.dictionary.find_word("the"))
        #test if false works correctly
        self.assertFalse(self.dictionary.find_word("samanthalouise"))

    def test_delete_word(self) -> None:
        """ Deleting valid words and ensuring we can't delete invalid words """
        self.dictionary.load_dictionary('english_small.txt')
        table_size = len(self.dictionary.hash_table)
        #test deleting phrase not in hash_table, won't get deleted, table size should remain the same
        with self.assertRaises(KeyError):
            self.dictionary.delete_word(TestDictionary.RANDOM_STR)
        self.assertEqual(len(self.dictionary.hash_table), table_size)
        #test deleting "test", word was in hash_table so length should decrease by 1
        self.dictionary.delete_word('test')
        self.assertEqual(len(self.dictionary.hash_table), table_size - 1)


if __name__ == '__main__':
    unittest.main()
