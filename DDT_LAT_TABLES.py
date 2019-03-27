#!/usr/bin/env python
# coding: utf-8

# ### Creating S-Box array

# In[1]:


import numpy
# S-box values
sBox=[0,1,'f','a',8,6,5,9,4,7,3,'e','d','c','b',2]


# ### LAT table function

# In[2]:


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


# ### DDT table function

# In[3]:


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
    
    


# # LAT TABLE PROJECTION

# In[4]:


latTable = numpy.zeros((16,16))
for i in range(len(sBox)):
    for j in range(len(sBox)):
        latTable[i][j]=LAT(i,j)
print('-'*100)        
print('LAT TABLE')
print('-'*100 + '\n')  
print(latTable)
print('\n')


# # DDT TABLE PROJECTION

# In[5]:


ddtTable = numpy.zeros((16,16))
for i in range(len(sBox)):
    for j in range(len(sBox)):
        ddtTable[i][j]=DDT(i,j)

print('-'*100)        
print('DDT TABLE')
print('-'*100 + '\n')  
print(ddtTable)
print('\n')


# # CALCULATION OF NON-LINEARITY (LAT)

# In[6]:


absLAT=numpy.absolute(latTable)
absLAT[0][0]=0
NLMs=8-numpy.max(absLAT)
nonLinear=NLMs/6*100
print('\n' + '-'*100)       
print('LAT NON-LINEARITY = %'+str(nonLinear))
print('-'*100 + '\n')       

