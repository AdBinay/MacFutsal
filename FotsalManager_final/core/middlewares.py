from urllib.parse import urlparse

def htmx_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if (
            request.headers.get("HX-Request") == "true"
            and response.status_code == 302
        ):
            ref_header = request.headers.get("Referer", "")
            if ref_header:
                referer = urlparse(ref_header)
                querystring = f"?next={referer.path}"
            else:
                querystring = ""

            redirect = urlparse(response["location"])
            response.status_code = 204
            response.headers["HX-Redirect"] = f"{redirect.path}"
            response.headers['Vary'] = 'HX-Request'
        return response

    return middleware