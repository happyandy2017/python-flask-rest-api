
def valid_book_object(book_object):
    if ('name' in book_object 
            and 'price' in book_object 
                and 'isbn' in book_object):
        return True
    else:
        return False

valid_object = {
	"name": "Frankenstein",
	"price": 7.99,
	"isbn": 12321321312
}

missing_name = {
	"price": 7.99,
	"isbn": 12321321312
}

missing_price = {
	"name": "Frankenstein",
	"isbn": 12321321312
}

missing_isbn = {
	"name": "Frankenstein",
	"price": 7.99,
}

empty_dictionary = {}