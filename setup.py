from distutils.core import setup
import tally
import os

def path_parts(path):
    parts = []
    while True:
        head, tail = os.path.split(path)
        parts.insert(0, tail)
        if not head:
            break
        path = head
    return parts

packages = []
package_data = {}
tally_dir = os.path.join(os.path.dirname(__file__), 'tally')
for path, dirnames, filenames in os.walk(tally_dir):
    parts = path_parts(path)
    if '__init__.py' in filenames:
        package_name = '.'.join(parts)
        packages.append(package_name)
    elif filenames:
        package_data.setdefault(parts[0], []).extend([os.path.join(*(parts[1:] + [f])) for f in filenames])

setup(
    name='tally',
    version=tally.__version__,
    description='A Django application (and daemon) for collecting, storing, and aggregating metrics.',
    author='Dan Watson',
    author_email='dcwatson@gmail.com',
    url='https://github.com/dcwatson/tally',
    license='BSD',
    packages=packages,
    package_data=package_data,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ]
)
