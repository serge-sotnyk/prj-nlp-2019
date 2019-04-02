import csv
from collections import namedtuple
from typing import List

Reviews = namedtuple('Reviews', 'goods_code stars review author permalink')


def load_reviews(filename: str) -> List[Reviews]:
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        res = []
        for row in reader:
            res.append(Reviews(**row))
    return res
