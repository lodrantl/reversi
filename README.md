# reversi
Reversi igra napisana v Python ogrodju Kivy.

[![Build status Appveyor](https://ci.appveyor.com/api/projects/status/tbeqt4jq9bvpayo9?svg=true)](https://ci.appveyor.com/project/lodrantl/reversi)
[![Build status Travis](https://travis-ci.org/lodrantl/reversi.svg?branch=master)](https://travis-ci.org/lodrantl/reversi)

## Nightly builds
* [Windows 32-bit](https://s3-eu-west-1.amazonaws.com/reversi-nightlies/reversi-v0.1-nightly-win32.exe)
* [Windows 64-bit](https://s3-eu-west-1.amazonaws.com/reversi-nightlies/reversi-v0.1-nightly-win_amd64.exe)
* [macOS](https://s3-eu-west-1.amazonaws.com/reversi-nightlies/reversi-v0.1-nightly-osx.dmg)
* [Linux](https://s3-eu-west-1.amazonaws.com/reversi-nightlies/reversi-v0.1-nightly-linux)

## Dependencies
* Linux
    ```bash
    sudo apt-get install -y  ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
    ```
* macOS - ima probleme, ker aplikacija ni podpisana, potrebno je začasno izklopiti GateKeeper
    ```bash
    sudo spctl --master-disable
    
    UPORABLJAJ APLIKACIJO
  
    sudo spctl --master-enable
    ```

## Priprava okolja
Razvojno okolje bomo nastavili z Anacondo, kasneje pa bomo aplikacijo zapakirali z PyInstaller oz. cx_freeze.

#### Anaconda
Ustvari okolje:
```bash
conda create --name reversi_env python=3.4
```
Windows:
```bash
activate reversi_env
```
Mac / Linux:
```bash
source activate reversi_env
```
Namesti kivy:
* [Windows](https://kivy.org/docs/installation/installation-windows.html)
* [macOS](https://kivy.org/docs/installation/installation-osx.html)
* [Linux](https://kivy.org/docs/installation/installation-linux.html)

### [Plan dela](./PLAN.md)

### [Shema projekta](./SHEMA.md)

