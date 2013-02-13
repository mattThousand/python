my_string=raw_input()


words=my_string.split(' ')

palindromes=[]
for word in words:
    if list(word)==list(reversed(list(word))):
        palindromes.append(word)
    else:
        continue

for i in palindromes:
    print '%s: %i' % (i, len(i))