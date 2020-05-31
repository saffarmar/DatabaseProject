from flask import jsonify
from dao.statustypes.reservedDAO import ReservedDao


class ReservedHandler:


    def build_resource_dict(self, row):
        result = {}
        result['pid'] = row[0]
        result['rid'] = row[1]
        result['uid'] = row[2]
        result['buyer'] = row[3]
        return result


    def build_resource_attributes(self, pid, rid, uid, buyer):
        result = {}
        result['pid'] = pid
        result['rid'] = rid
        result['uid'] = uid
        result['buyer'] = buyer
        return result

    def getAllReserved(self):
        dao = ReservedDao()
        resource_list = dao.getAllReserved()
        result_list = []
        for row in resource_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getReservedById(self, rid):
        dao = ReservedDao()
        row = dao.getReservedById(rid)
        if not row:
            return jsonify(Error="Part Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)


    def insertResource(self, uid, rid, buyer, form):
        print("form: ", form)
        if len(form) != 1:
            return jsonify(Error="Malformed post request"), 400
        else:
            buyer = form['buyer']
            if buyer:
                dao = ReservedDao()
                pid = dao.addReserved(uid, rid, buyer)
                result = self.build_resource_attributes(pid, rid, uid, buyer)
                return jsonify(Part=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400