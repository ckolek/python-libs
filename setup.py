from distutils.core import setup

PACKAGES = [
    'cwk',
    'cwk.usage',
    'cwk.util',
    'cwk.util.strings'
]

setup(
        name='cwk',
        version='1.0',
        description='CWK Python Libraries',
        author='Christopher W. Kolek',
        author_email='christopher.w@kolek.me',
        url='christopher-w.kolek.me',
        packages=PACKAGES,
        package_dir={'cwk': 'lib'}
    )
