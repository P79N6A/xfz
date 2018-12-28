from django.shortcuts import render, reverse
from django.http import *
from django.views.generic import View
from django.conf import settings
from django.views.decorators.http import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import string
import random
import hashlib
import base64
import os, time, json, re


# Create your views here.

@method_decorator([csrf_exempt, require_http_methods(['GET', 'POST'])], name='dispatch')
class UploadView(View):
    def __init__(self):
        super(UploadView, self).__init__()

    def _random_filename(self, rawfilename):
        letters = string.ascii_letters
        random_filename = str(time.time()) + "".join(random.sample(letters, 5))
        filename = hashlib.md5(random_filename.encode('utf-8')).hexdigest()
        subfix = os.path.splitext(rawfilename)[-1]
        return filename + subfix

    def _json_result(self, state='', url='', title='', original=''):
        result = {
            "state": state,
            'url': url,
            'title': title,
            'origianl': original
        }
        return JsonResponse(result)

    def _upload_to_server(self, upfile, filename):
        '''上传文件到自己服务器'''
        with open(os.path.join(settings.UEDITOR_UPLOAD_PATH, filename), 'wb') as fp:
            for chunk in upfile.chunks():
                fp.write(chunk)
        url = reverse("ueditor:send_file", kwargs={"filename": filename})
        return 'SUCCESS', url, filename, filename

    def _action_config(self):
        '''处理config类型的响应'''
        config_path = settings.UEDITOR_CONFIG_PATH
        with open(config_path, 'r', encoding='utf-8') as fp:
            result = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        return JsonResponse(result)

    def _action_upload(self, request):
        '''处理文件上传'''
        upfile = request.FILE.get('upfile')
        filename = self._random_filename(upfile.name)

        qiniu_result = None
        server_result = None

        if settings.UEDITOR_UPLOAD_TO_SERVER:
            server_result = self._upload_to_server(upfile, filename)

        if server_result and server_result[0] == 'SUCCESS':
            return self._json_result(*server_result)
        else:
            return self._json_result()

    def _action_scrawl(self, request):
        base64data = request.form.get("upfile")
        img = base64.b64decode(base64data)
        filename = self._random_filename('xx.png')
        with open(os.path.join(settings.UEDITOR_UPLOAD_PATH, filename), 'wb') as fp:
            fp.write(img)
        url = reverse('ueditor:send_file', kwargs={"filename": filename})
        return self._json_result('SUCCESS', url, filename, filename)

    def dispatch(self, request, *args, **kwargs):
        super(UploadView, self).dispatch(request, *args, **kwargs)
        action = request.GET.get('action')
        if action == 'config':
            return self._action_config()
        elif action in ['uploadimage', 'uploadvide', 'uploadfile']:
            return self._action_upload(request)
        elif action == 'uploadscrawl':
            return self._action_scrawl(request)
        else:
            return self._json_result()


def send_file(request, filename):
    fp = open(os.path.join(settings.UEDITOR_UPLOAD_PATH, filename), 'rb')
    response = FileResponse(fp)
    return response
