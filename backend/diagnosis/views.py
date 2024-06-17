import os
import pickle
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SymptomSerializer

current_dir = os.path.dirname(__file__)
ml_model_dir = os.path.join(current_dir, '../../ml_model')

MODEL_PATH = os.path.join(ml_model_dir, 'model.pkl')
TRAINING_PATH = os.path.join(ml_model_dir, 'dataset/training_data.csv')
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
                print(response_data)
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                # Handle the exception during prediction
                print(f"Error predicting: {e}")
                return Response({'error': 'Error predicting'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
