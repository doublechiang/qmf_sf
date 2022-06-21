#!/usr/bin/env python3
import os
from flask import Flask, jsonify, request, redirect, render_template, url_for
from flask import send_file

# local import
from pu9sf import Pu9sf

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = 'pu9sf'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/wip', methods=['get'])
def wip_rack():
    racks = Pu9sf().wip()
    return jsonify(racks)

@app.route('/racklink')
@app.route('/racklink/')
@app.route('/racklink/<racksn>')
def racklink(racksn=None):
    racklink = Pu9sf().racklink(racksn)
    return jsonify(racklink)

@app.route('/monitor')
@app.route('/monitor/')
@app.route('/monitor/<racksn>')
def monitor(racksn=None):
    test_monitor = Pu9sf().monitor(racksn)
    return jsonify(test_monitor)


if __name__ == '__main__':
    app.run(port=5000)
