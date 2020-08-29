from distutils.core import setup
setup(
  name = 'pycanvas_BaDo2001',         # How you named your package folder (MyLib)
  packages = ['pycanvas_BaDo2001'],   # Chose the same as "name"
  version = '0.0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library to develop games in python for the web',   # Give a short description about your library
  author = 'Balint Dolla',                   # Type in your name
  author_email = 'balint.dolla@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/BaDo2001/pycanvas',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/BaDo2001/pycanvas/archive/0.0.5.tar.gz',    # I explain this later on
  keywords = ["Canvas", "Python", "Game development"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          "tornado",
          "asyncio",
          "Pillow",
          "colormap",
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  include_package_data=True
)
