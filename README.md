# pi-assistant

A raspberry pi based smart home voice controlled assistant which can do things like get the time and date, find the weather,
play songs on Spotify, and control your home lighting!

## Prerequisites

Requirements for the software and other tools to build, test and push 
- [Python 3.9](https://www.python.org)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

Use `pipenv install` to install the necessary dependencies and then activate the virtual environment using:

```shell
$ source $(pipenv --venv)/bin/activate
```

## Installation

You will need to install `pocketsphinx`, `swig` and `portaudio` outside of pip before using this software. Pocketsphinx is used as a locally run NLP
solution which transcibes audio files to text. This is important because pi-assistant listens to all audio in the background waiting 
for your configured key words (think "hey google", or "alexa"). Instead of using a costly cloud service to process all audio (even when the user isn't directly speaking
to pi-assistant) pocketsphinx can do the audio transcription for free! 

Once the keyword is detected pi-assistant will then leverage the cloud service to do audio transcription because its faster and we know for a fact
we want to audio to be processed.

This software requires python version 3.9 which will automatically be installed in a virtual environment when you install with [Pipenv](https://pipenv.pypa.io/en/latest/).

### Linux

Run apt-get on linux to install pocketsphinx, swig, and portaudio:

````shell
$ apt-get install swig
$ apt-get install portaudio
$ apt-get install pocketsphinx 
````

### MacOS

You can install pocketsphinx, swig, and portaudio using [HomeBrew](https://brew.sh).

```shell
$ brew install swig
$ brew install portaudio

# Only install pocketsphinx with brew if it fails to install with pipenv
$ brew install pocketsphinx
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

## Running 

You can run this on any machine with a speaker and a microphone by using:

```shell
export ENVIRONMENT=prod
export WIT_ACCESS_TOKEN=<your wit.ai access token for your app>

python3 -m pi_assistant.main

# Now use the configured keyword to invoke the assistant try:
# "Hey google" then pause for a second while PocketSphinx processes the text 
# and then ask "what time is it?"
# pi-assistant should give you the current time!

```

Make sure you add various utterances to your [Wit.ai](https://wit.ai) account and tie the utterances to specific intents within the Wit
console. Once you have created your list of intents add them to `application.yml` like: 

```shell
wit:
  intents:
    - "date"
    - "time"
    - "wit$cancel"
    - "wit$get_weather"
    - "whatever_your_intent_is_called"
```

The default plugins which are enabled by default expect that within your [Wit.ai](https://wit.ai) account you have utterances for the following intents:

- date
- time
- wit$cancel

## Plugin Setup

See [Individual plugin setup](./docs/plugins.md) for more information on 
setting up and configuring each individual plugin like Philips Hue, Feit Electric, Weather, and more. 

## Running Unit Tests

Unit tests are managed through `pytest` and can be run by simply running the command:

```shell
$ python3 -m pytest ./test -v
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