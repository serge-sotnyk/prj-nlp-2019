
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

	def shmificate(self, word):
		if not word:
			return ''

		if self.lang.sh in word:
			shm = self.lang.sm
		else:
			shm = self.lang.shm

		if word.title() == word:
			shm = shm.title()

		if word[:len(self.lang.shm)] == self.lang.shm:
			shmord = word
		else:
			shmord = shm + self.cut_first_consonants(word)

		return '{}-{}'.format(word, shmord)


	def cut_first_consonants(self, word):
	    pattern = re.compile(r'.*?(?=[{vowels}])'.format(vowels=EngLang.vowels))
	    _, end = re.match(pattern,word).span()
	    return word[end:]
	    

def test_eng():
	shm = Shmificator(lang=EngLang)

	assert shm('table')     == 'table-shmable'
	assert shm('breakfast') == 'breakfast-shmeakfast'
	assert shm('apple')     == 'apple-shmapple'
	assert shm('shmutter')  == 'shmutter-shmutter'
	assert shm('ashmont')   == 'ashmont-smashmont'
	assert shm('Apple')     == 'Apple-Shmaple' 

	print('Tests for Eng passed')


def test_ukr():
	shm = Shmificator(lang=UkrLang)

	assert shm('совеня')   == 'совеня-шмовеня'
	assert shm('авокадо')  == 'авокадо-шмавокадо'
	assert shm('Вишгород') == 'Вишгород-Смишгород'
	assert shm('круглий')  == 'круглий-шмуглий'

	print('Tests for Ukr passed')
	


if __name__ == '__main__':
	test_eng()
	test_ukr()

