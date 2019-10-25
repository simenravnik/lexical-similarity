import numpy as np


def read_file(files):
    # texts is a dict of dicts, so that keys are languages, and values is a dict
    # of unique n-consecutive strings in language and their number of repetitions
    n = 3
    texts = {}
    for i in files:
        f = open(i, "rt", encoding="utf8").read().\
            replace("\n", "").\
            replace(".", " ").\
            replace(",", " ").\
            replace(";", " ").\
            replace("  ", " ").\
            upper()
        unique = {}
        # get all n-consecutive strings, and count the number of repetitions
        # default n = 3
        for j in range(n, len(f)):
            n_consecutive = f[j-n:j]
            # if n-consecutive exists, we increase their value
            if n_consecutive in unique:
                unique[n_consecutive] += 1
            else:
                # else we put new key in dict with value 1
                unique.update({n_consecutive: 1})
        # we put the count of unique n-consecutive strings in text dict
        texts.update({i: unique})

    return texts


class KMedoidsClustering:
    def __init__(self, data):
        self.data = data
        self.unique = self.get_unique()

    def get_unique(self):
        unique_elements = []
        for l in self.data:
            # unique n consecutive characters of lists
            unique_elements = list(set().union(unique_elements, l))
        return unique_elements

    def count_frequency(self, list1, list2):
        vector1 = []
        vector2 = []
        # counting number of times element appears in list1 and list2
        for element in self.unique:
            count_list1 = list1.count(element)
            count_list2 = list2.count(element)
            if count_list1 != 0 or count_list2 != 0:
                vector1.append(count_list1)
                vector2.append(count_list2)

        return vector1, vector2

    @staticmethod
    def cosine_similarity(vector1, vector2):
        # convert lists to np.array
        vector1 = np.array(vector1)
        vector2 = np.array(vector2)

        # calculating cosine distance between two vectors
        dot = np.dot(vector1, vector2)  # dot product
        norm_vector1 = np.sqrt(np.sum(vector1 ** 2))  # square root of sum of square element in values of vector1
        norm_vector2 = np.sqrt(np.sum(vector2 ** 2))  # square root of sum of square element in values of vector2
        cos = dot / (norm_vector1 * norm_vector2)

        return cos

    def k_means(self):
        for i in self.data:
            for j in self.data:
                if i != j:
                    v1, v2 = self.count_frequency(i, j)
                    dist = self.cosine_similarity(v1, v2)
                    print(dist)

    def run(self):
        self.k_means()


if __name__ == "__main__":
    DATA_FILE1 = "src3.txt"
    DATA_FILE2 = "slv.txt"
    DATA_FILE3 = "slo.txt"
    TEST = "test.txt"
    DATA_FILES = [DATA_FILE1, DATA_FILE2]

    file = read_file(DATA_FILES)

    # KMC = KMedoidsClustering(read_file(DATA_FILES))
    # KMC.run()

