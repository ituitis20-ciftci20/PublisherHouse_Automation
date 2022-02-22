#2. AŞAMA:
#Bu program sayesinde, web'ten çektiğim data ile excel'de hazır olan datayı karşılaştırdım.
#403 satırın ismi aynı aynı çıktı.
#Exceldeki bu satıları web'ten çektiğim id'lerle eşleştirebildim.
#403 id yazıldı, geri kalanlar 0 olarak yazıldı.
#13 Aralık 2021

import pandas as pd
import numpy as np

BOOK_NUMBER_EXCEL = 818
BOOK_NUMBER_WEB = 767

#B stünu excel datasıydı. 10. stün web'teki veriyinin isimleriydi. 11. stün web'teki verinin idleri idi.
loc = '..' + chr(92) + "2021 Kasım  Kaknüs Fiyat Listesi.xlsx"
excel_data = pd.read_excel(loc, "Sayfa1", usecols="B")
web_data = pd.read_excel(loc, "Sayfa1", usecols=[10,11])
web_arr = np.copy(web_data.values)
excel_arr = np.copy(excel_data.values)

def main():
    #array's 0 index == row_index 2 in sheet
    intersection_arr = np.zeros(BOOK_NUMBER_EXCEL, dtype='>i4') #store ids
    for i in range(BOOK_NUMBER_WEB):
        for j in range(BOOK_NUMBER_EXCEL):
            if(web_arr[i][0] == excel_arr[j]):
                intersection_arr[j] = web_arr[i][1]


    df = pd.DataFrame(intersection_arr)

    writer = pd.ExcelWriter('new.xlsx', engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.save()

if __name__ == '__main__':
    main()