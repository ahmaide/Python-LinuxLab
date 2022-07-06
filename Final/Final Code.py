# Final
# Ahmaide Al-awawdah
from typing import TextIO

num= input("Please enter a number: ")
li=[]
counter=0
s=""
def convToDitial(n):
    s=""
    n2=n
    while(n2 >= 1):
        mod= n2%2
        s = str(int(mod)) + s
        n2 = n2/2
    return s

m=0
while(m==0):
    if num.isdigit():
        num = int(num)
        m=1
        p=pow(2, num)
        for i in range(p):
            s=convToDitial(i)
            if len(s) < num:
                s = "0"*(num - len(s)) + s
            if s.count("1") >= s.count("0"):
                li.append(s)
        #print(li)
        for i in li:
            if li.index(i) < len(li) - 1:
                print(i, end = ", ")
            else:
                print(i)
        listStr = str(li)
        try:
            fi=open("output.txt", "w")
            fi.write(listStr)
            fi.close()
        except FileNotFoundError:
            with open("output.txt", 'a+') as fi:
                fi.write(listStr)
            fi.close()



    else:
        print("Thats not a valid number!")
        num= input("Please try again: ")
