import re
from string import ascii_uppercase, ascii_lowercase

try:  # использовать setuptools для установки зависимостей при оформлении в пакет
	import romanclass
except ImportError:
	import subprocess
	subprocess.call('pip install romanclass', shell=True)
	import romanclass

import prettytable

# ============================================================================
# Document Structure
# ============================================================================


def transition():
	return '\n%s\n\n' % ('-' * 80)

# ============================================================================
# Body Elements
# ============================================================================


def bullet_list(elements, level=0):
	return '\n'.join(['  ' * level + '- ' + i.replace('\n', '\n  ') for i in elements]) + '\n\n'


def enumerated_list(elements, start=1, style='arabic', formatting='.'):  # не сработает, если (N)
	"""
:param elements: итерируемая последовательность, объект преобразования
:param start: начальная позиция; по умолчанию - первый пункт
:param style: стиль перечисления; по умолчанию - арабские цифры
:param formatting: символ отделения перечислителя от строки; по умолчанию - точка
"""
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

	return '\n'.join([
				'%s%s %s' % (counter, formatting, text.replace('\n', '\n' + ' ' * (len(str(counter)) + 2)))
				for counter, text in zip((first, second, *tuple('#' * (len(elements) - 2))), elements)]) \
		+ '\n\n'


def field_list(elements):
	"""
:param elements: последовательность пар имя-описание
"""
	return '\n'.join([':%s: %s' % (name, body.replace('\n', '\n\t')) for name, body in elements])


def grid_table(body, headers=None):
	"""
создает ascii-подобную таблицу с опциональным заголовком. пока не поддерживает объединение ячеек.
:param body: двумерная последовательность, где внешний уровень - набор последовательностей,
	внутренний - содержимое ячеек. например:
	``(('q', 'w', 'e'), ('r', 't', 'y'))``
:param headers: последовательность с заголовками, по умолчанию - нет
:return:
"""
	table = prettytable.PrettyTable(header=True if headers else False, hrules=prettytable.ALL)
	if headers:
		table.field_names = headers
	for row in body:
		table.add_row(row)
	out_table = table.get_string()
	return re.sub('\|\n(\+-{3,})+\+\n\|', lambda s: s.group(0).replace('-', '='), out_table, 1) if headers else out_table


def header(text, level):
	"""
:param text: строка, над которой совершается преобразование
:param level: требуемый уровень заголовка; допустимые значения [0; 5]
"""
	symbols = '=-\'.:"'
	return '%s\n%s\n\n' % (text, symbols[level] * len(text))


def paragraph(text, level=0):
	"""

:param text: строка, над которой совершается преобразование
:param level: уровень абзаца
:return:
"""
	return ''.join(('\t' * level + i + '\n' for i in text.splitlines())) + '\n'


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


# ============================================================================
# Inline Markup
# ============================================================================

def emphasis(text):
	return '*%s*' % text


def internal_link_jump(name, link):  # мб переписать. обозначить цели
	return '`%s <#%s>`_' % (name, link)


def internal_link_label(text):
	return '.. _%s:\n\n' % text


def strong(text):
	return '**%s**' % text


if __name__ == '__main__':
	# print(enumerated_list(['def sourcecode(text, strlimit=None):\n\ndef italic(text):', 'xxx']))
	hs = ('h1', 'h2', 'h3')
	bo = (('q', 'w', 'e'), ('r', 't', 'y'))
	print(grid_table(bo, hs))
