import os
from pathlib import Path
from unittest import result
from django.shortcuts import render
from django.http import JsonResponse

# djangotemplates/example/views.py
from django.views.generic import TemplateView # Import TemplateView
from .price_prediction import *
from .scraper import run_scraper
from .ai_dataset_prep_df import run_ai
from .nn_final import run_neural

def home(request):
    return render(request, 'home.html', {})


def lstm_algorithm(request):
    
    # Get the all files into pickle folder where _history is append at the end to show in the frontend filter for chart
    CSV_DIR = Path.joinpath(Path(__file__).resolve().parent, 'pickles')
    pickle_files = []
    for pkl_file in os.listdir(CSV_DIR):
        if pkl_file.find('_history.pkl') > -1:
            pickle_files.append(pkl_file.replace('_history.pkl', ''))
    
    context = {'csv_files': pickle_files}
    
    # Handle the post request on the RUN button call
    if request.method == 'POST':
        responseData = {}
        
        # Run the price prediction from the py file and pass selected filter to the method
        prediction, true_price = run(request.POST.get('csv', None))
        responseData['prediction'] = [float(i[0]) for i in prediction]
        responseData['true_price'] = [float(i[0]) for i in true_price]
        return JsonResponse(responseData)
    
    return render(request, 'portfolio/lstm-algorithm.html', context)

@csrf_exempt
def web_scraping(request):
    
    # Handle the post request on the RUN button call
    if request.method == 'POST':
        responseData = {}
        result = run_scraper()
        responseData['result'] = result.to_dict('split')
        return JsonResponse(responseData)
    
    return render(request, 'portfolio/web_scraping.html')
    
@csrf_exempt
def decision_tree(request):
    
    # Get the all files into pickels folder to show in the frontend filter for datagrid
    CSV_DIR = Path.joinpath(Path(__file__).resolve().parent, 'pickles')
    context = {'pickle_files': os.listdir(CSV_DIR)}
    
    # Handle the post request on the RUN button call
    if request.method == 'POST':
        responseData = {}
        print(request.POST.get('pickle', None))
        result = run_ai(request.POST.get('pickle', None))
        result = result.fillna(0)
        responseData['result'] = result.to_dict('split')
        del responseData['result']['index']
        return JsonResponse(responseData)
    
    return render(request, 'portfolio/decision_tree.html', context)

@csrf_exempt
def neural_network(request):
    
    # Get the all files into pickels folder to show in the frontend filter for datagrid
    CSV_DIR = Path.joinpath(Path(__file__).resolve().parent, 'test_csv_nn')
    context = {'csv_files': os.listdir(CSV_DIR)}
    
    # Handle the post request on the RUN button call
    if request.method == 'POST':
        responseData = {}
        prediction, history = run_neural(request.POST.get('csv', None))
        responseData['prediction'] = str(prediction[0][0])
        responseData['history'] = history
        
        return JsonResponse(responseData)
    
    return render(request, 'portfolio/neural_network.html', context)

@csrf_exempt
def data_manipulation(request):
    
    # Get the all files into pickels folder to show in the frontend filter for datagrid
    CSV_DIR = Path.joinpath(Path(__file__).resolve().parent, 'pickles')
    context = {'pickle_files': os.listdir(CSV_DIR)}
    
    # Handle the post request on the RUN button call
    if request.method == 'POST':
        responseData = {}
        print(request.POST.get('pickle', None))
        result = run_ai(request.POST.get('pickle', None))
        result = result.fillna(0)
        responseData['result'] = result.to_dict('split')
        del responseData['result']['index']
        return JsonResponse(responseData)
    
    return render(request, 'portfolio/data_manipulation.html', context)