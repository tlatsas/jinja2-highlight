from setuptools import setup

setup (
    name='jinja2-highlight',
    version='0.4.0',
    description='Jinja2 extension to highlight source code using Pygments',
    keywords = 'syntax highlighting',
    author='Tasos Latsas',
    author_email='tlatsas2000@gmail.com',
    url='https://github.com/tlatsas/jinja2-highlight',
    license='GNU GPLv3',
    packages=['jinja2_highlight'],
    install_requires=[
        'Jinja2>=2.4',
        'Pygments>=1.5'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
)
