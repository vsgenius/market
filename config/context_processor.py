from frontend.forms import AuthenticationAjaxForm, CreateProductForm


def get_context_data(request):
    context = {
        'login_ajax':AuthenticationAjaxForm(),
    }
    return context

def get_context_data2(request):
    context = {
        'create_product':CreateProductForm(),
    }
    return context