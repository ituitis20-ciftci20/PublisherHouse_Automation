"""
4. AŞAMA - 1. KISIM:
exceldeki 0 olmayan id'lere karşılık, yeni fiyatları gösteren bir sözlük(map)
"""

import pandas as pd
import numpy as np

def constrct_dict():
    BOOK_NUMBER_EXCEL = 818
    INPUT_FILE = '..' + chr(92) + '2021 Kasım  Kaknüs Fiyat Listesi.xlsx'
    SHEET_INDEX = "Sayfa1"
    excel_doc = pd.read_excel(INPUT_FILE, SHEET_INDEX)

    price_col = np.copy(excel_doc["yeni fiyat"])
    id_col = np.copy(excel_doc["Ürün Id'leri"])

    books = {}
    for i in range(BOOK_NUMBER_EXCEL):
        if(int(id_col[i]) != 0 and price_col[i] != "B. Yok "):
                books[int(id_col[i])] = int(price_col[i])

    #for key in books.keys():
    #    print(key, " ", books[key])
    return books

