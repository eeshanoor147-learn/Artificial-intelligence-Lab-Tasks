# this is for case sensetive (follow by defult ascii order)
sentence = input("Enter the string:")
split_words = sentence.split()
sorted_words = sorted(split_words)
sorted_sentence = " ".join(sorted_words)
print(sorted_sentence)

# this is for insensetive
sentence = input("Enter the string:")
split_words = sentence.split()
sorted_words = sorted(split_words,key=str.lower)
sorted_sentence = " ".join(sorted_words)
print(sorted_sentence)
