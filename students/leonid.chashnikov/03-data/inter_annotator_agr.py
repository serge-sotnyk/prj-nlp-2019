

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


def _count_symbols(corrections, symbol):
    i = 0
    for c in corrections.itervalues():
        for s in c:
            if s == symbol:
                i += 1
    return i


if __name__ == "__main__":
    corrections = dict()
    sentence_count = 0
    with open('./data/official-2014.combined-withalt.m2', 'rb') as inp:
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
                    _update_corrections(corrections, team_id, error_identifier, sentence_count)
        N = len(corrections)
        k = 2
        n = NUMBER_OF_TEAMS
        p_common_div = float(1 / float(N * n))
        p0 = p_common_div * _count_symbols(corrections, '0')
        p1 = p_common_div * _count_symbols(corrections, '1')
        Pj = p_common_div * (p0 + p1)
        # print p_common_div
        print Pj
        print p0
        print p1

        pi_div = float(1 / float(n * (n - 1)))
        Pi = []
        for error in corrections.itervalues():
            pi0 = _count_symbols(corrections, '0') * (_count_symbols(corrections, '0') - 1)
            pi1 = _count_symbols(corrections, '1') * (_count_symbols(corrections, '1') - 1)
            pi = pi_div * (pi0 + pi1)
            Pi.append(pi)

#         calc P
#         calc Pe






# k = (p - pE) / (1 - pE)


# Let N be the total number of subjects,
# let n be the number of ratings per subject,
# and let k be the number of categories into which assignments are made.
# The subjects are indexed by i = 1, ... N
# and the categories are indexed by j = 1, ... k.
# Let nij represent the number of raters who assigned the i-th subject to the j-th category.

# N = total number of corrections across all teams (without duplicates)
# k = 2, categories - two, did correction or not
# n = 3? 5?, number of annotators
# i = index on errors
# j = 0, 1 - categories
# ni0 = number of raters, who missed error `i` (amount of 0's in dict[i])
# ni1 = number of raters, who specified error `i` (amount of 1's in dict[i])


# p0 is the relative observed agreement among raters (identical to accuracy)

# p0 - number of agreed corrections / number of all corrections by all annotators


# pE is the hypothetical probability of chance agreement, using the observed data to calculate the probabilities of
# each observer randomly seeing each category

# For categories k, number of items N and n-KI the number of times rater i predicted category k:
# pE = (1 / N^2) * sum(k) (nK1 * nK2)
# N - number of all sentences
# k - types of errors?
# n-KI - how many times rater i predicted mistake k


# p



# overall
#
# for each mistake type
#       select only this error type, check text position

# overall:
#   ignore error type, just look at text position
#   check both error type and position





# A 49 49|||Vm|||might|||REQUIRED|||-NONE-|||0
# A 49 49|||Vm|||may|||REQUIRED|||-NONE-|||1
# A 40 41|||ArtOrDet|||the|||REQUIRED|||-NONE-|||2
# A 49 49|||Vm|||might|||REQUIRED|||-NONE-|||2


# 1 sentence, 3 annotators, 2 categories

# Let nIJ represent the number of raters who assigned the i-th subject to the j-th category.
# n = 3, N = 2, k = 2
# pJ = (1 / (N * n)) * sum(1, N) nIJ
# pJ = (1 / 6) * (3 + 1) = 4 / 6 = 0.66

# Need to calculate - total amount of errors annotated.
# dict of all errors
# key = string, representing sentence and error position
# value = string like [1101] - what annotators did set an error



# team 0 said 49 49 - 1 time
# team 0 said 40 41 - 0 time
# team 1 said 49 49 - 1 time
# team 1 said 40 41 - 0 time
# team 2 said 49 49 - 1 time
# team 2 said 40 41 - 1 time
