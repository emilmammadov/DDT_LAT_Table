#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy
def LAT(inputMask, outputMask):
    count=0
    
    for a in range(len(sBox)):
        key=dec(a)
        value=dec(sBox[a])
        
        left=inputMask&key
        right=value&outputMask
        left=bin(left)[2:].zfill(4)
        right=bin(right)[2:].zfill(4)
        
        left=XOR(left)
        right=XOR(right)
        if left==right:
            count+=1
    
    count = count-pow(2,3)
    return count
        
        
def XOR(x):
    if len(x)==1:
        return x
    else:
        x=str(int(x[0])^int(x[1])) + x[2:]
        return XOR(x)    

def dec(x):
    if type(x)==int:
        return x
    else:
        if x == '9':
            return 9
        if x == '8':
            return 8
        if x == '7':
            return 7
        if x == '6':
            return 6
        if x == '5':
            return 5
        if x == '4':
            return 4
        if x == '3':
            return 3
        if x == '2':
            return 2
        if x == '1':
            return 1
        if x == '0':
            return 0
        if x=='A' or x=='a':
            return 10
        if x=='B' or x=='b':
            return 11
        if x=='C' or x=='c':
            return 12
        if x=='D' or x=='d':
            return 13
        if x=='E' or x=='e':
            return 14
        if x=='F' or x=='f':
            return 15


# In[2]:


def DDT(inputMask,outputMask):
    count=0
    for a in range(len(sBox)):
        key=dec(a)
        value=dec(sBox[a])
        left_right=dec(sBox[key^inputMask])
        left=value^left_right
        if left==outputMask:
            count+=1
    return count


# In[3]:


def LAT_calculate(sBox):
    latTable = numpy.zeros((16,16))
    for i in range(len(sBox)):
        for j in range(len(sBox)):
            latTable[i][j]=LAT(i,j)
    return latTable
    
def DDT_calculate(sBox):
    ddtTable = numpy.zeros((16,16))
    for i in range(len(sBox)):
        for j in range(len(sBox)):
            ddtTable[i][j]=DDT(i,j)

    printTable('DDT TABLE',ddtTable)
    return ddtTable

def printTable(title,table):
    print('-'*100)        
    print(title)
    print('-'*100 + '\n')  
    print(table)
    print('\n')
    
def LAT_nonlinearity(sBox):
    absLAT=numpy.absolute(LAT_calculate(sBox))
    absLAT[0][0]=0
    NLMs=8-numpy.max(absLAT)
    nonLinear=NLMs/6*100
    print('\n' + '-'*100)       
    print('LAT NON-LINEARITY = %'+str(nonLinear))
    print('-'*100 + '\n')


# In[4]:


def shift_left(x):
    x = x[1:] + '0'
    return x
    
def sBoxXOR(x,y):
    temp = ''
    for i in range(len(x)):
        temp = temp + str(int(x[i])^int(y[i]))
    return temp

def create_object(polinom):
    objectList = []
    objectList.append('0001')
    subPolinom = polinom[1:]
    #bin(left)[2:].zfill(4)
    for i in range(1,16):
        x = objectList[i-1]
        if x[0] == '1':
            x = shift_left(x)
            objectList.append(sBoxXOR(x,subPolinom))
        else:
            objectList.append(shift_left(x))
            
    
    for i in range(16):
        objectList[i] = int(objectList[i],2)
    return objectList
        
    
    
    
def mapping(mapTo):
    mappedList = []
    for i in range(16):
        mappedList.append((i*mapTo)%15)
    return mappedList

def create_sbox(polinom,mapTo):
    mappedList = mapping(mapTo)
    objectList = create_object(polinom)
    sBox = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    for i in range(len(mappedList)):
        index = objectList[i]
        adres = objectList[mappedList[i]]
        sBox[index] = adres
        
    return sBox       


# In[13]:


while True:
    qr = input('S-box değerlerini programın hesaplamasını ister misiniz? (istemezseniz S-box değerlerini manuel girmelisiniz.)')
    if qr == '' or not qr[0].lower() in ['e','h']:print('Lütfen evet veya hayır cevabı giriniz')
    else:break
if qr[0].lower() == 'e': 
    print("\nGF(2^4)'de indirgenemez polinomlar aşağıda verilmiştir.\n")
    print('x^4+x+1     (1)\nx^4+x^3+1   (2)')
    index = input('Seçmek istediğiniz polinomun yanındaki indisi giriniz.')
    mapTo = input('Haritalamayı hangi üsse yapmak istediğinizi girebilirsiniz (Örnek -1,2 veya 3)')
    if index=='1':
        polinom = '10011'
    elif index=='2':
        polinom = '11001'
    else:
        print('Doğru indis seçmediniz')
    
    sBox = create_sbox(polinom,int(mapTo))
    printTable('LAT TABLE',LAT_calculate(sBox))
    DDT_calculate(sBox)
    LAT_nonlinearity(sBox)
if qr[0].lower() == 'h':
    sBox = [x for x in input("S-box değerlerini arada boşluk bırakarak giriniz: ").split()] 
    printTable('LAT TABLE',LAT_calculate(sBox))
    DDT_calculate(sBox)
    LAT_nonlinearity(sBox)

