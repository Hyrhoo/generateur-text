import random

dots = ".?!"
ponctuation = "?,.;:!\"'()"
spaces = {"before": "?!:(«\"", "after": ",?.;:!)»\""}

# class Word:
#     def __init__(self, word):
#         self.word = word
#         self.next = {}
#         self.preview = {}
  
#     def get_nbr_next(self):
#         tot = 0
#         for next in self.next.values():
#             tot += next["nbr"]
#         return tot
  
#     def add_next(self, next):
#         if next not in self.next:
#             imp = 1 / self.get_nbr_next()
#             self.next[next] = {"nbr": 1, "imp": imp}


# data = {}   # {"word": {"infos": [nbr, coeff], "next": {"word": [nbr, coeff], "word": [nbr, coeff], ...}, "preview": {"word": [nbr, coeff], "word": [nbr, coeff], ...}}

# def add_into_data(word: str, data: dict):
#     if word in data.keys():
#         data[word] = {"infos": [1, 1], "next": {}, "preview": {}}

class Children:
    """une classe pour les liésons entre les instance de classe Word"""

    def __init__(self) -> None:
        self.total = 0
        self.data = {}
    
    def add_children(self, child):
        if child in self.data:
            self.data[child] += 1
        else:
            self.data[child] = 1
        self.total += 1
    
    def coeff_children(self, child):
        return self.data[child] / self.total


class Word:
    
    def __init__(self, word: str, nb_parent: int=5) -> None:
        self.word = word
        self.after = []
        self.before = []
        for _ in range(nb_parent):
            print(_)
            self.after.append(Children())
            self.before.append(Children())
    
    def insert_word_after(self, word, pos):
        self.after[pos].add_children(word)

    def insert_word_before(self, word, pos):
        self.before[pos].add_children(word)
    
def cut_text_to_words(text: str):    
    word = ""
    output = [""]
    
    for char in text:
        if char == "\n":
            if word:
                output += [word.lower()]
                word = ""
            output += [" "]
        
        elif char in ponctuation:
            if word:
                output += [word.lower()]
                word = ""
            output += [char]
        
        elif char == " ":
            if word:
                output += [word.lower()]
                word = ""
        
        else:
            word += char
    
    output += [""]
    return output

def load_data(graph, pertinance, *data_base):
    pass


if __name__ == "__main__":
    # import timeit
    # a="""cut_text_to_words("L'histoire de l'humanité est une chronique fascinante de la vie sur terre. Depuis l'aube de la civilisation, l'humanité a fait des progrès extraordinaires dans tous les domaines, de la science et de la technologie à l'art et à la culture. Des cultures et des civilisations entières ont émergé et disparu, laissant derrière elles des héritages durables qui ont façonné le monde tel que nous le connaissons aujourd'hui.")"""
    # print(timeit.timeit(a, "from __main__ import cut_text_to_words"))
    print(cut_text_to_words("L'histoire de l'humanité est une chronique fascinante de la vie sur terre. Depuis l'aube de la civilisation, l'humanité a fait des progrès extraordinaires dans tous les domaines, de la science et de la technologie à l'art et à la culture. Des cultures et des civilisations entières ont émergé et disparu, laissant derrière elles des héritages durables qui ont façonné le monde tel que nous le connaissons aujourd'hui.\nPourtant, l'histoire de l'humanité est également marquée par des conflits et des guerres. Les gens se sont battus pour le pouvoir, la richesse, la liberté et la survie tout au long de l'histoire. Des empires ont été érigés et détruits, des nations ont été créées et démantelées, des populations ont été déplacées et persécutées."))
