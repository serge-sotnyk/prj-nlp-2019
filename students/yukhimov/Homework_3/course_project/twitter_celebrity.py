from alphabet_detector import AlphabetDetector
ad = AlphabetDetector()

with open('Top-1000-Celebrity-Twitter-Accounts.csv', "r") as input_file:
    with open('twitter_celebrity_dataset.txt', "w") as output_file:
        for line in input_file:
            name = line.split(',')[2]
            if len(name.split(' ')) > 1 and ad.is_latin(name):
                output_file.write(name.title() + '\n')
