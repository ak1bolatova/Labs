def convert (n):
    ounces = 28.3495231 * n
    return ounces 

def convertf_c (f):
    C = (5 / 9) * (f - 32)
    return C

def solve(numheads, numlegs):
    rabbit=(numlegs-2*numheads)/2
    chik=numheads-rabbit
    return rabbit, chik

def permutations(arr):
    if len(arr) == 0:
        return []
    if len(arr) == 1:
        return [arr]
    
    result = []
    for i in range(len(arr)):
        first = arr[i]  # Берем один элемент
        remaining = arr[:i] + arr[i+1:]  # Убираем его из списка
        for perm in permutations(remaining):  # Рекурсивно получаем перестановки оставшегося списка
            result.append([first] + perm)
    
    return result

def reverse(n):
    n=n.split()
    a=[]
    for i in range(len(n)-1, -1,-1):
        a.append(n[i])
    return a    

def is_3(nums):
    for i in  range(len(nums)-1):
        if nums[i]==3 and nums[i+1]==3: 
            
            return True
            
      
    return False
def is_007(nums):
    zero_1=0
    zero_2=0
    
    for i in  range(len(nums)):
        
         if nums[i]==0 and zero_1==0:
            zero_1=1            
         elif nums[i]==0 and zero_1==1:
             zero_2=1
         if nums[i]==7 and zero_1==1 and zero_2==1: 
             return True
        
            
    return False
import math
def volume(r):

    n=(4/3)*r*r*r*math.pi
    return n
def un(l):
    uniq=[]
    for i in range(len(l)):
        if l[i] not in uniq:
            uniq.append(l[i])
    return uniq
def pal(n):
    a=n
    if n[::-1]==a:
        return True
    return False
def histogram(n):
    for i in range(len(n)):
        print(n[i]*"*")