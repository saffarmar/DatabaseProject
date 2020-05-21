from flask import jsonify
from dao.toolDAO import ToolDao


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



    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error="Malformed post request"), 400
        else:
            erequirement = form['erequirement']
            weight = form['weight']
            material = form['material']
            if weight and material and erequirement:
                dao = ToolDao()
                rid = dao.addTool(erequirement,weight,material)
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




