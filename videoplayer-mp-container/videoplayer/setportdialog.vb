Public Class setportdialog

  

    Private Sub OK_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles OK.Click
        If Convert.ToInt32(portnumber_input.Text) > 65535 Or portnumber_input.Text.Chars(0) = "0" Then
            ErrorProvider1.SetError(portnumber_input, "port doesnt exist")
            Return
        End If
        My.Settings.port_number = Convert.ToInt16(portnumber_input.Text)
        My.Settings.Save()
        MsgBox("please restart the program for change")
        Me.Close()
    End Sub

    Private Sub Cancel_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Cancel.Click
        Me.Close()
    End Sub

    Private Sub portnumber_input_KeyPress(sender As Object, e As KeyPressEventArgs) Handles portnumber_input.KeyPress
        If Asc(e.KeyChar) <> 8 Then
            If Asc(e.KeyChar) < 48 Or Asc(e.KeyChar) > 57 Then
                e.Handled = True
            End If
        End If
    End Sub



    Private Sub setportdialog_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        portnumber_input.Text = My.Settings.port_number.ToString
        Me.TopMost = True
    End Sub
End Class
