from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='led_matrix',
    version='0.64',
    description='Toolz to play with a LED matrix',
    long_description=long_description,
    author='ben64',
    author_email='ben64@time0ut.org',
    packages=['led_matrix','led_matrix/tools','led_matrix/fonts','led_matrix/animation','led_matrix/screens','led_matrix/animation/images'],
    scripts=["bin/matrix_animation","bin/led_matrix","bin/matrix_manager"]
)
