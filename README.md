# Lexical-similarity

## Intro

Developed k-medoids (similar to k-means) algorithm for clustering languages into groups and predicting languages.

> The attached file ([all_languages](https://github.com/simenravnik/lexical-similarity/tree/master/all_languages)) contains the Universal Declaration of Human Rights in 263 languages. The text was typed in a record number of languages: the <a href="http://www.ohchr.org/EN/UDHR/Pages/Introduction.aspx">United Nations website</a> offered as many as 512 (so possible in the attached website). The languages was used for testing the algorithm.

## Explanation

The aim of was to develop an algorithm that, based on the analysis of similarity of languages, divides the languages into groups of similar ones. To achieve this goal, we split each language (or text) into strings of length 3 and observe the frequency of occurrence of individual triples in the text. In this way, we determined the similarity between the languages with a cosine distance and divided them all into groups using an algorithm called k-medoids clustering. Then, using the silhouette method, we evaluated how well our algorithm allocated the languages into groups.

I ran the developed k-medoids clustering algorithm with 100 randomly selected initializations of random 5 medoids. After completing the algorithm, I calculated on a case-by-case basis how well the languages were grouped using the silhouette method. I saved the silhouette values and then plotted a histogram showing how often a given silhouette value appears.

![Silhouette score histogram](https://github.com/simenravnik/lexical-similarity/blob/master/hist-eng.png "Silhouette score histogram")

When grouping, we want the elements in the group to be a little distance from each other, and to have as much distance as possible from other groups. Because we have chosen random languages for the initial leaders, it happens that groups are not formulated correctly, respectively. non-optimal groups are obtained whose elements have a relatively large distance between them and are located close to other groups. Therefore, we calculate the values of the silhouette, which tells us how well the individual groups are defined.

Out of 100 results, I selected the best and the worst, and show them below.

```bash
------------------- BEST CLUSTERS -------------------

{’ITALIAN’, ’SPANISH’, ’PORTUGUESE’, ’ENGLISH’, ’FRENCH’, ’ROMANIAN’}

{’DANISH’, ’SWEDISH’, ’ICELANDIC’, ’NORWEGIAN’}

{’SERBIAN’, ’CZECH’, ’BOSNIAN’, ’POLISH’, ’SLOVENIAN’, ’UKRAINIAN’, ’SERBIAN-CYRILLIC’, ’SLOVAK’, ’RUSSIAN’, ’BELORUS’}

{’DUTCH’, ’GERMAN’}

{’GREEK’}

Silhouette score for best clusters: 0.3093189752840624
```

```bahs
------------------- WORST CLUSTERS -------------------

{’DANISH’, ’GERMAN’, ’SWEDISH’, ’ICELANDIC’, ’DUTCH’, ’NORWEGIAN’}

{’SERBIAN’, ’CZECH’, ’POLISH’, ’SLOVENIAN’, ’UKRAINIAN’, ’SERBIAN-CYRILLIC’, ’SLOVAK’, ’RUSSIAN’, ’BELORUS’}

{’BOSNIAN’}

{’SPANISH’, ’ITALIAN’, ’PORTUGUESE’, ’FRENCH’, ’ROMANIAN’, ’GREEK’} {’ENGLISH’}

Silhouette score for worst clusters: 0.02353354501771205
```

## Language prediction

To determine the likelihood of a given text in a particular language or language. In determining which language the text is written in, I implemented the following method. First, I ran the program, with the text already included, and selected the result with the best silhouette value. So I got optimally formed groups. I then searched for which group the text was located in and calculated a cosine similarity (1 - cosine distance) to all the languages in the group. In this way, I obtained the probabilities of how similar the text is to each language.

For the text I chose a Slovenian paragraph from Wikipedia that talks about the origin and development of the solar system ([Nastanek in razvoj Osoncja](https://github.com/simenravnik/lexical-similarity/blob/master/osoncje.txt)). I got the following results:

```bash
------------------- LANGUAGE PREDICTION ------------------- 

1. OSONCJE is SLOVENIAN language with probability: 59.99
 
2. OSONCJE is BOSNIAN language with probability: 50.33

3. OSONCJE is SERBIAN language with probability: 49.77
```

In the first place is Slovenian, with almost 60% similarity to the text. So we can say that the text with sixty percent is written in Slovene. It is followed by Bosnian and Serbian with approximately 50% similarity to the text, as there are many syllables ("triples") that occur in all three languages. If more texts were still available, the similarity to the Slovenian language would increase and the other languages would be diminished.

## Also

I selected 20 randomly selected news articles online in different languages (added as an attachment [./articles/](https://github.com/simenravnik/lexical-similarity/tree/master/articles)) and watched the algorithm group them together. I reached the highest value of the silhouette when I determined that I wanted 2 groups (k = 2), 0.21. This is logical, on the one hand, because the European languages are sufficiently similar to each other to have a relatively short distance between them and therefore the value of the silhouette is so high.

```bash
------------------- CLUSTERS -------------------

{'SLOVAK', 'HINDI', 'GERMAN', 'SLOVENIAN', 'SERBIAN', 'GREEK', 'HUNGARIAN', 
 'BULGARIAN', 'SPANISH', 'FRENCH', 'AZERBAIJANI', 'ENGLISH', 'PORTUGUEESE', 
 'SWEDISH', 'ALBANIAN', 'DUTCH', 'TURKISH', 'JAPANESE'}

{'PERSIAN', 'ARABIC'}

Silhouette score:  0.21203392736969467
```

But the most useful or however, I got the correct groups when I determined 8 groups (k = 8). The value of the silhouette was 0.17 here, and we can see how the languages are properly divided into groups.

```bash
------------------- CLUSTERS -------------------

{'PERSIAN', 'ARABIC'}

{'HUNGARIAN'}

{'SLOVAK', 'SLOVENIAN', 'SERBIAN', 'BULGARIAN'}

{'GREEK', 'SPANISH', 'FRENCH', 'ENGLISH', 'PORTUGUEESE'}

{'SWEDISH', 'DUTCH', 'GERMAN'}

{'AZERBAIJANI', 'TURKISH'}

{'JAPANESE'}

{'ALBANIAN', 'HINDI'}

Silhouette score:  0.17752025492228532
```

> Note: For running algorithm on articles replace main with:

```python
if __name__ == "__main__":
    entries = os.listdir('articles/')
    DATA_FILES = []
    for entry in entries:
        if entry[0] != '.':
            path = "articles/" + entry
            DATA_FILES.append(path)
    KMC = KMedoidsClustering(read_file(DATA_FILES))
    KMC.run()
```