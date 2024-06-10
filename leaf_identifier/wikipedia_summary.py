'''
Tavishi Bhatia
5/20/24

Program will take the scientific name of a plant and return the wikipedia description on that plant
Program only works when connected to the internet
'''


import pandas as pd
import wikipedia

# get data from leaves.csv
leaves = pd.read_csv("leaves.csv")
# set the max length of the descriptions and the number of words in each line
max_descript_word_count = 150
line_len = 15

# wikipedia.summary() does not work for these plants
# So each of their corresponding descriptions are stored in a dictionary
wiki_page_dne = {
    "Magnolia virginiana": "Magnolia virginiana is an evergreen or deciduous tree to 30 m (100 ft) tall,"
                           " native to the lowlands and swamps of the Atlantic coastal plain of the"
                           " eastern United States, from Florida to Long Island, New York. Magnolia virginiana "
                           "is often grown as an ornamental tree in gardens, and used in horticultural "
                           "applications to give an architectural feel to landscape designs. "
                           "It is an attractive tree for parks and large gardens, grown for its "
                           "large, conspicuous, scented flowers, for its clean, attractive foliage, "
                           "and for its fast growth. In warmer areas Magnolia virginiana is valued for "
                           "its evergreen foliage.",
    "Morus alba": "Morus alba, known as white mulberry, common mulberry and silkworm mulberry,"
                  " is a fast-growing, small to medium-sized mulberry tree which grows to 10–20 m"
                  " (33–66 ft) tall. The white mulberry is widely cultivated to feed the"
                  " silkworms employed in the commercial production of silk. It is also notable "
                  "for the rapid release of its pollen, which is launched at greater than half "
                  "the speed of sound. Its berries are edible when ripe.",
    "Picea abies": "Picea abies, the Norway spruce or European spruce, is a species of spruce native "
                   "to Northern, Central and Eastern Europe. The Norway spruce has a wide distribution "
                   "for it being planted for its wood, and is the species used as the main Christmas tree "
                   "in several countries around the world."}


# get_description() takes a tree's scientific name as an input and returns a wikipedia description for that tree
def get_description(name):
    # if the plant name is not in the wiki_page_dne dictionary, get its description using wikipedia.summary()
    if not (name in wiki_page_dne):
        try:
            descript = wikipedia.summary(name)
        # some plants do not have a wikipedia page for the name recorded in the dataset,
        # but they do have a page for an alternate name of the same plant,
        # so, when a page for a plant's name does not exist, use its alternate name recorded in leaves.csv
        except wikipedia.exceptions.PageError:
            alt_name = leaves[leaves["species"] == name].alternate_name.to_list()[0]
            descript = wikipedia.summary(alt_name)
    else:
        descript = wiki_page_dne[name]
    # get rid of the description's new line characters
    descript = descript.replace("\n", "")
    # get rid of wikipedia citations
    descript_list = descript.split(" ")
    for word in descript_list:
        if "[" in word:
            descript_list.remove(word)
    # restrict the description's length to fit in the max word count
    if len(descript_list) > max_descript_word_count:
        descript_list = descript_list[0: max_descript_word_count]
        descript = " " + " ".join(descript_list)
        # prevent sentences from being cut off
        descript_list = descript.split(".")
        descript_list = descript_list[0: len(descript_list) - 1]
        descript = ".".join(descript_list) + "."
    else:
        descript = " " + " ".join(descript_list)

    # add /n characters after a certain number of words to make the description into a short paragraph
    descript_list = descript.split(" ")
    for index in range(line_len, len(descript_list), line_len):
        descript_list.insert(index, "\n")
    descript = " ".join(descript_list)

    # return the edited description
    return descript
