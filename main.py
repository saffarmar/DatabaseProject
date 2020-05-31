from flask import Flask, jsonify, request
from handler.statustypes.availableHANDLER import AvailableHandler
from handler.usertypes.supplierHANDLER import SupplierHandler
from handler.usertypes.requesterHANDLER import RequesterHandler
from handler.usertypes.adminHANDLER import AdminHandler
from handler.statustypes.requestedHANDLER import RequestedHandler
from handler.statustypes.resourceHANDLER import ResourceHandler
from handler.statustypes.purchasedHANDLER import PurchasedHandler
from handler.statustypes.reservedHANDLER import ReservedHandler
from handler.rtypes.batteryHANDLER import BatteryHandler
from handler.rtypes.clothingHANDLER import ClothingHandler
from handler.rtypes.foodHANDLER import FoodHandler
from handler.rtypes.fuelHANDLER import FuelHandler
from handler.rtypes.hEquipmentHANDLER import HeavyEquipmentHandler
from handler.rtypes.mDeviceHANDLER import MedicalDeviceHandler
from handler.rtypes.medicationHANDLER import MedicationHandler
from handler.rtypes.pGeneratorHANDLER import PowerGeneratorHandler
from handler.rtypes.toolHANDLER import ToolHandler
from handler.rtypes.waterHANDLER import WaterHandler


#from flask_cors import CORS, cross_origin

# Activate
app = Flask(__name__)

#CORS(app)


@app.route('/')
def greeting():
    return 'Welcome to Resource Manager'


#Get All Available Resources

@app.route('/ResourceManager/available', methods=['GET'])
def getAllAvailable():
    if not request.args:
        return AvailableHandler().getAllResources()
    else:
        return AvailableHandler().searchResources(request.args)


#Get All Requested Resources

@app.route('/ResourceManager/requested', methods=['GET'])
def getAllRequested():
    if not request.args:
        return RequestedHandler().getAllResources()
    else:
        return RequestedHandler().searchResources(request.args)


#Add available resource

@app.route('/ResourceManager/available/<string:type>', methods=['GET', 'POST'])
def addAvailable(type):
    if request.method == 'POST':
        if type == 'battery':
            return BatteryHandler().insertAvailableResource(request.form)
        elif type == 'clothing':
            return ClothingHandler().insertAvailableResource(request.form)
        elif type == 'food':
            return FoodHandler().insertAvailableResource(request.form)
        elif type == 'fuel':
            return FoodHandler().insertAvailableResource(request.form)
        elif type == 'heavy equipment':
            return HeavyEquipmentHandler().insertAvailableResource(request.form)
        elif type == 'medical device':
            return MedicalDeviceHandler().insertAvailableResource(request.form)
        elif type == 'medication':
            return MedicationHandler().insertAvailableResource(request.form)
        elif type == 'generator':
            return PowerGeneratorHandler().insertAvailableResource(request.form)
        elif type == 'tool':
            return ToolHandler().insertAvailableResource(request.form)
        elif type == 'water':
            return WaterHandler().insertAvailableResource(request.form)
    else:
        if not request.args:
            return AvailableHandler().getAllResources()
        else:
            return AvailableHandler().searchResources(request.args)

#Add Requested Resource

@app.route('/ResourceManager/requested/<string:type>', methods=['GET', 'POST'])
def addRequested(type):
    if request.method == 'POST':
        if type == 'battery':
            return BatteryHandler().insertRequestedResource(request.form)
        elif type == 'clothing':
            return ClothingHandler().insertRequestedResource(request.form)
        elif type == 'food':
            return FoodHandler().insertRequestedResource(request.form)
        elif type == 'fuel':
            return FoodHandler().insertRequestedResource(request.form)
        elif type == 'heavy equipment':
            return HeavyEquipmentHandler().insertRequestedResource(request.form)
        elif type == 'medical device':
            return MedicalDeviceHandler().insertRequestedResource(request.form)
        elif type=='medication':
            return MedicationHandler().insertRequestedResource(request.form)
        elif type=='generator':
            return PowerGeneratorHandler().insertRequestedResource(request.form)
        elif type=='tool':
            return ToolHandler().insertRequestedResource(request.form)
        elif type=='water':
            return WaterHandler().insertRequestedResource(request.form)
    else:
        if not request.args:
            return RequestedHandler().getAllResources()
        else:
            return RequestedHandler().searchResources(request.args)


#Get Available Resource by ID

@app.route('/ResourceManager/available/<int:rid>', methods=['GET'])
def getAvailableById(rid):
    if request.method == 'GET':
        return AvailableHandler().getResourceById(rid)
    else:
        return jsonify(Error="Method not allowed."), 405


#Get Requested Resource by ID

