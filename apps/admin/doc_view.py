from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils import json_status
from apps.doc.models import Doc
from .forms import DocUploadForm
from utils.decorators import user_permission_required


@method_decorator([csrf_exempt,user_permission_required(Doc)], name="dispatch")
class DocUploadView(View):

    def get(self, request):
        return render(request, 'admin/doc/doc_upload.html')

    def post(self, request):
        form = DocUploadForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            desc = form.cleaned_data.get("desc")
            file_path = form.cleaned_data.get("file_path")
            Doc.objects.create(title=title, desc=desc, file_path=file_path, author=request.user)
            return json_status.result()
        print(form.errors)
        return json_status.params_error(message=form.get_error())
