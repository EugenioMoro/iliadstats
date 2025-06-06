from setuptools import setup, find_packages

setup(
    name='iliadstats',
    version='0.1.0',
    author='Eugenio Moro',
    author_email='eugenio.moro@polimi.it',
    description='A Python module for scraping information from Iliad\'s dashboard.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EugenioMoro/iliadstats',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'lxml>=4.9.3',
        'fastapi>=0.103.1',
        'uvicorn>=0.23.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='iliad scraper dashboard stats',
    project_urls={
        'Bug Tracker': 'https://github.com/EugenioMoro/iliadstats/issues',
        'Source Code': 'https://github.com/EugenioMoro/iliadstats',
    },
)