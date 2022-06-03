#!/usr/bin/env python3
import os
from flask import Flask, jsonify, request, redirect, render_template, url_for
from flask import send_file

# local import
import wip

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = 'pu9_data'

@app.route('/wip', methods=['get'])
def wip_rack():
    racks = wip.wip_test_monitor()
    return jsonify(racks)


@app.route('/racklink/<sn>')
def racklink(racksn):
    racklink = {}
    return jsonify(racklink)

if __name__ == '__main__':
    app.run(port=5000)
