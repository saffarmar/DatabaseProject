from flask import jsonify
from dao.rtypes.mDeviceDAO import MedicalDeviceDao
from dao.statustypes.requestedDAO import RequestedDao
from dao.statustypes.availableDAO import AvailableDao
from dao.statustypes.resourceDAO import ResourceDao


class MedicalDeviceHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['erequirement'] = row[1]
        result['weight'] = row[2]
        return result


    def build_resource_attributes(self, rid, erequirement, weight):
        result = {}
        result['rid'] = rid
        result['erequirement'] = erequirement
        result['weight'] = weight
        return result



    def getAllResources(self):
        dao = MedicalDeviceDao()
        parts_list = dao.getAllMedicalDevices()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = MedicalDeviceDao()
        row = dao.getMedicalDeviceById(rid)
        if not row:
            return jsonify(Error="Medical Device Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)



    def insertAvailableResource(self, form):
        print("form: ", form)
        if len(form) != 7:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = form['uid']
            kind = form['kind']
            amount = form['amount']
            price = form['price']
            restime = form['restime']
            erequirement = form['erequirement']
            weight = form['weight']
            if erequirement and weight and uid and kind and amount and price and restime:
                daor = ResourceDao()
                daoa = AvailableDao()
                rid = daor.addResource(uid, kind)
                daoa.addAvailable(rid, uid, amount, price, restime)
                dao = MedicalDeviceDao()
                dao.addMedicalDevice(rid, erequirement,weight)
                result = self.build_resource_attributes(rid,erequirement,weight)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertRequestedResource(self, form):
        print("form: ", form)
        if len(form) != 6:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = form['uid']
            kind = form['kind']
            amount = form['amount']
            restime = form['restime']
            erequirement = form['erequirement']
            weight = form['weight']
            if erequirement and weight and uid and kind and amount and restime:
                daor = ResourceDao()
                daoa = RequestedDao()
                rid = daor.addResource(uid, kind)
                daoa.addRequested(rid, uid, amount, restime)
                dao = MedicalDeviceDao()
                dao.addMedicalDevice(rid, erequirement,weight)
                result = self.build_resource_attributes(rid,erequirement,weight)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteResource(self, rid):
        dao = MedicalDeviceDao()
        if not dao.getMedicalDeviceById(rid):
            return jsonify(Error="Medical Device not found."), 404
        else:
            dao.deleteMedicalDevice(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = MedicalDeviceDao()
        if not dao.getMedicalDeviceById(rid):
            return jsonify(Error="Medical Device not found."), 404
        else:
            if len(form) != 2:
                return jsonify(Error="Malformed update request"), 400
            else:
                erequirement = form['erequirement']
                weight = form['weight']
                if erequirement and weight:
                    dao = MedicalDeviceDao()
                    dao.editMedicalDevice(erequirement,weight)
                    result = self.build_resource_attributes(rid,erequirement,weight)
                    return jsonify(Part=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




