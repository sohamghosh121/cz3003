from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden


def healthCheck(request):
    return HttpResponse('It\'s all good! Admin UI works :)')
