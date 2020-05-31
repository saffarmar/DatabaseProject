from flask import jsonify
from dao.statustypes.availableDAO import AvailableDao


class AvailableHandler:

    def build_supplier_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['name'] = row[1]
        result['email'] = row[2]
        result['username'] = row[3]
        return result


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['type'] = row[1]
        result['amount'] = row[2]
        result['price'] = row[4]
        result['restime'] = row[5]
        return result


    def build_resource_attributes(self, rid, type, amount, price, restime):
        result = {}
        result['rid'] = rid
        result['type'] = type
        result['amount'] = amount
        result['price'] = price
        result['restime'] = restime
        return result


    def getAllResources(self):
        dao = AvailableDao()
        parts_list = dao.getAllAvailable()
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = AvailableDao()
        row = dao.getAvailableById(rid)
        if not row:
            return jsonify(Error="Part Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)


    def searchResources(self, args):
        if len(args) > 1:
            return jsonify(Error="Malformed search string."), 400
        else:
            type = args.get("type")
            if type:
                dao = AvailableDao()
                admin_list = dao.getAvailableByResourceType(type)
                result_list = []
                for row in admin_list:
                    result = self.build_resource_dict(row)
                    result_list.append(row)
                return jsonify(Admins=result_list)
            else:
                return jsonify(Error="Malformed search string."), 400


    def getSupplierByResourceId(self, pid):
        dao = AvailableDao()
        if not dao.getAvailableById(pid):
            return jsonify(Error="Part Not Found"), 404
        suppliers_list = dao.getSupplierByPartId(pid)
        result_list = []
        for row in suppliers_list:
            result = self.build_supplier_dict(row)
            result_list.append(result)
        return jsonify(Suppliers=result_list)


    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            rid = form['rid']
            type = form['type']
            amount = form['amount']
            price = form['price']
            restime = form['restime']
            if type and amount and restime and price:
                dao = AvailableDao()
                rid = dao.addAvailable(rid, type, amount, price, restime)
                result = self.build_resource_attributes(rid, type, amount, price, restime)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400



    def deleteResource(self, rid):
        dao = AvailableDao()
        if not dao.getAvailableById(rid):
            return jsonify(Error="Part not found."), 404
        else:
            dao.deleteAvailable(rid)
            return jsonify(DeleteStatus="OK"), 200


    def updateResource(self, rid, form):
        dao = AvailableDao()
        if not dao.getAvailableById(rid):
            return jsonify(Error="Part not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                type = form['type']
                amount = form['amount']
                price = form['price']
                restime = form['restime']
                if type and amount and restime and price:
                    dao.editAvailable(rid, type, amount, price, restime)
                    result = self.build_resource_attributes(rid, type, amount, price, restime)
                    return jsonify(Part=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400




