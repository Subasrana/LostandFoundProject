#import packages
from flask import Blueprint, request,jsonify
from sqlalchemy import or_
from new import db,products_schema,product_schema,app
from new import Items

#Create blueprint
lostandfound = Blueprint("lostandfound",__name__)

# Route for Inserting an Item
@lostandfound.route('/products')
@lostandfound.route('/products/new', methods=['POST'])
def add_product():
  name = request.json['name']
  location = request.json['location']
  description = request.json['description']
  picture = request.json['picture']
  date = request.json['date']

  new_products = Items(name,location, description, picture, date)
#Add to database
  db.session.add(new_products)
  db.session.commit()

  return product_schema.jsonify(new_products)

#Route for Viewing all items
@lostandfound.route('/products')
@lostandfound.route('/products/page/<int:page>', methods=['GET'])
def get_products(page=1):
 all_products = Items.query.paginate(page,per_page=3)
 result = products_schema.dump(all_products.items)
 return jsonify(result)

#Route for Searching for an item
@lostandfound.route('/product')
@lostandfound.route('/productssss/page/<int:page>', methods=['GET','POST'])
def search_product(page = 1):
   if request.method == 'POST':
    name = request.json['name']
    location = request.json['location']
    #store all the items in results that have specified name and location and display them using pagination
    results = Items.query.filter(or_(Items.name.like(name),Items.location.like(location))).paginate(page,per_page=3)
    final_result = products_schema.dump(results.items)
    return jsonify(final_result)
   else:
       print("unsuccessful")



# Route for Updating an item
@lostandfound.route('/productsss/<id>', methods=['PUT'])
def update_product(id):
 product = Items.query.get(id)

 name = request.json['name']
 location = request.json['location']
 description = request.json['description']
 picture = request.json['picture']
 date = request.json['date']


 product.date = date
 product.description = description
 product.location = location
 product.name = name
 product.picture = picture

 db.session.commit()

 return product_schema.jsonify(product)


# Route for Deleting an item
@lostandfound.route('/productsss/<id>', methods=['DELETE'])
def delete_product(id):
 product = Items.query.get(id)
 db.session.delete(product)
 db.session.commit()

 return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)