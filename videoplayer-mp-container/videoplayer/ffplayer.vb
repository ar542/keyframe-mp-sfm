Imports System.Threading
Imports System.Diagnostics
Imports System.Runtime.InteropServices
Public Class ffplayer
    Dim WithEvents proc As New Process


    Declare Auto Function SetParent Lib "user32.dll" (ByVal hWndChild As IntPtr, ByVal hWndNewParent As IntPtr) As Integer
    Declare Auto Function SendMessage Lib "user32.dll" (ByVal hWnd As IntPtr, ByVal Msg As Integer, ByVal wParam As Integer, ByVal lParam As Integer) As Integer
    Private Const WM_SYSCOMMAND As Integer = 274
    Private Const SC_MAXIMIZE As Integer = 61488
    ' "C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64.exe" "C:\Users\AR\anthony\Dropbox\Public\assassins creed 2 brutal deaths.mp4" /start 5000
    Friend Sub Rodar_Processo()
        Dim p As System.Diagnostics.Process
        Dim pHelp As New ProcessStartInfo
        pHelp.FileName = "C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64.exe"
        'pHelp.Arguments = """C:\Users\AR\anthony\Dropbox\Public\assassins creed 2 brutal deaths.mp4"" /start 5000"""
        'pHelp.UseShellExecute = True
        'pHelp.WindowStyle = ProcessWindowStyle.Normal

        p = Process.Start(pHelp)
        p.WaitForInputIdle()

        Threading.Thread.Sleep(100)
        SetParent(p.MainWindowHandle, Panel1.Handle)
        SendMessage(p.MainWindowHandle, WM_SYSCOMMAND, SC_MAXIMIZE, 0)
        Me.BringToFront()
    End Sub

    Private Sub ffplayer_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Rodar_Processo()
    End Sub

    Private Sub Panel1_Paint(sender As Object, e As PaintEventArgs) Handles Panel1.Paint

    End Sub

    Private Sub Panel1_SizeChanged(sender As Object, e As EventArgs) Handles Panel1.SizeChanged
        '  SendMessage(p.MainWindowHandle, WM_SYSCOMMAND, SC_MAXIMIZE, 0)
    End Sub

    Private Sub ffplayer_SizeChanged(sender As Object, e As EventArgs) Handles Me.SizeChanged

    End Sub
End Class