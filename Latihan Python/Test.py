import math
import os
import random
import re
import sys

#import math
# def area(radius):
#     temp = math.pi * radius**2
#     return temp
# print(area(5))

# def absoluteValue(x): 
#     if x < 0: 
#         return -x 
#     else: 
#         return x
# print(absoluteValue(-3))

# def distance(x1, y1, x2, y2):
#     dx = x2 - x1
#     dy = y2 - y1
#     print ("dx is", dx)
#     print ("dy is", dy)
#     return 0.0
# print(distance(3.14, 2.2, 4.4, 4.3))

# def diagonal(arr):
#     # arr = [11,2,4,4,5,6,10,8,-12]
#     diag1 = 0
#     diag2 = 0
#     for i in range(0,len(arr)):
#         diag1 = diag1 + arr[i][i]
    
#     for j in range(0,len(arr)):
#         diag2 = diag2 + arr[j][len(arr)-1-j]
    
#     return abs(diag1 - diag2)

# print(diagonal([[11,2,4],[4,5,6],[10,8,-12]]))

# def plusMinus(arr):
#     # Write your code here
#     positif = 0
#     negatif = 0
#     zero = 0
#     for i in range(0,len(arr)):
#         if arr[i] > 0:
#             positif = positif + 1
#         elif arr[i] < 0:
#             negatif = negatif + 1
#         else:
#             zero = zero + 1

#     pst = (positif/len(arr))
#     ngt = (negatif/len(arr))
#     zro = (zero/len(arr))
#     print('{:.6f}'.format(pst))
#     print('{:.6f}'.format(ngt))
#     print('{:.6f}'.format(zro))

# print(plusMinus([-4,3,-9,0,4,1]))

# def staircase(n):
#     # Write your code here
#     for i in range(0,n):
#         for j in range(0,n):
#             if i + j >= n - 1:
#                 print("#",end='')
#         else:
#                 print(" ",end='')
#         print('\r')

# print(staircase(6))

# def data(n):
#     for x in range(1,n+1):
#         print(' '*(n-x)+'#'*x)

# (data(6))

# def miniMax(arr):
#     # sum1 = sum(arr[:4])
#     # sum2 = sum(arr[1:])
#     sum1 = sum(arr) - max(arr)
#     sum2 = sum(arr) - min(arr)
#     # print (sum,max[:4],sum,min[1:])
#     print (sum1,sum2)
# print(miniMax([1,2,3,4,5]))

# list = [1,2,3,4,5]
#print(sum(min(list[:4])))
# print()

#def birthday(candles):
    # count = 0
    # arr = candles[0]
    # for i in range(0,len(candles)):
    #     if candles[i] > arr:
    #         arr = candles[i]
    # for i in range(0,len(candles)):
    #     if candles[i] == arr:
    #         count = count + 1
    # return count

#     count=0
#     big = max(candles)
#     for i in range(len(candles)):
#         if(candles[i]==big):
#             count+=1
#     return count

# print(birthday([3,2,1,3]))

# def clock(s):
#     if s[-2:] == 'AM' and s[:2] == '12':
#         return '00' + s[2:-2]
#     elif s[-2:] == 'AM':
#         return s[:-2]
#     elif s[-2:] == 'PM' and s[:2] == '12':
#         return s[-2:]
#     else:
#         return str(int(s[:2])+12)+s[2:-2]

# print(clock('07:05:45PM'))

# def gradingStudents(grades):
#     for i in range(len(grades)):
#         nilai = grades[i]
#         if grades[i] < 38:
#             continue
#         elif grades[i] % 5 >= 3:
#             nilai = nilai +2
#         return grades

# print(gradingStudents([73,67,38,33]))

# def gradingStudents(grades):
#     for i in range(len(grades)):
#         nilai = grades[i]
#         result = nilai % 5
#         if grades[i] < 38 :
#             grades[i] = nilai
#         else:
#             if result == 3:
#                 nilai = nilai + 2
#                 grades[i] = nilai
#             elif result == 4 :
#                 nilai +=1
#                 grades[i] = nilai
#     return grades
# print(gradingStudents([73, 67, 38, 34]))
# print(gradingStudents([84, 69, 39, 33, 66]))

# def appleorange(s,t,a,b,apples,oranges):
#     count_apple = 0
#     count_orange = 0
#     for x in range(len(apples)):
#         if apples[x] + a >= s and apples[x] + a <= t:
#             count_apple += 1
#     for y in range(len(oranges)):
#         if oranges[y] + b >= s and oranges[y] + b <= t:
#             count_orange += 1

#     print(count_apple)
#     print(count_orange)
# (appleorange(7,11,5,15,[-2,2,1],[5,-5]))

