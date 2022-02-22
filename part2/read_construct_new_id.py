#2. AŞAMANIN İLK KISMI
"""
web'ten çektiğim id'ler bazı pürüzler içeriyordu.
onlardaki gereksiz kelime-boşluk çıkarıldı
"""
#temizlenmiş data'yı text dosyasından alıp
#onu excel formatınca yazdırmayı amaçladım.


import pandas as pd
import numpy as np
import re # re.sub()

BOOK_NUMBER_EXCEL = 818

def main():
    cleared_data = []
    #open directory
    #then clean my data and append it
    loc = 'last_data' +  chr(92) + 'fixed_data_part1.txt' #this directory is created in a lost step of the project(non-documented)
    with open(loc, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            s = re.sub(' {3,}', '$', line) #to remove multiple white spaces
            data = [] #has 4 elements
            data.append(int(s[0:3])) #rank
            data += s[4:].split('$')[:-1] #book names(excel/web)
            data[-1] = int(data[-1]) #book id
            cleared_data.append(data)
        f.close()


    #Excel format
    #expand 131 lenght to 818 lenght
    whole_data = []
    j = 0
    for i in range(BOOK_NUMBER_EXCEL):
        if j < 131:
            if(i == cleared_data[j][0]): # 'i' is rank
                whole_data.append(cleared_data[j])
                j += 1
            else:
                whole_data.append([-1, ' ', ' ', -1])
        else:
            whole_data.append([-1, ' ', ' ', -1])

    df = pd.DataFrame(whole_data, columns=[0,1,2,3])

    writer = pd.ExcelWriter('some_data.xlsx', engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.save()

if __name__ == '__main__':
    main()