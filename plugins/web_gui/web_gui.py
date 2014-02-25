#:coding=utf-8:
import os
import logging
import ujson
import tornado.web
import tornado.websocket
from twisted.internet import reactor
from plugins.core.player_manager import permissions, PlayerManager, UserLevels
from plugins.core.player_manager.manager import Player
from tornado.ioloop import PeriodicCallback
from base_plugin import BasePlugin


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("player")


class LoginHandler(BaseHandler):

    def initialize(self):
        self.failed_login = False
        self.player_manager = self.settings.get("playermanager")

    def get(self):
        self.render("login.html")

    def post(self):
        self.login_user = self.player_manager.get_by_name(self.get_argument("name"))

        if self.login_user is None or self.get_argument("password") != self.settings.get("ownerpassword"):
            self.failed_login = True
            self.render("login.html")
        else:
            self.set_secure_cookie("player", self.get_argument("name"))
            self.failed_login = False
            self.redirect(self.get_argument("next", "/"))


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.clear_cookie("player")
        self.redirect("/login")


class IndexHandler(BaseHandler):
    def initialize(self):
        self.player_manager = self.settings.get("playermanager")

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.playerlistonline = self.player_manager.who()
        self.render("index.html")


class PlayerListHandler(BaseHandler):

    def initialize(self):
        self.player_manager = self.settings.get("playermanager")
        self.playerlist = self.player_manager.all()

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.render("playerlist.html")


class PlayerEditHandler(BaseHandler):

    def initialize(self):
        self.player_manager = self.settings.get("playermanager")
        self.levels = UserLevels.ranks
        self.web_gui_user = self.player_manager.get_by_name(self.get_secure_cookie("player"))
        self.edit_player = self.player_manager.get_by_name(self.get_argument("playername"))
        self.edit_player_dict = self.edit_player.as_dict()

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        try:
            self.error_message = self.get_argument("error_message")
        except tornado.web.MissingArgumentError:
            self.error_message = ""
        self.render("playeredit.html")

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        if self.web_gui_user.access_level > self.edit_player.access_level:
            self.edit_player.access_level = self.get_argument("access_level")
        else:
            error_message = "You are not allowed to change this users' data!"
            self.redirect("playeredit.html?playername={n}&error_message={e}".format(n=self.get_argument("playername"),
                                                                                    e=error_message))
        self.redirect("playeredit.html?playername={n}".format(n=self.get_argument("playername")))


class AdminStopHandler(BaseHandler):

    def initialize(self):
        self.levels = UserLevels.ranks
        self.player_manager = self.settings.get("playermanager")
        self.web_gui_user = self.player_manager.get_by_name(self.get_secure_cookie("player"))

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        if self.web_gui_user.access_level == self.levels["OWNER"]:
            self.error_message = ""
            self.render("adminstop.html")
            reactor.stop()
        else:
            self.error_message = "Only owners can stop the server!"
            self.render("adminstop.html")


class WebSocketChatHandler(tornado.websocket.WebSocketHandler):

    def initialize(self):
        self.clients = []
        #self.messages = set()
        self.messages = self.settings.get("messages")
        self.callback = PeriodicCallback(self.update_chat, 500)

    def open(self, *args):
        self.clients.append(self)
        self.callback.start()

    def on_message(self, message):
        messagejson = ujson.loads(message)
        player = self.get_secure_cookie("player")
        factory = self.settings.get("factory")

        self.messages.add(message)
        factory.broadcast(messagejson["message"], 0, "", player)

    def update_chat(self):
        if len(self.messages) > 0:
            for message in self.messages:
                for client in self.clients:
                    client.write_message(message)
            self.messages.clear()

    def on_close(self):
        self.clients.remove(self)
        self.callback.stop()


class WebGuiApp(tornado.web.Application):
    def __init__(self, port, ownerpassword, playermanager, factory, cookie_secret, serverurl, messages):
        logging.getLogger('tornado.general').addHandler(logging.FileHandler("webgui.log"))
        logging.getLogger('tornado.application').addHandler(logging.FileHandler("webgui.log"))
        logging.getLogger('tornado.access').addHandler(logging.FileHandler("webgui_access.log"))

        handlers = [
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r'/chat', WebSocketChatHandler),
            (r'/stopserver', AdminStopHandler),
            (r'/playerlist.html', PlayerListHandler),
            (r'/playeredit.html', PlayerEditHandler),
            (r'/index.html', IndexHandler),
            (r'/', IndexHandler),
            (r'/style/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.join(os.path.dirname(__file__), 'style')}),
            (r'/css/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.join(os.path.dirname(__file__), 'static/css')}),
            (r'/js/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.join(os.path.dirname(__file__), 'static/js')}),
            (r'/images/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.join(os.path.dirname(__file__), 'static/images')})
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=cookie_secret,
            login_url="/login",
            xsrf_cookies=True,
            debug=True,
            ownerpassword=ownerpassword,
            playermanager=playermanager,
            factory=factory,
            wsport=port,
            serverurl=serverurl,
            messages=messages
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.listen(port)