import UpstreamAPI as api
from config import token
import os
import json


def info():
    with open('data.json', 'r', encoding='utf-8') as f1:
        data = json.loads(f1.read())
    for i in data:
        del data[i]['schoolGuid']
        data[i]['list'] = list(data[i]['list'].keys())
    return [200, json.dumps({'status': 200, 'message': 'success', 'data': data})]


def grades(campus, studentCode, examName):
    if len(studentCode) != 9:
        return [404, json.dumps({'status': 404, 'message': 'studentCode wrong length'})]
    with open('data.json', 'r', encoding='utf-8') as f1:
        examData = json.loads(f1.read())
    if campus not in examData:
        return [404, json.dumps({'status': 404, 'message': 'campus did not exist'})]
    if examName not in examData[campus]['list']:
        return [404, json.dumps({'status': 404, 'message': 'exam did not exist'})]
    cacheDir = 'cache/' + str(campus) + '/' + str(examData[campus]['list'][examName]['examGuid']) + '/'
    cacheFile = 'cache/' + str(campus) + '/' + str(examData[campus]['list'][examName]['examGuid']) + '/' + str(
        studentCode) + '.json'
    schoolGuid = examData[campus]['schoolGuid']
    examGuid = examData[campus]['list'][examName]['examGuid']
    ruCode = examData[campus]['list'][examName]['ruCode']
    grade = examData[campus]['list'][examName]['grade']

    if os.path.exists(cacheFile):
        with open(cacheFile, 'r', encoding='utf-8') as f2:
            alldata = json.loads(f2.read())
    else:
        SubjectsAll = api.Subjects(
            token=token,
            schoolGuid=schoolGuid,
            examGuid=examGuid,
            studentCode=studentCode,
            grade=grade,
            ruCode=ruCode
        )
        if SubjectsAll is None:
            return [500, json.dumps({'status': 500, 'message': 'Request UpstreamAPI error'})]

        GradeAll = api.SubjectGrade(
            token=token,
            examSchoolGuid=schoolGuid,
            schoolGuid=schoolGuid,
            examGuid=examGuid,
            studentCode=studentCode,
            grade=grade,
            examType=SubjectsAll['examType'],
            ruCode=ruCode
        )

        if GradeAll is None:
            return [500, json.dumps({'status': 500, 'message': 'Request UpstreamAPI error'})]

        if not os.path.exists(cacheDir):
            os.makedirs(cacheDir)
        with open(cacheFile, 'w', encoding='utf-8') as f3:
            f3.write(json.dumps({'subjects': SubjectsAll, 'grades': GradeAll}))
        alldata = {'subjects': SubjectsAll, 'grades': GradeAll}

    data = {'exam': {}, 'grades': {}, 'questions': {}}

    data['exam']['total'] = alldata['grades']['report']['total']
    data['exam']['class'] = alldata['subjects']['unitCode'].replace(grade, '')

    data['grades']['all'] = {
        'Score': alldata['grades']['report']['myScore'],
        'fullScore': alldata['grades']['report']['fullScore'],
        'grade': alldata['grades']['report']['grade'],
        'classAvg': alldata['grades']['report']['classAvg'],
        'schoolAvg': alldata['grades']['report']['schoolAvg']
    }
    data['grades']['subjects'] = alldata['grades']['report']['otherKM']
    for i in data['grades']['subjects']:
        del i['kmTag']
    data['grades']['conclusion'] = alldata['grades']['pk']['conclusion']

    for i in alldata['subjects']['subjects']:
        if i['km'] != '总分':
            if i['code'] != 0:
                data['questions'][i['km']] = []
            else:
                data['questions'][i['km']] = i['question']['THs']
                for n in data['questions'][i['km']]:
                    if 'radar' in n:
                        del n['radar']
                    if 'objective' in n:
                        del n['objective']

    return [200, json.dumps({'status': 200, 'message': 'success', 'data': data})]


def answercard(campus, studentCode, examName):
    if len(studentCode) != 9:
        return [404, json.dumps({'status': 404, 'message': 'studentCode wrong length'})]
    with open('data.json', 'r', encoding='utf-8') as f1:
        examData = json.loads(f1.read())
    if campus not in examData:
        return [404, json.dumps({'status': 404, 'message': 'campus did not exist'})]
    if examName not in examData[campus]['list']:
        return [404, json.dumps({'status': 404, 'message': 'exam did not exist'})]
    cacheDir = 'cache/' + str(campus) + '/' + str(examData[campus]['list'][examName]['examGuid']) + '/'
    cacheFile = 'cache/' + str(campus) + '/' + str(examData[campus]['list'][examName]['examGuid']) + '/' + str(
        studentCode) + '.json'
    schoolGuid = examData[campus]['schoolGuid']
    examGuid = examData[campus]['list'][examName]['examGuid']
    ruCode = examData[campus]['list'][examName]['ruCode']
    grade = examData[campus]['list'][examName]['grade']

    if os.path.exists(cacheFile):
        with open(cacheFile, 'r', encoding='utf-8') as f2:
            alldata = json.loads(f2.read())['subjects']
    else:
        SubjectsAll = api.Subjects(
            token=token,
            schoolGuid=schoolGuid,
            examGuid=examGuid,
            studentCode=studentCode,
            grade=grade,
            ruCode=ruCode
        )
        if SubjectsAll is None:
            return [500, json.dumps({'status': 500, 'message': 'Request UpstreamAPI error'})]

        GradeAll = api.SubjectGrade(
            token=token,
            examSchoolGuid=schoolGuid,
            schoolGuid=schoolGuid,
            examGuid=examGuid,
            studentCode=studentCode,
            grade=grade,
            examType=SubjectsAll['examType'],
            ruCode=ruCode
        )

        if GradeAll is None:
            return [500, json.dumps({'status': 500, 'message': 'Request UpstreamAPI error'})]

        if not os.path.exists(cacheDir):
            os.makedirs(cacheDir)
        with open(cacheFile, 'w', encoding='utf-8') as f3:
            f3.write(json.dumps({'subjects': SubjectsAll, 'grades': GradeAll}))
        alldata = SubjectsAll

    urls = {}
    for i in alldata['subjects']:
        if 'question' in i:
            urls[i['km']] = api.getAnswerCardUrl(
                token=token,
                asiResponse=i['question']['asiresponse'],
                examGuid=examGuid,
                scoreStatus=alldata['scoreStatus'],
                examType=alldata['examType'],
                ruCode=ruCode
            )

    return [200, json.dumps({'status': 200, 'message': 'success', 'data': urls})]