<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class debugwin
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.debugbox = New System.Windows.Forms.TextBox()
        Me.SuspendLayout()
        '
        'debugbox
        '
        Me.debugbox.Cursor = System.Windows.Forms.Cursors.Default
        Me.debugbox.Dock = System.Windows.Forms.DockStyle.Fill
        Me.debugbox.Font = New System.Drawing.Font("Microsoft Sans Serif", 14.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.debugbox.Location = New System.Drawing.Point(0, 0)
        Me.debugbox.Multiline = True
        Me.debugbox.Name = "debugbox"
        Me.debugbox.ReadOnly = True
        Me.debugbox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical
        Me.debugbox.Size = New System.Drawing.Size(493, 266)
        Me.debugbox.TabIndex = 0
        '
        'debugwin
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.AutoScroll = True
        Me.ClientSize = New System.Drawing.Size(493, 266)
        Me.Controls.Add(Me.debugbox)
        Me.Name = "debugwin"
        Me.Text = "Debug"
        Me.TopMost = True
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents debugbox As System.Windows.Forms.TextBox
End Class
