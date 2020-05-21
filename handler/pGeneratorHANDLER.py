from flask import jsonify
from dao.pGeneratorDAO import PowerGeneratorDao


class PowerGeneratorHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['eout'] = row[1]
        result['weight'] = row[2]
        result['age'] = row[3]
        return result


    def build_resource_attributes(self, rid, eout, weight, age):
        result = {}
        result['rid'] = rid
        result['eout'] = eout
        result['weight'] = weight
        result['age'] = age
        return result



    def getAllResources(self):
        dao = PowerGeneratorDao()
        parts_list = dao.getAllTools()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = PowerGeneratorDao()
        row = dao.getPowerGeneratorById(rid)
        if not row:
            return jsonify(Error="Power Generator Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)



    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error="Malformed post request"), 400
        else:
            eout = form['eout']
            weight = form['weight']
            age = form['age']
            if weight and eout and age:
                dao = PowerGeneratorDao()
                rid = dao.addPowerGenerator(eOut=eout, age=age, weight=weight)
                result = self.build_resource_attributes(rid,eout,weight,age)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def deleteResource(self, rid):
        dao = PowerGeneratorDao()
        if not dao.getPowerGeneratorById(rid):
            return jsonify(Error="Power Generator not found."), 404
        else:
            dao.deletePowerGenerator(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = PowerGeneratorDao()
        if not dao.getPowerGeneratorById(rid):
            return jsonify(Error="Power Generator not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request"), 400
            else:
                eout = form['eout']
                weight = form['weight']
                age = form['age']
                if weight and eout and age:
                    dao = PowerGeneratorDao()
                    dao.editPowerGenerator(eOut=eout,age=age,weight=weight,rid=rid)
                    result = self.build_resource_attributes(rid,eout,weight,age)
                    return jsonify(Part=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




