from cs50 import get_string

text = get_string("Text: ")
textList = list(text)
letters = 0
sentences = 0
words = 1
index = 0

length = len(text)
for i in range(0,length):
    # check if it is a sentence
    if (text[i] == '.' or text[i] == '!' or text[i] == '?'):
        sentences += 1
    # check if it is a word
    if text[i] == ' ':
        words += 1
    if text[i].isalpha():
        letters += 1

L = float(letters / words) * 100;
S = float(sentences / words) * 100;
index = (0.0588 * L) - (0.296 * S) - 15.8;

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print("Grade " + str(round(index)))