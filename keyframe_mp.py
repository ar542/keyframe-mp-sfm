# -*- coding: utf-8 -*-



###############################################################################
# Name: 
#   keyframe_mp.py
#
# Description: 
#   User interface for syncing the SFM timeline with Keyframe MP.
#

#
# Notes:
#   The port set in the Keyframe MP preference must match the 
#   KEYFRAME_MP_PORT constant defined below.
#
# Original Author: 
#   Chris Zurbrigg (http://zurbrigg.com)
# SFM port by:
#   http://steamcommunity.com/id/OMGTheresABearInMyOatmeal
#
###############################################################################













from PySide import QtCore, QtGui
import os,socket,subprocess,sys,traceback,vs



class KeyframeMpHelper(QtGui.QMainWindow):
    @classmethod
    def error(cls,e):
        #error box

        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical,
                "ERROR", " \n"+str(e),
                QtGui.QMessageBox.NoButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        msgBox.setFont(font)
        msgBox.addButton("&Continue", QtGui.QMessageBox.RejectRole)
        if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:pass




    
    '''
    Helper class for connecting and sending commands to Keyframe MP
    '''
    
    #if sys.platform == "win32":
     #   KEYFRAME_MP_PATH = "C:/Program Files/Zurbrigg/Keyframe MP/bin/keyframe_mp.exe"
    #else:
    KEYFRAME_MP_PATH = "C:/Program Files/Keyframe MP 2/bin/KeyframeMP.exe"
    
    KEYFRAME_MP_PORT = 17174

    kf_socket = None
    
    @classmethod
    def open_player(cls):
        if os.path.exists(cls.KEYFRAME_MP_PATH):
            subprocess.Popen(cls.KEYFRAME_MP_PATH, shell=False, stdin=None, stdout=None, stderr=None)
            
        else:
            cls.error("Keyframe MP not found. Please update path.")
                     
    
    @classmethod
    def connect(cls):
        if cls.is_connected():
            return True
        
        try:
            cls.kf_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cls.kf_socket.connect(("localhost", cls.KEYFRAME_MP_PORT))

            return True
        except:
            cls.kf_socket = None
            cls.error("Can not connect to player, possible reasons:\n1.Keyframe MP player must be running\n2.Keyframe MP player requires a licence to connect\n3.Set Keyframe MP player port setting to 17171")
            traceback.print_exc()
            return False
            
    @classmethod
    def disconnect(cls):
        
        if (cls.kf_socket):
            try:
                cls.kf_socket.close()
                om.MGlobal.displayInfo("Connection disconnected");
            except:
                om.MGlobal.displayError("Failed to disconnect")
        
        cls.kf_socket = None
        
    @classmethod
    def is_connected(cls):
        if not cls.kf_socket:
            return False
        
        try:
            
            cls.kf_socket.send("ping\n")
            
            
            return True
        except:
            return False
        
    @classmethod
    def send(cls, command):
        if not cls.connect():
            return False
        
        try:
            cls.kf_socket.send(command)
            return True
        except:
            traceback.print_exc()
            return False
        
        
    @classmethod
    def load_media(cls, filename, range_start=-1, range_end=-1):
        cls.send("file '{0}' {1} {2}\n".format(filename, range_start, range_end))
        
    @classmethod
    def set_current_frame(cls, frame):
        return cls.send("frame {0}\n".format(frame))
        
    @classmethod
    def set_current_frame_relative(cls, frame):

        return cls.send("frameRelative {0}\n".format(frame))
        