@app.route('/ResourceManager/requested/<int:rid>', methods=['GET'])
def getRequestedById(rid):
    if request.method == 'GET':
        return RequestedHandler().getResourceById(rid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/ResourceManager/available/<int:rid>/suppliers')
def getSuppliersByResourceId(rid):
    return AvailableHandler().getSupplierByResourceId(rid)

@app.route('/ResourceManager/requested/<int:rid>/requesters')
def getSuppliersByResourceId(rid):
    return RequestedHandler().getSupplierByResourceId(rid)

#Get Resource details

@app.route('/ResourceManager/resources/<int:rid>', methods=['GET'])
def getResourceDetails(rid):
    type = ResourceHandler().getResourceType(rid)
    if type == 'battery':
        return BatteryHandler().getResourceById(rid)
    elif type == 'clothing':
        return ClothingHandler().getResourceById(rid)
    elif type == 'food':
        return FoodHandler().getResourceById(rid)
    elif type == 'fuel':
        return FoodHandler().getResourceById(rid)
    elif type == 'heavy equipment':
        return HeavyEquipmentHandler().getResourceById(rid)
    elif type == 'medical device':
        return MedicalDeviceHandler().getResourceById(rid)
    elif type == 'medication':
        return MedicationHandler().getResourceById(rid)
    elif type == 'generator':
        return PowerGeneratorHandler().getResourceById(rid)
    elif type == 'tool':
        return ToolHandler().getResourceById(rid)
    elif type == 'water':
        return WaterHandler().getResourceById(rid)


#Get All Purchased

@app.route('/ResourceManager/purchased', methods=['GET'])
def getAllPurchased():
        return PurchasedHandler().getAllPurchased()

#Get All Reserved

@app.route('/ResourceManager/reserved', methods=['GET'])
def getAllReserved():
        return ReservedHandler().getAllReserved()

#Get Purchased by Id

@app.route('/ResourceManager/purchased/<int:rid>', methods=['GET'])
def getPurchasedById(rid):
    if request.method == 'GET':
        return PurchasedHandler().getPurchasedById(rid)
    else:
        return jsonify(Error="Method not allowed."), 405

#Get Reserved by ID

@app.route('/ResourceManager/reserved/<int:rid>', methods=['GET'])
def getReservedById(rid):
    if request.method == 'GET':
        return ReservedHandler().getReservedById(rid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/ResourceManager/purchase/<int:rid>', methods=['POST'])
def purchase(rid):
    if request.method == 'POST':
        type = ResourceHandler().getResourceType(rid)
        uploader = AvailableHandler().getSupplierByResourceId(rid)
        AvailableHandler().deleteResource(rid)
        return PurchasedHandler().insertResource(uploader, rid, request.form)

@app.route('/ResourceManager/purchase/<int:rid>', methods=['POST'])
def reserve(rid):
    if request.method == 'POST':
        type = ResourceHandler().getResourceType(rid)
        uploader = AvailableHandler().getSupplierByResourceId(rid)
        AvailableHandler().deleteResource(rid)
        return ReservedHandler().insertResource(uploader, rid, request.form)


#Get and post suppliers

@app.route('/ResourceManager/suppliers', methods=['GET', 'POST'])
def getAllSuppliers():
    if request.method == 'POST':
        return SupplierHandler().insertSupplier(request.form)
    else:
        if not request.args:
            return SupplierHandler().getAllSuppliers()
        else:
            return SupplierHandler().searchSuppliers(request.args)


#Get and post requesters

@app.route('/ResourceManager/requesters', methods=['GET', 'POST'])
def getAllRequesters():
    if request.method == 'POST':
        return RequesterHandler().insertRequester(request.form)
    else:
        if not request.args:
            return RequesterHandler().getAllRequesters()
        else:
            return RequesterHandler().searchRequesters(request.args)


#Get and post admins

@app.route('/ResourceManager/admins', methods=['GET', 'POST'])
def getAllAdmins():
    if request.method == 'POST':
        return AdminHandler().insertAdmin(request.form)
    else:
        if not request.args:
            return AdminHandler().getAllAdmins()
        else:
            return AdminHandler().searchAdmins(request.args)


@app.route('/ResourceManager/suppliers/<int:sid>', methods=['GET'])
def getSupplierById(sid):
    if request.method == 'GET':
        return SupplierHandler().getSupplierById(sid)
    else:
        return jsonify(Error = "Method not allowed"), 405


@app.route('/ResourceManager/requester/<int:sid>', methods=['GET'])
def getRequesterById(sid):
    if request.method == 'GET':
        return RequesterHandler().getRequesterById(sid)
    else:
        return jsonify(Error = "Method not allowed"), 405

@app.route('/ResourceManager/admin/<int:sid>', methods=['GET'])
def getAdminById(sid):
    if request.method == 'GET':
        return AdminHandler().getAdminById(sid)
    else:
        return jsonify(Error = "Method not allowed"), 405

@app.route('/ResourceManager/suppliers/<int:sid>/resource')
def getResourceBySupplierId(sid):
    return SupplierHandler().getResourcesBySupplierId(sid)


if __name__ == '__main__':
    app.run()