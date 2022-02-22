#İlk yorum(comment)lerim ingilizce olduğu için dil karmaşası yaşayan bir proje oldu.
#Türkçe açıklamalar ekledim ama ingilizceleri değiştirmedim.

#KAYNAKÇA:
#https://docs.python-requests.org/en/latest/
#https://curlconverter.com/# convert cURL(bash) cookie
#for login part
#look for form submition: https://www.thepythoncode.com/article/extracting-and-submitting-web-page-forms-in-python
#main video: https://www.youtube.com/watch?v=XVv6mJpFOb0&t=90s
#others: https://www.youtube.com/watch?v=0BBPhu4n57I https://www.youtube.com/watch?v=5GzVNi0oTxQ

#seleniumla benzer bir işlem yapılabilir
#eğer requests ile cookie(cookie, data, header)'yi , bu yola başvurun.

from bs4 import BeautifulSoup as bS
import requests
import os
import pandas as pd

PAGE_NUMBER_WEB = 26 ##toplam url sayısı
BOOK_NUMBER_WEB = 767 ##toplam ürün sayısı
longin_url = "http://www.yapıyoruzbuisi.com/wp-admin/" #isim trolldür
url_template = "http://www.yapıyoruzbuisi.com/books_url?=" ##bu bir template diğer sayfalar bundan kolayca türetilebilir
##not: her sitede url türetecek bir adres örüntüsü olmayabilir
urls = []
for i in range(PAGE_NUMBER_WEB): #web pages are line up in a simple pattern
    urls.append(url_template + f'{i+1}') ##diğer sayfa türetme


##REQUEST
##bunlar #https://curlconverter.com/#
#sitesinden elde ediliyor
#ayrıntı için kaynakçayı incele
cookies = {
}

headers = {
}

data = {
}

##bu veriyi biraz düzenler ve txt formatında yazar.
def get_all_data(req, url_arr): #beautiful soop is bS, requests is req

    for j, u in enumerate(url_arr): ##url array'inde dolaş(toplam 26 sayfamız vardı)
        index_page = req.get(u) ##zaten requestle girdik, sadece url'e gitmemiz yeterli
        soup = bS(index_page.text, 'lxml') #bütün html'i al
        table = soup.find('table') #html'den ilk beliren tabloyu al
        table_body = table.find('tbody') #tablo'nun gövde kısmını al
        books = table_body.find_all('tr') #gövdedeki satırları al

        book_info = {}
        for book in books: ##satırlara arasında dolaşırken bulduğun bilgikeri book_info'ya ekle
            book_name = book.find('td', class_='name column-name has-row-actions column-primary') #kitap ismi
            book_price = book.find('span', class_='woocommerce-Price-amount amount').text #kitap fiyatını bul text'e çevir
            book_id = book_name.find('div', class_='row-actions').find('span', class_='id').text #text'e çevir
            
            #bir dictionary kur. 
            #kitap ismi ---> [kitap fiyatı, id], list data tipinde
            book_info[book_name.find('a').text] = [book_price.replace('₺', '').strip()] + [book_id.split()[1]] 

        #soup'la çekip temizledik
        #şimdi bunları bir txt dosyasına yazmalıyız

        #relative path, chr(92) = back slash
        writing_path = 'old_data' + chr(92) + f'{j+1}.txt' 
        if(os.path.isfile(writing_path)): #hali hazırda aynı isimli bir dosya varsa sil, her ihtimale karşı
            os.remove(writing_path)
        with open(writing_path, 'w') as f: #dosyaya yazmaya başla
            for c in book_info.keys(): #kitap isimleri
                f.write(c) #kitap ismini yaz
                f.write('|') #bu bir ayraç
                f.write(book_info[c][0]) #kitap fiyatı
                f.write('|') #ayraç
                f.write(book_info[c][1]) #kitap id'si
                f.write('\n')
            f.close()
    
def get_specific_data(req, url_arr, typ): #verilen type'a göre sadece o tipteki özelliği txt'ye yazar.
                                            #name, price, id (kitabın 3 özelliğinden sadece 1'i)
    loc = 'old_' + typ + 's' + chr(92) + f'{1}.txt'
    if(os.path.isfile(loc)):
        os.remove(loc)
    for u in url_arr:
        index_page = req.get(u)
        soup = bS(index_page.text, 'lxml')
        table = soup.find('table')
        table_body = table.find('tbody')
        books = table_body.find_all('tr')

        book_info = []
        for book in books:
            if typ == 'name':
                data = book.find('td', class_='name column-name has-row-actions column-primary').find('a').text
            elif typ == 'price':
                data = book.find('span', class_='woocommerce-Price-amount amount').text.replace('₺', '').strip()
            else:
                data = book.find('td', class_=
                'name column-name has-row-actions column-primary').find('div', class_='row-actions').find('span', class_='id').text.split()[1]
            book_info.append(data)

        with open(loc, 'a') as f:
            for c in book_info:
                f.write(c)
                f.write('\n')
            f.close()

def write_excel(req, url_arr):
    book_info = [] ##verimiz, kitaplar
    #soup'la veri çekme, dictionary oluşturma işlemimiz aynı
    for u in url_arr:
        index_page = req.get(u) ##zaten requestle girdik, sadece url'e gitmemiz yeterli
        soup = bS(index_page.text, 'lxml')
        table = soup.find('table')
        table_body = table.find('tbody')
        books = table_body.find_all('tr')

        for book in books:
            book_name = book.find('td', class_='name column-name has-row-actions column-primary')
            book_price = book.find('span', class_='woocommerce-Price-amount amount').text
            book_id = book_name.find('div', class_='row-actions').find('span', class_='id').text
            a = [book_name.find('a').text, book_price.replace('₺', '').strip(), book_id.split()[1]]
            book_info.append(a)
    
    #bu sefer excele yazmalıyız
    indicies_of_rows = [] #hangi satırları kullanacağımı belirtmeliyim.
    for i in range(BOOK_NUMBER_WEB): #veri sayımız kadar satır
        indicies_of_rows.append(str(i))
    my_data = pd.DataFrame(book_info, index=indicies_of_rows, columns = ['1','2','3'])
    
    loc = 'excel_output' + chr(92) + 'output.xlsx'
    if(os.path.isfile(loc)):
        os.remove(loc)
    my_data.to_excel(loc)


def main():
    s = requests.Session()
    #part 1, login
    #giriş gerçekleşti, parametreleri convertcurl.com'dan bul.
    response = s.post(longin_url, headers=headers, cookies=cookies, data=data, verify=False) 
    
    #part 2, traverse between urls and get my data
    command = input
    ('What is your opperation? (input: 1 for get all data/2 for get specific data/3 for write all data into excell file)')
    if(command == 1):
        get_all_data(s, urls)
    if(command == 2):
        #another choice is traverse between urls and get only a one type attribute
        attr_type = input('data type: (input only name, price or id)')
        while(attr_type != 'name' and attr_type != 'price' and attr_type != 'id'):
            attr_type = input('data type: (input only "name", "price" or "id")')
        get_specific_data(s, urls, 'id')
    if(command == 3):
        #part 3, if you want, we can write into an excel file instead of a txt file
        write_excel(s, urls)
  
  
if __name__=="__main__":
    main()

