from setuptools import setup

package_name = 'matrix_3_5'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='prathamesh',
    maintainer_email='prathamesh@todo.todo',
    description='TODO: Package description',
    license='Apache license 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'homo = matrix_3_5.homo:main'
        ],
    },
)
