Imports System.Runtime.InteropServices

Public Class User32Wrappers

    Public Enum GWL As Integer
        ExStyle = -20
    End Enum

    Public Enum WS_EX As Integer
        Transparent = &H20
        Layered = &H80000
    End Enum

    Public Enum LWA As Integer
        ColorKey = &H1
        Alpha = &H2
    End Enum

    <DllImport("user32.dll", EntryPoint:="GetWindowLong")> _
    Public Shared Function GetWindowLong( _
        ByVal hWnd As IntPtr, _
        ByVal nIndex As GWL _
            ) As Integer
    End Function

    <DllImport("user32.dll", EntryPoint:="SetWindowLong")> _
    Public Shared Function SetWindowLong( _
        ByVal hWnd As IntPtr, _
        ByVal nIndex As GWL, _
        ByVal dwNewLong As WS_EX _
            ) As Integer
    End Function

    <DllImport("user32.dll", _
      EntryPoint:="SetLayeredWindowAttributes")> _
    Public Shared Function SetLayeredWindowAttributes( _
        ByVal hWnd As IntPtr, _
        ByVal crKey As Integer, _
        ByVal alpha As Byte, _
        ByVal dwFlags As LWA _
            ) As Boolean
    End Function



    Public Shared Function opp()
        Form1.Opacity = 0.5
        Return 0

    End Function











End Class