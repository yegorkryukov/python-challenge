import re, os

# Set variable for input file
folder = 'Resources/'
raw_file = 'raw_text.txt'
raw_file = os.path.join(folder, raw_file)

#read the file
with open(raw_file) as text:
    paragraph = text.read()

word_count = len(paragraph.split(' '))
letters = re.sub('[^a-zA-Z]', '', paragraph)
sentences = re.split("(?<=[.!?]) +", paragraph)
average_sentence_length = word_count/len(sentences)
average_letter_count = len(letters)/word_count

print('Paragraph Analysis\n-----------------')
print('Approximate Word Count:', word_count)
print('Approximate Sentence Count:', len(sentences))
print('Average Letter Count: {:,.2f}'.format(average_letter_count))
print('Average Sentence Length: {}'.format(average_sentence_length))
print('-----------------')

