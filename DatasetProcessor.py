import pandas as pd
import csv
import re

# Functions for process data and convert them to desirable format
def fixPrice(price): # Convert price from farsi to english
    f2eDigit = { 
        '۰':'0',
        '۱':'1',
        '۲':'2',
        '۳':'3',
        '۴':'4',
        '۵':'5',
        '۶':'6',
        '۷':'7',
        '۸':'8',
        '۹':'9',
        '۰':'0',
        ',':''
    }

    for digit in f2eDigit.keys():
        price = price.replace(digit, f2eDigit[digit])

    return price

def fa2en(lst): # Convert price from farsi to english
    for i in range(len(lst)):
        lst[i] = fixPrice(lst[i])
    
    return lst

def fixWeight(lst): # Hold weight value without unit
    for i in range(len(lst)):
        lst[i]=(lst[i].split(" "))[0]
    return lst

def fixDisplaySize(lst): # Hold display size value without unit
    for i in range(len(lst)):
        lst[i]=(lst[i].split(" "))[0]
    return lst

def fixCPUSpeed(lst): #Hold minimum CPU speed value
    for i in range(len(lst)):
        try:
            lst[i] = re.findall("\d+\.\d+", lst[i])[0]
        except:
            lst[i]=None
    return lst

def fixCPUCacheSize(lst): #Hold CPU cache size
    for i in range(len(lst)):
        try:
            lst[i] = re.search(r'\d+', lst[i]).group()
        except:
            lst[i]=None
    return lst

def fixRAMCapacity(lst): # Hold RAM capacity value without unit
    for i in range(len(lst)):
        lst[i]=(lst[i].split(" "))[0]
    return lst

def splitScreenResulutionWidth(lst):
    
    for i in range(len(lst)):
        try:
            lst[i] = re.search(r'\d+', lst[i]).group()
        except:
            continue
    
    return lst

def splitScreenResulutionHeight(lst):
        
        for i in range(len(lst)):
            try:
                lst[i]=(lst[i].split("x"))
            except:
                continue
        
        for i in range(len(lst)):
            try:
                lst[i] = re.search(r'\d+', lst[i][1]).group()
            except:
                continue
        
        return lst


df = pd.read_csv("products.csv")

#rename columns
df.rename(columns={"_key":"ProductID",
                    "price":"Price",
                    "صفحه نمایش/اندازه صفحه نمایش":"DisplaySize",
                    "پردازنده مرکزی/محدوده سرعت پردازنده":"CPUSpeed",
                    "پردازنده مرکزی/حافظه Cache":"CPUCacheSize",
                    "حافظه RAM/ظرفیت حافظه RAM":"RAMCapacity",
                    "مشخصات فیزیکی/وزن":"Weight",
                    "پردازنده مرکزی/سازنده پردازنده":"CPUCompany",
                    "پردازنده مرکزی/سری پردازنده" : "CPUModel",
                    "حافظه RAM/نوع حافظه RAM":"RAMTechnology",
                    },inplace=True)
df.head()

price = list(df["Price"])
weight = list(df["Weight"])
displaySize = list(df["DisplaySize"])
cpuSpeed = list(df["CPUSpeed"])
cpuCacheSize = list(df["CPUCacheSize"])
ramCapacity = list(df["RAMCapacity"])

price = fa2en(price)
weight = fixWeight(weight)
displaySize = fixDisplaySize(displaySize)
cpuSpeed = fixCPUSpeed(cpuSpeed)
cpuCacheSize = fixCPUCacheSize(cpuCacheSize)
ramCapacity = fixRAMCapacity(ramCapacity)
width = splitScreenResulutionWidth(list(df["صفحه نمایش/دقت صفحه نمایش"]))
height = splitScreenResulutionHeight(list(df["صفحه نمایش/دقت صفحه نمایش"]))

# Add new columns
df['DisplayPixelWidth']=""
df['DisplayPixelHeight']=""

# Substituting new values for old values
for i in range(len(df)):
    df.loc[i, 'Price'] = price[i]
    df.loc[i, 'Weight'] = weight[i]
    df.loc[i, 'DisplaySize'] = displaySize[i]
    df.loc[i, 'CPUSpeed'] = cpuSpeed[i]
    df.loc[i, 'CPUCacheSize'] = cpuCacheSize[i]
    df.loc[i, 'RAMCapacity'] = ramCapacity[i]
    df.loc[i, 'DisplayPixelWidth'] = width[i]
    df.loc[i, 'DisplayPixelHeight'] = height[i]

# Delete expendable columns
df.drop('مشخصات فیزیکی/ابعاد', axis=1, inplace=True)
df.drop('url', axis=1, inplace=True)
df.drop('name', axis=1, inplace=True)
df.drop('پردازنده مرکزی/مدل پردازنده', axis=1, inplace=True)
df.drop('پردازنده مرکزی/فرکانس پردازنده', axis=1, inplace=True)
df.drop('حافظه داخلی/ظرفیت حافظه داخلی', axis=1, inplace=True)
df.drop('حافظه داخلی/نوع حافظه داخلی', axis=1, inplace=True)
df.drop('حافظه داخلی/مشخصات حافظه داخلی', axis=1, inplace=True)
df.drop('پردازنده گرافیکی/سازنده پردازنده گرافیکی', axis=1, inplace=True)
df.drop('پردازنده گرافیکی/مدل پردازنده گرافیکی', axis=1, inplace=True)
df.drop('پردازنده گرافیکی/حافظه اختصاصی پردازنده گرافیکی', axis=1, inplace=True)
df.drop('صفحه نمایش/نوع صفحه نمایش', axis=1, inplace=True)
df.drop('صفحه نمایش/دقت صفحه نمایش', axis=1, inplace=True)
df.drop('صفحه نمایش/صفحه نمایش مات', axis=1, inplace=True)
df.drop('صفحه نمایش/صفحه نمایش لمسی', axis=1, inplace=True)
df.drop('صفحه نمایش/توضیحات صفحه نمایش', axis=1, inplace=True)

# Build new CSV file with these new values and settings
df.to_csv("fixed.csv", index=False)
