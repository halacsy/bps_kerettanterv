To build on OSX:

     brew cask install mactex-no-gui tex-live-utility  # install latex
     tlmgr update --self --all  # update tex packages
     pipenv shell  # create a virtualenv
     pipenv install  # install python dependencies
     make pedprog.pdf  # build the pdf
