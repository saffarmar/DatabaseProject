from flask import jsonify
from dao.batteryDAO import BatteryDao


class BatteryHandler:


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
        result['exdate'] = exdate
        result['size'] = size
        return result



    def getAllResources(self):
        dao = BatteryDao()
        parts_list = dao.getAllBatteries()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = BatteryDao()
        row = dao.getBatteryById(rid)
        if not row:
            return jsonify(Error="Battery Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)



    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error="Malformed post request"), 400
        else:
            brand = form['brand']
            exdate = form['exdate']
            size = form['size']
            if brand and exdate and size:
                dao = BatteryDao()
                rid = dao.addBattery(brand,exdate,size)
                result = self.build_resource_attributes(rid,brand,exdate,size)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteResource(self, rid):
        dao = BatteryDao()
        if not dao.getBatteryById(rid):
            return jsonify(Error="Battery not found."), 404
        else:
            dao.deleteBattery(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = BatteryDao()
        if not dao.getBatteryById(rid):
            return jsonify(Error="Battery not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                exdate = form['exdate']
                size = form['size']
                if brand and exdate and size:
                    dao = BatteryDao()
                    dao.editBattery(brand,exdate,size)
                    result = self.build_resource_attributes(rid,brand,exdate,size)
                    return jsonify(Part=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




