from setuptools import setup, find_packages

setup(
    name='get_iplayer_python',
    version='1.0.3',
    author='Adam Brewer',
    author_email='adam@adambrewer.co.uk',
    url="https://github.com/a-m-brewer/get-iplayer-python",
    packages=find_packages(),
    install_requires=['tldextract', 'requests', 'beautifulsoup4', 'lxml', 'enlighten', 'urllib3'],
    entry_points={
        'console_scripts': [
            'get-iplayer-python = get_iplayer_python.__main__:main'
        ]
    }
)
