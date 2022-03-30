# pi-assistant
A raspberry pi based smart home voice controlled assistant.

## Prerequisites

Requirements for the software and other tools to build, test and push 
- [Python 3.9](https://www.python.org)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

Use `pipenv install` to install the necessary dependencies and then activate the virtual environment using:

```shell
$ source $(pipenv --venv)/bin/activate
```

## Installation

You will need to install both `swig` and `portaudio` outside of pip before using this software. This software requires
python version 3.9 which will automatically be installed in a virtual environment when you install with [Pipenv](https://pipenv.pypa.io/en/latest/).

### Linux

Run apt-get on linux to install swig and portaudio

````shell
apt-get install swig
apt-get install portaudio
````

### MacOS

You can install swig and portaudio using [HomeBrew](https://brew.sh).

```shell
$ brew install swig
$ brew install portaudio 
```

Once you have installed swig and portaudio you can use [Pipenv](https://pipenv.pypa.io/en/latest/) to install the other
python dependencies.

```shell
$ pipenv install
```

### Troubleshooting Installation

You may have to install and `pyaudio` outside of pipenv using if `pipenv install` fails for any reason. Sometimes pyaudio complains about missing
C files. Use the command below to install pyaudio into your virtual env outside of pipenv.

```shell

$ pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
```

You may also run into issues installing `pocketsphinx` like: `fatal error: 'al.h' file not found` if you are running on MacOS Big Sur (catalina seems to be fine).
This snippet installs from a fork of the project with a patch for MacOS Big Sur:

```shell
$ pip3 install git+https://github.com/Im-Fran/pocketsphinx-python
```

## Running Unit Tests

Unit tests are managed through `pytest` and can be run by simply running the command:

```shell
$ pytest
```

### Style test

Coming soon

## Deployment

Coming soon

## Built With

  - [Python 3.9](https://python.org/) - Programming language
  - [Wit.ai](https://wit.ai/) - Intent and utterance recognition service
  - [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) - Python audio analysis and speech recognition library

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code
of conduct, and the process for submitting pull requests to us.

## Versioning

We use [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/cbartram/pi-assistant/tags).

## Authors

  - **Christian Bartram** - *Initial code & project concept* - [cbartram](https://github.com/cbartram/pi-assistant)

See also the list of
[contributors](https://github.com/cbartram/pi-assistant/contributors)
who participated in this project.

## License

This project is licensed under the [MIT LICENSE](LICENSE.md)
Creative Commons License - see the [LICENSE.md](LICENSE.md) file for
details

## Acknowledgments

  - SpeechRecognition python package for taking the time to make a great developer experience!