### _Пример использования Python-библиотеки [Streamlit] для подготовки сложноструктурных аналитических документов с помощью системы компьютерной верстки LaTeX_

#### Для работы с примерами будет достаточно установить:
* дистрибутив [MikTeX],
* LaTeX-редактор [TeXstudio].

#### Порядок работы с приложением
Создать директорию проекта
```bash
$ mkdir my_project
```
Скопировать в созданную директорию файлы из директории python_examples/, а именно:
* опорный LaTeX-шаблон `latex_template_for_python.txt` и стилевой файл `latex_templates/style_template.sty`,
* главный сценарий `streamlit_analyt_report_example.py`,
* вспомогательный сценарий `helper_functions.py`

Запустить Streamlit-приложение
```bash
$ streamlit run python_examples/streamlit_analyt_report_example.py
```
На главной странице приложения задать значения управляющих параметров
Скопировать в рабочую директорию проекта подготовленный tex-файл (`base_template_for_latex.tex`)
Запустить в рабочей директории pdf-компилятор, передав ему имя tex-файла
```bash
$ pdflatex base_template_for_latex.tex
```
В рабочей директории будет создан pdf-файл аналтического отчета `base_template_for_latex.pdf`

[MikTeX]: <https://miktex.org/download>
[TeXstudio]: <https://www.texstudio.org/>
[Streamlit]: <https://streamlit.io/>
