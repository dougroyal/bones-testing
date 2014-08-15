from setuptools import setup, find_packages

requires = [
]

setup(
    name='bones-testing',
    version='0.0.1',
    description='A behavior-driven testing framework',
    long_description=open('README.rst').read(),
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Python Software Foundation License',
    ],
    author='Doug Royal',
    author_email='douglasroyal@gmail.com',
    license='Python Software Foundation License',
    url='http://houseofquark.com/bones-testing',
    keywords='test',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=requires,
    entry_points = {
        'console_scripts': ['bones = bones.main:main']
    },
)
