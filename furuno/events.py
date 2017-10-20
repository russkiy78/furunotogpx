# -*- coding: utf-8 -*-

import re
import wx
import wx.xrc
import serial
from furuno.design import MainFrame
from serial.threaded import LineReader, ReaderThread
from furuno.serial import PrintLines
from _datetime import datetime
from pubsub import pub
from furuno.const import Const
from xml.etree import cElementTree
import math
import threading
from sys import exit

Const = Const()


class EventFrame(MainFrame):
    serialConnect = None
    serialProtocol = None
    serialPorts = list()
    parseWaypoints = {}
    parseRoutes = dict()
    fileObject = None

    def clearVars(self, full):

        # reinit serial ports
        if full:
            self.serialPorts = []
            self.initcom()

        if hasattr(self, 'serialConnect') and self.serialConnect:
            self.serialConnect.close()
        if hasattr(self, 'fileObject') and self.fileObject:
            self.fileObject.close()
        self.serialConnect = None
        self.serialThread = None
        self.serialProtocol = None
        self.fileObject = None
        self.parseWaypoints = {}
        self.parseRoutes = {}
        self.m_buttonDStart.Disable()
        self.m_buttonDStop.Disable()
        self.m_buttonUStart.Disable()
        self.m_buttonUStop.Disable()
        self.m_fileUpload.SetPath('')
        self.m_fileDownload.SetPath('')
        self.m_panelD.Enable()
        self.m_panelU.Enable()
        self.m_fileDownload.Enable()
        self.m_fileUpload.Enable()
        self.m_state.SetValue('')

    def initcom(self):
        # find com ports
        self.serialPorts = PrintLines.searchcom(None)
        if (len(self.serialPorts) == 0):
            self.Error('Not found COM ports on this computer')
            exit()
        self.m_comport.Set(self.serialPorts)
        self.m_comport.Select(0)

    def __init__(self, parent):
        # create form
        super(EventFrame, self).__init__(parent)

        # define variables + init COM
        self.clearVars(True)

        # Connect Events
        self.m_fileDownload.Bind(wx.EVT_FILEPICKER_CHANGED, self.fileDownload)
        self.m_fileUpload.Bind(wx.EVT_FILEPICKER_CHANGED, self.fileUpload)
        self.m_buttonDStart.Bind(wx.EVT_BUTTON, self.buttonDStart)
        self.m_buttonDStop.Bind(wx.EVT_BUTTON, self.buttonDStop)
        self.m_buttonUStart.Bind(wx.EVT_BUTTON, self.buttonUStart)
        self.m_buttonUStop.Bind(wx.EVT_BUTTON, self.buttonUStop)

        # connect to Thread
        pub.subscribe(self.getFromCom, "update")

    def __del__(self):
        pass

    def getFromCom(self, msg):

        # print(msg)

        # catch errors
        mError = re.match('^\#\#(error|info|clear) (.+)$', msg)
        if (mError):
            if (mError.group(1) == 'error'):
                self.Error(mError.group(2))
                self.clearVars(False)
                return
            elif (mError.group(1) == 'info'):
                self.m_state.SetValue(mError.group(2))
            elif (mError.group(1) == 'clear'):
                self.clearVars(False)
            else:
                self.Error('Unknown error: ' + mError.group(0))
                self.clearVars(False)
                return
        else:
            msg = re.sub(r'[\n\r]', '', msg)
            splitstr = re.split(',', msg)

            # parse waypoints & routes
            if (splitstr and len(splitstr) > 1):
                if splitstr[0] == '$PFEC' and splitstr[1] == 'GPwpl':

                    # detect waypoint
                    self.m_state.SetValue("Receive waypoint: " + splitstr[6])

                    # find description/mark
                    mark = re.match('^(\@[a-z]{1})(.+)$', splitstr[8])

                    self.parseWaypoints[splitstr[6].strip()] = {
                        'color': Const.colors[int(splitstr[7])] if splitstr[7] and len(splitstr[7]) > 0 and int(
                            splitstr[7]) < len(
                            Const.colors) else Const.defaultColorText,
                        'mark': Const.marks[mark.group(1)] if mark and mark.group(
                            1) in Const.marks  else Const.defaultMark,
                        'desc': mark.group(2).strip() if mark and mark.group(2).strip() else splitstr[8][2:].strip(),
                        'lat': round(float(splitstr[2][2:]) / 60 + float(splitstr[2][:2]), 15) if splitstr[
                                                                                                      3] == 'N' else round(
                            -float(splitstr[2][2:]) / 60 - float(splitstr[2][:2]), 15),
                        'lon': round(float(splitstr[4][3:]) / 60 + float(splitstr[4][:3]), 15) if splitstr[
                                                                                                      5] == 'E' else round(
                            -float(splitstr[4][3:]) / 60 - float(splitstr[4][:3]), 15)
                    }
                elif splitstr[0] == '$GPRTE':
                    self.m_state.SetValue("Receive track: " + splitstr[4])
                    for x in range(5, len(splitstr)):
                        # parse route
                        # dirty hack remove first symbol from start ( "-" == "skip this point" but I ignore it)
                        routename = splitstr[4].strip()
                        if routename in self.parseRoutes:
                            self.parseRoutes[routename]['track'].append(splitstr[x][1:].strip())
                        else:
                            self.parseRoutes[routename] = {'name': '', 'track': []}
                            self.parseRoutes[routename]['track'].append(splitstr[x][1:].strip())

                elif splitstr[0] == '$PFEC' and splitstr[1] == 'GPrtc':
                    # track name
                    self.m_state.SetValue("Complete track name: " + splitstr[3].strip())
                    self.parseRoutes[splitstr[2].strip()]['name'] = splitstr[3].strip()
                elif splitstr[0] == '$PFEC' and splitstr[1] == 'GPxfr':
                    # end transmission, write result
                    print(self.parseWaypoints)
                    print(self.parseRoutes)

                    try:
                        self.fileObject = open(self.m_fileDownload.GetPath().strip(), 'w', encoding='utf-8')
                    except:
                        self.Error('Could not open output file!')
                        self.clearVars(False)
                        return
                    else:
                        self.fileObject.write(Const.header)
                        self.fileObject.write(Const.metadata.format(
                            time=str(datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ"))
                        ))
                        # waypoints
                        for key, value in self.parseWaypoints.items():
                            self.fileObject.write(Const.waypoint.format(
                                desc=value['desc'],
                                mark=value['mark'],
                                color=value['color'],
                                name=str(key).strip(),
                                lat=value['lat'],
                                lon=value['lon'],
                            ))
                        # tracks
                        for key, value in self.parseRoutes.items():
                            self.fileObject.write(Const.routeStart.format(name=str(value['name']).strip()))
                            for x in value['track']:
                                if x in self.parseWaypoints:
                                    self.fileObject.write(Const.route.format(
                                        desc=self.parseWaypoints[x]['desc'],
                                        mark=self.parseWaypoints[x]['mark'],
                                        color=self.parseWaypoints[x]['color'],
                                        name=str(x).strip(),
                                        lat=self.parseWaypoints[x]['lat'],
                                        lon=self.parseWaypoints[x]['lon']
                                    ))
                            self.fileObject.write(Const.routeEnd)
                        self.fileObject.write(Const.footer)
                        self.clearVars(False)
                        self.m_state.SetValue("Done...")
                else:
                    #  It's a trash! waiting for correct data...
                    self.m_state.SetValue("Waiting for data...")

    def fileDownload(self, event):
        if bool(self.m_fileDownload.GetPath().strip()):
            self.m_buttonDStart.Enable()
        else:
            self.m_buttonDStart.Disable()

    def fileUpload(self, event):
        if bool(self.m_fileUpload.GetPath().strip()):
            self.m_buttonUStart.Enable()
        else:
            self.m_buttonUStart.Disable()

    def buttonDStart(self, event):
        if bool(self.m_fileDownload.GetPath().strip()):

            self.Warn('Please click  "Save WPT/RTE -> PC" in menu on your Furuno, ONLY and when click "OK" here')
            self.m_buttonDStart.Disable()
            self.m_buttonDStop.Enable()
            self.m_panelD.Enable()
            self.m_panelU.Disable()
            self.m_fileDownload.Disable()

            try:
                ser = serial.Serial(
                    port=str(self.m_comport.GetStringSelection()),
                    baudrate=int(self.m_comspeed.GetStringSelection()),
                    timeout=100,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                )
                self.serialConnect = ReaderThread(ser, PrintLines)
                self.serialProtocol = self.serialConnect.__enter__()
            except:
                self.Error("Can't open COM port!")
                self.clearVars(False)
                return
            self.m_state.SetValue("Waiting for data...")

    def buttonDStop(self, event):
        self.clearVars(False)

    def buttonUStop(self, event):
        self.clearVars(False)

    def buttonUStart(self, event):
        self.m_buttonUStart.Disable()
        self.m_buttonUStop.Enable()
        self.m_panelU.Enable()
        self.m_panelD.Disable()
        self.m_fileUpload.Disable()
        if bool(self.m_fileUpload.GetPath().strip()):
            root = ''
            try:
                root = cElementTree.parse(self.m_fileUpload.GetPath().strip()).getroot()
            except:
                self.Error('Could not open input file!')
                self.clearVars(False)
                return
            else:
                try:
                    self.m_state.SetValue('Parse XML')
                    waypointsCounter = 0
                    routesCounter = 0
                    for child in root:
                        if (re.search('\}wpt$', child.tag) and ('lon' in child.attrib) and ('lat' in child.attrib)):
                            # find waypoint
                            lon = float(child.attrib['lon'])
                            furunoLon = round(math.floor(abs(lon)) * 100 + ((abs(lon) - math.floor(abs(lon))) * 60), 3)
                            lat = float(child.attrib['lat'])
                            furunoLat = round(math.floor(abs(lat)) * 100 + ((abs(lat) - math.floor(abs(lat))) * 60), 3)
                            tmpWaypoint = {
                                'lon': '%09.3f' % furunoLon,
                                'NS': 'S' if lon > 0 else 'N',
                                'lat': '%08.3f' % furunoLat,
                                'EW': 'W' if lat > 0 else 'E',
                                'name': '',
                                'desc': '',
                                'color': Const.defaultColor,
                                'mark': Const.defaultMark
                            }
                            for wpt in child:
                                if (re.search('\}name', wpt.tag) and wpt.text):
                                    tmpWaypoint['name'] = wpt.text.strip().upper()
                                if (re.search('\}desc', wpt.tag) and wpt.text):
                                    tmpWaypoint['desc'] = wpt.text.strip().upper()
                                if (re.search('\}sym', wpt.tag) and wpt.text):
                                    splitSym = re.split(',', wpt.text)
                                    if len(splitSym) == 2:
                                        foundmark = [f for f in Const.marks if (Const.marks[f] == splitSym[0].strip())]
                                        tmpWaypoint['mark'] = foundmark[0] if len(foundmark) > 0 else  Const.defaultMark
                                        tmpWaypoint['color'] = Const.colors.index(splitSym[1].strip()) if splitSym[
                                                                                                              1].strip() in Const.colors else Const.defaultColor
                                    else:
                                        foundmark = [f for f in Const.marks if (Const.marks[f] == wpt.text.strip())]
                                        tmpWaypoint['mark'] = foundmark[0] if len(foundmark) > 0 else  Const.defaultMark
                            self.parseWaypoints[waypointsCounter] = tmpWaypoint
                            waypointsCounter += 1

                        if (re.search('\}rte$', child.tag)):
                            tmpRoute = {
                                'name': '',
                                'desc': '',
                                'track': []
                            }
                            for rte in child:
                                if (re.search('\}name$', rte.tag) and rte.text):
                                    tmpRoute['name'] = rte.text.strip().upper()
                                if (re.search('\}desc$', rte.tag) and rte.text):
                                    tmpRoute['desc'] = rte.text.strip().upper()
                                if (re.search('\}rtept$', rte.tag) and ('lon' in rte.attrib) and ('lat' in rte.attrib)):
                                    lon = float(rte.attrib['lon'])
                                    furunoLon = round(
                                        math.floor(abs(lon)) * 100 + ((abs(lon) - math.floor(abs(lon))) * 60), 3)
                                    lat = float(rte.attrib['lat'])
                                    furunoLat = round(
                                        math.floor(abs(lat)) * 100 + ((abs(lat) - math.floor(abs(lat))) * 60), 3)
                                    tmpRoute['track'].append({
                                        'lon': '%09.3f' % furunoLon,
                                        'NS': 'S' if lon > 0 else 'N',
                                        'lat': '%08.3f' % furunoLat,
                                        'EW': 'W' if lat > 0 else 'E',
                                        'name': '',
                                        'desc': '',
                                        'color': Const.defaultColor,
                                        'mark': Const.defaultMark
                                    })
                                    routesTrackCounter = len(tmpRoute['track']) - 1
                                    for rtept in rte:
                                        if (re.search('\}name', rtept.tag) and rtept.text):
                                            tmpRoute['track'][routesTrackCounter]['name'] = rtept.text.strip().upper()
                                        if (re.search('\}desc', rtept.tag) and rtept.text):
                                            tmpRoute['track'][routesTrackCounter]['desc'] = rtept.text.strip().upper()
                                        if (re.search('\}sym', rtept.tag) and rtept.text):
                                            splitSym = re.split(',', rtept.text)
                                            if len(splitSym) == 2:
                                                foundmark = [f for f in Const.marks if
                                                             (Const.marks[f] == splitSym[0].strip())]
                                                tmpRoute['track'][routesTrackCounter]['mark'] = foundmark[0] if len(
                                                    foundmark) > 0 else  Const.defaultMark
                                                tmpRoute['track'][routesTrackCounter]['color'] = Const.colors.index(
                                                    splitSym[1].strip()) if splitSym[
                                                                                1].strip() in Const.colors else Const.defaultColor
                                            else:
                                                foundmark = [f for f in Const.marks if
                                                             (Const.marks[f] == rtept.text.strip())]
                                                tmpRoute['track'][routesTrackCounter]['mark'] = foundmark[0] if len(
                                                    foundmark) > 0 else  Const.defaultMark
                            self.parseRoutes[routesCounter] = tmpRoute
                            routesCounter += 1
                except:
                    self.Error('Error parse XML')
                    self.clearVars(False)
                    return
                else:
                    # pub.subscribe(self.serialTransport.writeMessage, "download")
                    putData = []
                    # waypoints
                    for key, value in self.parseWaypoints.items():
                        putData.append(
                            '$PFEC,GPwpl,{lat},{NS},{lon},{EW},{name:6.6},{color},{desc:18.18},A,,,,'.format(
                                lat=value['lat'],
                                NS=value['NS'],
                                lon=value['lon'],
                                EW=value['EW'],
                                name=value['name'],
                                color=value['color'],
                                desc=str(value['mark']) + str(value['desc'])))
                    # routes
                    routeNum = 0
                    for key, value in self.parseRoutes.items():

                        # print(value)
                        if value['track'] and len(value['track']) > 0:
                            routeNum += 1
                            sentenceNum = math.ceil(len(value['track']) / 8)
                            sentenceCount = 1
                            innersentenceCount = 1
                            line = '$GPRTE,{sentenceNum},{sentenceCount},C,{routeNum:02d}'.format(
                                sentenceNum=sentenceNum,
                                sentenceCount=sentenceCount,
                                routeNum=routeNum
                            )
                            for x in range(0, len(value['track'])):
                                line += ', {name:6}'.format(
                                    name=value['track'][x]['name']
                                )
                                if innersentenceCount == 8 or x == len(value['track']) - 1:
                                    innersentenceCount = 1
                                    sentenceCount += 1
                                    # print (line)
                                    # self.serialProtocol.write_line(line)
                                    putData.append(line)
                                    line = '$GPRTE,{sentenceNum},{sentenceCount},C,{routeNum:02d}'.format(
                                        sentenceNum=sentenceNum,
                                        sentenceCount=sentenceCount,
                                        routeNum=routeNum
                                    )
                                else:
                                    innersentenceCount += 1

                            # name track
                            putData.append('$PFEC,GPrtc,{routeNum:02d},{name:16.16}'.format(
                                routeNum=routeNum,
                                name=value['name']
                            ))

                    putData.append('$PFEC,GPxfr,CTL,E')
                    # for val in putData:
                    # print(val)
                    # connect to Thread

                    if putData and len(putData) > 0:
                        self.m_state.SetValue('Save to Furuno')
                        self.Warn(
                            'Please click "Load WPT/RTE <- PC" in menu on your Furuno, when click "Yes", and when click "OK" here')
                        self.serialThread = threading.Thread(target=self.toCom, args=[putData])
                        self.serialThread.start()
                    else:
                        self.Warn('TNo data to upload')
                        self.clearVars(False)

    def toCom(self, args):
        try:
            self.serialConnect = serial.Serial(
                port=str(self.m_comport.GetStringSelection()),
                baudrate=int(self.m_comspeed.GetStringSelection()),
                timeout=1,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
        except:
            self.Error("Can't open COM port!")
            self.clearVars(False)
            return
        else:
            for val in args:
                try:
                    # print(val)
                    self.serialConnect.write(val.encode('utf-8', 'replace') + b'\r\n')
                    wx.CallAfter(pub.sendMessage, "update", msg='##info Write: ' + val)
                except:
                    wx.CallAfter(pub.sendMessage, "update", msg='##error Write cancelled!')
                    return
            self.Info('Success!')
            self.clearVars(False)
