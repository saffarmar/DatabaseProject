from flask import jsonify
from dao.usertypes.requesterDAO import RequesterDAO


class RequesterHandler:

    def build_requester_dict(self, row):
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
        result['restime'] = row[5]
        return result

    def getAllRequesters(self):

        dao = RequesterDAO()
        suppliers_list = dao.getAllRequesters()
        result_list = []
        for row in suppliers_list:
            result = self.build_requester_dict(row)
            result_list.append(result)
        return jsonify(Suppliers=result_list)

    def getRequesterById(self, uid):

        dao = RequesterDAO()

        row = dao.getRequesterById(uid)
        if not row:
            return jsonify(Error="Supplier Not Found"), 404
        else:
            part = self.build_requester_dict(row)
        return jsonify(Supplier=part)

    def getResourcesByRequesterId(self, sid):
        dao = RequesterDAO()
        if not dao.getRequesterById(sid):
            return jsonify(Error="Supplier Not Found"), 404
        parts_list = dao.getResourcesByRequesterId(sid)
        result_list = []
        for row in parts_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(PartsSupply=result_list)

    def searchRequesters(self, args):
        if len(args) > 1:
            return jsonify(Error="Malformed search string."), 400
        else:
            username = args.get("name")
            if username:
                dao = RequesterDAO()
                supplier_list = dao.getRequesterByUsername(username)
                result_list = []
                for row in supplier_list:
                    result = self.build_requester_dict(row)
                    result_list.append(row)
                return jsonify(Admins=result_list)
            else:
                return jsonify(Error="Malformed search string."), 400

    def insertRequester(self, form):
        if form and len(form) == 3:
            name = form['name']
            email = form['email']
            username = form['username']
            if name and email and username:
                dao = RequesterDAO()
                uid = dao.insert(name, email, username)
                result = {}
                result["uid"] = uid
                result["name"] = name
                result["email"] = email
                result["username"] = username
                return jsonify(Supplier=result), 201
            else:
                return jsonify(Error="Malformed post request")
        else:
            return jsonify(Error="Malformed post request")