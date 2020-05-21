from flask import jsonify
from dao.clothingDAO import ClothingDao


class ClothingHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['gender'] = row[1]
        result['brand'] = row[2]
        result['size'] = row[3]
        result['material'] = row[4]
        return result


    def build_resource_attributes(self, rid, gender, brand, size, material):
        result = {}
        result['rid'] = rid
        result['gender'] = gender
        result['brand'] = brand
        result['size'] = size
        result['material'] = material
        return result



    def getAllResources(self):
        dao = ClothingDao()
        parts_list = dao.getAllClothing()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = ClothingDao()
        row = dao.getClothingById(rid)
        if not row:
            return jsonify(Error="Clothing Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)



    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            gender = form['gender']
            brand = form['brand']
            size = form['size']
            material = form['material']
            if gender and brand and size and material:
                dao = ClothingDao()
                rid = dao.addClothing(gender, brand, material, size)
                result = self.build_resource_attributes(rid, gender, brand, size, material)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteResource(self, rid):
        dao = ClothingDao()
        if not dao.getClothingById(rid):
            return jsonify(Error="Clothing not found."), 404
        else:
            dao.deleteClothing(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = ClothingDao()
        if not dao.getClothingById(rid):
            return jsonify(Error="Clothing not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                gender = form['gender']
                brand = form['brand']
                size = form['size']
                material = form['material']
                if gender and brand and size and material:
                    dao = ClothingDao()
                    dao.editClothing(gender,brand,material,size,rid)
                    result = self.build_resource_attributes(rid, gender, brand, size, material)
                    return jsonify(Part=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




