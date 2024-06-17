import pandas as pd
import pickle
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import os

current_dir = os.path.dirname(__file__)
dataset_dir = os.path.join(current_dir, 'dataset')

VERBOSE = True
TRAIN_DATA_PATH = os.path.join(dataset_dir, 'training_data.csv')
TEST_DATA_PATH = os.path.join(dataset_dir, 'test_data.csv')
MODEL_PATH = os.path.join(current_dir, 'model.pkl')
RANDOM_SEED = 101
TEST_SIZE = 0.33

def load_train_dataset():
    df_train = pd.read_csv('./dataset/training_data.csv')
    features = df_train.iloc[:, :-2]
    labels = df_train['prognosis']
    if VERBOSE:
        print("Training data dimensions:", df_train.shape)
        print("Features shape:", features.shape)
        print("Labels shape:", labels.shape)
    return features, labels, df_train

def load_test_dataset():
    df_test = pd.read_csv('./dataset/test_data.csv')
    features = df_test.iloc[:, :-1]
    labels = df_test['prognosis']
    if VERBOSE:
        print("Testing data dimensions:", df_test.shape)
        print("Features shape:", features.shape)
        print("Labels shape:", labels.shape)
    return features, labels, df_test

def train_val_split(features, labels):
    X_train, X_val, y_train, y_val = train_test_split(
        features, labels,
        test_size=0.33,
        random_state=101
    )
    if VERBOSE:
        print("Training samples:", X_train.shape[0], "Validation samples:", X_val.shape[0])
    return X_train, y_train, X_val, y_val

def train_model():
    features, labels, train_data = load_train_dataset()
    X_train, y_train, X_val, y_val = train_val_split(features, labels)
    model = RandomForestClassifier(n_estimators=10, random_state=101)
    model.fit(X_train, y_train)
    val_accuracy = model.score(X_val, y_val)
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)
    conf_matrix = confusion_matrix(y_val, y_pred)
    class_report = classification_report(y_val, y_pred)
    cv_score = cross_val_score(model, X_val, y_val, cv=3)
    if VERBOSE:
        print("Training accuracy:", val_accuracy)
        print("Validation predictions:", y_pred)
        print("Validation accuracy:", accuracy)
        print("Confusion matrix:\n", conf_matrix)
        print("Cross-validation score:\n", cv_score)
        print("Classification report:\n", class_report)
    with open(MODEL_PATH, 'wb') as model_file:
        pickle.dump(model, model_file)

def predict(model_path=MODEL_PATH, input_data=None):
    try:
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
    except Exception as error:
        print(f"Error loading model: {error}")
        return None

    if input_data is not None:
        probabilities = model.predict_proba(input_data)
        predictions = model.classes_[probabilities.argmax(axis=1)]
        return predictions, probabilities.max(axis=1)
    else:
        features, labels, _ = load_test_dataset()
        probabilities = model.predict_proba(features)
        predictions = model.classes_[probabilities.argmax(axis=1)]
        accuracy = accuracy_score(labels, predictions)
        class_report = classification_report(labels, predictions)
        return accuracy, class_report, probabilities.max(axis=1)

if __name__ == "__main__":
    train_model()
    test_accuracy, test_report, test_probabilities = predict()
    print("Test accuracy:", test_accuracy)
    print("Test data classification report:\n", test_report)
    print("Test data probabilities:\n", test_probabilities)
