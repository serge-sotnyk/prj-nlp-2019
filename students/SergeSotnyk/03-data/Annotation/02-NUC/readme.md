# Task

Process data from the 
[NUCLE Error Corpus](http://www.comp.nus.edu.sg/~nlp/conll14st.html#nucle32) and 
analyze inter-annotator agreement in it (general and for each error type).

# Solution

All code can be found in [process_and_analyze_nuc.py](process_and_analyze_nuc.py). 
Run it and you'll get the processing results.

It is assumed that every sentence has at least 3 annotators. If we found more 
annotators in the mistakes annotations, this number is accordingly increased. 

# Results

```
C:\Users\ssotn\Anaconda3\envs\nlp\python.exe D:/git-nlp/ss-prj-nlp-2019/students/SergeSotnyk/03-data/Annotation/02-NUC/process_and_analyze_nuc.py
File 'D:\git-nlp\ss-prj-nlp-2019\students\SergeSotnyk\03-data\Annotation\02-NUC\data\official-2014.combined-withalt.m2' is already existed, downloading was skipped.
1312 sentences found.
Total corrections: 4821
Total corrections agreed by position: 1633
Total corrections agreed by type: 1370
Detailed log can be found in file "D:/git-nlp/ss-prj-nlp-2019/students/SergeSotnyk/03-data/Annotation/02-NUC\data/log.txt"
```

Fragment of log file:

```
S Hence , there were also tensions if participants felt that they could neither pass on information to relatives who needed to know ( such as nieces and nephews ) nor persuade those with authority ( the parents ) to do so .

Annotators assumed: 4 (agreement threshold = 2.0)
Total corrections: 7
Agreed by pos: 4
Agreed by type: 4


S The notion of authority also extended 'vertically' .

Annotators assumed: 3 (agreement threshold = 1.5)
Total corrections: 1
Agreed by pos: 0
Agreed by type: 0


S For example , a grandmother may have more authority to pass on information than an aunt , even when she is not at genetic risk herself while the aunt is .

Annotators assumed: 3 (agreement threshold = 1.5)
Total corrections: 1
Agreed by pos: 0
Agreed by type: 0


S From a practitioner 's perspective these findings are important because if lay constructs of the family and kinship are a social construct they may not be in line with geneticists ' views of family relationships , or about which blood ( or non-blood ) relatives should be informed and by whom ; this is also likely to be dependent on the cultural and ethnic context .

Annotators assumed: 3 (agreement threshold = 1.5)
Total corrections: 3
Agreed by pos: 1
Agreed by type: 1


S Ultimately , one must bring attention to who may benefit from such information and assisting those at risk to make considered decisions about disclosure .

Annotators assumed: 3 (agreement threshold = 1.5)
Total corrections: 3
Agreed by pos: 2
Agreed by type: 2


S Whose duty it is to inform at risk relatives or not greatly depends on the personal moral and the nature of how 'directive ' the risk is to them .

Annotators assumed: 4 (agreement threshold = 2.0)
Total corrections: 4
Agreed by pos: 2
Agreed by type: 1


S People with close blood relationship generally carry some similar genes .

Annotators assumed: 3 (agreement threshold = 1.5)
Total corrections: 2
Agreed by pos: 0
Agreed by type: 0


S In this case , if one of the family members or close relatives is found to carry genetic risk , it is better for the patient to tell his/her close relatives about the issue and let others known about the risk so that his/her familay members are able to perform some daily excesses to prevent the potential disease or they may go to hospital and check for the correspongding flows .

Annotators assumed: 4 (agreement threshold = 2.0)
Total corrections: 10
Agreed by pos: 6
Agreed by type: 5

```