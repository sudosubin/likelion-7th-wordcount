from django.shortcuts import render
import hgtk


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def result(request):
    raw_text = request.GET['raw_text']
    word_list = raw_text.split()
    word_dic = {}
    max_num = 1

    for word in word_list:
        if hgtk.checker.is_hangul(word):
            alphabet = str(hgtk.letter.decompose(word[0])[0])  # 단어의 첫 자음
        else:
            alphabet = str(word[0])  # 단어의 첫 글자

        if alphabet not in word_dic:
            word_dic[alphabet] = {}

        if word not in word_dic[alphabet]:
            word_dic[alphabet][word] = 1
        else:
            word_dic[alphabet][word] += 1
            if max_num < word_dic[alphabet][word]:
                max_num = word_dic[alphabet][word]

    return render(request, 'result.html', {
        'raw_text': raw_text,
        'char_num_withb': len(raw_text),
        'char_num_withoutb': len(raw_text.strip()) - raw_text.strip().count(' '),
        'word_num': len(word_list),
        'word_dic': sorted(word_dic.items()),
        'max_num': max_num
    })
