pyinstaller -y -F "temp-mail-service.py"

move dist/temp-mail-service.exe ../

rmdir /s /q build __pycache__ 

del /s /q temp-mail-service.spec

cd dist

move temp-mail-service.exe ..

cd ..

rmdir /s /q dist

rem upx -9 temp-mail-service.exe

exit