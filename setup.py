from setuptools import setup

setup(
    name='seizure',
    version='',
    packages=['seizure', 'seizure.lib'],
    url='',
    license='',
    author='Shane Drury',
    author_email='shane.r.drury@gmail.com',
    description='Download VODs from Twitch',
    entry_points={'console_scripts': ['seizure = seizure.scripts:main'], },
    install_requires=['requests >= 2.5, < 2.6',
                      'progressbar2 >= 2.7 < 2.8'],
    )
