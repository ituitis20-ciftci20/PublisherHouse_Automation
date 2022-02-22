#excel dosyasındaki bazı sütunlar kaldırıldığından bu program şuan doğru çalışmamaktadır

"""
1. AŞAMA:
web scrapping ile(soup, request, selenium) veriyi çekme


2. AŞAMA:
hata(noise) içermeyen excel verilerini güncelleme


3. AŞAMA: (şuanki aşama)
Bu aşamanın amacı
Elimizde bulunan excel verileri ile web verilerini karşılaştırmaktır.
Web verileri daha önceden excele, çekilmiştir.

Excel verilerine uygun id'ler atamak istiyoruz.
Ancak web verilerinin isimleri ile exceldekilerin isimleri uyuşmuyor.
(Önceki adımalarda uyuşan id'lere, web'teki id'ler atandı.)
Uyuşmayan id'lere de uygun id'lerin atanması gerekiyor.

Hem excel verilerinin isimlerindeki noise'u kaldırıyoruz
Hem de excel verilerine uygun id'leri atıyoruz.
Difflib'in bize sağladığı güçle!


4. AŞAMA: (sonra)
Güncel id'leri buldum.
Asıl amacım, eski fiyatları yenileriyle değiştirmek.
Bunun için HTML'deki istenilen id'ye sahip elementin
fiyatını yeni fiyatla değiştireceğim.

Aralık 2021 - Ocak 2022
"""

"""
Fonksiyonlar:
-Excel verisi ile web verisini karşılatırıp kalan işi gösterme. --> show_progress()
-Olası benzer kelimeleri listeleme. --> find_pairs_write_into_excel()
    -Excel'deki kelime için web'ten uygun bir kelime seçip(listeden) 
    exceldeki veri'nin ismini düzeltme. ona bir id atama.
"""


import pandas as pd
import numpy as np
import difflib as dfl
import time as t

#row numbers
BOOK_NUMBER_EXCEL = 818 
BOOK_NUMBER_WEB = 767

INPUT_FILE = '..' + chr(92) + '2021 Kasım  Kaknüs Fiyat Listesi.xlsx'
OUTPUT_FILE = 'test.xlsx'
SHEET_EXCEL = "Sayfa1"
SHEET_WEB = "Sayfa1"
excel_doc = pd.read_excel(INPUT_FILE, SHEET_EXCEL)
web_doc = pd.read_excel(INPUT_FILE, SHEET_WEB)
key = "no" #ekleme yapacak mıyız?
#sütunların header'ları
EXCEL_BOOK_COLUMN = "ÜrünAçıklama"
EXCEL_ID_COLUMN = "Ürün Id'leri"
NEW_BOOK_COLUMN = "yeni isim-excel" #istediğimiz bilgileri içeren yeni sütunlar
NEW_ID_COLUMN = "yeni id-excel"
WEB_BOOK_COLUMN = "web"
WEB_ID_COLUMN = "web_id"

def show_progress():
    excel_arr = np.copy(excel_doc[EXCEL_ID_COLUMN])
    num_cleared_cols = 0
    
    for i in range(BOOK_NUMBER_EXCEL):
        if excel_arr[i] != 0:
            num_cleared_cols += 1

    print(num_cleared_cols, '/', BOOK_NUMBER_WEB, 'is done!')


def search_index(arr, key):
    for i in range(len(arr)):
        if(arr[i] == key):
            return i

def find_pairs_write_into_excel(num_close_elements):
    global key
    key = input("Do y want to append new info? ")
    if(key == "yes"):
        print("Enter proper index from the given list, (start from 0)")
        print("If you want to skip an element enter -1, if you want to go to the menu enter -2.")
    
    book_names_in_excel = np.copy(excel_doc[EXCEL_BOOK_COLUMN]).tolist()
    book_ids_in_excel = np.copy(excel_doc[EXCEL_ID_COLUMN]).tolist()
    book_names_in_web = np.copy(web_doc[WEB_BOOK_COLUMN]).tolist()
    book_ids_in_web = np.copy(web_doc[WEB_ID_COLUMN]).tolist()


    for i in range(BOOK_NUMBER_EXCEL):
        book_ids_in_excel[i] = int(book_ids_in_excel[i])
    for i in range(BOOK_NUMBER_WEB):
        book_ids_in_web[i] = int(book_ids_in_web[i])

    web_books = []
    for j, i in enumerate(book_names_in_web):
        if(j < BOOK_NUMBER_WEB):
            web_books.append(i)
    
    if(key == "yes"):
        new_names = book_names_in_excel
        new_ids = book_ids_in_excel
    
    for i in range(BOOK_NUMBER_EXCEL):
        excel_name = book_names_in_excel[i]
        excel_id = book_ids_in_excel[i]
        my_web_data = dfl.get_close_matches(excel_name, web_books, 100)
        if(excel_id == 0 and len(my_web_data) != 0): #and len(my_web_data) == num_close_elements
            print("\n", excel_name, ' //***// ', my_web_data)
            #veriyi ekrana bastır, soru al. hangisini değiştriemk istersin

            #append new info to a file
            if(key == "yes"):
                index = int(input("Which of them, do y want; enter a proper index? "))

                if(index == -2): #fonksiyonu durdur ve eldekileri yazdır
                    excel_doc[NEW_ID_COLUMN] = new_ids #id
                    excel_doc[NEW_BOOK_COLUMN] = new_names #isim
                    return 0
                if(index != -1): #insert two keys from web array into excel array

                    #evet şimdi, bu web datanın efradını bulmamız lazım
                    #onun excel_data'daki sütunu ve satırı lazım
                    #ikisinin satırı ortak...
                    #sütun numpy array'inde key üzerinden indexini bulak
                    r_web = search_index(book_names_in_web, my_web_data[index])
                    print(book_names_in_web[r_web], int(book_ids_in_web[r_web]))

                    #ve bizim excel_name'in sütunu ve satırı, id'nin sütunu
                    #excel_name ve excel_id için row_index
                    r_excel = search_index(book_names_in_excel, excel_name)
                    new_ids[r_excel] = int( book_ids_in_web[r_web] )
                    new_names[r_excel] = book_names_in_web[r_web]
    
    if(key == "yes"):
        excel_doc[NEW_ID_COLUMN] = new_ids #id
        excel_doc[NEW_BOOK_COLUMN] = new_names #isim
                
def main():
    command = 1
    while(command):
        command = int(input("Press, 1 to show progress; 2 to get some info about remaining job; 0 to exit: "))
        for i in range(3):
            print('.', end='')
            t.sleep(0.5)
        print()
        if command == 1:
            show_progress()
        elif(command == 2):
            pair_number_for_each = 2 #number of pairs for each sample
            find_pairs_write_into_excel(pair_number_for_each) 
            if(key == "yes"): #append new info
                df = excel_doc
                writer = pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') #write appended data sheet into a test file
                df.to_excel(writer, index=False)
                writer.save()
  
if __name__=="__main__":
    main()

