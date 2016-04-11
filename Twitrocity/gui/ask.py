import wx
def ask(parent=None, message='', default_value=''):
	"""Simple dialog to get a response from the user"""
	dlg = wx.TextEntryDialog(parent, message, defaultValue=default_value)
	dlg.ShowModal()
	result = dlg.GetValue()
	dlg.Destroy()
	return result
