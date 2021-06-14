from distutils.core import setup

setup(
    name='while-lang',  # How you named your package folder (MyLib)
    packages=['whilelang'],  # Chose the same as "name"
    version=
    '0.1',  # Start with a small number and increase it with every change you make
    license=
    'MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description=
    'TA small Parser and Interpreter for the Educational WHILE - Programming Language by Uwe Schoening.',  # Give a short description about your library
    author='Henrik Wachowitz',  # Type in your name
    author_email='henrik.wachowitz@campus.lmu.de',  # Type in your E-Mail
    url=
    'https://github.com/ricffb/while-lang',  # Provide either the link to your github or to your website
    download_url=
    'https://github.com/ricffb/while-lang/archive/refs/tags/v0.1.tar.gz',  # I explain this later on
    keywords=['WHILE', 'EDUCATIONAL', 'LMU', 'FSK',
              'TIMI'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'parsy',
    ],
    entry_points={'console_scripts': ['whilelang = whilelang.__main__:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Education',  # Define that your audience are developers
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)