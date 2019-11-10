
import random
import numpy as np
import os

from unidecode import unidecode
import matplotlib.pyplot as plt


def read_file(files, n=3):
    # texts is a dict of dicts, so that keys are languages, and values is a dict
    # of unique n-consecutive strings in language and their number of repetitions
    texts = {}
    for i in files:
        f = open(i, "rt", encoding="utf8").read().\
            replace("\n", " ").\
            replace(".", " ").\
            replace(",", " ").\
            replace(";", " ").\
            replace("(", " ").\
            replace(")", " ").\
            replace("    ", " ").\
            replace("   ", " ").\
            replace("  ", " ")
        f = unidecode(f)    # unidecode for normalizing letters
        f = f.upper()   # to upper letters
        f = f.split(' ', 1)
        country_name = f[0]  # country name
        f = f[1]    # everything else is language
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
        texts.update({country_name: unique})
    return texts


class KMedoidsClustering:
    def __init__(self, data):
        self.data = data
        # memoization dictionary
        self.distances = {}

    def get_distance(self, language1, language2):
        # val1 and val2 are dictionaries of values n-consecutive strings and key that are "country" names
        if language1 in self.distances:
            distance_to = self.distances.get(language1)
            if language2 in distance_to:
                dist = distance_to.get(language2)
                return dist

        # n-consecutive strings of both languages
        val_language1 = self.data.get(language1)
        val_language2 = self.data.get(language2)

        # calculating cosine similarity
        similarity = self.cosine_similarity(val_language1, val_language2)
        distance = 1 - similarity

        # adding language to dict if not present
        if language1 not in self.distances:
            self.distances[language1] = {}
        if language2 not in self.distances:
            self.distances[language2] = {}

        # evaluating distance between languages
        self.distances[language1][language2] = distance
        self.distances[language2][language1] = distance

        return distance

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

    def select_randomly(self, k=2):
        list_of_languages = list(self.data.keys())
        random_leaders = []
        while len(random_leaders) != k:
            leader = random.choice(list_of_languages)
            if leader not in random_leaders:
                random_leaders.append(leader)
        groups = {}
        for leader in random_leaders:
            groups.update({leader: set()})
        return groups

    def reorganize_groups(self, groups):
        # ----------- CREATING NEW GROUPS BECAUSE LEADERS MIGHT CHANGE ----------- #
        # iterate over all languages and see which leader it belongs
        for i in self.data:
            max_similarity = -1
            # remove element from current group and put it next to the right leader
            for leader in groups.keys():
                if i in groups.get(leader):
                    groups[leader].remove(i)
            belong_to = "None"  # currently belong to nobody
            # iterate over leaders and calculating cosine distance between current language and leader language
            for leader in groups.keys():
                distance = self.get_distance(i, leader)     # cosine distance
                similarity = 1 - distance   # cosine similarity
                if max_similarity < similarity:
                    max_similarity = similarity
                    belong_to = leader
            # update current language (i) to leader who is most similar (belong_to)
            groups[belong_to].update([i])
        return groups

    def recalculate_leaders(self, groups):
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
                for j in group:
                    if i != j:
                        dist += self.get_distance(i, j)     # cosine distance
                # choosing min distance from element to all other elements as the new leader
                if min_dist == -1 or dist < min_dist:
                    min_dist = dist
                    new_leader = i
                dist = 0
            # setting current group new leader
            new_groups[new_leader] = group
        return new_groups

    def k_medoids(self, k=2):
        # choose k random languages
        groups = self.select_randomly(k)
        old_groups = {}  # for saving previous state of groups
        # while loop until the groups remain the same
        while groups.keys() != old_groups.keys():
            # save current groups to old_groups for comparison in while loop
            old_groups = groups
            # ----------- CREATING NEW GROUPS BECAUSE LEADERS MIGHT HAVE CHANGED ------------ #
            groups = self.reorganize_groups(groups)
            # ----- RECALCULATING WHO ARE THE LEADERS BECAUSE GROUPS MIGHT HAVE CHANGED ----- #
            groups = self.recalculate_leaders(groups)
        return groups

    def silhouette(self, groups):
        all_silhouettes = []  # storing silhouettes from each data point
        for leader in groups.keys():
            cluster = groups.get(leader)

            # ---- if only one element in cluster silhouette score is zero ---- #
            if len(cluster) < 2:
                s = 0
                all_silhouettes.append(s)
                continue

            # calculating silhouette score for each data point
            for i in cluster:
                # ---- initialization of a(i) and b(i) ----- #
                a = 0   # a(i)
                b = 0   # b(i)

                # ---------- CALCULATING a(i) ---------- #
                # calculating distance from data point i to all others points in group
                for j in cluster:
                    if i != j:
                        a += self.get_distance(i, j)    # cosine distance
                # normalization of a(i)
                a /= (len(cluster) - 1)

                # ---------- CALCULATING b(i) ---------- #
                # calculating to other clusters
                all_b = []  # for saving all b(i) to other clusters and than choosing the min
                for other_clusters_leader in groups.keys():
                    tmp_b = 0
                    if other_clusters_leader != leader:
                        other_cluster = groups.get(other_clusters_leader)
                        for j in other_cluster:
                            tmp_b += self.get_distance(i, j)    # cosine distance
                        # normalization of tmp_b
                        tmp_b /= len(other_cluster)
                        all_b.append(tmp_b)
                b = min(all_b)

                # ----- SILHOUETTE ----- #
                s = (b - a) / max(a, b)     # silhouette score of one data point
                all_silhouettes.append(s)
        # calculating the average silhouette score
        silhouette_score = sum(all_silhouettes) / len(all_silhouettes)
        return silhouette_score

    def run(self):
        k = 5
        all_silhouette_scores = []
        # storing the best and worst clusters and their silhouettes
        worst_silhouette_score = 1
        worst_clusters = {}
        best_silhouette_score = 0
        best_clusters = {}
        for i in range(0, 1000):
            clusters = self.k_medoids(k)
            silhouette_score = self.silhouette(clusters)
            all_silhouette_scores.append(silhouette_score)

            if silhouette_score < worst_silhouette_score:
                worst_silhouette_score = silhouette_score
                worst_clusters = clusters
            if silhouette_score > best_silhouette_score:
                best_silhouette_score = silhouette_score
                best_clusters = clusters

        # printing best and worst clusters
        print("--------------- BEST CLUSTERS ---------------")
        self.print_clusters(best_clusters, best_silhouette_score, "best")
        print("--------------- WORST CLUSTERS ---------------")
        self.print_clusters(worst_clusters, worst_silhouette_score, "worst")
        # --------- HISTOGRAM ---------
        self.plot_hist(all_silhouette_scores)

        print("--------------- LANGUAGE PREDICTION ---------------")
        self.find_language(best_clusters, "OSONCJE")

    @staticmethod
    def plot_hist(all_silhouette_scores):
        # plotting
        plt.hist(all_silhouette_scores, bins=50, range=(0, 1), edgecolor='black')
        plt.title("A histogram of the frequency of silhouette values at k = 5")
        plt.ylabel("Frequency")
        plt.xlabel("Silhouette score")
        plt.show()

    @staticmethod
    def print_clusters(clusters, silhouette_score, name):
        for leader in clusters.keys():
            group = clusters.get(leader)
            print(group)
            print()
        print("Silhouette score for " + name + " clusters: ", silhouette_score)
        print()

    def find_language(self, clusters, name):
        similarities = []   # for storing the similarity values
        languages = []  # for storing which language
        # calculating similarities
        for leader in clusters.keys():
            group = clusters.get(leader)
            if name in group:
                for i in group:
                    if i != name:
                        similarity = 1 - self.get_distance(name, i)
                        similarities.append(similarity)
                        languages.append(i)
        # preparing for printing out the top 3 probabilities
        zipped = zip(languages, similarities)
        sorted_probabilities = sorted(zipped, key=lambda t: t[1])
        if len(sorted_probabilities) > 2:
            sorted_probabilities = sorted_probabilities[-3:]
            sorted_probabilities.reverse()
        for language, probability in sorted_probabilities:
            print(name, " is ", language, " language with probability: ", round(probability*100, 2))


if __name__ == "__main__":
    entries = os.listdir('languages/')
    DATA_FILES = []
    for entry in entries:
        if entry[0] != '.':
            path = "languages/" + entry
            DATA_FILES.append(path)
    DATA_FILES.append("osoncje.txt")
    KMC = KMedoidsClustering(read_file(DATA_FILES))
    KMC.run()

