# Plugin Setup

This document details how to setup some of the plugins which are require additional configuration. This document also
details each of the plugins as well as what they do!


# Weather Plugin

### Utterances

- "What's the weather like?"
- "What's the temperature?"
- "What's the temperature outside?"
- "What is the weather like today?"
- "Is it hot out today?"
- "Is it cold out today?"

### About

The weather plugin is intended to grab the local weather for your region and have the assistant convey information like:

- temperature
- sky conditions
- what the temperate feels like
- forecast

### Configuration

You will need an API key from [OpenWeatherMap](https://openweathermap.org/) in order to use this plugin. Simply sign up
grab your API key from your dashboard and set it as an environmental variable like so: 

```shell
export OPEN_WEATHER_API_KEY=<your API key>
```

The plugin configuration will handle the rest! 

**Note:** Since this plugin is disabled by default you need to go into `resources/application.yml` and change the `plugins.weather.enabled` value 
to `true`.

# Feit Electric Lights

## Utterances

- "Turn on my living room lights"
- "Turn off my kitchen lights"
- "Turn <off/on> my <insert room here> lights"

## About

The Feit electric plugin allows you to control your Feit electric home smart lights through the pi-assistant. You
can turn on/off any of your Feit electric bulbs in any room. 


## Configuration 
Since the bulbs themselves are manufactured and setup through
[Tuya](https://www.tuya.com/) there is a fairly involved set of steps to setting them up (unlike philips hue or Lifx).

The process is very well documented and [can be found here](https://github.com/jasonacox/tinytuya#tuya-device-preparation). This
process has been tested and verified to work with this codebase once the TinyTuya package is setup properly. Once
you have your Tuya client id and secret export them as environmental variables like so:

```shell
export TUYA_CLIENT_ID=<your client id>
export TUYA_CLIENT_SECRET=<your client secret>
```

The application configuration will use this with the `TinyTuya` package to scan for bulbs on your network. This process can
take up to 30-40 seconds so the initial scan will write all the information it needs about your lights to a file called: 
`devices.json` which can be found in: `plugins/feit_electric_smart_lights/devices.json`. This file acts as a cache to 
quickly load your Feit electric lights. The file will look something like this:

```json
{
  "192.168.1.1": {
    "ip": "192.168.116",
    "gwId": "7607160e3370",
    "active": 2,
    "ability": 0,
    "mode": 0,
    "encrypt": true,
    "productKey": "MaeaHJC",
    "version": "3.3",
    "dps": {
      "devId": "716cc50eda",
      "dps": {
        "1": false,
        "2": "white",
        "3": 255,
        "4": 0,
        "5": "ff00000000ffff",
        "6": "00ff0000000000",
        "7": "ffff500100ff00",
        "8": "ffff8003ff000000ff000000ff000000000000000000",
        "9": "ffff5001ff0000",
        "10": "ffff0505ff000000ff00ffff00ff00ff0000ff000000"
      }
    },
    "name": "Kitchen Light 2",
    "key": "<A unique authorization key generated using your tuya client id / secret>"
  },
  { ... Other lights on the network }
}
```

# Philips Hue Smart Lights

## Utterances

## About

## Configuration
