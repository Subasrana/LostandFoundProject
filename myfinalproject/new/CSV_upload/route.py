#Import packages
from numpy import genfromtxt
from flask import Blueprint,   jsonify
from new import Items, db,product_schema,app

#Create a blueprint
csv = Blueprint("csv",__name__)

#Load data from the file
def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

#Create a route for uploading bulk records from CSV in database
@csv.route('/products/csv', methods=['GET'])
def get_products():

        try:
            file_name = "myfile.csv"  # sample CSV file used
            data = Load_Data(file_name)

            #Stores the specified index in the specified entities in database
            for i in data:

                Items.name = i[0]
                Items.location = i[1]
                Items.description = i[2]
                Items.picture = i[3]
                Items.date = i[4]

                new_products = Items(Items.name, Items.location, Items.description, Items.picture,
                                     Items.date)
                db.session.add(new_products)  # Add all the records
                db.session.commit()  # Attempt to commit all the records
                return product_schema.jsonify(new_products)
        except:
            db.session.rollback()
        finally:
            db.session.close()  # Close the connection
            
# Run Server
if __name__ == '__main__':
    app.run(debug=True)