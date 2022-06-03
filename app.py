#!/usr/bin/env python3
import os
from flask import Flask, jsonify, request, redirect, render_template, url_for
from flask import send_file

# local import
from pu9sf import Pu9sf

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = 'pu9_data'


@app.route('/wip', methods=['get'])
def wip_rack():
    racks = Pu9sf().wip()
    return jsonify(racks)

@app.route('/racklink/<racksn>')
def racklink(racksn):
    racklink = Pu9sf().racklink(racksn)
    return jsonify(racklink)

if __name__ == '__main__':
    app.run(port=5000)
