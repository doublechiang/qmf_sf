# API for PU9 Big data

## Get Current WIP Rack
Rack Line Data Query -> RealTimeMonitor -> WIPQuery

## Get Racklink 
Rack Line Data Query -> Query -> Base Query

## Get Monitor Test
Rack Line Data Query -> Query -> Base Query

# Test
python -m unittest

# Documentation.


# Deployment
## To Apache WSGI
On CentOS
$ yum install python-flask

For Apache configuration /etc/httpd/base.conf|<ssl.conf>

    WSGIDaemonProcess qmf_sf user=cchiang group=root threads=5 python-path=/usr/lib/python3.6/site-packages
    WSGIScriptAlias /racklog /home/cchiang/qmf_sf/app.wsgi

    <Directory /home/cchiang/qmf_sf >
        LogLevel info
        WSGIProcessGroup qmf_sf
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>


