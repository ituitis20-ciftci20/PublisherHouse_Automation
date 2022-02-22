#difflab test program
#this program is not work properly now, because some columns of excel file are removed.

import pandas as pd
import numpy as np
import difflib as dfl

def find_pairs_write_into_text(web_arr, excel_arr):
    str_web_data = []
    for i in range(767):
        s = web_arr[i][0] + 'é' + str(int(web_arr[i][1]))
        str_web_data.append(s)
    
    loc = '..' + chr(92) + 'part2' + chr(92) + 'last_data' + chr(92) + '1.txt'
    with open(loc, 'w', encoding="utf-8") as f:
        for i in range(818):
            excel_name = excel_arr[i][0]
            excel_id = excel_arr[i][1]
            my_web_data = dfl.get_close_matches(excel_name, str_web_data, 100)
            if(excel_id == 0 and len(my_web_data) == 1):
                ls = my_web_data[0].split('é')
                web_name = ls[0]
                web_id = ls[1]
                f.write(f"{i: <4}")
                f.write(f"{excel_name : <90}")
                f.write(f"{web_name : <90}")
                f.write(f"{web_id : <50}")
                f.write("\n")
        f.close()

def main():
    loc = '..' + chr(92) + "2021 Kasım  Kaknüs Fiyat Listesi.xlsx"
    excel_data = pd.read_excel(loc, "Sayfa1", usecols=[1,9])#excel_name and excel_id
    web_data = pd.read_excel(loc, "Sayfa1", usecols=[10, 11])#web_name and web_id
    web_arr = np.copy(web_data.values)
    excel_arr = np.copy(excel_data.values)

    find_pairs_write_into_text(web_arr, excel_arr)

if __name__=="__main__":
    main()