# PUYA PY32F0: development platform for [PlatformIO](https://platformio.org)

## What's tested?

* OS: Windows 10
* Programmer device: J-Link (most probably, Chinese replica)
* Programmer tool: PyOCD
* MCU: PY32F002AW15U6TR
* Features tested:
    * Firmware compilation with Puya LL SDK
    * Erasing and flashing using PyOCD

## TODO

* Test build in debug mode
* Test and fix debugging via PyOCD
* Add support for HAL drivers
* Add more examples
* Add support for PY32F002Bx5, PY32F072xB MCU series (and probably others if I missed them)
* Add support for FreeRTOS

## Credits

Many thanks to creators and contributors of the following projects, this work is based on them.

* [OpenPuya](https://github.com/OpenPuya)
* [IOsetting/py32f0-template](https://github.com/IOsetting/py32f0-template)
