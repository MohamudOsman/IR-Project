# from textblob import Word
from autocorrect import Speller




def check_spelling(stringlist):
        spell = Speller(lang='en')

        spells = [spell(w) for w in (stringlist)]

        # return " ".join(spells)
        return spells