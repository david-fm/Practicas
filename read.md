# Digital Library

## License

[Creative Commons CCZero](http://www.opendefinition.org/licenses/cc-zero)

## Dataset Description

Dataset based on the public domain dataset "Biblioteca Digital. Documentos en dominio público"
<br>
This Dataset is based on the 11 april of 2023 it could have change in the future.

## Metadata Description

| Field | Description |
| ----- | ----------- |
| title | Title of the document |
| Author | Author or authors of the document |
| date | Date of the document |
| origin_country | Country of the document |
| language | Language of the document |
| subject | Subject of the document |
| genre | Genre of the document |
| digital_version | Digital version of the document |
| ocr | OCR version of the document |
| words | Number of words of the document |
| book_id | Identifier of the book |
| number_of_volumes | Indicate the number of volumes there are of the same book |
| entropy | Entropy of the document |

Entropy values can be compared with the ones in the file 'mean_entropy.csv' which contains the mean entropy of 5 texts in spanish that have been properly converted to digital format.


The process to get the values and to select the ns to be calculated in the entropy where obtain from an analysis done in the next [paper](https://arxiv.org/pdf/0901.4784.pdf). Where the authors analyze the entropy of spanish texts and between the things they find out one is that the n should be calculated between 1 and 18, to get the best results.

## File Description

The file are made up of 2 parts, the first one is the id of the book and the second is the volume identifier, which goes from 0 to number_of_volumes - 1.