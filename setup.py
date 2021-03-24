from setuptools import setup, find_packages

with open('README_pypi.md') as f:
    long_description = f.read()


setup(
    name='OpenSpecimenAPIconnector',
    version='0.9.2',    
    description='Python API commands to interact with OpenSpecimen',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    url='https://github.com/bibbox/OpenSpecimenAPIconnector.py/tree/master',
    author='Christam Schorn and Simon Streit',
    author_email='simon.streit@medunigraz.at',
    license='BSD 2-clause',
    install_requires=['pandas',
                      'numpy',               
                      'requests',
		      'faker',
		      'names',
		      'xlsxwriter',
		      'openpyxl'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='Openspecimen, API, Python Openspecimen',  # Optional,
    packages=find_packages(where='src'),
    package_dir={"":"src"}

)

