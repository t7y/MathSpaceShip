from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    'background.png',
    'spaceship.png',
    'player.png',
    'alien.png',
    'sad_alien.png',
    'bullet.png',
    'background.wav',
    'laser.wav',
    'explosion.wav'
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],
    'iconfile': 'spaceship.png',  # This will be your app icon
    'plist': {
        'CFBundleName': 'MathSpaceShip',
        'CFBundleDisplayName': 'MathSpaceShip',
        'CFBundleIdentifier': 'com.mathspaceship.game',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.10',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 