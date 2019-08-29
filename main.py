a = [1,2,3,4,5,6,7,8,9,10]

for i in range(len(a)):
    if a[i] == 5:
        a.pop(i)

print(a)