import os
import pickle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SymptomSerializer

current_dir = os.path.dirname(__file__)

MODEL_PATH = os.path.join(current_dir, '../../ml_model/model.pkl')

class DiagnoseView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(MODEL_PATH, 'rb') as model_file:
            self.model = pickle.load(model_file)

    def post(self, request):
        serializer = SymptomSerializer(data=request.data)
        if serializer.is_valid():
            symptoms = serializer.validated_data['symptoms']
            predictions, probabilities = self.model.predict_proba([symptoms]), self.model.classes_
            max_prob_idx = predictions.argmax(axis=1)
            disease = probabilities[max_prob_idx]
            probability = predictions[0][max_prob_idx] * 100
            return Response({
                'disease': disease[0],
                'probability': probability[0]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
