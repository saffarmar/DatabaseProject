from flask import jsonify
from dao.statustypes.purchasedDAO import PurchasedDao


class PurchasedHandler:


    def build_resource_dict(self, row):
        result = {}
        result['pid'] = row[0]
        result['rid'] = row[2]
        result['uid'] = row[1]
        result['buyer'] = row[3]
        return result


    def build_resource_attributes(self, pid, rid, uid, buyer):
        result = {}
        result['pid'] = pid
        result['rid'] = rid
        result['uid'] = uid
        result['buyer'] = buyer
        return result

    def getAllPurchased(self):
        dao = PurchasedDao()
        resource_list = dao.getAllPurchased()
        result_list = []
        for row in resource_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getPurchasedById(self, rid):
        dao = PurchasedDao()
        row = dao.getPurchasedById(rid)
        if not row:
            return jsonify(Error="Part Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)

    def insertResource(self, uid, rid, buyer):
        dao = PurchasedDao()
        pid = dao.addPurchased(uid, rid, buyer)
        result = self.build_resource_attributes(pid, rid, uid, buyer)
        return jsonify(Part=result), 201

    def insertResource(self, uid, rid, buyer, form):
        print("form: ", form)
        if len(form) != 1:
            return jsonify(Error="Malformed post request"), 400
        else:
            buyer = form['buyer']
            if buyer:
                dao = PurchasedDao()
                pid = dao.addPurchased(uid, rid, buyer)
                result = self.build_resource_attributes(pid, rid, uid, buyer)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400