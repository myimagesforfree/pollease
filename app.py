from bottle import route, run, template, request

gbl = dict()
gbl['data'] = []

@route('/')
def home():
  return gbl

@route('/hello/<name>')
def index(name):
  return template('<b>Hello {{name}}</b>!', name=name)

@route('/bjork', method='POST')
def do_a_thing():
  gbl['data'].append(request.body.read())

run(host='0.0.0.0', port=8080)
