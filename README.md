# NLPbrl Project        
**Pypi**: **link**     
**Package demo video**: **link**            
            
## Group information          
- **Group name: Ctrl-Alt-Del**          
- **Group members: Yuxin Chen & Siyue Gao**           
                      
## Introduction              
Natural Language Processing(NLP) is an important direction in Computer Science and Artificial Intelligent domains. It studies theories and methods that enable effective communication between computers and humans using natural language. NLP can be used in many applications like Question&Answer System, Spam Email Program, Voice Assistants and Translate, etc. An advanced and completer NLP application usually can be divided into two parts: Natural Language Understanding(NLU) and Natural Language Generation(NLG), which two aspects can also be divided into many small tasks such as Tokenization, Syntax Parsing, and Text Mining. So when we need to work on some big applications, it is very complicated to begin with the basic tasks. At this time, the Rosette Text Analytics API will be extremely powerful because it can help user to achieve many underlying tasks of NLP which makes completing an application much easier and more efficient.                                         
The NLPbrl wrapper API is a package for wrapping The Rosette Text Analytics API's functions. It can use natural language processing, and machine learning to analyze unstructured and semi-structured text in multilingual. It can provide a large number of powerful text analyses which has largely helped people to learn about natural language processing and to develop various applications for processing text.                        
         
- **Word Frequency Counter (cal_frequency)**         
- **Word Frequency Visualization (word_viz)**          
- **TF-IDF (key_extra_tfidf)**               
- **Entity Similarity (cal_simi)**               
- **Text Rank (cal_textRank)** (to find keywords)         
- **Entity Relationship Visualization (relation_viz)**               
- **Text Classification (cal_classification)**                           

## Application of NLPbrl       
NLP is a branch of Artificial Intelligence. Using this usable NLP Library, NLP can finding variety of applications in a wide range of industries with many languages, such as **Deep Learning research**, **Developing chatbots**, **patient data processing**, **text mining**, **text classification**, **text analysis**, **sentiment analysis**, **word sequencing**, **speech recognition and synthesis**, **machine translation** are only a few of the major NLP tasks this package can help achieve
This Library makes text preprocessing easier, which is able to transform free text phrases into structured characteristics that can be readily fed into Machine Learning or Deep Learning pipelines.             
               
## Package Structure
```
NLPbrlpackage
|
| README.md
| LICENSE.md
| requirements.txt
└─── NLPbrl 
    | Data_.py
    └─── Data (class)
        | get_token: Text tokenization
        | get_lang: Recognition of text language
        | get_vec: Word/Sentence embedding
        | get_posTag: Part-of-Speech tagging
        | get_senTag: Sentence cutting
        | get_relation: Relation extraction
        | get_classification: Text categorization
    | NLP_.py
    └─── NLP (class)
        | cal_frequency: Word frequency counter
        | word_viz: Word frequency visualization
        | key_extra_tfidf: TF-IDF
        | cal_simi: Entity similarity
        | cal_textRank: Text Rank to find keywords
        | relation_viz: Entity Relationship Visualization
        | cal_classification: Text categorization
        | __word_wash: Remove stop-words from the text
        | __check_limit: Check if the text length exceeds the API limit
        | __check_limit_tool: Cut out of length text to text list
        | __cal_TF: Calculate TF
        | __cal_IDF: Calculate IDF
        | __cal_TFIDF: Calculate TF-IDF
        | __simi_cal_euc: Euclidean distance calculation
        | __simi_cal_cos: Cosine distance calculation
        | __simi_cal_jac: Jaccard similarity calculation
```

## How to use

