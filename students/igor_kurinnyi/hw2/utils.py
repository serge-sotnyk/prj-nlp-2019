 
def line_reader(file_name):
	with open(file_name, 'r') as f:
		for line in f:
			yield line.strip()


def write_line_to_file(file_name, text):
    with open(file_name, 'a') as f:
        f.write('{}\n'.format(text))