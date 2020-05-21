from flask import jsonify
from dao.foodDAO import FoodDao


class FoodHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['brand'] = row[1]
        result['flavor'] = row[2]
        result['exdate'] = row[3]
        result['size'] = row[4]
        return result


    def build_resource_attributes(self, rid, brand, flavor, exdate, size):
        result = {}
        result['rid'] = rid
        result['flavor'] = flavor
        result['brand'] = brand
        result['size'] = size
        result['exdate'] = exdate
        return result



    def getAllResources(self):
        dao = FoodDao()
        parts_list = dao.getAllFood()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = FoodDao()
        row = dao.getFoodById(rid)
        if not row:
            return jsonify(Error="Food Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)



    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            flavor = form['flavor']
            brand = form['brand']
            size = form['size']
            exdate = form['exdate']
            if flavor and brand and size and exdate:
                dao = FoodDao()
                rid = dao.addFood(brand, flavor,exdate,size)
                result = self.build_resource_attributes(rid, brand, flavor, exdate, size)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteResource(self, rid):
        dao = FoodDao()
        if not dao.getFoodById(rid):
            return jsonify(Error="Food not found."), 404
        else:
            dao.deleteFood(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = FoodDao()
        if not dao.getFoodById(rid):
            return jsonify(Error="Food not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                flavor = form['flavor']
                brand = form['brand']
                size = form['size']
                exdate = form['exdate']
                if flavor and brand and size and exdate:
                    dao = FoodDao()
                    dao.editFood(brand,flavor,exdate,size,rid)
                    result = self.build_resource_attributes(rid,brand,flavor,exdate,size)
                    return jsonify(Part=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




