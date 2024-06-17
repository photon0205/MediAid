import os
import pickle
import pandas as pd
import openai 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SymptomSerializer

current_dir = os.path.dirname(__file__)
ml_model_dir = os.path.join(current_dir, '../../ml_model')

MODEL_PATH = os.path.join(ml_model_dir, 'model.pkl')
TRAINING_PATH = os.path.join(ml_model_dir, 'dataset/training_data.csv')
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

class SymptomSuggestionView(APIView):
    def get(self, request, format=None):
        try:
            df_train = pd.read_csv(TRAINING_PATH)
            symptoms = list(df_train.columns[:-2])
            return Response(symptoms, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiagnoseView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(MODEL_PATH, 'rb') as model_file:
            self.model = pickle.load(model_file)
        openai.api_key = OPENAI_API_KEY 

    def post(self, request):
        if not self.model:
            return Response({'error': 'Model not loaded'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = SymptomSerializer(data=request.data)
        if serializer.is_valid():
            try:
                symptoms = serializer.validated_data['symptoms']
                symptoms_dict = {symptom: 1 if symptom in symptoms else 0 for symptom in self.model.columns[:-1]}
                df_test = pd.DataFrame([symptoms_dict])
                predictions = self.model.predict(df_test)
                probabilities = self.model.predict_proba(df_test)
                disease = predictions[0]
                probability = probabilities.max() * 100
                response_data = {
                    'disease': disease,
                    'probability': probability
                }
                # Interaction with OpenAI for chat advice
                chat_input = f"I have been infected with {disease} disease. What should I do next?"
                gpt3_response = self.ask_openai(chat_input)
                response_data['advice'] = gpt3_response
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Error predicting: {e}")
                return Response({'error': 'Error predicting'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def ask_openai(self, question):
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=question,
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error while querying OpenAI: {e}")
            return "Sorry, I'm unable to process your request right now."