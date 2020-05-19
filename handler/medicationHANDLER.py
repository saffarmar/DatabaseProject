from flask import jsonify
from dao.medicationDAO import MedicationDao


class MedicationHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['kind'] = row[1]
        result['brand'] = row[2]
        result['form'] = row[3]
        result['prescription'] = row[4]
        result['exdate'] = row[5]
        result['size'] = row[6]
        return result


    def build_resource_attributes(self, rid, kind, brand, form, prescription, exdate, size):
        result = {}
        result['rid'] = rid
        result['kind'] = kind
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



    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            kind = form['kind']
            brand = form['brand']
            form = form['form']
            prescription = form['prescription']
            exdate = form['exdate']
            size = form['size']
            if kind and brand and exdate and form and prescription:
                dao = MedicationDao()
                rid = dao.addMedication(kind, brand, form, prescription, exdate, size)
                result = self.build_resource_attributes(rid, kind, brand, form, prescription, exdate, size)
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
                kind = form['kind']
                brand = form['brand']
                form = form['form']
                prescription = form['prescription']
                exdate = form['exdate']
                size = form['size']
                if kind and brand and exdate and form and prescription:
                    dao.editMedication(rid, kind, brand, form, prescription, exdate, size)
                    result = self.build_resource_attributes(rid, kind, brand, form, prescription, exdate, size)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




