#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:46:28 2024

@author: noamgal
"""

        
# function implements sieve of Eratosthenes 
# returns all primes below the integer inputted by user
def Eratosthenes():
    # takes an integer input from user
    n = int(input('Enter an integer:'))
    # Creates a list of length n of Boolean values set to True
    A = [True for n in range(n+1)]
    A[0] = False
    A[1] = False
    # implements the sieve 
    i = 2
    while i <= n**(1/2):
        if A[i]:
            j = i**2
            while j <= n:
                A[j] = False
                j += i
        i += 1
    # stores the indices of the Booleans that remaain True which correspond to the primes
    primes = [i for i,p in enumerate(A) if p]
    return primes
# test
print(Eratosthenes())


# function implements sieve of Sundaram 
# returns all primes below the integer inputted by user,input must be greater than 2
def Sundaram():
    # takes an integer input from user
    n = int(input('Enter an integer:'))
    # implements the sieve
    k = int((n-1)/2)
    A = [True for k in range(k+1)]  
    for i in range(1,int(k**(1/2))):
        j = i
        while i+j+2*i*j<=k:
            A[i+j+2*i*j] = False
            j += 1
    T = [2*i+1 for i,p in enumerate(A) if p]
    # adjusts the first index to 2, from 1, because the sieve begins at 3
    T[0]=2
    return T
# test
print(Sundaram())


# sieve of Atkins
# returns all primes below the integer inputted by user,input must be greater than 5
def Atkins():
    # takes an integer input from user
    n = int(input('Enter an integer:'))
    
    # implements the sieve
    S = [1,7,11,13,17,19,23,29,31,37,41,43,47,49,53,59]
    A = [False for _ in range(n + 1)]  # Fixed the size of A to n + 1
    x = 1
    while x <= n**(1/2):
        y = 1
        while y <= n**(1/2):
            m = 4*x**2 + y**2
            if m <= n and (m % 60 in [1,13,17,29,37,41,49,53]):
                A[m] = not A[m]
            y += 2
        x += 1
    
    x = 1
    while x <= n**(1/2):
        y = 2
        while y <= n**(1/2):
            m = 3*x**2 + y**2
            if m <= n and (m % 60 in [7,19,31,43]):
                A[m] = not A[m]
            y += 2
        x += 2
       
    x = 2
    while x <= n**(1/2):
        y = x-1
        while y >= 1:
            m = 3*x**2 - y**2
            if m <= n and (m % 60 in [11,23,47,59]):
                A[m] = not A[m]
            y -= 2
        x += 1
        
    M = [60*w + s for w in range(int(n/60)+1) for s in S]
    for m in M:
        if m == 1: continue
        if m**2 > n: 
            break
        else:
            mm = m**2
            if A[m]:
                for m2 in M:
                    c = mm*m2
                    if c > n:
                        break
                    else:
                        A[c] = False
    primes = [2,3,5]
    primes += [i for i, p in enumerate(A) if p]
    return primes

    
print(Atkins())
    
    

# function that checks if positive real numbers are prime
def is_prime(n):
    if n == 1:
        return False
    i = 2
    while i**2 <= n:
        if n % i == 0:
            return False
        i += 1
    # if the number is not returned False above, it is prime
    return True

# function that will find the nth prime for arbitrary n
def find_Prime():
    n = int(input('Enter the nth prime number you want:'))    
    if n == 1:
        return print('The first prime number is 2')
    num = 3
    count = 2
    while count<n:
        num +=2
        if is_prime(num):
            count += 1
    print('The', count, "Prime number is", num)  
find_Prime()



    

