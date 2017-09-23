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
import os,socket,subprocess,sys,traceback,vs,json,time


class KeyframeMPClient(object):
    """
    Client API for Keyframe MP
    """


    API_VERSION = "2.0.1"

    PORT = 17174

    HEADER_SIZE = 10
    KEYFRAME_MP_PATH = "C:/Program Files/Keyframe MP 2/bin/KeyframeMP.exe"
    kmp_socket = None
    kmp_initialized = False

    def __init__(self, timeout=2):
        """
        """
        self.timeout = timeout
        self.show_timeout_errors = True


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
        msgBox.setWindowFlags( QtCore.Qt.WindowStaysOnTopHint)
        if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:pass

    @classmethod
    def open_keyframe_mp(cls, application_path=""):
        """
        Open the Keyframe MP application.

        :param application_path: Application path override.
        """
        if not application_path:
            application_path = cls.KEYFRAME_MP_PATH

        if not application_path:
            self.error("Keyframe MP application path not set.")
        elif not os.path.exists(application_path):
            self.error("Keyframe MP application path does not exist: {0}".format(application_path))
        else:
            try:
                subprocess.Popen(cls.KEYFRAME_MP_PATH, shell=False, stdin=None, stdout=None, stderr=None)
            except:
                traceback.print_exc()
                self.error("Failed to open Keyframe MP. See script editor for details.")












    def connect(self, port=-1, display_errors=True):
        """
        Create a connection with the application.

        :param port: The port Keyframe MP is listening on.
        :return: True if connection was successful (or already exists). False otherwise.
        """
        if self.is_connected():
            return True

        if port < 0:
            port = self.__class__.PORT

        try:
            self.__class__.kmp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__class__.kmp_socket.connect(("localhost", port))
            self.__class__.kmp_socket.setblocking(0)

            self.__class__.kmp_initialized = False

        except:
            self.__class__.kmp_socket = None
            if display_errors:
                traceback.print_exc()
            return False

        return True

    def disconnect(self):
        """
        Disconnect from the application.

        :return: True if the existing connection was disconnect successfully. False otherwise.
        """
        result = False
        if self.__class__.kmp_socket:
            try:
                self.__class__.kmp_socket.close()
                result = True
            except:
                traceback.print_exc()

        self.__class__.kmp_socket = None
        self.__class__.kmp_initialized = False

        return result

    def is_connected(self):
        """
        Test if a connection exists.

        :return: True if a connection exists. False otherwise.
        """
        self.show_timeout_errors = False
        connected = self.__class__.kmp_socket and self.echo("conn")
        self.show_timeout_errors = True

        if connected:
            return True
        else:
            self.disconnect()
            return False

    def send(self, cmd):
        """
        Send a command to the application and wait for a processed reply.

        :param cmd: Dictionary containing the cmd and args
        :return: Variable depending on cmd.
        """
        json_cmd = json.dumps(cmd)

        message = []
        message.append("{0:10d}".format(len(json_cmd)))  # header
        message.append(json_cmd)
        
        try:
            self.__class__.kmp_socket.sendall(''.join(message))
        except:
            traceback.print_exc()
            
            return None

        return self.recv(cmd)

    def recv(self, cmd):
        """
        Wait for the application to reply to a previously sent cmd.

        :param cmd: Dictionary containing the cmd and args
        :return: Variable depending on cmd.
        """
        total_data = []
        data = ""
        reply_length = 0
        bytes_remaining = self.__class__.HEADER_SIZE

        begin = time.time()
        while time.time() - begin < self.timeout:

            try:
                data = self.__class__.kmp_socket.recv(bytes_remaining)
            except:
                time.sleep(0.01)
                continue

            if data:
                total_data.append(data)

                bytes_remaining -= len(data)
                if(bytes_remaining <= 0):

                    if reply_length == 0:
                        header = "".join(total_data)
                        reply_length = int(header)
                        bytes_remaining = reply_length
                        total_data = []
                    else:
                        reply_json = "".join(total_data)
                        return json.loads(reply_json)

        if self.show_timeout_errors:
            if "cmd" in cmd.keys():
                cmd_name = cmd["cmd"]
                print('[KeyframeMP][ERROR] "{0}" timed out.'.format(cmd_name))
            else:
                print('[KeyframeMP][ERROR] Unknown cmd timed out.')

        return None

    def is_valid_reply(self, reply):
        """
        Test if a reply from the application is valid. Output any messages.

        :param reply: Dictionary containing the response to a cmd
        :return: True if valid. False otherwise.
        """
        if not reply:
            return False

        if not reply["success"]:
            print('[KeyframeMP][ERROR] "{0}" failed: {1}'.format(reply["cmd"], reply["msg"]))
            return False

        return True

    def initialize(self):
        """
        One time initialization required by the application.

        :return: True if successfully initalized. False otherwise.
        """
        if self.__class__.kmp_initialized:
            return True

        cmd = {
            "cmd": "initialize",
            "api_version": self.__class__.API_VERSION
        }

        reply = self.send(cmd)
        if reply and reply["success"] and reply["result"] == 0:
            self.__class__.kmp_initialized = True
            return True
        else:
            print('[KeyframeMP][ERROR] Initialization failed: {0}'.format(reply["msg"]))
            self.disconnect()
            return False

    # ------------------------------------------------------------------
    # COMMANDS
    # ------------------------------------------------------------------
    def echo(self, text):
        """
        Get an echo response from the application.

        :param text: The string to be sent to the application.
        :return: A string containing the text on success. None otherwise.
        """
        cmd = {
            "cmd": "echo",
            "text": text
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["result"]
        else:
            return None

    def get_config(self):
        """
        Get the configuration settings for the application.

        :return: Dictionary containing the config values.
        """
        cmd = {
            "cmd": "get_config"
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply
        else:
            return None

    def set_playing(self, playing, play_forwards=True):
        """
        Set the play state to playing or paused. Option to control play direction.

        :param playing: Enable playing state
        :param play_forwards: Play direction (ignored if playing is False)
        :return: True on success. False otherwise.
        """
        cmd = {
            "cmd": "set_playing",
            "playing": playing,
            "play_forwards": play_forwards
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return True
        else:
            return False

    def is_autoplay(self):
        """
        Get the autoplay state of the player.

        :return: Autoplay state (True/False). None on error.
        """
        cmd = {
            "cmd": "is_autoplay"
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["autoplay"]
        else:
            return None

    def import_file(self, file_path, name="", range_start=-1, range_end=-1):
        """
        Import a source file into the project.

        :param file_path: Path to the source
        :param name: Name of the source
        :param range_start: Range start frame
        :param range_end: Range end frame
        :param parent_id: Parent folder of the source
        :return: Dictionary representing the source object. None on error.
        """
        cmd = {
            "cmd": "import_file",
            "file_path": file_path,
            "name": name,
            "range_start": range_start,
            "range_end": range_end,
            "parent_id": ""
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["source"]
        else:
            return None

    def get_frame(self):
        """
        Get the current frame.

        :return: The current frame. Zero on error.
        """
        cmd = {
            "cmd": "get_frame"
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["frame"]
        else:
            return 0

    def set_frame(self, frame, audio=False, from_range_start=False):
        """
        Set the current frame.

        :param frame: Requested frame number
        :param audio: Play audio for the frame after setting it.
        :param from_range_start: Frame number is relative to the range start.
        :return: The current frame. Zero on error.
        """
        cmd = {
            "cmd": "set_frame",
            "frame": frame,
            "audio": audio,
            "from_range_start": from_range_start
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply["frame"]
        else:
            return 0

    def get_range(self):
        """
        Get the current range.

        :return: Tuple containing the range. None on error.
        """
        cmd = {
            "cmd": "get_range"
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return (reply["start_frame"], reply["end_frame"])
        else:
            return None

    def set_range(self, start_frame, end_frame):
        """
        Set the current range.

        :param start_frame: Requested range start frame number.
        :param end_frame: Requested range end frame number.
        :return: Tuple containing the range. None on error.
        """
        cmd = {
            "cmd": "set_range",
            "start_frame": start_frame,
            "end_frame": end_frame
        }

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return (reply["start_frame"], reply["end_frame"])
        else:
            return None




fps = sfmApp.GetFramesPerSecond()
framerate = vs.DmeFramerate_t( fps )
shotlist=[]
sfmoffset=0
class KeyframeMpSync(QtGui.QMainWindow):
    

 
    def setoffset(self):
        sliderframe=(self.horizontalSlider.value()+ self.offsetnum.value())
        
        self.KeyframeMpHelper.set_frame(sliderframe+sfmoffset)

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
        
        
        if self.synccheck.checkState() and self.KeyframeMpHelper.is_connected():
            sfmoffset=self.getcurrentshotStartTime()
            self.KeyframeMpHelper.set_frame(frame)
        
            self.horizontalSlider.setMaximum(self.getcurrentshotDuration())
            self.horizontalSlider.setValue(0)
        else:
            self.synccheck.setChecked(False)
            self.KeyframeMpHelper.disconnect()
           # self.KeyframeMpHelper.error("could not connect to player\n make sure keyframe mp is running")
            
            
        self.horizontalSlider.setValue(frame-sfmoffset)
        self.label2.setText(str(self.horizontalSlider.value()+sfmoffset)+"/"+str(self.getfilmDuration()))

        
    def OffSet(self):
        if sfmoffset !=0:
            
            return sfmoffset
        else:
            return 0
    
    def on_sfm_time_change(self):
        frame = sfmApp.GetHeadTimeInFrames()
        if self.synccheck.checkState() and self.KeyframeMpHelper.is_connected():

            
            sliderframe=(self.horizontalSlider.value()+ self.offsetnum.value())         
                
                


            self.KeyframeMpHelper.set_frame(sliderframe,from_range_start=True)
            
            sfmApp.SetHeadTimeInFrames(self.horizontalSlider.value()+sfmoffset)
            self.label2.setText(str(self.horizontalSlider.value()+sfmoffset)+"/"+str(self.getfilmDuration()))
                
        else:
            self.synccheck.setChecked(False)
            self.KeyframeMpHelper.disconnect()
           # self.KeyframeMpHelper.error("could not connect to player\n make sure keyframe mp is running")
        
        


    def sync(self):
        
       #will reconnect and disconnect with player depending on if sync is checked
        
        if self.synccheck.checkState():
            
            s = subprocess.check_output('tasklist', shell=True) # get list of running Programs
            
            if "KeyframeMP.exe" in s and  not self.KeyframeMpHelper.is_connected():#reconnect
                self.KeyframeMpHelper.connect()
                self.KeyframeMpHelper.initialize()              
                frame = sfmApp.GetHeadTimeInFrames()
                self.horizontalSlider.setValue(frame-sfmoffset)
            else:
                self.synccheck.setChecked(False)
                self.KeyframeMpHelper.disconnect()
                self.KeyframeMpHelper.error("Could not connect to the player\nmake sure keyframe mp is running")
                
        else:
            #self.synccheck.setChecked(False)
            self.KeyframeMpHelper.disconnect()
            





    def resetall(self):
        self.label2.setText("0/"+str(self.getfilmDuration()))
        global sfmoffset
        sfmoffset=False
        self.synccheck.setChecked(False)
        self.offsetnum.setValue(0)
        self.getshotlist()
        self.horizontalSlider.setMaximum(self.getfilmDuration())
        self.horizontalSlider.setValue(0)
        
        

    

    def on_exit(self,event):
        self.KeyframeMpHelper.disconnect()
        


    
    def setupUi(self, window):
        self.getshotlist()
        window.setObjectName("window")
        window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #window.setWindowModality(QtCore.Qt.ApplicationModal)
        window.resize(360, 60)
        window.closeEvent=self.on_exit
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
        
        
        self.KeyframeMpHelper=KeyframeMPClient()
        self.KeyframeMpHelper.open_keyframe_mp()

        
    def retranslateUi(self, window):
        window.setWindowTitle(QtGui.QApplication.translate("window", "Keyframe MP V1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.synccheck.setText(QtGui.QApplication.translate("window", "Sync", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("window", "Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.current.setText(QtGui.QApplication.translate("window", "current", None, QtGui.QApplication.UnicodeUTF8))
        self.reset.setText(QtGui.QApplication.translate("window", "Reset", None, QtGui.QApplication.UnicodeUTF8))



   
if __name__ == "__main__":
    
   
    
    window = QtGui.QWidget()
    ui = KeyframeMpSync()
    ui.setupUi(window)
    window.show()
   # sys.exit(app.exec_())
    
