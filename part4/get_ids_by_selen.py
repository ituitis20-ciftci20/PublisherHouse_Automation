#Bu kısım önce program olarak tasarlandı, sonra fonksiyonlara döndürüldü

"""
4. AŞAMA: 3. ve 4. KISIMLAR

3. KISIM
seçtiğim elementin sahip olduğu id'yi bul. (tbody'e ait tr'ların id'lerine bak: örnek 'post-8765')
kelimenin başındaki fazlalığı kes. id'yi int'e çevir.
onu bastır. hiiç sayfalara girmeden 760 ürünün de id'lerini bastır!

4. KISIM
seçtiğim id'ye yönelik olan fiyatı sözlüğümden bul
ona uygun fiyatı ID ile beraber bastır.
sözlüğün içindeki veri ile bunu karşılaştır
"""

def str_to_int(s): #convert str id into integer
    str_len = len(s)
    j = 0
    for i in range(str_len):
        c = int(s[str_len-1-i])
        j += c * pow(10, i)
    return j

def find_tr_id(row, dict): #find id in table row (HTML)
    str_key = str(row.get_attribute("id"))
    if(str_key[:4] == "post"): #it is a book
        int_key = str_to_int(str_key[5:])
        if(int_key in dict): #if that id is in my dictionary
            return int_key
    return 0


def find_tr_price(price_info): #find price in table row (HTML)
    text_info = price_info.text
    price = str_to_int(text_info.split(',')[0].split()[1])#clear after point and money sign 
    return price
