

class Coords:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(tuple([self.x, self.y]))


def _process_current_sentence(sentence: dict):
    if sentence:
        pairwise_agr = []
        pairwise_list = list(zip(list(sentence.keys()), list(sentence.keys())[1:]))
        for team1, team2 in pairwise_list:
            overlap_count = len(sentence[team1].intersection(sentence[team2]))
            union_count = len(sentence[team1].union(sentence[team2]))
            pairwise_agr.append(overlap_count / float(union_count))
        pairs_len = len(pairwise_agr)
        if pairs_len == 0:
            return None
        else:
            return sum(pairwise_agr) / pairs_len
    else:
        return None


if __name__ == "__main__":
    agreement = []
    sentence_count = 0
    # with open('./data/test.m2', 'r') as inp:
    with open('./data/official-2014.combined-withalt.m2', 'r') as inp:
        lines = [line.rstrip('\n') for line in inp]
        current_sentence = dict()
        for line in lines:
            if line:
                if line[0] == 'S':
                    sentence_count += 1
                    current_agreement = _process_current_sentence(current_sentence)
                    agreement.append(current_agreement)
                    current_sentence = dict()
                if line[0] == 'A':
                    team_id = line[-1]
                    line = line.split()
                    coords = Coords(line[1], line[2].split('|||')[0])
                    if current_sentence.get(team_id):
                        current_sentence[team_id].add(coords)
                    else:
                        current_sentence[team_id] = {coords}
        agreement = [a for a in agreement if a is not None]
        annotated_sentences = len(agreement)
        print(annotated_sentences)
        avg_agreement = sum(agreement) / float(len(agreement))
        print(avg_agreement)
