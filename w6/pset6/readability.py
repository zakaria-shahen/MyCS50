import re
from cs50 import get_string


def main():
    
    # input text
    text = get_string("Text: ")

    # Number word of text 
    # space => word
    words = re.split('\s+', text)
    
    length = 0
    l = 0
    s = 0
    while length <= len(words):
        input = ' '.join(words[length:length+100])
        
        #  . ? ! => sentence
        letter_count = len(re.findall('[A-Z-a-z]', input))

        # a-z A-Z => char
        sentence_count = len(re.findall('.*?[.!?]', input))

        # count word
        count_word = 100
        if length+100 > len(words):
            count_word = len(words) - length
        
        length += 100

        # average number of letters per 100 words in the text
        l += letter_count / count_word * 100

        # average number of sentences per 100 words in the text
        s += sentence_count / count_word * 100 

    grade = round(0.0588 * l - 0.296 * s - 15.8)

    if grade < 1:
        print('Before Grade 1')
    elif grade > 16:
        print('Grade 16+')
    else:
        print(f'Grade {grade}')


if __name__ == '__main__':
    main()