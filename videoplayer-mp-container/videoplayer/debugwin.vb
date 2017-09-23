Public Class debugwin

    Private Sub debugwin_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        System.Windows.Forms.Control.CheckForIllegalCrossThreadCalls = False
        Me.TopMost = True

    End Sub

End Class