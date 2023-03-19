import random
from bisect import bisect_left, insort_left

dots = ".?!"
ponctuation = "?,.;:!\"'()-«»…"
spaces = {"before": "?!:(«\"", "after": "…,?.;:!)»\""}


    # ===== classes ===== #


class Children:
    """une classe pour les liésons entre les instance de classe Word"""

    def __init__(self, coeff) -> None:
        self.coeff = coeff
        self.total = 0
        self.data = {}
    
    def __repr__(self) -> str:
        return f"{self.data}"
    
    def add_children(self, child):
        if child in self.data:
            self.data[child] += self.coeff
        else:
            self.data[child] = self.coeff
        self.total += self.coeff
    
    def coeff_children(self, child):
        return self.data[child] / self.total


class Word(str):
    
    def __new__(cls, word, _=0) -> object:
        return str.__new__(cls, word)

    def __init__(self, word, nb_parent=0) -> None:
        super().__init__()
        self.word = word
        self.after = []
        self.before = []
        self.nb_parent = nb_parent
        # self.total_multi = round((nb_parent*(nb_parent+1))/2)
        for i in range(nb_parent, 0, -1):
            self.after.append(Children(i))
            self.before.append(Children(i))

    def insert_word_after(self, word, pos):
        self.after[pos].add_children(word)

    def insert_word_before(self, word, pos):
        self.before[pos].add_children(word)
    
    def calcule_possible_next(self, last_words):
        possible = {}
        return ({"": 1}, 1)
        #for word in self.after[0].data:
        #    pass



    # ===== fonctions ===== #


def get_index(tab, x):
    pos = bisect_left(tab, x)
    return pos if pos != len(tab) and tab[pos] == x else -1


def cut_data_to_texts(data: str) -> str:
    """charge un fichier .txt et le coup en textes

    Args:
        data (str): nom du fichier à charger

    yield:
        str: un texte contenue dans le fichier
    """
    with open(data+'.txt', "r", encoding="utf-8") as f:
        texts = f.read().split("/")
        
    for text in texts:
        yield text.strip("\n")


def cut_text_to_words(text: str) -> str:
    """découpe un texte en mots

    Args:
        text (str): le texte à découper

    Yields:
        str: un mot du texte
    """
    yield ""
    yield " "
    word = ""
    
    for char in text:
        if char == "\n":
            if word:
                yield word.lower()
                word = ""
            yield " "
        
        elif char in ponctuation:
            if word:
                yield word.lower()
                word = ""
            yield char
        
        elif char == " ":
            if word:
                yield word.lower()
                word = ""
        
        else:
            word += char
    
    if word: yield word
    yield " "
    yield ""


def load_data(graph: list[Word], nb_parent: int, *data_base: str):
    """charge toutes les données dans le format de donnée prévue

    Args:
        graph (list[Word]): le graph dans lequel sauvgarder les données
        nb_parent (int): le nombre de mot avant et après chaque mot enregistrer
    """
    for data in data_base:
        
        for text in cut_data_to_texts(data):
            last_words: list[Word] = []
            
            for word in cut_text_to_words(text):
                word = Word(word, nb_parent)
                
                if (i:=get_index(graph, word)) != -1:
                    word = graph[i]
                
                else:
                    insort_left(graph, word)
                
                for index in range(len(last_words)):
                    last_word = last_words[index]
                    last_word.insert_word_after(word, (len(last_words) - index - 1))
                    word.insert_word_before(last_word, (len(last_words) - index - 1))
                
                add_last_word(last_words, word, nb_parent)


def add_last_word(last_words: list[Word], word: Word, nb_parent: int):
    """ajoute un mot dans la liste des derniers mots

    Args:
        last_words (list[Word]): la liste dans lequel ajouter le mot
        word (Word): le mot à ajouter
        nb_parent (int): la taile max de la liste
    """
    last_words.append(word)
    while len(last_words) > nb_parent:
        del last_words[0]


def select_random_word(words, total_coeff):
    nb_aleatoire = random.randint(0, total_coeff)
    cumulative_coef = 0
    for mot, coef in words.items():
        cumulative_coef += coef
        if nb_aleatoire <= cumulative_coef:
            return mot


def assemble_words(words):
    sentence = ""
    add_space = False
    maj = True
    for word in words:
        if word == "":
            continue
        if word == " ":
            sentence += "\n"
            maj = True
        
        elif word in ponctuation:
            if word in spaces["before"]: sentence += " "
            sentence += word
            if word in spaces["after"]: sentence += " "
            if word in dots: maj = True
            add_space = False
        else:
            if add_space:
                sentence += " "
            
            if maj:
                maj = False
                word = word.capitalize()
            
            sentence += word
            add_space = True
    return sentence



def generat_text(pertinence: int, graph: list[Word], start: str=""):
    words = []
    for word in cut_text_to_words(start):
        if (i:=get_index(graph, word)) != -1:
            words.append(graph[i])
        else:
            return "- Mot inconnue -"
    words.pop()
    words.pop()

    last_words = []
    for word in words:
        add_last_word(last_words, word, pertinence)
    
    word = words[-1]
    while last_words[-1]:
        possible, total = word.calcule_possible_next(last_words)
        word = select_random_word(possible, total)
        add_last_word(last_words, word, pertinence)
        words.append(word)

    return assemble_words(words[2:])


def main():
    """boucle principal du programme"""
    quit_str = "exit"
    pertinence = 10
    graph = []
    load_data(graph, pertinence, "learn")
    run = True
    while run:
        start = input(f"premier mot ('{quit_str}' pour quitter): ")
        if start == quit_str:
            run = False
            continue
        print("\n"+generat_text(pertinence, graph, start)+"\n")


if __name__ == "__main__":
    main()
    # graph = []
    # load_data(graph, 1, "learn")
    # print(graph)
    # for i in graph[graph.index(" ")].before:
    #    print(i)
    #    print(i.total)
