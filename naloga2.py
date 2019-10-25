
import random
import numpy as np


def read_file(files, n=3):
    # texts is a dict of dicts, so that keys are languages, and values is a dict
    # of unique n-consecutive strings in language and their number of repetitions
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

    @staticmethod
    def cosine_similarity(language1, language2):
        # calculating cosine similarity between two languages

        # intersection of the same n-consecutive strings for dot product
        # common elements (keys) of both dicts
        common = set(language1.keys()) & set(language2.keys())
        # initialize dot product
        dot = 0
        for i in common:
            dot += (language1.get(i) * language2.get(i))

        # calculating the magnitude of vectors
        vector1 = np.array(list(language1.values()))
        vector2 = np.array(list(language2.values()))
        norm_vector1 = np.sqrt(np.sum(vector1 ** 2))  # square root of sum of square element in values of vector1
        norm_vector2 = np.sqrt(np.sum(vector2 ** 2))  # square root of sum of square element in values of vector2
        # cosine similarity
        cos = dot / (norm_vector1 * norm_vector2)
        return cos

    def k_medoids(self, n=2):
        # choose k random languages
        list_of_languages = list(self.data.keys())
        random_leaders = []
        while len(random_leaders) != n:
            leader = random.choice(list_of_languages)
            if leader not in random_leaders:
                random_leaders.append(leader)

        print(random_leaders)
        groups = {}
        for leader in random_leaders:
            groups.update({leader: set()})

        old_groups = {}  # for saving previous state of groups

        # while loop until the groups remain the same
        while groups.keys() != old_groups.keys():
            # save current groups to old_groups for comparison in while loop
            old_groups = groups

            # ----------- CREATING NEW GROUPS BECAUSE LEADERS MIGHT CHANGE ----------- #
            # iterate over all languages and see which leader it belongs
            for i in self.data:
                v = self.data.get(i)    # values of current language
                max_similarity = -1
                # remove element from current group and put it next to the right leader
                for leader in groups.keys():
                    if i in groups.get(leader):
                        groups[leader].remove(i)
                belong_to = "None"  # currently belong to nobody
                # iterate over leaders and calculating cosine distance between current language and leader language
                for leader in groups.keys():
                    values = self.data.get(leader)
                    similarity = self.cosine_similarity(values, v)  # cosine similarity
                    if max_similarity < similarity:
                        max_similarity = similarity
                        belong_to = leader
                # update current language (i) to leader who is most similar (belong_to)
                groups[belong_to].update([i])

            # ----- RECALCULATING WHO ARE THE LEADERS BECAUSE GROUPS MIGHT HAVE CHANGED ----- #
            new_groups = {}  # new dict because we cannot change one (groups) in loop
            # iterate over all groups
            for leader in groups.keys():
                group = groups.get(leader)
                dist = 0
                min_dist = -1
                new_leader = "None"
                # iterate over all elements in group and calculating
                # the distance from all elements to all other elements
                for i in group:
                    values_i = self.data.get(i)
                    for j in group:
                        if i != j:
                            values_j = self.data.get(j)
                            dist += (1 - self.cosine_similarity(values_i, values_j))    # cosine distance
                    # choosing min distance from element to all other elements as the new leader
                    if min_dist == -1 or dist < min_dist:
                        min_dist = dist
                        new_leader = i
                    dist = 0
                # setting current group new leader
                new_groups[new_leader] = group
            groups = new_groups
        print(groups)

    def run(self):
        self.k_medoids()


if __name__ == "__main__":
    DATA_FILE1 = "src3.txt"
    DATA_FILE2 = "slv.txt"
    DATA_FILE3 = "slo.txt"

    # test files
    TEST1 = "test/slo.txt"
    TEST2 = "test/svk.txt"
    TEST3 = "test/hrv.txt"
    TEST4 = "test/ang.txt"
    TEST5 = "test/nem.txt"
    TEST6 = "test/pol.txt"
    TEST7 = "test/spn.txt"
    TEST8 = "test/prt.txt"
    TEST9 = "test/itl.txt"
    DATA_FILES = [TEST1, TEST2, TEST3, TEST4, TEST5, TEST6, TEST7, TEST8, TEST9]

    KMC = KMedoidsClustering(read_file(DATA_FILES))
    KMC.run()

