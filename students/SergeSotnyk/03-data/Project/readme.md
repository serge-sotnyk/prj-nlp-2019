# Task

0. Perform initial data collection for your project.
0. Devise and describe a way to collect data for your course project using crowdsourcing or from the users. Implement a proof-of-concept.

# Що знайдено 

(Далі просто копіюю текст із текстового файлику, то ж россійською):

* AutomaticKeyphraseExtraction - https://github.com/snkim/AutomaticKeyphraseExtraction.git
Содержит несколько корпусов с текстами и ключевыми словами


* sentence-compression - https://github.com/google-research-datasets/sentence-compression.git
Корпус с предложениями и их сокращенными, но эквивалентными по смыслу вариантами.


* seq2seq-keyphrase - закачано со ссылки в https://github.com/memray/seq2seq-keyphrase
Несколько корпусов с английскими текстами и ключевыми словами к ним.
inspec\
kp20k\
krapivin\
nus\
semeval\


* WikiHow-Dataset - https://github.com/mahnazkoupaee/WikiHow-Dataset.git
английская версия аннотаций по WikiHow. Для других языков нужно скрепить сайт


* BBC_News_Summary - https://www.kaggle.com/pariza/bbc-news-summary/data
Достаточно чистый набор из двух директорий аналогичной структуры, содержащий новостные статьи и их аннотации.


* NEWS SUMMARY (https://www.kaggle.com/sunnysai12345/news-summary) consists of 4515 examples.
Два CSV файла. В меньшем (news_summary.csv) такие поля: 
author	date	headlines	read_more	text (тут 3 предложения саммари)	ctext (текст статьи)
В большем (98402 строки, непонятно, где саммари): 
headlines	text

* SUMMAC - TIPSTER Text Summarization Evaluation Conference(https://www-nlpir.nist.gov/related_projects/tipster_summac/cmp_lg.html)
As part of the TIPSTER SUMMAC effort, a corpus of 183 documents from the Computation and Language (cmp-lg) collection has been marked up in xml and made available as a general resource to the information retrieval, extraction, and summarization communities.
Как указано в описании - XML, аннотация содержится в теге <ABSTRACT>, Текст в <BODY>

# Як збирати

Ці корпуси в більшості випадків знайдено через аналіз різних papers та ісходних кодів до них.

Також є плани скрейпити Вікіпедию для того, щоб отримати сінопсіси до літературних творів. Літературні твори планую зібрати ті, що є у відкритому доступі (ресурси по типу проекту Гутенберг). Це дозволить самостійно створити корпуси для різних мов та мати досить об'ємні аннотації.
