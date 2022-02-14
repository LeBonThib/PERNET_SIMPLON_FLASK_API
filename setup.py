from setuptools import setup

setup(
    name='G3_API',
    version='1.0',
    long_description=__doc__,
    packages=['G3_API'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)