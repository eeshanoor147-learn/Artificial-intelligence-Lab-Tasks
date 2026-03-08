punctuations="!~@#$%^&*()_+`-=[\"]|\';:'/.,?><{}``"
user=input("Enter the string:")
new_string=""
for char in user:
    if char not in punctuations:
       new_string+=char
print("NEW string after removing punctuation is :",new_string)       