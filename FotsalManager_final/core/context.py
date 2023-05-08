from django.urls import reverse_lazy

def app_context(request):
    context = dict()
    context["is_htmx"] = None
    if request.META.get('HTTP_HX_REQUEST') == "true":
       context["is_htmx"] = True 
    else:
       context["is_htmx"] = False 
    context["current_view"] = request.resolver_match.view_name
    context["current_url"] = reverse_lazy(request.resolver_match.view_name)
    return context