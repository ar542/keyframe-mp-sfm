Imports System.Net
Imports System.Net.Sockets
Imports System.Text
Imports System.Threading
Imports System.Runtime.InteropServices
Imports System.IO
Imports System.Globalization


Public Module GlobalVariables
    Public stream As NetworkStream
    Public client As New TcpClient
    Public port As Integer = Convert.ToInt16(My.Settings.port_number) 'this is the port number
    Public localAddr As IPAddress = IPAddress.Loopback ' this is the IP address
    Public server As TcpListener = New TcpListener(localAddr, port)


End Module
Public Class Form1
    ' Dim listenthread As New Thread(AddressOf listen)
    '  Dim server As New TcpListener(8000)
    Dim pid As Integer
    Dim k As System.Diagnostics.Process
    Private InitialStyle As Integer
    Declare Auto Function SetParent Lib "user32.dll" (ByVal hWndChild As IntPtr, ByVal hWndNewParent As IntPtr) As Integer
    Declare Auto Function SendMessage Lib "user32.dll" (ByVal hWnd As IntPtr, ByVal Msg As Integer, ByVal wParam As Integer, ByVal lParam As Integer) As Integer
    Private Const WM_SYSCOMMAND As Integer = 274
    Private Const SC_MAXIMIZE As Integer = 61488
    Dim tcpClientThread As New System.Threading.Thread(AddressOf lisstion)
    Dim windowclosing As Boolean = False





    Public Property ScrubbingEnabled As Boolean = True
    Protected Overrides ReadOnly Property CreateParams() As CreateParams
        Get
            Const WS_EX_TOPMOST As Integer = &H8

            Dim cp As CreateParams = MyBase.CreateParams
            cp.ExStyle = cp.ExStyle Or WS_EX_TOPMOST
            Return cp
        End Get
    End Property










    Dim p As System.Diagnostics.Process




    Private Sub Form1_FormClosing(sender As Object, e As FormClosingEventArgs) Handles Me.FormClosing
        ' client.Close()
        server.Stop()
        ' tcpClientThread.Abort
        '  AsynchronousSocketListener.closeserver()
        'Console.WriteLine(pid)

        If pid > 0 Then
            p.Kill()
            Console.WriteLine(pid)
        End If

    End Sub


    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        TopMost = My.Settings.topmost
        If TopMost Then
            MakeTopMost()
            FhToolStripMenuItem.Checked = True
        Else
            MakeNormal()

            FhToolStripMenuItem.Checked = False
        End If
        ' multithead()
        tcpClientThread.Start()
        System.Windows.Forms.Control.CheckForIllegalCrossThreadCalls = False
        InitialStyle = GetWindowLong(Me.Handle, User32Wrappers.GWL.ExStyle)
        Dim strPath As String = System.IO.Path.GetDirectoryName( _
    System.Reflection.Assembly.GetExecutingAssembly().CodeBase)
        'Dim p As System.Diagnostics.Process
        Dim pHelp As New ProcessStartInfo
        strPath = strPath.Substring(6)

        If (File.Exists(strPath + "\KeyframeMP.exe")) Then
            pHelp.FileName = strPath + "\KeyframeMP.exe"

        Else
            MsgBox("KeyframeMP.exe was not found in the current directory.", MsgBoxStyle.OkOnly)
            Return

        End If

        Try

            'pHelp.FileName = "C:\Program Files\Zurbrigg\Keyframe MP\bin\keyframe_mp.exe"

            p = Process.Start(pHelp)

            p.WaitForInputIdle()
            pid = p.Id

            Threading.Thread.Sleep(300)
            SetParent(p.MainWindowHandle, Panel2.Handle)
            SendMessage(p.MainWindowHandle, WM_SYSCOMMAND, SC_MAXIMIZE, 0)
            Me.BringToFront()

        Catch ex As Exception
            MsgBox("mpc-hc.exe was not found in the current directory.", MsgBoxStyle.Critical)
            Console.WriteLine(ex)
        End Try



    End Sub






    <DllImport("user32.dll", EntryPoint:="GetWindowLong")> Public Shared Function GetWindowLong(ByVal hWnd As IntPtr, ByVal nIndex As Integer) As Integer
    End Function

    <DllImport("user32.dll", EntryPoint:="SetWindowLong")> Public Shared Function SetWindowLong(ByVal hWnd As IntPtr, ByVal nIndex As Integer, ByVal dwNewLong As Integer) As Integer
    End Function

    <DllImport("user32.dll", EntryPoint:="SetLayeredWindowAttributes")> Public Shared Function SetLayeredWindowAttributes(ByVal hWnd As IntPtr, ByVal crKey As Integer, ByVal alpha As Byte, ByVal dwFlags As Integer) As Boolean
    End Function


    <DllImport("user32.dll", SetLastError:=True)> _
    Private Shared Function SetWindowPos(ByVal hWnd As IntPtr, ByVal hWndInsertAfter As IntPtr, ByVal X As Integer, ByVal Y As Integer, ByVal cx As Integer, ByVal cy As Integer, ByVal uFlags As Integer) As Boolean
    End Function

    Private Const SWP_NOSIZE As Integer = &H1
    Private Const SWP_NOMOVE As Integer = &H2

    Private Shared ReadOnly HWND_TOPMOST As New IntPtr(-1)
    Private Shared ReadOnly HWND_NOTOPMOST As New IntPtr(-2)
    Private Shared ReadOnly HWND_TOP = New IntPtr(0)

    Public Const SWP_NOACTIVATE As Integer = &H10

    Public Const SWP_SHOWWINDOW As Integer = &H40
    Public Sub MakeTopMost()
        SetWindowPos(Me.Handle(), HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE Or SWP_NOSIZE)
    End Sub

    Public Sub MakeNormal()
        SetWindowPos(Me.Handle(), HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE Or SWP_NOSIZE)
    End Sub



    Delegate Sub UpdateTextBoxDelg(text As String)
    Public myDelegate As UpdateTextBoxDelg = New UpdateTextBoxDelg(AddressOf UpdateTextBox)

    Public Sub UpdateTextBox(text As String)
        debugwin.debugbox.AppendText(text & Environment.NewLine)
    End Sub

    Public Sub lisstion()



        server.Start()


        Me.Invoke(myDelegate, "server started")
        Try
            Dim bytes(1024) As Byte
            Dim data As String = Nothing

            ' Enter the listening loop.
            While True
                Console.Write("Waiting for a connection... ")
                Me.Invoke(myDelegate, "Waiting for a connection... ")

                ' Perform a blocking call to accept requests.
                ' You could also user server.AcceptSocket() here.
                client = server.AcceptTcpClient


                Console.WriteLine("Connected!")
                Me.Invoke(myDelegate, "Connected!")
                data = Nothing

                ' Get a stream object for reading and writing
                Dim stream As NetworkStream = client.GetStream()

                Dim i As Int32

                ' Loop to receive all the data sent by the client.
                i = stream.Read(bytes, 0, bytes.Length)

                While (i <> 0)
                    ' Translate data bytes to a ASCII string.
                    data = System.Text.Encoding.ASCII.GetString(bytes, 0, i) 'data from client

                    '  Console.WriteLine(data)
                    Me.Invoke(myDelegate, "cmd:" & data.ToString)
                    Try



                        Select Case True
                            Case data.Contains("clickthough")
                                SetWindowLong(Me.Handle, User32Wrappers.GWL.ExStyle, InitialStyle Or User32Wrappers.WS_EX.Layered Or User32Wrappers.WS_EX.Transparent)
                            Case data.Contains("clickable")

                                SetWindowLong(Me.Handle, User32Wrappers.GWL.ExStyle, InitialStyle Or User32Wrappers.WS_EX.Layered)

                            Case data.Contains("opacity:")
                                ' Dim percent As Double = data.Substring(8)

                                Dim percent As Double = Convert.ToDouble(data.Substring(8), New CultureInfo("en-US"))
                                ' Me.Invoke(myDelegate, percent.ToString)
                                Me.Opacity = percent
                            Case data.Contains("ver")
                                Dim msg As Byte() = System.Text.Encoding.ASCII.GetBytes("ver:1.2")
                                stream.Write(msg, 0, msg.Length)


                        End Select

                    Catch ex As Exception
                        Me.Invoke(myDelegate, "Error:" & ex.ToString)
                    End Try





                    ' Console.WriteLine("Received: {0}", data)

                    ' Process the data sent by the client.
                    '  data = data.ToUpper()
                    ' Dim msg As Byte() = System.Text.Encoding.ASCII.GetBytes(AxWindowsMediaPlayer1.Ctlcontrols.currentPosition) 'sent to client

                    ' Send back a response.
                    ' stream.Write(msg, 0, msg.Length)
                    'Console.WriteLine("Sent: {0}", data)
                    'Console.WriteLine(i)
                    i = stream.Read(bytes, 0, bytes.Length)



                End While

                ' Shutdown and end connection
                'client.Close()


            End While

            'multithead()


        Catch ex As Exception
            server.Stop()
            '  MsgBox(ex.ToString, MsgBoxStyle.Critical)



            Console.WriteLine(ex)


        End Try






    End Sub






    Private Sub multithead()



        Dim tcpClientThread As New System.Threading.Thread(AddressOf lisstion)
        tcpClientThread.Start()
    End Sub




    Private Sub FhToolStripMenuItem_Click(sender As Object, e As EventArgs) Handles FhToolStripMenuItem.Click
        If FhToolStripMenuItem.Checked Then
            MakeTopMost()
            My.Settings.topmost = True
        Else
            MakeNormal()
            My.Settings.topmost = False
        End If
        My.Settings.Save()

    End Sub

  






    Private Sub ToolStripMenuItem1_Click(sender As Object, e As EventArgs) Handles ToolStripMenuItem1.Click
        Dim fd As OpenFileDialog = New OpenFileDialog()
        'Dim strFileName As String
        Dim pHelp As New ProcessStartInfo
        fd.Title = "Open .exe"
        fd.InitialDirectory = "C:\"
        fd.Filter = ".exe files (*.exe*)|*.exe*"
        'fd.FilterIndex = 2
        fd.RestoreDirectory = True

        If fd.ShowDialog() = DialogResult.OK Then
            pHelp.FileName = fd.FileName


            Try


                If pid > 0 Then
                    p.CloseMainWindow()
                End If
                ' pHelp.FileName = "C:\Program Files\Zurbrigg\Keyframe MP\bin\keyframe_mp.exe"

                p = Process.Start(pHelp)
                k = p

                pid = p.Id
                p.WaitForInputIdle()

                Threading.Thread.Sleep(1000)

                SetParent(p.MainWindowHandle, Panel2.Handle)
                SendMessage(p.MainWindowHandle, WM_SYSCOMMAND, SC_MAXIMIZE, 0)
                Me.BringToFront()

            Catch ex As Exception
                MsgBox(ex.ToString, MsgBoxStyle.Critical)
                UpdateTextBox("Error:" & ex.ToString)
                Console.WriteLine(ex)
            End Try



        End If








    End Sub



    Private Sub Form1_SizeChanged(sender As Object, e As EventArgs) Handles Me.SizeChanged


        Try
            If pid > 0 Then
                SetWindowPos(p.MainWindowHandle, HWND_TOP, Panel2.ClientRectangle.Left, Panel2.ClientRectangle.Top, Panel2.ClientRectangle.Width, Panel2.ClientRectangle.Height, SWP_NOACTIVATE Or SWP_SHOWWINDOW)
            End If
        Catch ex As Exception
            Console.WriteLine(ex)
        End Try

    End Sub

    Private Sub DebugWindowToolStripMenuItem_Click(sender As Object, e As EventArgs) Handles DebugWindowToolStripMenuItem.Click
        debugwin.Show()

    End Sub

 

 
    Private Sub setportmenu_Click(sender As Object, e As EventArgs) Handles setportmenu.Click
        setportdialog.Show()

    End Sub

    Private Sub AboutToolStripMenuItem_Click(sender As Object, e As EventArgs) Handles AboutToolStripMenuItem.Click
        MsgBox("version: 1.3")

    End Sub
