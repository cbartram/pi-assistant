# pi-assistant
A raspberry pi based smart home voice controlled assistant.

## Prerequisites

Requirements for the software and other tools to build, test and push 
- [Python 3.9](https://www.python.org)
- [Example 2](https://www.example.com)

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

**NOTE:** You may have to install `pocketsphinx` and `pyaudio` outside of pipenv using:
```shell

$ pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
```

## Running the tests

Coming Soon

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