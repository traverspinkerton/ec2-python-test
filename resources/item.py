from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required=True,
        help="Every item needs a price!"
    )
    parser.add_argument('store_id', 
        type=int,
        required=True,
        help="Every item needs a store id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found.'}, 404
    

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with this name already exists!'}, 500

        data = Item.parser.parse_args()
        item = ItemModel(name, **data) ## data price and data store_id

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name) # if an item wit the given name already exists in the db

        if item is None:
            item = ItemModel(name, **data) # assign item var to an object (new instance) of ItemModel class with name from url and price from req body
        else:
            item.price = data['price']
            
        item.save_to_db() # call save_to_db on our item instance (of ItemModel class)

        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item succesfully deleted'}
        return {'message': 'Item does not exist'}
        


class ItemList(Resource):
    def get(self):


        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # select_query = "SELECT * FROM items"
        # result = cursor.execute(select_query)
        # items = []
        # for row in result:
        #     items.append({'id':row[0], 'name': row[1], 'price': row[2]})

        # connection.close()
        
        return {'items': [item.json() for item in ItemModel.query.all()]}

        # list(map(lambda x: x.json(), ItemModel.query.all()))
