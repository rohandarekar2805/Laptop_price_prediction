import os
import pickle
import pandas as pd
from django.shortcuts import render # Needed for the index_page
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LaptopSerializer

# 1. THE API VIEW (For JSON/DRF)
class PredictPriceAPI(APIView):
    def post(self, request):
        serializer = LaptopSerializer(data=request.data)
        if serializer.is_valid():
            try:
                CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
                model = pickle.load(open(os.path.join(CURRENT_DIR, 'model.pkl'), 'rb'))
                encoders = pickle.load(open(os.path.join(CURRENT_DIR, 'encoders.pkl'), 'rb'))

                d = serializer.validated_data
                
                # Encode and prepare data (Order: Status, Brand, Model, CPU, RAM, Storage, Storage type, GPU, Screen, Touch)
                input_data = {
                    'Status': encoders['Status'].transform([d['Status']])[0],
                    'Brand': encoders['Brand'].transform([d['Brand']])[0],
                    'Model': encoders['Model'].transform([d['Model']])[0],
                    'CPU': encoders['CPU'].transform([d['CPU']])[0],
                    'RAM': d['RAM'],
                    'Storage': d['Storage'],
                    'Storage type': encoders['Storage type'].transform([d['Storage_type']])[0],
                    'GPU': encoders['GPU'].transform([d['GPU']])[0],
                    'Screen': d['Screen'],
                    'Touch': encoders['Touch'].transform([d['Touch']])[0],
                }

                df = pd.DataFrame([input_data])
                prediction = model.predict(df)
                return Response({'prediction': round(float(prediction[0]), 2)})
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)

# 2. THE PAGE VIEW (To load the initial HTML with dropdowns)
def index_page(request):
    # This loads the dropdown options from your encoders
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        encoders = pickle.load(open(os.path.join(CURRENT_DIR, 'encoders.pkl'), 'rb'))
        context = {
            'brands': sorted(encoders['Brand'].classes_),
            'cpus': sorted(encoders['CPU'].classes_),
            'gpus': sorted(encoders['GPU'].classes_),
            'models': sorted(encoders['Model'].classes_),
            'storage_types': sorted(encoders['Storage type'].classes_),
            'statuses': sorted(encoders['Status'].classes_),
        }
    except:
        context = {} # Fallback if pkl isn't found yet
        
    return render(request, 'index.html', context)