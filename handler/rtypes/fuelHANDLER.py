from flask import jsonify
from dao.rtypes.fuelDAO import FuelDao
from dao.statustypes.requestedDAO import RequestedDao
from dao.statustypes.availableDAO import AvailableDao
from dao.statustypes.resourceDAO import ResourceDao


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

    def insertAvailableResource(self, form):
        print("form: ", form)
        if len(form) != 6:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = form['uid']
            kind = form['kind']
            amount = form['amount']
            price = form['price']
            restime = form['restime']
            octane = form['octane']

            if octane and uid and kind and amount and price and restime:
                daor = ResourceDao()
                daoa = AvailableDao()
                rid = daor.addResource(uid, kind)
                daoa.addAvailable(rid, uid, amount, price, restime)
                dao = FuelDao()
                dao.addFuel(rid, octane)
                result = self.build_resource_attributes(rid, octane)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertRequestedResource(self, form):
        print("form: ", form)
        if len(form) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = form['uid']
            kind = form['kind']
            amount = form['amount']
            restime = form['restime']
            octane = form['octane']

            if octane and uid and kind and amount and restime:
                daor = ResourceDao()
                daoa = RequestedDao()
                rid = daor.addResource(uid, kind)
                daoa.addRequested(rid, uid, amount, restime)
                dao = FuelDao()
                dao.addFuel(rid, octane)
                result = self.build_resource_attributes(rid, octane)
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




