from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'PokerAI'
LONG_DESCRIPTION = "Texas Holdem' simulator for up to 23 players."

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pokerAI", 
        version=VERSION,
        author="Matthew Barbattini",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy", "collections", "copy"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)