# Classification and Detection of Toxic Content on Reddit

This project aims to develop and toxicity detection model for online systems. We have trained and tested 5 models: Logistic Regression, Random Forest, Decision Trees, XGBoost, and Fine-tuned Distill-BERT.

# Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)
- [Contact](#contact)

## Installation

Step 1: Fork this project to your work environment
Step 2: Run the command "pip install -r requirements.txt"

## Usage

### Getting the Dataset

Step 1: Open the file "get_comments.py", and set subreddits of your choice in the 'subreddit_names' list. Also set the csv file name in which you want the comments to be added.
Step 2: Now hit run and the comments will be collected automatically in the csv file.

### Classifying the Comments

Step 1: Arrange all the csv files in a directory, and specify the path of the directory in "classify_comments.py".
Step 2: Now hit run and all the csv files will be automatically labelled and collected in an "output_subreddit" directory.

Note: Make sure to replace all the API Key values by your own API Key.

### Concatenation

Step 1: You can concat all the files in the directory into one csv file by giving path to "output_subreddit" in "concat.py".

### Finally creating our own model

Open up "create_models.ipynb" in Google Collab and changing runtime type to GPU. Now specify the paths to your 'total_comments_labelled.csv' file, and run the model. You can save the model.

Note: At the bottom we have tested the models using new dataset too. You can extract new comments and test them using the same process.

### Making streamlit app 

Once the process is done, you can specify the saved model's path on "app.py", and run "streamlit run app.py" on the terminal. Voila, your app is ready!

## Configuration

The modules used in "create_models.ipynb" might not be installed in your system. Make sure to install them using "!pip install [module_name]" in your notebook.

## License

This project is licensed under the [MIT License](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

Ujjawal Gusain - ujjawalgusain31@gmail.com
