from flask import jsonify
from dao.rtypes.waterDAO import WaterDao
from dao.statustypes.requestedDAO import RequestedDao
from dao.statustypes.availableDAO import AvailableDao
from dao.statustypes.resourceDAO import ResourceDao


class WaterHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['brand'] = row[1]
        result['exdate'] = row[2]
        result['size'] = row[3]
        return result


    def build_resource_attributes(self, rid, brand, exdate, size):
        result = {}
        result['rid'] = rid
        result['brand'] = brand
        result['size'] = size
        result['exdate'] = exdate
        return result



    def getAllResources(self):
        dao = WaterDao()
        parts_list = dao.getAllWater()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = WaterDao()
        row = dao.getWaterById(rid)
        if not row:
            return jsonify(Error="Water Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)



    def insertAvailableResource(self, form):
        print("form: ", form)
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = form['uid']
            kind = form['kind']
            brand = form['brand']
            size = form['size']
            exdate = form['exdate']
            amount = form['amount']
            price = form['price']
            restime = form['restime']

            if brand and size and exdate and uid and kind and amount and price and restime:
                dao = WaterDao()
                daor = ResourceDao()
                daoa = AvailableDao()
                rid = daor.addResource(uid, kind)
                daoa.addAvailable(rid, uid, amount, price, restime)
                dao.addWater(rid, brand, exdate, size)
                result = self.build_resource_attributes(rid,brand,exdate,size)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertRequestedResource(self, form):
        print("form: ", form)
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = form['uid']
            kind = form['kind']
            brand = form['brand']
            size = form['size']
            exdate = form['exdate']
            amount = form['amount']
            restime = form['restime']

            if brand and size and exdate and uid and kind and amount and restime:
                dao = WaterDao()
                daor = ResourceDao()
                daoa = RequestedDao()
                rid = daor.addResource(uid, kind)
                daoa.addRequested(rid, uid, amount, restime)
                dao.addWater(rid, brand, exdate, size)
                result = self.build_resource_attributes(rid,brand,exdate,size)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteResource(self, rid):
        dao = WaterDao()
        if not dao.getWaterById(rid):
            return jsonify(Error="Water not found."), 404
        else:
            dao.deleteWater(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = WaterDao()
        if not dao.getWaterById(rid):
            return jsonify(Error="Water not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                size = form['size']
                exdate = form['exdate']
                if brand and size and exdate:
                    dao = WaterDao()
                    dao.editWater(brand, exdate, size, rid)
                    result = self.build_resource_attributes(rid, brand, exdate, ize)
                    return jsonify(Part=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




