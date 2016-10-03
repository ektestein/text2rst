from string import ascii_uppercase, ascii_lowercase

try:  # использовать setuptools для установки зависимостей при оформлении в пакет
	import romanclass
except ImportError:
	import subprocess
	subprocess.call('pip install romanclass')
	import romanclass

# ============================================================================
# Document Structure
# ============================================================================


def transition():
	return '\n%s\n\n' % '-' * 8

# ============================================================================
# Body Elements
# ============================================================================


def bullet_list(elements, level=0):
	return '\n\n'.join(['  ' * level + '- ' + i.replace('\n', '\n  ') for i in elements]) + '\n\n'


def enumerated_list(elements, start=1, style='arabic', formatting='.'):  # не сработает, если (N)
	first = '#'
	if start == 1:
		if style == 'alpha_low':
			first = 'a'
		elif style == 'alpha_up':
			first = 'A'
		elif style == 'roman_low':
			first = 'i'
		elif style == 'roman_up':
			first = 'I'
		second = '#'
	else:
		first = start
		second = '#'
		if style == 'alpha_low':
			second = ascii_lowercase[ascii_lowercase.index(first) + 1]
		elif style == 'alpha_up':
			second = ascii_uppercase[ascii_uppercase.index(first) + 1]
		elif style == 'roman_low' or style == 'roman_up':
			second = romanclass.toRoman(romanclass.fromRoman(first) + 1)
			if style == 'roman_low':
				second = second.lower()

	return '\n'.join(['%s%s %s' % (counter, formatting, text.replace('\n', '\n' + ' ' * (len(str(counter)) + 2)))
						for counter, text in zip((first, second, *tuple('#' * (len(elements) - 2))), elements)]) + '\n\n'


def header(text, level):
	"""
:param text: строка, над которой совершается преобразование
:param level: требуемый уровень заголовка; допустимые значения [0; 5]
"""
	symbols = '=-\'.:"'
	return '%s\n%s\n\n' % (text, symbols[level] * len(text))


def sourcecode(text, strlimit=None):
	"""
:param text: строка, над которой совершается преобразование
:param strlimit: количество символов, не больше которого будет находиться в одной строке.
"""
	if strlimit:
		sliced = []
		for line in text.split('\n'):
			accum_len = 0
			accum_str = ''
			resstrs = []
			for word in line.split(' '):
				accum_len += len(word)
				if accum_len < strlimit:
					if accum_str:
						accum_str += ' ' + word
					else:
						accum_str = word
				else:
					resstrs.append(accum_str)
					accum_str = word
					accum_len = len(word)
			resstrs.append(accum_str)
			line = '\n\t\t'.join(resstrs)
			sliced.append(line)
		text = '\n'.join(sliced)
	return '::\n\n\t%s\n\n' % text.replace('\n', '\n\t')


'''
def paragraph(text, level=0):
	return
'''

# ============================================================================
# Inline Markup
# ============================================================================


def bold(text):
	return '**%s**' % text


def italic(text):
	return '*%s*' % text


print(enumerated_list(['def sourcecode(text, strlimit=None):\n\ndef italic(text):', 'xxx']))
