from bottle import route, run, request


@route('/<bbb>')
def do(bbb):
    print(f"{bbb}: {request.json}")
    print(f"{bbb}: {request.body}")
    return "OK"


run(host='0.0.0.0', port=8080, debug=True)
