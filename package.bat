pyinstaller corpsestacker.py -F -w --add-bin C:\Anaconda3\Lib\site-packages\bearlibterminal\BearLibTerminal.dll;. --hidden-import pythoncom --exclude-module numpy --exclude-module scipy --exclude-module pandas --exclude-module IPython --exclude-module matplotlib --exclude-module PyQt --exclude-module PyQt5 --exclude-module PIL --exclude-module setuptools --exclude-module dist-utils --exclude-module sqlite3  --exclude-module jinja2 --exclude-module lib2to3 --exclude-module cryptography --exclude-module pygments --exclude-module requests --exclude-module PyQt5.QtGui --exclude-module tkinter --exclude-module jsonschema --exclude-module gevent --exclude-module multiprocessing --exclude-module decimal --exclude-module lzma --exclude-module tornado --exclude-module zmq --exclude-module ssl --exclude-module overlapped --exclude-module email --exclude-module socket
xcopy FAQ.md dist\ /Y
xcopy UbuntuMono-R.ttf dist\ /Y
cd dist
del corpsestacker.zip
"C:\Program Files\7-Zip\7z.exe" a corpsestacker.zip * 
cd ..