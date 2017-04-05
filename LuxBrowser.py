import gtk
import webkit

#Browser
class Lux():

    def __init__(self):

        self.window = gtk.Window()
        self.window.set_icon_from_file('lux.png')
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.window.set_default_size(360, 600)

        self.favourites = list()

        fav = open('fav.txt','r')
        saved = fav.read()
        fav.close()
        self.favourites = saved.split()

        self.navigation = gtk.HBox()

        self.back = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.forward = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.refresh = gtk.ToolButton(gtk.STOCK_REFRESH)
        self.home = gtk.ToolButton(gtk.STOCK_HOME)
        self.favourite = gtk.ToolButton(gtk.STOCK_APPLY)
        self.address_bar = gtk.Entry()
        #self.progress_bar = gtk.ProgressBar()
        #self.progress_bar.set_fraction(0)

        self.back.connect('clicked', self.go_back)
        self.forward.connect('clicked', self.go_forward)
        self.refresh.connect('clicked', self.refresh_page)
        self.home.connect('clicked', self.homepage)
        self.favourite.connect('clicked', self.save_to_fav)
        self.address_bar.connect('activate', self.load_page)

        self.navigation.pack_start(self.back, False)
        self.navigation.pack_start(self.forward, False)
        self.navigation.pack_start(self.refresh, False)
        self.navigation.pack_start(self.home, False)
        self.navigation.pack_start(self.favourite,False)
        self.navigation.pack_start(self.address_bar)

        self.view = gtk.ScrolledWindow()
        self.webview = webkit.WebView()
        self.webview.open('http://google.it')
        self.webview.connect('title-changed', self.change_title)
        self.webview.connect('load-committed', self.change_url)
        self.view.add(self.webview)

        self.container = gtk.VBox()
        self.container.pack_start(self.navigation, False)
        self.container.pack_start(self.view)

        self.window.add(self.container)
        self.window.show_all()
        gtk.main()

    def load_page(self, widget):
        add = self.address_bar.get_text()
        google_search= 'https://www.google.it/#q='
        closure = '&*'
        if add.startswith('http://') or add.startswith('https://'):
            self.webview.open(add)
        elif 'www' not in add:
            new_google_search = google_search + add + closure
            self.webview.open(new_google_search)
        else:
            add = 'http://' + add
            self.address_bar.set_text(add)
            #self.progress_bar.pulse();
            #self.progress_bar.set_pulse_step(0.5)
            self.webview.open(add)
            #self.progress_bar.set_pulse_step(1.0)
            #self.progress_bar.set_fraction(0.0)

    def change_title(self, widget, frame, title):
        self.window.set_title(title)

    def change_url(self, widget, frame):
        uri = frame.get_uri()
        self.address_bar.set_text(uri)

    def go_back(self, widget):
        self.webview.go_back()

    def go_forward(self, widget):
        self.webview.go_forward()

    def refresh_page(self, widget):
        self.webview.reload()

    def homepage(self,widget):
        self.webview.open('http://www.google.it')

    def save_to_fav(self,widget):
        fav = open('fav.txt','a')
        fav.write(self.address_bar.get_text())
        fav.close()


lux = Lux()
