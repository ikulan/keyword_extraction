# Customized Dictionaries


| File Name       | Description                                             |
| ---             | ---                                                     |
| dict.txt.big    | Default dictionary for tokenization and PoS tagging.    |
| stop_words.txt  | Filter words for keyword extraction                     |
| userdict.txt    | Customized dictionary for tokenization and PoS tagging. |


### Installation

OpenCC: Conversion between Traditional and Simplified Chinese

```shell
brew install opencc
```

### Edit the dictionary

* Edit in Simplified Chinese file (\*.zhs.txt)

* Generate Traditional Chinese version
```shell
opencc -i userdict.zhs.txt -o userdict.zht.txt
```

* Merge two versions of dictionary
```shell
cat userdict.zhs.txt userdict.zht.txt > userdict.txt
```

Only userdict.txt will be used.


### Abbreviations

| Abbreviation | Description         |
| ---          | ---                 |
| zhs          | Simplified Chinese  |
| zht          | Traditional Chinese |

