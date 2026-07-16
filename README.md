# تعليمات التشغيل
1- افتح الطرفية(cmd.exe) واذهب الى مجلد ```finta-final```

2- اكتب هذا الأمر:
```backend\venv\Scripts\activate.bat  ```

ثم اكتب لتنزيل المكتبات المستخدم للمشروع:
``` pip install -r backend\requirements.txt ```

3- الآن لتشغيل backend اكتب هذا الأمر:
``` python.exe backend\main.py ```
اضغط Ctrl-C بشكل متكرر، لتوقف عمل backend.
ثم اكتب هذا الأمر:
``` python.exe -m app.seed```
ثم مرة اخرى شغل backend:
``` python.exe backend\main.py ```

4- قم بفتح طرفية ثانية (cmd.exe) واذهب الى مجلد ```finta-final```
اكتب هذه الأوامر:
```backend\venv\Scripts\activate.bat  ```

بنفس الطرفية الثانية، اذهب لمجلد ```finta-final\frontend```
اكتب هذه الأمر:
``` python -m http.server 3000 ```

5- فتح المتصفح(web browser)، واكتب:
localhost:3000
