from setuptools import setup
import os
from glob import glob

package_name = 'img_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Aki Moto',
    maintainer_email='aki.robosys2025@gmail.com',
    description='Processing image',
    license='BSD-3-Clause',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'exte_img = img_pkg.exte_img:main',
            'denoi_img = img_pkg.denoi_img:main',
        ],
    },
)
