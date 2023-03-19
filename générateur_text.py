import random

dots = ".?!"
ponctuation = "?,.;:!\"'()-«»…"
spaces = {"before": "?!:(«\"", "after": "…,?.;:!)»\""}


    # ===== classes ===== #


class Children:
    """une classe pour les liésons entre les instance de classe Word"""

    def __init__(self) -> None:
        self.total = 0
        self.data = {}
    
    def __repr__(self) -> str:
        return f"{self.data}"
    
    def add_children(self, child):
        if child in self.data:
            self.data[child] += 1
        else:
            self.data[child] = 1
        self.total += 1
    
    def coeff_children(self, child):
        return self.data[child] / self.total


class Word(str):
    
    def __new__(cls, word, _=0):
        return str.__new__(cls, word)

    def __init__(self, word, nb_parent=0) -> None:
        super().__init__()
        self.word = word
        self.after = []
        self.before = []
        self.nb_parent = nb_parent
        self.total_multi = round((nb_parent*(nb_parent+1))/2)
        for _ in range(nb_parent):
            self.after.append(Children())
            self.before.append(Children())

    def insert_word_after(self, word, pos):
        self.after[pos].add_children(word)

    def insert_word_before(self, word, pos):
        self.before[pos].add_children(word)


    # ===== fonctions ===== #


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
    word = ""
    yield ""
    yield " "
    
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
                
                if word in graph:
                    word = graph[graph.index(word)]
                
                else:
                    graph.append(word)
                
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


def generat_text(pertinence: int, graph: list[Word], start: str=""):
    if start not in graph:
        return start
    word = graph[graph.index(start)]
    last_words = [start]


def main():
    """boucle principal du programme"""
    quit_str = "$*"
    pertinence = 10
    graph = []
    load_data(graph, pertinence, "learn")
    run = True
    while run:
        start = input(f"premier mot ('{quit_str}' pour quitter): ")
        if start == quit_str:
            run = False
            continue
        print(generat_text(pertinence, graph, start))


if __name__ == "__main__":
    main()
    # graph = []
    # load_data(graph, 1, "learn")
    # for i in graph[graph.index(" ")].after:
    #     print(i)
    #     print(i.total)
