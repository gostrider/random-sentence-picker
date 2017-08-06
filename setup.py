from distutils.core import setup

setup(
    name='random_sentence',
    url='https://github.com/gostrider/random-sentence-picker',
    description='Random picking sentences from url',
    author='gostrider',
    author_email='tiddybeardaywalker@hotmail.com',
    version='0.1',
    packages=['random_sentence', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=['beautifulsoup4==4.6.0', 'spacy==1.9.0', 'requests==2.18.3']
)
