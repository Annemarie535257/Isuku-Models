# Waste Complaint Classification Using Word Embeddings

This project implements a waste complaint classification model using word embeddings for feature extraction. The model is designed to classify various types of waste complaints based on text descriptions.

## Project Structure

- `train_waste_complaint_embeddings.ipynb`: A Jupyter notebook that contains the implementation of the classification model. It includes sections for:
  - Loading and preprocessing the dataset
  - Creating word embeddings
  - Training the classification model
  - Evaluating its performance
  - Saving the trained model

- `waste_complaints_nlp_dataset.csv`: A CSV file that contains the labeled dataset of waste complaints. It includes the following columns:
  - `id`: Unique identifier for each complaint
  - `text`: Text description of the complaint
  - `label`: Corresponding label for the complaint

- `model/.gitkeep`: An empty file used to ensure that the model directory is tracked by Git.

- `requirements.txt`: A file that lists the Python package dependencies required for the project, including libraries for data manipulation, machine learning, and word embeddings.

## Setup Instructions

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages using the following command:

   ```
   pip install -r requirements.txt
   ```

## Usage Guidelines

- Open the `train_waste_complaint_embeddings.ipynb` notebook in Jupyter Notebook or Jupyter Lab.
- Follow the instructions in the notebook to load the dataset, preprocess the text, create word embeddings, train the model, and evaluate its performance.
- The trained model will be saved in the `model` directory for future use.

## License

This project is licensed under the MIT License.