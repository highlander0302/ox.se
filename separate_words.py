import csv


def remove_columns_except_word(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)

        header = next(reader)
        word_index = header.index('word')

        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([header[word_index]])

            for row in reader:
                writer.writerow([row[word_index]])


remove_columns_except_word('oxford5k.csv', 'oxford500.csv')
