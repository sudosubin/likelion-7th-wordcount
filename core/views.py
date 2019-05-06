from django.shortcuts import render
from itertools import groupby
from konlpy.tag import Mecab
import hgtk


class Word:  # 단어, 초성, 출현 횟수, 품사 정보
    def __init__(self, wrapped_word):
        self.word = wrapped_word[0]

        if hgtk.checker.is_hangul(self.word):
            self.alpha = str(hgtk.letter.decompose(self.word[0])[0])  # 단어의 첫 자음
        else:
            self.alpha = str(self.word[0])  # 단어의 첫 글자

        self.show = 1
        self.type = mecab_tags(wrapped_word[1])

    def showen(self):
        self.show += 1

    def __str__(self):
        return self.word

    def __eq__(self, other):
        return self.word == other.word and self.type == other.type

    def __ne__(self, other):
        return self.word != other.word or self.type != other.type


# ('인가', 'VCP+EF') => ['긍정 지정사', '종결 어미']
def mecab_tags(type):
    mecab_dict = {
        'NNG': '일반 명사',
        'NNP': '고유 명사',
        'NNB': '의존 명사',
        'NNBC': '단위 의존 명사',
        'NR': '수사',
        'NP': '대명사',
        'VV': '동사',
        'VA': '형용사',
        'VX': '보조 용언',
        'VCP': '긍정 지정사',
        'VCN': '부정 지정사',
        'MM': '관형사',
        'MAG': '일반 부사',
        'MAJ': '접속 부사',
        'IC': '감탄사',
        'JKS': '주격 조사',
        'JKC': '보격 조사',
        'JKG': '관형격 조사',
        'JKO': '목적격 조사',
        'JKB': '부사격 조사',
        'JKV': '호격 조사',
        'JKQ': '인용격 조사',
        'JC': '접속 조사',
        'JX': '보조사',
        'EP': '선어말어미',
        'EF': '종결 어미',
        'EC': '연결 어미',
        'ETN': '명사형 전성 어미',
        'ETM': '관형형 전성 어미',
        'XPN': '체언 접두사',
        'XSN': '명사 파생 접미사',
        'XSV': '동사 파생 접미사',
        'XSA': '형용사 파생 접미사',
        'XR': '어근',
        'SF': '마침표, 물음표, 느낌표',
        'SE': '말줄임표',
        'SSO': '여는 괄호',
        'SSC': '닫는 괄호',
        'SC': '쉼표, 가운뎃점, 콜론, 빗금',
        'SY': '기타 기호',
        'SH': '한자',
        'SL': '외국어',
        'SN': '숫자',
    }

    return list(map(mecab_dict.get, type.split('+')))


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def result(request):
    mecab = Mecab()
    raw_text = request.GET['raw_text']

    # word_list 리스트
    word_list = []
    for word in mecab.pos(raw_text):
        dest_word = Word(word)
        if dest_word in word_list:
            dest_pos = word_list.index(dest_word)
            word_list[dest_pos].showen()
        else:
            word_list.append(dest_word)

    # word_dic 딕셔너리
    word_dic = {}
    for word in word_list:
        word_dic.setdefault(word.alpha, []).append(word)

    # 테스트 출력
    print('word_list')
    print(word_list)
    print('word_dic')
    print(word_dic)

    max_num = max(word.show for word in word_list)

    return render(request, 'result.html', {
        'raw_text': raw_text,
        'char_num_withb': len(raw_text),
        'char_num_withoutb': len(raw_text.strip()) - raw_text.strip().count(' '),
        'word_num': len(word_list),
        'word_dic': sorted(word_dic.items()),
        'max_num': max_num,
    })
