from setuptools import setup

setup (
    name='jinja2-highlight',
    version='0.2',
    description='Jinja2 extension to highlight source code using Pygments',
    author='Tasos Latsas',
    author_email='tlatsas2000@gmail.com',
    url='https://github.com/tlatsas/jinja2-highlight',
    license='GNU GPLv3',
    packages=['jinja2_highlight'],
    install_requires=['Jinja2>=2.4'],
)
