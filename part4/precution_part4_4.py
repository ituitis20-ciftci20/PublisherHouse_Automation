#bu kod, internet yavaşlığına karşı programa bir bağışıklık kazandırmak için yazıldı.

def main():
    input_file = 'report.txt' #programın kaç sayfa işlediği burada yazıyor
    source_code = 'insert_price_part4_2_funcless.py' #fonksiyonsuz belgeyi, öbürtürlü hata veriyor
    correct_flag = 26 ##bütün sayfalar gezildi
    current_flag = 0

    while(1):
        with open(input_file, 'r') as file:
            current_flag = int(file. readline().split(None, 1)[0])
        if(current_flag == correct_flag):
            break
        else:
            try :
                #programı çalıştır
                exec(open(source_code, encoding='utf-8').read())
            except:
                continue

if __name__ == '__main__':
    main()

