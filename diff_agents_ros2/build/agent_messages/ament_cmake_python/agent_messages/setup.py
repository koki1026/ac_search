from setuptools import find_packages
from setuptools import setup

setup(
    name='agent_messages',
    version='0.0.0',
    packages=find_packages(
        include=('agent_messages', 'agent_messages.*')),
)
