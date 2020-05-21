from flask import jsonify
from dao.hEquipmentDAO import HeavyEquipmentDao


class HeavyEquipmentHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['erequirement'] = row[1]
        result['etype'] = row[2]
        result['weight'] = row[3]
        result['age'] = row[4]
        result['brand'] = row[5]
        return result


    def build_resource_attributes(self, rid, erequirement, brand, etype, weight, age):
        result = {}
        result['rid'] = rid
        result['erequirement'] = erequirement
        result['etype'] = etype
        result['weight'] = weight
        result['age'] = age
        result['brand'] = brand
        return result


    def getAllResources(self):
        dao = HeavyEquipmentDao()
        parts_list = dao.getAllHeavyEquipment()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = HeavyEquipmentDao()
        row = dao.getHeavyEquipmentById(rid)
        if not row:
            return jsonify(Error="Heavy Equipment Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)



    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            erequirement = form['erequirement']
            brand = form['brand']
            etype = form['etype']
            weight = form['weight']
            age = form['age']
            if erequirement and brand and etype and weight and age:
                dao = HeavyEquipmentDao()
                rid = dao.addHeavyEquipment(erequirement, etype, weight, age, brand)
                result = self.build_resource_attributes(rid, erequirement, etype, weight, age, brand)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteResource(self, rid):
        dao = HeavyEquipmentDao()
        if not dao.getHeavyEquipmentById(rid):
            return jsonify(Error="Heavy Equipment not found."), 404
        else:
            dao.deleteHeavyEquipment(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = HeavyEquipmentDao()
        if not dao.getHeavyEquipmentById(rid):
            return jsonify(Error="Part not found."), 404
        else:
            if len(form) != 5:
                return jsonify(Error="Malformed update request"), 400
            else:
                erequirement = form['erequirement']
                brand = form['brand']
                etype = form['etype']
                weight = form['weight']
                age = form['age']
                if erequirement and brand and etype and weight and age:
                    dao.editHeavyEquipment(erequirement, etype, weight, age, brand)
                    result = self.build_resource_attributes(rid, erequirement, etype, weight, age, brand)
                    return jsonify(Part=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