End Class








'Public Class StateObject
'    ' Client  socket.
'    Public workSocket As Socket = Nothing
'    ' Size of receive buffer.
'    Public Const BufferSize As Integer = 1024
'    ' Receive buffer.
'    Public buffer(BufferSize) As Byte
'    ' Received data string.
'    Public sb As New StringBuilder
'End Class 'StateObject


'Public Class AsynchronousSocketListener
'    ' Thread signal.
'    Public Shared allDone As New ManualResetEvent(False)

'    ' This server waits for a connection and then uses  asychronous operations to
'    ' accept the connection, get data from the connected client, 
'    ' echo that data back to the connected client.
'    ' It then disconnects from the client and waits for another client. 
'    Shared listener As New Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp)

'    Public Shared Sub closeserver()
'        listener.Close()
'    End Sub


'    Public Shared Sub Main()
'        ' Data buffer for incoming data.
'        Dim bytes() As Byte = New [Byte](1023) {}

'        ' Establish the local endpoint for the socket.

'        Dim localEndPoint As New IPEndPoint(IPAddress.Loopback, 13578)

'        ' Create a TCP/IP socket.



'        ' Bind the socket to the local endpoint and listen for incoming connections.
'        listener.Bind(localEndPoint)
'        listener.Listen(100)

'        While True
'            ' Set the event to nonsignaled state.
'            allDone.Reset()

