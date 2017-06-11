from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from forms import *
from models import *

import psycopg2



# Get connection from database entry util
def get_connection(database):
	connect_string = "host={} port={} dbname={} user={} password={}".format(database.host_and_port.split(':')[0], database.host_and_port.split(':')[1], database.name, database.user, database.password)
	conn = psycopg2.connect(connect_string)
	return conn


# Create your views here.
def index(request):
	return render(request, 'frontend/index.html', {})

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if not form.is_valid():
			context = {'form': form}
			return render(request, 'frontend/login.html', context)

		users = User.objects.all()
		user = users.filter(username=request.POST.get('username')).first()

		if user is None:
			context = {'message': 'This profile does not exist.', 'form': form}
			return render(request, 'frontend/login.html', context)
		else:
			auth = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
			if auth:
				auth_login(request, auth)
				return redirect('queries')
			else:
				context = {'message': 'Unable to log in.', 'form': form}
				return render(request, 'frontend/login.html', context)
	else:
		form = LoginForm()
		context = {
			"form": form,
			"next": request.GET.get('next')
		}
	return render(request, 'frontend/login.html', context)

def create_account(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			querydict = {
				"first_name": request.POST['first_name'],
				"last_name": request.POST['last_name'],
				"username": request.POST['username'],
				"email": request.POST['email'],
				"password":	request.POST['password'],
			}
			user = User.objects.create_user(querydict['username'], querydict['email'], querydict['password'])

			if querydict.get('first_name'):
				user.first_name = querydict['first_name']
			if querydict.get('last_name'):
				user.last_name = querydict['last_name']
			user.save()

			profile = Profile(user=user)
			profile.save()

			auth = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
			if auth:
				auth_login(request, auth)
				return redirect('queries')
			else:
				context = {'message': 'Unable to log in.', 'form': form}
				return render(request, 'frontend/create.html', context)
		else:
			context = {'form': form, "message": form.errors}
			return render(request, 'frontend/create.html', context)
	else:
		form = UserForm()
		context = {'form': form}
		return render(request, 'frontend/create.html', context)

def query_view(request):
	queries = [{
		"id": query.id,
		"timestamp": query.created_ts,
		"database": query.database.name,
		"created_by": query.created_by.user.username,
		"query_string": query.querystring[:50],
	} for query in Query.objects.all()]

	context = {
		"queries": queries
	}
	return render(request, 'frontend/requests.html', context)

def query_view_json(request):
	queries = [{
		"timestamp": str(query.created_ts),
		"database": query.database.name,
		"created_by": query.created_by.user.username,
		"query_string": query.querystring[:50],
	} for query in Query.objects.all()]

	return JsonResponse({"queries": queries})

@login_required
def query_id(request, num):
	query = Query.objects.get(id=num)
	database = query.database

	conn = get_connection(database)

	cur = conn.cursor()

	cur.execute(query.querystring)

	context = {
		"headers": [desc[0] for desc in cur.description],
		"data": cur.fetchall(),
		"query_id": query.id,
	}
	return render(request, 'frontend/query.html', context)

@login_required
def prepare_query(request):
	databases = Database.objects.all()
	databases_json = [{
		"name": database.name,
		"id": database.id
	} for database in databases ]

	context = {
		"databases": databases_json
	}
	return render(request, 'frontend/prepare.html', context)

@login_required
def make_query(request):
	try:
		query = request.POST.get('query')
		database = request.POST.get('database')

		query = Query(database=Database.objects.get(id=database), querystring=query, created_by=request.user.profile)
		query.save()
	except Exception as e:
		return JsonResponse({
			"success": False,
			"message": str(e),
		})

	return JsonResponse({
		"success": True,
		"message": "Created query for {}".format(query.database.name),
	})


@login_required
def graph_view_json(request):
	query_id = request.GET.get('id')
	queries = [{
		"parameters": graph.x + ", " + graph.y,
		"database": graph.query.database.name,
		"created_by": graph.created_by.user.username,
		"id": graph.id,
	} for graph in Graph.objects.filter(query_id=query_id)]

	return JsonResponse({"graphs": queries})

def graph_id(request, num):
	graph = Graph.objects.get(id=num)
	query = graph.query
	database = query.database

	conn = get_connection(database)

	cur = conn.cursor()

	cur.execute(query.querystring)
	headers = [desc[0] for desc in cur.description]
	data = cur.fetchall()
	dictified_data = []
	for datum in data:
		dictified_datum = {}
		for index in range(0, len(headers)):
			if headers[index] == graph.x:
				dictified_datum['x'] = datum[index]
			if headers[index] == graph.y:
				dictified_datum['y'] = datum[index]
		dictified_data.append(dictified_datum)

	context = {
		"data": dictified_data,
		"x": graph.x,
		"y": graph.y,
	}

	return render(request, 'frontend/graph.html', context)

@login_required
def make_graph(request):
	try:
		x_param = request.POST.get('x')
		y_param = request.POST.get('y')
		query = Query.objects.get(id=request.POST.get('query'))

		graph = Graph(x=x_param, y=y_param, query=query, created_by=request.user.profile)
		graph.save()

	except Exception as e:
		return JsonResponse({
			"success": False,
			"message": str(e),
		})

	return JsonResponse({
		"success": True,
		"message": "Created graph for query {}".format(query.id),
	})
