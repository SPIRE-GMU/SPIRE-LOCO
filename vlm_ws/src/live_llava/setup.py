from setuptools import find_packages, setup

package_name = 'live_llava'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubu',
    maintainer_email='ubu@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'vlm_start = live_llava.live_llava_start:main',
		'vlm_pub = live_llava.live_llava_pub:main',
		'vlm_sub = live_llava.live_llava_sub:main',        	
        ],
    },
)
