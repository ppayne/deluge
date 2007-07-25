#
# signals.py
#
# Copyright (C) 2007 Andrew Resch ('andar') <andrewresch@gmail.com>
# 
# Deluge is free software.
# 
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 2 of the License, or (at your option)
# any later version.
# 
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA    02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.

import logging

try:
    import dbus, dbus.service
    dbus_version = getattr(dbus, "version", (0,0,0))
    if dbus_version >= (0,41,0) and dbus_version < (0,80,0):
        import dbus.glib
    elif dbus_version >= (0,80,0):
        from dbus.mainloop.glib import DBusGMainLoop
        DBusGMainLoop(set_as_default=True)
    else:
        pass
except: dbus_imported = False
else: dbus_imported = True

import pygtk
pygtk.require('2.0')
import gtk, gtk.glade

import functions
from deluge.config import Config

# Get the logger
log = logging.getLogger("deluge")

class Signals:
    def __init__(self, ui):
        self.ui = ui
        self.core = functions.get_core()
        self.core.connect_to_signal("torrent_added", self.torrent_added_signal)
        self.core.connect_to_signal("torrent_removed", 
                                                    self.torrent_removed_signal)
        self.core.connect_to_signal("torrent_queue_changed",
                                            self.torrent_queue_changed_signal)
        self.core.connect_to_signal("torrent_paused", self.torrent_paused)
    
    def torrent_added_signal(self, torrent_id):
        log.debug("torrent_added signal received..")
        log.debug("torrent id: %s", torrent_id)
        # Add the torrent to the treeview
        self.ui.main_window.torrentview.add_row(torrent_id)

    def torrent_removed_signal(self, torrent_id):
        log.debug("torrent_remove signal received..")
        log.debug("torrent id: %s", torrent_id)
        # Remove the torrent from the treeview
        self.ui.main_window.torrentview.remove_row(torrent_id)

    def torrent_queue_changed_signal(self):
        log.debug("torrent_queue_changed signal received..")
        # Force an update of the torrent view
        self.ui.main_window.torrentview.update()

    def torrent_paused(self, torrent_id):
        log.debug("torrent_paused signal received..")
        self.ui.main_window.torrentview.update()