# def kangguru(x1,v1,x2,v2):
#     if x2 > x1 and v2 > v1:
#         return 'NO'
#     elif x1 < x2 and v1 < v2:
#         return 'NO'
#     else:
#         if v1-v2 != 0:
#             hasil = (x1-x2) % (v1-v2)
#             if hasil == 0:
#                 return 'YES'        
#             else:
#                 return 'NO'
#         else:
#             return 'NO'

# print(kangguru(0,3,4,2))
# print(kangguru(0,2,5,3))
# print(kangguru(2,1,1,2))
#print(kangguru(43,2,70,2))

# from tkinter import E


# def getTotalX(a,b):
#     c = []
#     d = []
#     e = []
#     for x in range(1, 101):
#         for num in a:
#             if x % num == 0:
#                 c.append(x)
#         for num1 in b:
#             if num1 % x == 0:
#                 d.append(x)
#     z = c+d
#     for y in range(len(z)):
#         if z.count(z[y]) == len(a+b):
#             e.append(z[y])
#     return len(set(e))
# print(getTotalX([2,4],[16,32,96]))

# def breaking(scores):
#     count_high = 0
#     highest_scores = scores[0]
#     count_low = 0
#     lowest_scores = scores[0]
#     for i in range(len(scores)):
#         if highest_scores < scores[i]:
#             count_high += 1
#             highest_scores = scores[i]
#     for y in range (len(scores)):
#         if lowest_scores > scores[y]:
#             lowest_scores = scores[y]
#             count_low += 1
#     return count_high, count_low
# print(breaking([10,5,20,20,4,5,2,25,1]))
# print(breaking([3,4,21,36,10,28,35,5,24,42]))

# def dayOfProgrammer(year):
#     if (year == 1918):
#         return '26.09.1918'
#     elif ((year <= 1917) & (year%4 == 0)) or ((year > 1918) & (year%400 == 0 or ((year%4 == 0) & (year%100 != 0)))):
#         return '12.09.' + str(year)
#     else:
#         return '13.09.' + str(year)
# print(dayOfProgrammer(2017))
# print(dayOfProgrammer(2016))
# print(dayOfProgrammer(1800))

# def sockMerchant(n, ar):
#     pair = 0
#     warna = set(ar)
#     for i in warna:
#         pair += ar.count(i) // 2
#     return pair
# print(sockMerchant(9,[10, 20, 20, 10, 10, 30, 50, 10, 20]))

# def pageCount(n, p):
#     return min(p//2,n//2 - p//2)

# print(pageCount(5,4))

# def countingValleys(steps, path):
#     level = 0
#     valleys = 0
#     for x in path:
#         if x == 'U':
#             level += 1
#             if level == 0:
#                 valleys += 1
#         else:
#             level -= 1
#     return valleys

# def countingValleys(steps, path):
#     level = 0
#     valley = 0
#     for i in steps:
#         if i == 'U':
#             level  += 1
#         elif 

# def getMoneySpent(keyboards, drives, b):
#     total = -1
#     for i in keyboards:
#         for j in drives:
#             if i+j <= b:
#                 total = max(total,i+j)
#     return total
# print(getMoneySpent([10,2,3],[3,1],[5,2,8]))
# print(getMoneySpent([5,1,1],[4],[5]))

# def catAndMouse(x, y, z):
#     a = abs(x-z)
#     b = abs(z-y)
#     if a<b:
#         return('Cat A')
#     elif b<a:
#         return('Cat B')
#     else:
#         return('Mouse C')
# print(catAndMouse(2,4,3))
    
# def pickingnumber(a):
    # hasil = 0
    # for i in a:
    #     b = a.count(i)
    #     c = a.count(i-1)
    #     d = b+c
    # if d > hasil:
    #     hasil = d
    # return hasil
#     a.sort()
#     b = []
#     b.append(a[0])
#     s = []
#     num = 0
#     for i in range(1,len(a)):
#         if a[i] - b[0] <= 1:
#             b.append(a[i])
            
#         if a[i] - b[-1] >= 2 :
#             s.append(b)
#             b = []
#             b.append(a[i])
#         if a[i] - b[0] == 2:
#             num = (b[0] + a[i]) // 2
#             s.append(b)
#             b = b[b.index(num):]
#             b.append(a[i])
#     s.append(b)
#     return len(max(s,key=len))
# print(pickingnumber([4,6,5,3,3,1]))
# print(pickingnumber([1,1,2,2,4,4,5,5,5]))
# print(pickingnumber([1,2,2,3,1,2]))

# def hurdleRace(k, height):
#     hasil = 0
#     if max(height) >= k:
#         hasil = (max(height) - k)
#     else:
#         return hasil
#     return hasil

# print(hurdleRace(4,[1,6,3,5,2]))
# print(hurdleRace(7,[2,5,4,5,2]))

def designerPdfViewer(h, word):


print()