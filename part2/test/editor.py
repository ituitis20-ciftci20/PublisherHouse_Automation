def edit(s):
    if(len(s) > 1):
        arr = s.split()
        for i in range(len(arr)):
            if i >= len(arr):
                continue
            if arr[i] == 'Ve':
                arr[i] = 've'
            if len(arr[i]) == 1:
                arr[i] = arr[i].lower()
                arr[i-1] += arr[i]
                arr.remove(arr[i])
            if i >= len(arr):
                continue
            if arr[i][-1] == '-' or arr[i][-1] == "'":
                k = list(arr[i+1])
                k[0] = k[0].lower()
                arr[i+1] = "".join(k)
                arr[i] += arr[i+1]
                arr.remove(arr[i+1])
            for c in range(len(arr[i])):
                if arr[i][c] == '’':
                    l = list(arr[i])
                    l[c] = "'"
                    arr[i] = "".join(l)
                if arr[i][c] == '.':
                    l = list(arr[i])
                    l[c] = ". "
                    arr[i] = "".join(l)
                if arr[i][c] == '-' or arr[i][c] == "'":
                    l = list(arr[i])
                    l[c+1] = l[c+1].lower()
                    arr[i] = "".join(l)
        s = ' '.join(arr)
    return s

with open('excel_kitaplar.txt', 'r', encoding='utf-8') as fr:
    with open('out.txt', 'w', encoding='utf-8') as fw:
        for l in fr:
            line = edit(l)
            fw.write(line)
            fw.write('\n')
        fw.close()
    fr.close()