fps = sfmApp.GetFramesPerSecond()
framerate = vs.DmeFramerate_t( fps )
shotlist=[]
sfmoffset=0
class KeyframeMpSync(QtGui.QMainWindow):
    

 
    def setoffset(self):
        sliderframe=(self.horizontalSlider.value()+ self.offsetnum.value())
        
        KeyframeMpHelper.set_current_frame(sliderframe+sfmoffset)

    def getshotlist(self):
        global shotlist
        shotlist=[]
        shots = sfmApp.GetShots()
        for shot in shots:
            nStartFrame = shot.GetStartTime().CurrentFrame( framerate, 0 )
            nDuration =  shot.GetDuration().CurrentFrame( framerate, 0 )
            shotlist.append( [ shot.name, shot.text, nStartFrame, nDuration ] )
        

    def getfilmDuration(self):
        Duration=0
        for shot in shotlist:
            
            Duration+=shot[3]
        
        return Duration

    def getcurrentshotDuration(self):
        shot = sfmApp.GetShotAtCurrentTime()
        return shot.GetDuration().CurrentFrame( framerate, 0 )
        
    def getcurrentshotStartTime(self):

        shot = sfmApp.GetShotAtCurrentTime()
        
        return shot.GetStartTime().CurrentFrame( framerate, 0 )

    def setcurrent(self):
        global sfmoffset
        
        frame =sfmApp.GetHeadTimeInFrames()
        KeyframeMpHelper.set_current_frame(frame)
        
        if self.synccheck.checkState():
            sfmoffset=self.getcurrentshotStartTime()
        
            self.horizontalSlider.setMaximum(self.getcurrentshotDuration())
            self.horizontalSlider.setValue(0)
        self.horizontalSlider.setValue(frame-sfmoffset)
        self.label2.setText(str(self.horizontalSlider.value()+sfmoffset)+"/"+str(self.getfilmDuration()))

        
    def OffSet(self):
        if sfmoffset !=0:
            
            return sfmoffset
        else:
            return 0
    
    def on_sfm_time_change(self):
        frame = sfmApp.GetHeadTimeInFrames()
        if self.synccheck.checkState():

            
            sliderframe=(self.horizontalSlider.value()+ self.offsetnum.value())
            
                
                


            KeyframeMpHelper.set_current_frame_relative(sliderframe)
            
            sfmApp.SetHeadTimeInFrames(self.horizontalSlider.value()+sfmoffset)
            self.label2.setText(str(self.horizontalSlider.value()+sfmoffset)+"/"+str(self.getfilmDuration()))
                
            
        
        


    def sync(self):
        if self.synccheck.checkState():
            
            frame = sfmApp.GetHeadTimeInFrames()
            self.horizontalSlider.setValue(frame-sfmoffset)





    def resetall(self):
        self.label2.setText("0/"+str(self.getfilmDuration()))
        global sfmoffset
        sfmoffset=False
        self.synccheck.setChecked(False)
        self.offsetnum.setValue(0)
        self.getshotlist()
        self.horizontalSlider.setMaximum(self.getfilmDuration())
        self.horizontalSlider.setValue(0)
        
        






    
    def setupUi(self, window):
        self.getshotlist()
        window.setObjectName("window")
        window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #window.setWindowModality(QtCore.Qt.ApplicationModal)
        window.resize(360, 60)
        self.verticalLayout = QtGui.QVBoxLayout(window)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.synccheck = QtGui.QCheckBox(window)
        self.synccheck.setObjectName("synccheck")
        self.horizontalLayout.addWidget(self.synccheck)
        self.label = QtGui.QLabel(window)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.offsetnum = QtGui.QSpinBox(window)
        self.offsetnum.setMaximum(999999)
        self.offsetnum.setMinimum(-999999)
        self.offsetnum.valueChanged[int].connect(self.setoffset)
        self.horizontalLayout.addWidget(self.offsetnum)
        self.current = QtGui.QPushButton(window)
        self.current.setObjectName("current")
        self.horizontalLayout.addWidget(self.current)
        self.reset = QtGui.QPushButton(window)
        self.reset.setObjectName("reset")
        self.horizontalLayout.addWidget(self.reset)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(self.reset)
        #self.verticalLayout.addLayout(self.horizontalLayout)
        self.label2 = QtGui.QLabel(window)
        self.verticalLayout.addWidget(self.label2)
        self.label2.setText("0/"+str(self.getfilmDuration()))
        self.horizontalSlider = QtGui.QSlider(window)
        self.getshotlist()
        self.horizontalSlider.setMaximum(self.getfilmDuration())
        #self.horizontalSlider.setPageStep(7)
        self.horizontalSlider.setProperty("value", 16)
        self.horizontalSlider.setSliderPosition(0)
        self.horizontalSlider.setTracking(True)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.horizontalSlider.setTickInterval(self.getfilmDuration()/30)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.valueChanged.connect(self.on_sfm_time_change)	
        
        QtCore.QMetaObject.connectSlotsByName(window)


        self.verticalLayout.addWidget(self.horizontalSlider)
        
        
        self.retranslateUi(window)
        self.synccheck.stateChanged.connect(self.sync)
        
        
        self.reset.clicked.connect(lambda: self.resetall())
        self.current.clicked.connect(lambda: self.setcurrent())
        
    def retranslateUi(self, window):
        window.setWindowTitle(QtGui.QApplication.translate("window", "Keyframe MP V1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.synccheck.setText(QtGui.QApplication.translate("window", "Sync", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("window", "Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.current.setText(QtGui.QApplication.translate("window", "current", None, QtGui.QApplication.UnicodeUTF8))
        self.reset.setText(QtGui.QApplication.translate("window", "Reset", None, QtGui.QApplication.UnicodeUTF8))



   
if __name__ == "__main__":
    
    KeyframeMpHelper.open_player()
    
    window = QtGui.QWidget()
    ui = KeyframeMpSync()
    ui.setupUi(window)
    window.show()
   # sys.exit(app.exec_())
    
