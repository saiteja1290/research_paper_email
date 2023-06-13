import html

html_encoded_text = 'Synthesis, Crystal Structure and Spectroscopic Studies of 2-{(<em class="a-plus-plus">E</em>)-[2-Hydroxyphenyl)imino]methyl}'

normal_text = html.escape(html_encoded_text)
print(normal_text)