import re

class EngLang:
	sh  = 'sh'
	shm = 'shm'
	sm  = 'sm'
	vowels = 'aeiou'


class UkrLang:
	sh  = 'ш'
	shm = 'шм'
	sm  = 'см'
	vowels = 'аеиіоу'



class Shmificator:

	def __init__(self, lang):
		self.lang = lang

	def __call__(self, word):
		return self.shmificate(word)


	def shmificate(self, phrase):
		if not phrase:
			return ''

		*pre_words, word = phrase.split(' ')
		shmord = self.shmificate_word(word)
		shmase = self.make_shmase(pre_words, shmord)
		return '{}-{}'.format(phrase, shmase)


	def shmificate_word(self, word):
		shm = self.choose_shm(word)
		shm, word = self.case_aligment(shm, word)
		shmord = self.make_shmord(shm, word)
		return shmord


	def choose_shm(self, word):
		if self.lang.sh in word:
			shm = self.lang.sm
		else:
			shm = self.lang.shm
		return shm


	def case_aligment(self, shm, word):
		if word.title() == word:
			shm = shm.title()
			word = word.lower()
		elif word.upper() == word:
			shm = shm.upper()
		return shm, word


	def make_shmord(self, shm, word):
		if word[:len(self.lang.shm)] == self.lang.shm:
			shmord = word
		else:
			shmord = shm + self.cut_first_consonants(word)
		return shmord


	def cut_first_consonants(self, word):
	    pattern = re.compile(r'.*?(?=[{vowels}])'.format(vowels=self.lang.vowels))
	    _, end = re.match(pattern,word).span()
	    return word[end:]


	def make_shmase(self, pre_words, shmord):
		if pre_words:
			shmase = '{} {}'.format(' '.join(pre_words), shmord)
		else:
			shmase = shmord
		return shmase

