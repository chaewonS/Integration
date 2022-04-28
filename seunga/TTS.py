from gtts import gTTS
import os

def txt_reader(ment):
    f = open("./"+ment+".txt", 'r')
    f = f.read()
    os.system('gtts-cli \"'+f+'\" --lang ko | mpg123 -')


def path_reader(ment):
    distance = ment
    os.system('gtts-cli "%s 미터 앞에서 우회전입니다." --lang ko | mpg123 -' %distance)


# 조사 문제로 멘트 직접 입력 했음
def dest_reader(ment):
    if ment == 1:
        os.system('gtts-cli "목적지를 도서관으로 설정하셨습니다." --lang ko | mpg123 -')
    elif ment == 2:
        os.system('gtts-cli "목적지를 음악실로 설정하셨습니다." --lang ko | mpg123 -')
    else:
        print("오류 삐리삐리삑.")

if __name__ == "__main__":
    print("TTS 입니다.")