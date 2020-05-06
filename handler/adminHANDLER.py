from flask import jsonify
from dao.adminDAO import AdminDao


class AdminHandler:

    def build_admin_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['name'] = row[1]
        result['email'] = row[2]
        result['username'] = row[3]
        return result

    def getAllAdmins(self):
        dao = AdminDao()
        admin_list = dao.getAllAdmin()
        result_list = []
        for row in admin_list:
            result = self.build_admin_dict(row)
            result_list.append(result)
        return jsonify(Admin=result_list)

    def getAdminById(self, uid):

        dao = AdminDao()

        row = dao.getAdminById(uid)
        if not row:
            return jsonify(Error="Supplier Not Found"), 404
        else:
            admin = self.build_admin_dict(row)
        return jsonify(Admin=admin)

    def searchAdmins(self, args):
        if len(args) > 1:
            return jsonify(Error="Malformed search string."), 400
        else:
            username = args.get("username")
            if username:
                dao = AdminDao()
                admin_list = dao.getAdminByUsername(username)
                result_list = []
                for row in admin_list:
                    result = self.build_admin_dict(row)
                    result_list.append(row)
                return jsonify(Admins=result_list)
            else:
                return jsonify(Error="Malformed search string."), 400

    def insertAdmin(self, form):
        if form and len(form) == 3:
            name = form['name']
            email = form['email']
            username = form['username']
            if name and email and username:
                dao = AdminDao()
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
