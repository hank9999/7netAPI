import requests
import json

base_headers = {
    'Accept-Charset': 'UTF-8',
    'X-CodePush-Plugin-Name': 'cordova-plugin-code-push',
    'Version': '3.0.9',
    'X-CodePush-SDK-Version': '3.0.1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 5G Build/QKQ1.191222.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36',
    'X-CodePush-Plugin-Version': '1.13.1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'szone-score.7net.cc',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}


def Subjects(token, examGuid, studentCode, schoolGuid, grade, ruCode=3709021):
    if not examGuid or not studentCode or not schoolGuid or not grade:
        raise Exception('Missing required parameters')
    url = 'https://szone-score.7net.cc/Question/Subjects'
    headers = base_headers
    headers['Token'] = token
    data = {
        'examGuid': str(examGuid),
        'studentCode': str(studentCode),
        'grade': str(grade),
        'ruCode': str(ruCode),
        'schoolGuid': str(schoolGuid),
    }
    r = requests.post(url, data=data, headers=headers)
    r = json.loads(r.text)
    if r['message'] != 'success':
        return None
    return r['data']


def SubjectGrade(token, examSchoolGuid, examGuid, studentCode, schoolGuid, grade, subject='总分', studentName='刘',
                 ruCode=3709021, examType=3):
    if not token or not examSchoolGuid or not examGuid or not studentCode or not schoolGuid:
        raise Exception('Missing required parameters')
    url = 'https://szone-score.7net.cc/Question/SubjectGrade'
    headers = base_headers
    headers['Token'] = token
    data = {
        'examSchoolGuid': str(examSchoolGuid),
        'examGuid': str(examGuid),
        'studentCode': str(studentCode),
        'subject': str(subject),
        'studentName': str(studentName),
        'grade': str(grade),
        'ruCode': str(ruCode),
        'examType': str(examType),
        'vip': '1',
        'compareClassAvg': '1',
        'schoolGuid': str(schoolGuid),
    }
    r = requests.post(url, headers=headers, data=data)
    r = json.loads(r.text)
    if r['message'] != 'success':
        return None
    return r['data']


def getAnswerCardUrl(token, asiResponse, examGuid, scoreStatus, examType, ruCode=3709021, studentName='刘'):
    if not token or not asiResponse or not examGuid or not scoreStatus or not examType:
        raise Exception('Missing required parameters')
    url = 'https://szone-score.7net.cc/Question/AnswerCardUrl'
    headers = base_headers
    headers['Token'] = token
    data = {
        'asiResponse': str(asiResponse),
        'examGuid': str(examGuid),
        'studentName': str(studentName),
        'scoreStatus': str(scoreStatus),
        'examType': str(examType),
        'ruCode': str(ruCode)
    }
    r = requests.post(url, data=data, headers=headers)
    r = json.loads(r.text)
    if r['message'] != 'success':
        return None
    return r['data']