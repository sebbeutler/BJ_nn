import wx 
import wx.html2 

class MyBrowser(wx.Frame): 
  def __init__(self, *args, **kwds): 
    wx.Dialog.__init__(self, *args, **kwds) 
    sizer = wx.BoxSizer(wx.VERTICAL) 
    self.browser = wx.html2.WebView.New(self) 
    sizer.Add(self.browser, 1, wx.EXPAND, 10) 
    self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.browser)
    self.SetSizer(sizer) 
    self.SetSize((700, 700))

  def OnWebViewLoaded(self, evt):
    # The full document has loaded
    print(self.browser.IsBackendAvailable(wx.html2.WebViewBackendIE))

if __name__ == '__main__': 
  app = wx.App() 
  dialog = MyBrowser(None, -1) 
  dialog.browser.LoadURL("http://www.google.com") 
  dialog.Show() 
  app.MainLoop() 