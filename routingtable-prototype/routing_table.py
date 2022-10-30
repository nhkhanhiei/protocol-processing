__all__ = ['RoutingTable']

from contact_list import ContactList


class RoutingTable(object):
    def __init__(self):
        self.contacts = ContactList()
        self.add_contacts = ContactList()
        self.remove_contacts = ContactList()
