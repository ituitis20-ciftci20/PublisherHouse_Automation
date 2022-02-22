#INSERT NEW PRICE INTO WEBSITE

"""
Proje'nin ilk hali bitmiştir.
Bu kod arada bir yenileniyor.

Şuanki yaptığı:
-istenen sitedeki ürünlere ulaşır.
-sayfalar boyunca döner
-eğer sayfada bir tane değişmesi gereken ürün bulursa
    -o ürünün sayfasına girip günceller
    -önceki url'ye geri döner
-fiyat karşılaştırmasını sitedeki html fiyatları ile
excel tablosundaki fiyatlar arasında yapar.

son değişiklik:
önceden her ürünün sayfasındaki fiyatı teker teker güncelliyordu,
bunun yerine, ürünün sayfasına girmeden fiyatını kontrol ediyor.
"""


"""
4. AŞAMA - 2. KISIM:
selenium kullanarak herhangi bir fiyatı değiştirmek.

sonrası: (4. AŞAMA)
3. KISIM
seçtiğim elementin sahip olduğu id'yi bul. (tbody'e ait tr'ların id'lerine bak: örnek 'post-8765')
kelimenin başındaki fazlalığı kes. id'yi int'e çevir.
onu bastır. hiiç sayfalara girmeden 760 ürünün de id'lerini bastır!

4. KISIM
seçtiğim id'ye yönelik olan fiyatı sözlüğümden bul
ona uygun fiyatı ID ile beraber bastır.
sözlüğün içindeki veri ile bunu karşılaştır

5. KISIM:
2. kısım ile 4. kısımda yaptığımı birleştir.
ilk önce tek sayfa için fonksiyonu çalıştır
sonra sonunca sayfa için (az ürün var)
sonra 1 ve 2. sayfalar için
en son tüm sayfalar için! Okulda internetin kesilmeyeceği yerde başlat.
"""


"""
güzel fonksiyonlar:

find_element(By.ID, "user_login")
#istediğim id'ye sahip elemanı alır

find_elemnets(By.CLASS_NAME, "cook")
#istediğim class'a ait elemanları alır

element = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.ID, "user_login"))
)
#istediğim id'ye sahip eleman html'de belirne kadar bekler, sonra onu alır

element.send_key(USER_NAME) #forma user_name'i yazar

element.send_key(Key.RETURN) #enter'a basar
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time as t
from find_prices import constrct_dict #books from excel file
from get_ids_by_selen import find_tr_id, find_tr_price #some functions to use in HTML searching


#plug urls and login info.
USER_NAME = ""
PASSWORD = ""
PAGE_NUMBER_WEB = 26
log_in_page = ""
url_template = ""
urls = []
for i in range(PAGE_NUMBER_WEB): #web pages are line up in a simple pattern
    urls.append(url_template + f'{i+1}')
book_dict = constrct_dict() #a map that keys are id's and values are updated prices


def pass_enterence(drv):
    drv.get(log_in_page)

    WebDriverWait(drv, 10).until(
    EC.presence_of_element_located((By.ID, "user_login"))
    ).send_keys(USER_NAME)
    drv.find_element(By.ID, "user_pass").send_keys(PASSWORD + Keys.RETURN)
    t.sleep(10) #wait to main page loaded

def main():
    with webdriver.Edge() as driver:
        pass_enterence(driver)

        for url in urls: #iterate over pages
            driver.get(url)
            t.sleep(10)#wait to load the page
            
            #*** search before edit ***
            table_rows = driver.find_elements(By.XPATH, "//tbody[@id='the-list']//tr")
            price_infos = driver.find_elements(By.XPATH, "//tbody[@id='the-list']/tr/td[@class='price column-price']/span")

            book_id_list = []
            book_old_price_list = []
            for row in table_rows:
                #if we append 0, it means null id
                book_id_list.append(find_tr_id(row, book_dict))
            for price_info in price_infos:
                book_old_price_list.append(find_tr_price(price_info))
            #*** ------------------- ***

            num_of_books = len(table_rows)
            for i in range(num_of_books): #change price, iterate over every book on the web page

                books = driver.find_elements(By.CLASS_NAME, "row-title") #we need to re-define our books, because we refreshed the page.

                for j, element in enumerate(books):
                    if(j == i): #find our element, on the html table
                        if(book_id_list[j] == 0): #id is not in our dictionary or row is not belong to our table
                            continue
                        element_id = book_id_list[j]
                        new_price = book_dict[element_id]

                        if(book_old_price_list[j] == new_price): #no need to update
                            continue

                        element.send_keys(Keys.RETURN) #click the book's page
                        t.sleep(10) #wait to load the page
                        price_form = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "_regular_price"))
                        )
                        price_form.clear() #yazmadan önce eskiden olanları silmeliyiz
                        price_form.send_keys(new_price)

                        update = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "publish"))
                        )
                        update.send_keys(Keys.RETURN)
                        t.sleep(10) #wait to update the page!
                        
                        driver.get(url) #return the book table
                        t.sleep(10)#wait to load the page
                        break
                    elif(j > i): #if we already found book
                        break

if __name__ == '__main__':
    main()