
def get_post_data(request, *fields):
    data = {}
    for field in fields:
        data[field] = request.POST.get(field)
    return data
