cd doc_sphinx
rmdir /Q /S _build
call make html
xcopy /S /Y _build\html ..\doc\
cd ..