'            ' Start an asynchronous socket to listen for connections.
'            Console.WriteLine("Waiting for a connection...")
'            listener.BeginAccept(New AsyncCallback(AddressOf AcceptCallback), listener)

'            ' Wait until a connection is made and processed before continuing.
'            allDone.WaitOne()
'        End While
'    End Sub 'Main


'    Public Shared Sub AcceptCallback(ByVal ar As IAsyncResult)
'        ' Get the socket that handles the client request.
'        Dim listener As Socket = CType(ar.AsyncState, Socket)
'        ' End the operation.
'        Dim handler As Socket = listener.EndAccept(ar)

'        ' Create the state object for the async receive.
'        Dim state As New StateObject
'        state.workSocket = handler
'        handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, New AsyncCallback(AddressOf ReadCallback), state)
'    End Sub 'AcceptCallback


'    Public Shared Sub ReadCallback(ByVal ar As IAsyncResult)
'        Dim content As String = String.Empty

'        ' Retrieve the state object and the handler socket
'        ' from the asynchronous state object.
'        Dim state As StateObject = CType(ar.AsyncState, StateObject)
'        Dim handler As Socket = state.workSocket

'        ' Read data from the client socket. 
'        Dim bytesRead As Integer = handler.EndReceive(ar)

'        If bytesRead > 0 Then
'            ' There  might be more data, so store the data received so far.
'            state.sb.Append(Encoding.ASCII.GetString(state.buffer, 0, bytesRead))

