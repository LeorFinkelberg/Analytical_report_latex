### _Пример использования Python-библиотеки [Streamlit] для подготовки сложноструктурных аналитических отчетов с помощью системы компьютерной верстки LaTeX_

#### Для работы с примерами будет достаточно установить:
- дистрибутив [MikTeX],
- LaTeX-редактор [TeXstudio].

#### Порядок работы с [приложением](https://share.streamlit.io/leorfinkelberg/analytical_report_latex/python_templates/streamlit_analyt_report_example.py)
- Создать директорию проекта, поддиректорию `python_templates` для Python-сценариев, поддиректорию `latex` для файлов \*.tex и \*.sty и поддиректорию `figures` для графических материалов
```bash
$ mkdir my_project/python_templates
$ mkdir my_project/latex 
$ mkdir my_project/latex/figures
```
- Скопировать в директорию `my_project/python_templates` файлы из директории `python_templates/`:
    - главный сценарий `streamlit_analyt_report_example.py` (здесь должна быть реализована логика Streamlit),
    - вспомогательный сценарий `helper_functions.py` (здесь собраны вспомогательные функции),
	- опорный LaTeX-шаблон для Python `latex_template_for_python.txt` (каркас LaTeX-документа).
- В директорию `my_project/latex` скопировать:
    - стилевой файл из `latex_templates/style_templates.sty` (конфигурирует макет страницы).
- А в директорию `my_project/latex/figures` из директории `latex_templates/figures` скопировать:
    - графические материалы, которые должны войти в аналитический отчет.
- Из корня проекта запустить Streamlit-приложение
```bash
$ streamlit run python_templates/streamlit_analyt_report_example.py
```
- На главной странице приложения задать значения управляющих параметров
- Скачать в поддиректорию проекта `my_project/latex` созданный приложением файл `base_template_for_latex.tex`
- Запустить в директории `my_project/latex` pdf-компилятор (дважды!), передав ему имя tex-файла
```bash
$ pdflatex base_template_for_latex.tex
```
- Изучить резульататы работы компилятора. В текущей директории будет создан pdf-файл аналтического отчета `base_template_for_latex.pdf`

[MikTeX]: <https://miktex.org/download>
[TeXstudio]: <https://www.texstudio.org/>
[Streamlit]: <https://streamlit.io/>
