from flask import jsonify
from dao.rtypes.medicationDAO import MedicationDao

from dao.statustypes.requestedDAO import RequestedDao
from dao.statustypes.availableDAO import AvailableDao
from dao.statustypes.resourceDAO import ResourceDao

class MedicationHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['brand'] = row[1]
        result['form'] = row[2]
        result['prescription'] = row[3]
        result['exdate'] = row[4]
        result['size'] = row[5]
        return result


    def build_resource_attributes(self, rid, brand, form, prescription, exdate, size):
        result = {}
        result['rid'] = rid
        result['brand'] = brand
        result['form'] = form
        result['prescription'] = prescription
        result['exdate'] = exdate
        result['size'] = size
        return result


    def getAllResources(self):
        dao = MedicationDao()
        parts_list = dao.getAllMedications()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = MedicationDao()
        row = dao.getMedicationById(rid)
        if not row:
            return jsonify(Error="Part Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)



    def insertAvailableResource(self, form):
        print("form: ", form)
        if len(form) != 10:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = form['uid']
            kind = form['kind']
            amount = form['amount']
            price = form['price']
            restime = form['restime']
            brand = form['brand']
            form = form['form']
            prescription = form['prescription']
            exdate = form['exdate']
            size = form['size']
            if brand and exdate and form and prescription and uid and amount and price and restime:
                daor = ResourceDao()
                daoa = AvailableDao()
                rid = daor.addResource(uid, kind)
                daoa.addAvailable(rid, uid, amount, price, restime)
                dao = MedicationDao()
                dao.addMedication(rid, brand, form, prescription, exdate, size)
                result = self.build_resource_attributes(rid, brand, form, prescription, exdate, size)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400



    def insertRequestedResource(self, form):
        print("form: ", form)
        if len(form) != 9:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = form['uid']
            kind = form['kind']
            amount = form['amount']
            restime = form['restime']
            brand = form['brand']
            form = form['form']
            prescription = form['prescription']
            exdate = form['exdate']
            size = form['size']
            if brand and exdate and form and prescription and uid and amount and restime:
                daor = ResourceDao()
                daoa = RequestedDao()
                rid = daor.addResource(uid, kind)
                daoa.addRequested(rid, uid, amount, restime)
                dao = MedicationDao()
                dao.addMedication(rid, brand, form, prescription, exdate, size)
                result = self.build_resource_attributes(rid, brand, form, prescription, exdate, size)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteResource(self, rid):
        dao = MedicationDao()
        if not dao.getMedicationById(rid):
            return jsonify(Error="Part not found."), 404
        else:
            dao.deleteMedication(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = MedicationDao()
        if not dao.getMedicationById(rid):
            return jsonify(Error="Part not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                brand = form['brand']
                form = form['form']
                prescription = form['prescription']
                exdate = form['exdate']
                size = form['size']
                if brand and exdate and form and prescription:
                    dao.editMedication(rid, brand, form, prescription, exdate, size)
                    result = self.build_resource_attributes(rid, brand, form, prescription, exdate, size)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




