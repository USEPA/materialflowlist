from setuptools import setup

setup(
    name='materialflowlist',
    version='0.1',
    packages=['materialflowlist'],
    package_dir={'materialflowlist': 'materialflowlist'},
    package_data={'materialflowlist': [
        "input/*.*", "output/*.*", "flowmapping/*.*"]},
    include_package_data=True,
    install_requires = ['pandas>=0.22'],
    url='https://github.com/USEPA/materialflowlist.git',
    license='CC0',
    author='Troy Hottle',
    author_email='ta.hottle@gmail.com',
    classifiers=[
        "Development Status :: Alpha",
        "Environment :: IDE",
        "Intended Audience :: Science/Research",
        "License :: CC0",
        "Programming Language :: Python :: 3.x",
        "Topic :: Utilities",
    ],
    description=''
)
