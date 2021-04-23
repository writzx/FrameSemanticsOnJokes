
The open-sesame module used in this contains a few configuration changes over the official repository.
However the changes are minimal and the official repository version can be used interchangeably. The changes are mostly related to training the dataset and for multi prediction.
For multiprediction it is required to use the open-sesame from this repo, since it changes the output ever so slightly to decide which frames belong to which joke.

The model data from the link below needs to be downloaded and placed in the repository root in order to run any kind of predictions.

Model data link: https://drive.google.com/file/d/1j0nmyqXG532J_TQ5ZL2dKOf9KweB_qV4/view?usp=sharing

There are three versions of the parser that can be used.

- **predict.py** should be used for single (or a few) joke parsing. It runs the parser individually for every joke line. It is very slow for multiple jokes.
- **predict_onepass.py** should be used for a long list of jokes. It runs the parser only once for all the jokes passed. It is fast since it only runs once.
- **multiparse.py** should be used when there are multiple jokes stored in multiple files. It is fast and lists the frames under the respective jokes.


To run the parser:
- place your jokes inside `sentences.txt` in `sesame-predict`. one joke per line.
- run the parser (either `predict.py` or `predict_onepass.py`)
- collect output from the `frames.txt`

To run the multiparser:
- place your jokes inside **.txt* files in `sesame-predict/jokes/`. one joke per line.
- run the multiparser `multiparser.py` 
- collect output **.frames* files from the jokes folder