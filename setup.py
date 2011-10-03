from setuptools import setup, find_packages

setup(
    name="charon",
    packages=find_packages(),
    version="0.1.0",
    author="Matt Long",
    license="MIT",
    author_email="matt@mattlong.org",
    url="http://pypi.python.org/pypi/charon/",
    description="A set of tools to manage the load balancer HAProxy",
    long_description="Charon is a set a tools to manage an instance of the load balancer HAProxy. You can do so either locally or remotely using either the command-line directly or via a Fabric wrapper.",
    install_requires=['Fabric==1.2.2'],
    zip_safe=False,
    entry_points={
        'console_scripts': ['charon = charon:main',],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
