from flask import jsonify
from dao.rtypes.toolDAO import ToolDao
from dao.statustypes.requestedDAO import RequestedDao
from dao.statustypes.availableDAO import AvailableDao
from dao.statustypes.resourceDAO import ResourceDao


class ToolHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['erequirement'] = row[1]
        result['weight'] = row[2]
        result['material'] = row[3]
        return result


    def build_resource_attributes(self, rid, erequirement, weight, material):
        result = {}
        result['rid'] = rid
        result['erequirement'] = erequirement
        result['weight'] = weight
        result['material'] = material
        return result



    def getAllResources(self):
        dao = ToolDao()
        parts_list = dao.getAllTools()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = ToolDao()
        row = dao.getToolById(rid)
        if not row:
            return jsonify(Error="Tool Not Found"), 404
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
            amount = form['amount']
            price = form['price']
            restime = form['restime']
            erequirement = form['erequirement']
            weight = form['weight']
            material = form['material']
            if weight and material and erequirement and uid and kind and amount and price and restime:
                daor = ResourceDao()
                daoa = AvailableDao()
                rid = daor.addResource(uid, kind)
                daoa.addAvailable(rid, uid, amount, price, restime)
                dao = ToolDao()
                dao.addTool(rid, erequirement,weight,material)
                result = self.build_resource_attributes(rid,erequirement,weight,material)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertRequestedResource(self, form):
        print("form: ", form)
        if len(form) != 7:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = form['uid']
            kind = form['kind']
            amount = form['amount']
            restime = form['restime']
            erequirement = form['erequirement']
            weight = form['weight']
            material = form['material']
            if weight and material and erequirement and uid and kind and amount and restime:
                daor = ResourceDao()
                daoa = RequestedDao()
                rid = daor.addResource(uid, kind)
                daoa.addRequested(rid, uid, amount, restime)
                dao = ToolDao()
                dao.addTool(rid, erequirement,weight,material)
                result = self.build_resource_attributes(rid,erequirement,weight,material)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400



    def deleteResource(self, rid):
        dao = ToolDao()
        if not dao.getToolById(rid):
            return jsonify(Error="Tool not found."), 404
        else:
            dao.deleteTool(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = ToolDao()
        if not dao.getToolById(rid):
            return jsonify(Error="Tool not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request"), 400
            else:
                erequirement = form['erequirement']
                weight = form['weight']
                material = form['material']
                if erequirement and weight and material:
                    dao = ToolDao()
                    dao.editTool(erequirement,weight,material,rid)
                    result = self.build_resource_attributes(rid,erequirement,weight,material)
                    return jsonify(Part=result), 201
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




