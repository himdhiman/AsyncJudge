from celery import shared_task
from api import models, serializers
from rest_framework.response import Response
from django.http import JsonResponse
import os, shutil
from pathlib import Path
from random import randint
from api.models import Problem, Submission
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from django.core import serializers as djSerializer

BASE_DIR = Path(__file__).resolve().parent.parent


channel_layer = get_channel_layer()

@shared_task
def runCode(body, uid):
    response = serializers.SubmissionSerializer(data = body)
    if(response.is_valid()):
        inst = response.save()

        if(inst.inputGiven != ""):
            data = {'id' : inst.id, 'code' : inst.code, 'lang' : inst.language, 'inp' : inst.inputGiven, 'problemId' : inst.problemId}
        else:
            data = {'id' : inst.id, 'code' : inst.code, 'lang' : inst.language, 'problemId' : inst.problemId}
        
        probId = data['problemId']
        totaltc = Problem.objects.get(id = probId).totalTC

        tempPath = os.path.join(BASE_DIR, "Codes", str(uid))
        
        os.mkdir(tempPath)

        open(os.path.join(tempPath, 'input.txt'), 'a').close()
        open(os.path.join(tempPath, 'output.txt'), 'a').close()
        open(os.path.join(tempPath, 'output.log'), 'a').close()

        if data['lang'] == "CP":
            open(os.path.join(tempPath, 'main.cpp'), 'a').close()
            f = open(os.path.join(tempPath, 'main.cpp'), "w")
            f.write(data['code'])
            f.close()
        if data['lang'] == "P3":
            open(os.path.join(tempPath, 'main.py'), 'a').close()
            f = open(os.path.join(tempPath, 'main.py'), "w")
            f.write(data['code'])
            f.close()      

        isInputGiven = False
        
        if('inp' in data.keys() and data['inp'] != None):
            isInputGiven = True
            f = open(os.path.join(tempPath, 'input.txt'), "w")
            f.write(data['inp'])
            f.close()

        os.chdir(tempPath)
        
        if data['lang'] == "CP":
            os.system('g++ "main.cpp"')
            cnt = 0
            if(isInputGiven == False):
                for i in range(1, totaltc+1):
                    isSame = True
                    inpPath = os.path.join(BASE_DIR, "media", 'TestCases', str(probId), 'input'+str(i)+'.txt')
                    os.system(f'a.exe < {inpPath} > output.txt')
                    with open(os.path.join(BASE_DIR, "media", 'TestCases', str(probId), 'output'+str(i)+'.txt')) as f1, open('output.txt') as f2:
                        for line1, line2 in zip(f1, f2):
                            if line1 != line2:
                                isSame = False
                                break
                    if(isSame):
                        cnt += 1
                        async_to_sync(channel_layer.group_send)("user_"+str(uid), {'type': 'sendStatus', 'text' : f"1/{i}/{totaltc}"})
                    else:
                        async_to_sync(channel_layer.group_send)("user_"+str(uid), {'type': 'sendStatus', 'text' : f"0/{i}/{totaltc}"})

                f = open(os.path.join(tempPath, 'output.txt'), "r+")
                f.truncate(0)
                f.close()
            else:
                os.system('a.exe < input.txt > output.txt')
            
            os.system('g++ "main.cpp" 2> "output.log"')

        if data['lang'] == "P3":
            os.system('python main.py < input.txt > output.txt 2>"output.log"')
        os.chdir(BASE_DIR)
        out = open(os.path.join(tempPath, 'output.txt'), "r")
        code_output = out.read()
        out.close()
        f = open(os.path.join(tempPath, 'input.txt'), "r+")
        f.truncate(0)
        f.close()
        tcString = str(cnt) + "/" + str(totaltc)
        if os.stat(os.path.join(tempPath, "output.log")).st_size != 0:
            f = open(os.path.join(tempPath, "output.log"), "r")
            error = f.read()
            f.close()
            shutil.rmtree(tempPath)
            Submission.objects.filter(pk = data['id']).update(error = error, status = "CE", testCasesPassed = tcString)
        else:
            shutil.rmtree(tempPath)
            Submission.objects.filter(pk = data['id']).update(outputGen = code_output, status = "AC", testCasesPassed = tcString)

        # response = serializers.SubmissionSerializer(models.Submission.objects.get(id = inst.id))
        response = models.Submission.objects.filter(id = inst.id)
        async_to_sync(channel_layer.group_send)("user_"+str(uid), {'type': 'sendResult', 'text' : djSerializer.serialize('json', response)})
        
        # return JsonResponse(response, safe = False)