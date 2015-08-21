from setuptools import setup,  find_packages

VERSION = '0.1.0'

setup(
    name='bones-testing',
    version=VERSION,
    description='A behavior-driven testing framework',
    long_description=open('README.rst').read(),
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
    ],
    author='Doug Royal',
    author_email='douglasroyal@gmail.com',
    license='Apache Software License',
    url='http://houseofquark.com/bones-testing',
    keywords='test',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=open('requirements.txt').readlines(),
    tests_require=open('test-requirements.txt').readlines(),
    entry_points = {
        'console_scripts': ['bones = bones.main:main']
    },
)
