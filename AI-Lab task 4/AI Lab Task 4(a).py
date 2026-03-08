card_num=("5893804115457289")
# Step 1: Remove the last digit
X =int(card_num[-1])  # X variable store the last digit 
number=card_num[:-1]
print("Number after removing last digit:",number)
print("Checking digit (X):", X)
# Step 2: Reverse digits
reversed_num= number[::-1]
print("Reversed digits:", reversed_num)
# for doubling the even indices
digits=[]
for i in range(len(reversed_num)):
    num = int(reversed_num[i])
    if i % 2 == 0:
        num = num * 2
        if num > 9:
            num = num - 9
    digits.append(num)
print("After doubling even index digits:", digits)
# Step 4: Sum  of digits
total = sum(digits) + X
print("digits + X:", total)
# Step 5: Check validity of card
if total % 10 == 0:
    print("Card number is VALID")
else:
    print("Card number is INVALID")