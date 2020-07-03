__Student__ ='Samantha Elliott 30119057'

from hash_table import LinearProbeHashTable
import timeit


class Dictionary(LinearProbeHashTable):
    def __init__(self, hash_base: int, table_size: int) -> None:
        """time complexity: min and max O(1) creates a new hash table with give hash base and table size"""
        self.hash_table = LinearProbeHashTable(hash_base, table_size)
        self.timeout_line_count = 0

    def load_dictionary(self, filename: str, time_limit: int = None) -> int:
        """time complexity: min and max O(n)
        reads file and adds each word to self.hash_table with 1 as associated data, raise timeout error if above timelimit"""
        start_timer = timeit.default_timer()
        try:
            file = open(filename, encoding="UTF-8")
            line_count = 0
            for line in file:
                # strips each line (one word) and removes the new line character
                strip_line = line.strip("\n")
                # adds that word to hash_table and adds int = 1 as associated data
                self.hash_table[strip_line] = 1
                if time_limit is not None:
                    if timeit.default_timer() - start_timer > time_limit:
                        raise TimeoutError
                line_count += 1
            return line_count
        except TimeoutError:
            self.timeout_line_count = line_count
            raise


    def add_word(self, word: str) -> None:
        """Best and Worst Case Time Complexity: O(1)
        adds given word to self.hash_table with int 1 as associated date"""
        word = word.lower()
        self.hash_table.__setitem__(word, 1)

    def find_word(self, word: str) -> bool:
        """ Best and Worst Case Time Complexity: O(1)
        returns true if key is in table otherwise false"""
        word = word.lower()

        try:
            _ = self.hash_table[word]
            return True
        except KeyError:
            return False

    def delete_word(self, word: str) -> None:
        """Best and Worst Case Time Complexity: O(n)
        deletes word from hash table"""
        word = word.lower()
        if self.find_word(word):
            self.hash_table.__delitem__(word)
        else:
            raise KeyError

    def menu(self) -> None:
        """Best and Worst Case Time Complexity: O(n)
        displays menu that user can choose option from """
        print()

        user = input("""1. Read File
2. Add Word
3. Find Word
4. Delete Wor
5. Exit
Enter option: """)
        if user == '1':
            print()
            filename = input("Enter filename : ")
            self.load_dictionary(filename)
            print("Successfully read file " + filename)
            self.menu()
        elif user == "2":
            print()
            word = input("Enter word : ")
            self.add_word(word)
            print(word + " Successfully added")
            self.menu()
        elif user == "3":
            print()
            word = input("Enter word : ")
            self.find_word(word)

            if self.find_word(word) == True:
                print(word + " found in dictionary")
            else:
                print(word + " not found in dictionary")
            self.menu()
        elif user == "4":
            print()
            word = input("Enter word : ")
            try:
                self.delete_word(word)
                print(word + " Deleted from dictionary")
            except KeyError:
                print("Word not in file, cannot be deleted")

            self.menu()
        elif user == "5":
            exit

        else:
            print("You must only choose 1,2,3,4,5")
            print("Please try again")
            self.menu()


class Statistics:
    def load_statistics(self, hash_base: int, table_size: int, filename: str, max_time: int) -> tuple:
        """ Best and Worst Case Time Complexity: O(n)
        creates the new dictionary with hash base and table size and return the tuples
        (words, time, collisions_count, probe_length, probe_max, rehash_count)
        words is number of words in dictionary
        time is time taken to load dict"""

        d = Dictionary(hash_base, table_size)
        try:
            time_at_start = timeit.default_timer()
            words = d.load_dictionary(filename, max_time)
            time_after_create = timeit.default_timer()
            time_taken = time_after_create - time_at_start

        except TimeoutError:
            time_taken = max_time
            words = d.timeout_line_count

        d.hash_table.statistics()
        results = (words, time_taken, d.hash_table.collision_count, d.hash_table.probe_total, d.hash_table.probe_max,
                   d.hash_table.rehash_count)
        return results


    def table_load_statistics(self, max_time) -> None:
        """ Best and Worst Case Time Complexity: O(n^2)
        for each dictionary and each combo of tablesize and hashbase uses load_statistics to time run load_dictionary, prints line to output_task2.csv"""
        TABLESIZE = (250727, 402221, 1000081)
        b = (1, 27183, 250726)
        filename = ("english_small.txt", "english_large.txt", "french.txt")
        print('file name,', 'hash_base,', 'table size,', 'number of words,', 'time taken,', 'collisions count,',
              'probe total,',
              'probe max,', 'rehash count')
        for tablesize in TABLESIZE:
            for hash in b:
                for fi in filename:
                    d = Dictionary(hash, tablesize)
                    stats = self.load_statistics(hash, tablesize, fi, max_time)
                    words = stats[0]
                    time = stats[1]
                    if time > max_time:
                        time = max_time
                    collisions = stats[2]
                    probe_total = stats[3]
                    probe_max = stats[4]
                    rehash_count = stats[5]

                    print(fi, ',', hash, ',', tablesize, ',', words, ',', time, ',', collisions, ',', probe_total, ',',
                          probe_max, ',', rehash_count)

if __name__ == '__main__':
    d = Dictionary(31, 25072)
    # file for testing called testing.txt
   # d.menu()
    s = Statistics()
    print(s.load_statistics(31, 10, 'english_small.txt', 10))
    #s.table_load_statistics(3)
