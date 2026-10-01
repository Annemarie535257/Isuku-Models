# Isuku Waste Complaint Classification

This project builds a lightweight Natural Language Processing (NLP) system that classifies waste-management complaints into predefined categories such as missed pickup, delayed pickup, full bin, illegal dumping, and recycling questions.

The models are trained on labeled complaint data and exposed through a Streamlit application. Users can submit a complaint description for an automatic prediction, and the **Compare models** page can test the TF-IDF and GloVe embedding models on the same complaint.

## Project goal

Households often report waste issues in very informal, short, and varied language. The goal is to turn those natural-language complaints into a consistent label that can be routed to the correct waste service or admin team.

Examples:

- "The garbage truck did not collect our waste today." -> `missed_pickup`
- "The communal bin is overflowing." -> `full_bin`
- "Someone dumped rubbish by the roadside." -> `illegal_dumping`
- "Where can I recycle plastic bottles?" -> `recycling_question`

## Dataset

The project uses the waste complaint dataset stored in the repository as `waste_complaints_nlp_dataset.csv`.

It contains a balanced set of labeled text examples with the following structure:

```text
id | text | label
```

There are 1,000 examples total, with 200 samples in each of the five complaint categories.

## Model workflow

The training pipeline follows this flow:

1. Load the text dataset and validate the labels.
2. Clean the complaint text by lowercasing, removing punctuation, URLs, and extra spacing.
3. Split the data into training and testing sets using stratification.
4. Convert text to numeric features using TF-IDF.
5. Train a Logistic Regression classifier.
6. Evaluate the model with accuracy, precision, recall, F1-score, and a confusion matrix.
7. Save the final pipeline to `model/waste_complaint_classifier.joblib`.

## Problem being solved

Waste-management complaints are often short, informal, and inconsistent. A person may write that the truck did not arrive, the collection was late, a bin is overflowing, rubbish was dumped illegally, or they need recycling information. Sorting these complaints manually makes it harder for service teams to prioritize and respond consistently.

This project converts free-text complaints into one of five operational categories:

- `missed_pickup`
- `delayed_pickup`
- `full_bin`
- `illegal_dumping`
- `recycling_question`

The predicted category can be used by the household application, the admin dashboard, or the API to support faster complaint routing.

## Why TF-IDF?

TF-IDF stands for Term Frequency-Inverse Document Frequency. It is a popular feature extraction method for text classification because it converts raw text into numerical values that a machine-learning model can understand.

How it works:

- Term Frequency (TF): measures how often a word appears in a complaint.
- Inverse Document Frequency (IDF): reduces the weight of words that appear in many complaints and increases the importance of words that are more specific to certain categories.

This is useful in waste complaints because words like:

- "truck"
- "collect"
- "bin"
- "overflowing"
- "recycle"
- "dumped"
- "late"

carry strong category-specific meaning. TF-IDF helps the model focus on words that are more informative while ignoring common words that do not help much.

TF-IDF is especially useful here because the complaints are short, informal, and text-heavy rather than numerical. It transforms the text into sparse numerical vectors that capture important keyword patterns without needing deep language models.

## Why Logistic Regression?

Logistic Regression is a strong baseline model for text classification tasks, especially when the feature space is large but the dataset is still relatively small and structured.

It was chosen because it performs well with TF-IDF features, is fast to train, is easy to interpret, and is highly effective for multiclass text classification when the categories are distinct and the vocabulary is informative.

In this project, Logistic Regression learns patterns such as:

- "overflowing", "bin", "full" -> `full_bin`
- "recycle", "plastic", "bottles" -> `recycling_question`
- "truck", "not", "collected" -> `missed_pickup`
- "dumped", "roadside", "illegal" -> `illegal_dumping`

The model is also lightweight, which makes it practical for deployment in a Streamlit app or backend service where quick predictions are needed.

## Why these two were chosen together

TF-IDF + Logistic Regression is a classic and reliable combination for document classification:

- TF-IDF converts text into meaningful numeric features.
- Logistic Regression uses those features to separate classes.
- The pair works well even with a modest dataset size.
- Training is fast and the model is easy to deploy and maintain.
- It gives good accuracy without requiring large deep-learning models or heavy infrastructure.

This makes the approach ideal for a practical civic-tech project where the goal is a clear, accurate, and low-cost text classifier.

## Embeddings used for comparison

