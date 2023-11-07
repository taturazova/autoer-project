from gibberish import Gibberish
gib = Gibberish()
print(gib.generate_word())
print(gib.generate_word(start_vowel=True))
print(gib.generate_word(end_vowel=True))
print(print(gib.generate_words(3)))