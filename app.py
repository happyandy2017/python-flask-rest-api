from flask import Flask, jsonify, request, Response
import json
from BookModel import *
from settings import *
import jwt, datetime
from UserModel import User
from functools import wraps

books = Book.get_all_books()

DEFAULT_PAGE_LIMIT =3
app.config['SECRET_KEY'] = 'meow'


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['name'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if not match:
        return Response('', 401, mimetype='application/json')

    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode(payload={'exp': expiration_date}, key=app.config['SECRET_KEY'], algorithm='HS256')
    return token
# books = [
#     {
#         'name': 'Green Eggs and Ham',
#         'price': 7.99,
#         'isbn': 978039400165
#     },
#     {
#         'name': 'The Cat In The Hat',
#         'price': 6.99,
#         'isbn': 9782371000193
#     },
#     {
#         'name': 'San Guo',
#         'price': 10,
#         'isbn': 14354645765
#     }
# ]

# GET /books/978039400165
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    # return_value = {}
    # for book in books:
    #     if book['isbn'] == isbn:
    #         return_value = {
    #             'name': book['name'],
    #             'price': book['price']
    #         }
    return jsonify(return_value)

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}), 401
        return wrapper


#GET /books?token=fjdksjfklsajfksadj
# GET /books
@app.route('/books')
@token_required
def get_books():
    # token = request.args.get('token')
    # try:
    #     jwt.decode(token, app.config['SECRET_KEY'])
    # except:
    #     return jsonify({'error': 'Need a valid token to view this page'}), 401
    return jsonify({'books': Book.get_all_books()}) 

# POST /books
# {
#     'name': 'F',
#     'price': 6.99,
#     'isbn': 32323
# }

def valid_book_object(book_object):
    if ('name' in book_object 
            and 'price' in book_object 
                and 'isbn' in book_object):
        return True
    else:
        return False


#/books/isbn_number
# POST /books
@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()

    if valid_book_object(request_data):
        # new_book = {
        #     "name": request_data['name'],
        #     "price": request_data['price'],
        #     "isbn": request_data['isbn']
        # }
        # books.insert(0, new_book)
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype="application/json")
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invlid book object passed in request",
            "helpString": "Data passed in similar to this {'name:'bookname', 'price':7.99, 'isbn':32143214}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    
#PATCH /books/9392939293
# {
#     'name': 'Harry Potter'
# }
def valid_put_request_data(request_data):
    if("name" in request_data and "price" in request_data):
        return True
    else:
        return False

#PUT /books/9392939293
# {
#     'name': 'Harry Potter',
#     'price': 0.99
# }
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Invlid book object passed in request",
            "helpString": "Data passed in similar to this {'name:'bookname', 'price':7.99}"
        }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
    return response 
    
    # new_book = {
    #     'name': request_data['name'],
    #     'price': request_data['price'],
    #     'isbn': isbn
    # }

    # num = len(books)
    # for i in range(num):
    #     book = books[i]
    #     if book['isbn'] == isbn:
    #         #update
    #         books[i] = new_book
    #         break

    Book.replace_book(isbn, replace_book['name'], replace_book['price'])

    response = Response("", status=204)
    return response


def valid_patch_request_data(request_data):
    if("name" in request_data or "price" in request_data):
        return True
    else:
        return False

# PATCH /books/89898989
# {
#     'name': 'Harry potter',
# }
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()

    if(not valid_patch_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Invlid book object passed in request",
            "helpString": "Data passed in similar to this {'name:'bookname', 'price':7.99}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response 

    # updated_book = {}
    if 'price' in request_data:
        # updated_book['price'] = request_data['price']
        Book.update_book_price(isbn, request_data['price'])
    if 'name' in request_data:
        # updated_book['name'] = request_data['name']
        Book.update_book_name(isbn, request_data['name'])

            
    # for book in books:
    #     if book['isbn'] == isbn:
    #         #update
    #         book.update(updated_book)
    #         break

    response = Response("", status=204)
    response.headers['Location'] = '/books/'+str(isbn)

    return response

# DELETE /books/978039400165
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    # i = 0
    # for book in books:
    #     if book['isbn'] == isbn:
    #         books.pop(i)
    #         return Response('', status=204)
    #     i += 1
    if Book.delete_book(isbn):
        return Response('', status=204)

    invalidBookObjectErrorMsg = {
        'error': 'Book with the ISBN that was provided was not found, so therefore unable to delete'
    }
    return Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
app.run(port=5000)