The separate notebook `waste-complaint-embeddings/train_waste_complaint_embeddings.ipynb` compares three ways of representing complaint text as numeric vectors. Each representation is evaluated with the same Logistic Regression classifier and the same stratified train/test split.

### Word2Vec

Word2Vec is trained on the complaint corpus. A complaint vector is created by averaging the vectors of the words in the complaint. It is lightweight and learns relationships from the project vocabulary, but its quality is limited when the training dataset is small.

### GloVe

GloVe uses the pre-trained `glove-wiki-gigaword-100` vectors loaded through Gensim. Complaint vectors are created by averaging the vectors for known words. This gives the model general word relationships learned from a larger corpus.

### BERT

The notebook uses `distilbert-base-uncased` and mean-pools its token representations to create a 768-dimensional complaint vector. BERT can capture more contextual information, but it requires substantially more memory and downloads model weights at first use.

The notebook compares accuracy, macro precision, macro recall, and macro F1, then selects the best embedding by macro F1 with accuracy as the tie-breaker.

## Training notebook

The full training workflow is implemented in `train_waste_complaint_classifier.ipynb`.

It includes:

- dataset validation
- text cleaning
- stratified train/test split
- TF-IDF vectorization
- Logistic Regression training
- evaluation metrics and confusion matrix
- saving the model pipeline to `model/waste_complaint_classifier.joblib`

The embedding comparison notebook includes:

- Word2Vec, GloVe, and DistilBERT feature extraction
- one shared stratified split for a fair comparison
- a metric table and confusion matrix for the best embedding
- saving the selected embedding classifier to `waste-complaint-embeddings/model/waste_complaint_embeddings_classifier.joblib`

## Model files

The trained pipeline is stored in:

```text
model/waste_complaint_classifier.joblib
```

This saved object contains both the TF-IDF vectorizer and the trained Logistic Regression classifier, so new complaint text can be passed directly into the model for prediction.

## Run the application

Install dependencies and start the Streamlit app from the project root:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app loads the saved model from `model/waste_complaint_classifier.joblib`, stores complaints in a local SQLite database, and saves uploaded images in the `uploads/` folder.

Use the following pages in the sidebar:

- **Household**: submit a complaint and receive a TF-IDF prediction.
- **Admin Dashboard**: review submitted complaints and their predicted categories.
- **Compare models**: test the TF-IDF and GloVe embedding models side by side.

The first comparison using GloVe may take longer because the pre-trained vectors are downloaded and cached locally by Gensim.

To run the embedding notebook separately:

```powershell
cd waste-complaint-embeddings
jupyter notebook train_waste_complaint_embeddings.ipynb
```

Run the dependency-installation cell first, then run the notebook cells in order. The notebook downloads the GloVe and DistilBERT resources when those cells are reached.

The current Streamlit application is designed for Python-capable hosts such as Streamlit Community Cloud, Render, or Railway. Netlify does not run Streamlit or Python model inference directly; a Netlify frontend would need a separate hosted Python API behind it.

## Results

The embedding comparison was executed on the balanced 10-record embedding sample, using five training records and five test records. Because the test set contains only one example per class, these results are illustrative rather than a production benchmark.

| Embedding | Accuracy | Macro precision | Macro recall | Macro F1 |
|---|---:|---:|---:|---:|
| Word2Vec | 0.60 | 0.467 | 0.60 | 0.500 |
| GloVe | 0.80 | 0.700 | 0.80 | 0.733 |
| BERT | 0.80 | 0.700 | 0.80 | 0.733 |

GloVe was selected as the best embedding by the notebook's tie-breaking order and saved for application comparison. A smoke test using the complaint `The communal bin is completely full.` produced `full_bin` from both models; the TF-IDF confidence was 91.7% and the GloVe confidence was 49.9%.

For a stronger conclusion, expand the embedding dataset and evaluate with cross-validation or a larger held-out test set. The current five-example test split is too small to support reliable generalization claims.

## Legacy Django API

The project also includes a Django API, which is retained for possible integrations that still require HTTP endpoints.

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000`.

Endpoints:

- `GET /api/health/` checks API and model availability.
- `POST /api/predict/` accepts JSON with a `description` and returns the predicted category and confidence.
- `POST /api/complaints/` accepts multipart form data and stores complaints after calling the model.
- `GET /api/complaints/` lists recent complaints.

## Summary

This project demonstrates a practical NLP classification workflow for civic service management. It provides a fast TF-IDF baseline and a side-by-side embedding experiment, allowing users to inspect how different text representations affect waste-complaint classification.

