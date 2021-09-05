from setuptools import setup

setup(
    name='materialflowlist',
    version='0.1',
    packages=['materialflowlist'],
    package_dir={'materialflowlist': 'materialflowlist'},
    package_data={'materialflowlist': [
        "input/*.*", "output/*.*", "flowmapping/*.*"]},
    include_package_data=True,
    install_requires = [
        'fedelemflowlist @ git+https://github.com/USEPA/Federal-LCA-Commons-Elementary-Flow-List@#egg=fedelemflowlist',
        'pandas>=0.22'],
    url='https://github.com/USEPA/materialflowlist.git',
    license='CC0',
    author='Wesley Ingwersen, Ashley Edelen, Ben Young, Troy Hottle',
    author_email='ingwersen.wesley@epa.gov',
    classifiers=[
        "Development Status :: Alpha",
        "Environment :: IDE",
        "Intended Audience :: Science/Research",
        "License :: CC0",
        "Programming Language :: Python :: 3.x",
        "Topic :: Utilities",
    ],
    description='Compiles and provides a standardized list of technosphere '
    'and waste flows for life cycle assessment'
)
