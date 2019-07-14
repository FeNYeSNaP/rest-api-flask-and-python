from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)  # store = StoreModel(name, data['store_id'])
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted"}, 200

    def put(self, name):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_name(name)
        if store is None:
            store = StoreModel(name, **data)  # item = ItemModel(name, data['xxx'], data['yyy'])
        else:
            pass
        store.save_to_db()

        return store.json()


class StoreList(Resource):
    def get(self):
        # return {'item': list(map(lambda x: x.json(), StoreModel.query.all()))}
        return {'stores': [x.json() for x in StoreModel.query.all()]}
