from setuptools import setup, find_packages

setup(
    name='OpenSpecimenAPIconnector',
    version='0.9.1',    
    description='Python API commands to interact with OpenSpecimen',
    url='https://github.com/bibbox/OpenSpecimenAPIconnector.py/tree/master',
    author='Christam Schorn and Simon Streit',
    author_email='simon.streit@medunigraz-at',
    license='BSD 2-clause',
    install_requires=['pandas',
                      'numpy'               
                      ],

    classifiers=[
        'Development Status :: 3 -Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: API communication interface',
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

