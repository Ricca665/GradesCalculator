# GradesCalculator
Your virtual diary that is probably useful idk

# Features
- [x] Calculate your average grades
- [x] Get the minimum grade to not fail a subject
- [x] Memorizes your grades
- [x] Allows you to graph your grades
- [x] ESP32 Support

# How to install
Now, keep in mind that this program is still in beta and so i still didn't finalize the installation process
For now you have to do the following:

1. Clone the repo
```
git clone --recursive https://github.com/Ricca665/GradesCalculator
cd GradesCalculator
```

2. Install depedencies
```
pip install -r requirements.txt
```

3. Run the main program
```
cd src
python main.py
```

Soon this will get streamlined to a single .exe file (probably)

To install on an ESP32 as a requirement you **must** have [MicroPython with ulab](https://github.com/v923z/micropython-builder) AND pmremote already installed!

1. Download the latest package.zip from github releases
2. Clone the repo
```
git clone --recursive https://github.com/Ricca665/GradesCalculator
cd GradesCalculator
```
3. Run the installer with the package.zip path
```
cd src
python installer.py path/to/package.zip
```
4. Let it install (it's going to restart automatically)
5. Profit
