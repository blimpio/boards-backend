def get_ip_address(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')

    if ip_address:
        return ip_address.split(',')[-1]

    return request.META.get('REMOTE_ADDR')
