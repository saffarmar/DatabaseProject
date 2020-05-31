from flask import jsonify
from dao.statustypes.resourceDAO import ResourceDao


class ResourceHandler:


    def build_resource_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['uid'] = row[1]
        result['kind'] = row[2]
        return result


    def build_resource_attributes(self, rid, uid, kind):
        result = {}
        result['rid'] = rid
        result['uid'] = uid
        result['kind'] = kind
        return result

    def getAllResources(self):
        dao = ResourceDao()
        resource_list = dao.getAllResource()
        result_list = []
        for row in resource_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)


    def getResourceById(self, rid):
        dao = ResourceDao()
        row = dao.getResourceById(rid)
        if not row:
            return jsonify(Error="Part Not Found"), 404
        else:
            part = self.build_resource_dict(row)
            return jsonify(Part=part)

    def getResourceType(self, rid):
        dao = ResourceDao()
        type = dao.getResourceType(rid)
        return type

    def searchResources(self, args):
        if len(args) > 1:
            return jsonify(Error="Malformed search string."), 400
        else:
            type = args.get("type")
            if type:
                dao = ResourceDao()
                admin_list = dao.getResourceByResourceType(type)
                result_list = []
                for row in admin_list:
                    result = self.build_resource_dict(row)
                    result_list.append(row)
                return jsonify(Admins=result_list)
            else:
                return jsonify(Error="Malformed search string."), 400