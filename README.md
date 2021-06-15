### _Пример использования Python-библиотеки [Streamlit] для подготовки сложноструктурных аналитических отчетов с помощью системы компьютерной верстки LaTeX_

#### Для работы с примерами будет достаточно установить:
- дистрибутив [MikTeX],
- LaTeX-редактор [TeXstudio].

#### Порядок работы с приложением
- Создать директорию проекта
```bash
$ mkdir my_project
```
- Скопировать в созданную директорию файлы из директории `python_examples/`, а именно:
    - опорный LaTeX-шаблон `latex_template_for_python.txt` (каркас LaTeX-документа) и стилевой файл `latex_templates/style_templates.sty` (конфигурирует макет страницы),
    - главный сценарий `streamlit_analyt_report_example.py` (здесь должна быть реализована логика Streamlit),
    - вспомогательный сценарий `helper_functions.py` (здесь собраны вспомогательные функции)
- Запустить Streamlit-приложение
```bash
$ streamlit run python_examples/streamlit_analyt_report_example.py
```
- На главной странице приложения задать значения управляющих параметров
- Скачать в рабочую директорию проекта подготовленный tex-файл (`base_template_for_latex.tex`)
- Запустить в рабочей директории pdf-компилятор (дважды!), передав ему имя tex-файла
```bash
$ pdflatex base_template_for_latex.tex
```
- Изучить резульататы работы компилятора. В текущей директории будет создан pdf-файл аналтического отчета `base_template_for_latex.pdf`

[MikTeX]: <https://miktex.org/download>
[TeXstudio]: <https://www.texstudio.org/>
[Streamlit]: <https://streamlit.io/>
