

NUMBER_OF_TEAMS = 5


def _update_corrections(corrections, team_id, error_identifier, sentence_count):
    identifier = 's{}:{}'.format(sentence_count, error_identifier)
    if corrections.get(identifier):
        current_value = list(corrections.get(identifier))
        current_value[int(team_id)] = '1'
        corrections[identifier] = current_value
    else:
        new_value = list('0' * NUMBER_OF_TEAMS)
        new_value[int(team_id)] = '1'
        corrections[identifier] = new_value


def _count_values(l, symbol):
    return sum([1 for s in l if s == symbol])


def _count_symbols(corrections, symbol):
    i = 0
    for c in corrections.values():
        i += _count_values(c, symbol)
    return i


if __name__ == "__main__":
    corrections = dict()
    sentence_count = 0
    with open('./data/official-2014.combined-withalt.m2', 'r') as inp:
        lines = [line.rstrip('\n') for line in inp]
        for line in lines:
            if line:
                line = line.split()
                if line[0] == 'S':
                    sentence_count += 1
                if line[0] == 'A':  # and check for noop
                    line = ' '.join(line).split('|||')
                    error_identifier = '-'.join(line[0].split(' ')[1:3])
                    team_id = line[-1]
                    # if int(team_id) <= 2:
                    _update_corrections(corrections, team_id, error_identifier, sentence_count)
        N = len(corrections)
        k = 2
        n = NUMBER_OF_TEAMS

        p_common_div = float(1 / float(N * n))

        symb0 = _count_symbols(corrections, '0')
        symb1 = _count_symbols(corrections, '1')

        p0 = p_common_div * symb0
        p1 = p_common_div * symb1
        print(p0)
        print(p1)

        pi_div = float(1 / float(n * (n - 1)))
        Pi = []
        for error in corrections.values():
            pi0 = _count_values(error, '0') * (_count_values(error, '0') - 1)
            pi1 = _count_values(error, '1') * (_count_values(error, '1') - 1)
            pi = pi_div * (pi0 + pi1)
            Pi.append(pi)

        P = float(1 / N) * sum(Pi)
        print(P)

        Pe = (pow(p0, 2)) + (pow(p1, 2))
        print(Pe)

        k = float(P - Pe) / float(1 - Pe)
        print(k)


# overlap / overall annotators number for sentence (including noop)

# overlap / union
