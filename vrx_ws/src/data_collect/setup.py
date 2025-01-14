from setuptools import setup
from glob import glob

package_name = 'data_collect'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='koki-22',
    maintainer_email='amakou2626@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'data_collect_node = data_collect.data_collect:main',
            'wave_gain = data_collect:main',
            'wave_direction = data_collect:main',
            'wave_stepness = data_collect:main',
            'wave_period = data_collect:main',
        ],
    },
)
