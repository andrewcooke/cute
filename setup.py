
import setuptools

setuptools.setup(name='cute',
                 packages=setuptools.find_packages(),
                 version='0.0.0',
                 author='andrew cooke',
                 author_email='andrew@acooke.org',
                 description='static website generator',
                 url='https://github.com/andrewcooke/cute',
                 include_package_data=True,
                 install_requires=[
                     'PyRSS2Gen',
                     ],
                 classifiers=(
                     "Programming Language :: Python :: 2.7",
                     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                     "Operating System :: OS Independent",
                     "Development Status :: 4 - Beta",
                 ),
                 )