'            ' Check for end-of-file tag. If it is not there, read 
'            ' more data.
'            content = state.sb.ToString()
'            If content.IndexOf("<EOF>") > -1 Then
'                ' All the data has been read from the 
'                ' client. Display it on the console.
'                Console.WriteLine("Read {0} bytes from socket. " + vbLf + " Data : {1}", content.Length, content)
'                ' Echo the data back to the client.
'                Send(handler, content)
'            Else
'                ' Not all data received. Get more.
'                handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, New AsyncCallback(AddressOf ReadCallback), state)
'            End If
'        End If
'    End Sub 'ReadCallback

'    Private Shared Sub Send(ByVal handler As Socket, ByVal data As String)
'        ' Convert the string data to byte data using ASCII encoding.
'        Dim byteData As Byte() = Encoding.ASCII.GetBytes(data)

'        ' Begin sending the data to the remote device.
'        handler.BeginSend(byteData, 0, byteData.Length, 0, New AsyncCallback(AddressOf SendCallback), handler)
'    End Sub 'Send


'    Private Shared Sub SendCallback(ByVal ar As IAsyncResult)
'        ' Retrieve the socket from the state object.
'        Dim handler As Socket = CType(ar.AsyncState, Socket)

'        ' Complete sending the data to the remote device.
'        Dim bytesSent As Integer = handler.EndSend(ar)
'        Console.WriteLine("Sent {0} bytes to client.", bytesSent)

'        handler.Shutdown(SocketShutdown.Both)
'        handler.Close()
'        ' Signal the main thread to continue.
'        allDone.Set()
'    End Sub 'SendCallback
'End Class 'AsynchronousSocketListener