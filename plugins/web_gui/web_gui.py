#:coding=utf-8:
import os
import logging
import json
import tornado.web
import tornado.websocket
import subprocess
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
        self.factory = self.settings.get("factory")
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
            self.factory.broadcast("An admin has joined the server through Web-GUI.", 0, "", self.get_argument("name"))
            self.failed_login = False
            self.redirect(self.get_argument("next", "/"))


class RestartHandler(BaseHandler):

    def initialize(self):
        self.levels = UserLevels.ranks
        self.player_manager = self.settings.get("playermanager")
        self.web_gui_user = self.player_manager.get_by_name(self.get_current_user())

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        if self.web_gui_user.access_level == self.levels["OWNER"]:
            self.error_message = ""
            self.render("restart.html")
            print(subprocess.call(self.settings.get("restart_script"), shell=True))
        else:
            self.error_message = "Only owners can restart the server!"
            self.render("restart.html")


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.clear_cookie("player")
        self.redirect("/login")


class IndexHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.user = self.get_current_user()
        self.render("index.html")


class DashboardHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.user = self.get_current_user()
        self.render("ajax/dashboard.html")


class PlayerListHandler(BaseHandler):

    def initialize(self):
        self.player_manager = self.settings.get("playermanager")
        self.playerlist = self.player_manager.all()

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.render("ajax/playerlist.html")


class PlayerOnlineSideBarHandler(BaseHandler):

    def initialize(self):
        self.player_manager = self.settings.get("playermanager")
        self.playerlistonline = self.player_manager.who()

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.render("ajax/playersonline.html")


class PlayerOnlineListHandler(BaseHandler):

    def initialize(self):
        self.player_manager = self.settings.get("playermanager")
        self.playerlistonline = self.player_manager.who()

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.render("ajax/playerlistonline.html")


class PlayerEditHandler(BaseHandler):

    def initialize(self):
        self.player_manager = self.settings.get("playermanager")
        self.levels = UserLevels.ranks
        self.web_gui_user = self.player_manager.get_by_name(self.get_current_user())
        self.edit_player = self.player_manager.get_by_name(self.get_argument("playername"))

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        try:
            self.error_message = self.get_argument("error_message")
        except tornado.web.MissingArgumentError:
            self.error_message = ""
        self.render("ajax/playeredit.html")

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        if self.web_gui_user.access_level > self.edit_player.access_level:
            self.edit_player.access_level = self.get_argument("access_level")
            self.error_message = ""
        else:
            error_message = "You are not allowed to change this users' data!"
            self.redirect("ajax/playeredit.html?playername={n}&error_message={e}".format(
                n=self.get_argument("playername"), e=error_message))
        self.render("ajax/playeredit.html")


class AdminStopHandler(BaseHandler):

    def initialize(self):
        self.levels = UserLevels.ranks
        self.web_gui_user = self.player_manager.get_by_name(self.get_current_user())

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
        self.messages = self.settings.get("messages")
        self.messages_log = self.settings.get("messages_log")
        self.callback = PeriodicCallback(self.update_chat, 500)
        self.factory = self.settings.get("factory")

    def open(self, *args):
        self.clients.append(self)
        print(self.messages_log)
        for msg in self.messages_log:
            print(msg)
            self.write_message(msg)
        self.callback.start()

    def on_message(self, message):
        messagejson = json.loads(message)
        user = self.get_current_user()

        self.messages.add(message)
        self.messages_log.add(message)
        self.factory.broadcast(messagejson["message"], 0, "", user)

    def update_chat(self):
        if len(self.messages) > 0:
            for message in self.messages:
                for client in self.clients:
                    client.write_message(message)
            self.messages.clear()

    def on_close(self):
        self.clients.remove(self)
        self.callback.stop()


class WebChatJsHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.render("js/webgui.chat.js")


class WebGuiApp(tornado.web.Application):
    def __init__(self, port, ownerpassword, playermanager, factory, cookie_secret, serverurl, messages, messages_log,
                 restart_script):
        logging.getLogger('tornado.general').addHandler(logging.FileHandler("webgui.log"))
        logging.getLogger('tornado.application').addHandler(logging.FileHandler("webgui.log"))
        logging.getLogger('tornado.access').addHandler(logging.FileHandler("webgui_access.log"))

        handlers = [
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/restart", RestartHandler),
            (r'/chat', WebSocketChatHandler),
            (r'/stopserver', AdminStopHandler),
            (r'/ajax/playerlistonline.html', PlayerOnlineListHandler),
            (r'/ajax/playerlist.html', PlayerListHandler),
            (r'/ajax/playeredit.html', PlayerEditHandler),
            (r'/ajax/playersonline.html', PlayerOnlineSideBarHandler),
            (r'/ajax/dashboard.html', DashboardHandler),
            (r'/js/webgui.chat.js', WebChatJsHandler),
            (r'/index.html', IndexHandler),
            (r'/', IndexHandler),
            (r'/ajax/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.join(os.path.dirname(__file__), 'static/ajax')}),
            (r'/css/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.join(os.path.dirname(__file__), 'static/css')}),
            (r'/js/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.join(os.path.dirname(__file__), 'static/js')}),
            (r'/plugins/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.join(os.path.dirname(__file__), 'static/plugins')}),
            (r'/img/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.join(os.path.dirname(__file__), 'static/img')}),
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
            messages=messages,
            messages_log=messages_log,
            restart_script=restart_script
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.listen(port)