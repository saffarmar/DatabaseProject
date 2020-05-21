from flask import jsonify
from dao.fuelDAO import FuelDao


class FuelHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['octane'] = row[1]
        return result


    def build_resource_attributes(self, rid, octane):
        result = {}
        result['rid'] = rid
        result['octane'] = octane
        return result



    def getAllResources(self):
        dao = FuelDao()
        parts_list = dao.getAllFuel()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = FuelDao()
        row = dao.getFuelById(rid)
        if not row:
            return jsonify(Error="Fuel Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)



    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 1:
            return jsonify(Error="Malformed post request"), 400
        else:
            octane = form['octane']
            if octane:
                dao = FuelDao()
                rid = dao.addFuel(octane)
                result = self.build_resource_attributes(rid,octane)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteResource(self, rid):
        dao = FuelDao()
        if not dao.getFuelById(rid):
            return jsonify(Error="Fuel not found."), 404
        else:
            dao.deleteFuel(id)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = FuelDao()
        if not dao.getFuelById(rid):
            return jsonify(Error="Fuel not found."), 404
        else:
            if len(form) != 1:
                return jsonify(Error="Malformed update request"), 400
            else:
                octane = form['octane']
                if octane:
                    dao = FuelDao()
                    dao.editFuel(octane)
                    result = self.build_resource_attributes(rid,octane)
                    return jsonify(Part=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




