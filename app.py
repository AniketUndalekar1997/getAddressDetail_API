import os
import requests
from logging import exception
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring, ElementTree

from flask import Flask
from flask import request
from flask import jsonify
from flask import Response

from helper import createXMLResObj, createXmlResponse

API_KEY = os.environ.get('API_KEY')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'This is my test API call!'


@app.route('/getAddressDetails', methods=['GET', 'POST'])
def getLocation():
    request_data = request.get_json()
    addr = request_data["address"]
    address = re.sub(r"^\W+", "", addr).strip()
    output_format = request_data["output_format"].lower()
    base_url = "https://maps.googleapis.com/maps/api/geocode/{}?".format(
        output_format)
    params = {
        'key': API_KEY,
        'address': address
    }
    ret_res = {}
    ret_res["coordinates"] = {}
    if output_format == "xml":
        try:
            response = requests.get(base_url, params=params)
            tree = ElementTree(fromstring(response.content))
            xmlDataObj = createXMLResObj(tree)
            xmlResponse = createXmlResponse(xmlDataObj)
            return Response(ET.tostring(xmlResponse), mimetype='application/xml')
        except exception as e:
            return e
    else:
        try:
            response = requests.get(base_url, params=params).json()
            if response["status"] == "OK":
                geometry = response['results'][0]['geometry']
                formatted_address = response['results'][0]['formatted_address']
                lat = geometry['location']['lat']
                lng = geometry['location']['lng']

            ret_res['coordinates']['lat'] = lat
            ret_res['coordinates']['lng'] = lng
            ret_res["address"] = formatted_address
            res = jsonify(ret_res)
            return res
        except exception as e:
            return e


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True)
