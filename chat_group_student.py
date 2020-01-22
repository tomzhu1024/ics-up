S_ALONE = 0
S_TALKING = 1

# ==============================================================================
# Group class:
# member fields:
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
# ==============================================================================


class Group:

    def __init__(self):
        self.members = {}
        self.chat_grps = {}
        self.grp_ever = 0

    def join(self, name):
        self.members[name] = S_ALONE
        return

    def is_member(self, name):

        # IMPLEMENTATION
        # ---- start your code ---- #
        return name in self.members.keys()
        # ---- end of your code --- #

    # implement
    def leave(self, name):
        """
        leave the system, and the group
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        self.disconnect(name)
        try:
            del self.members[name]
        except:
            pass
        # ---- end of your code --- #
        return

    def find_group(self, name):
        """
        Auxiliary function internal to the class; return two
        variables: whether "name" is in a group, and if true
        the key to its group
        """

        found = False
        group_key = 0
        # IMPLEMENTATION
        # ---- start your code ---- #
        if name in self.members.keys() and self.members[name] == S_TALKING:
            for k, v in self.chat_grps.items():
                if name in v:
                    found = True
                    group_key = k
                    break
        # ---- end of your code --- #
        return found, group_key

    def connect(self, me, peer):
        """
        me is alone, connecting peer.
        if peer is in a group, join it
        otherwise, create a new group with you and your peer
        """
        peer_in_group, group_key = self.find_group(peer)

        # IMPLEMENTATION
        # ---- start your code ---- #
        # me must be different from peer and me must exist and must be alone to connect
        if me != peer and me in self.members.keys() and self.members[me] == S_ALONE:
            if peer_in_group:
                self.chat_grps[group_key].append(me)
                # Set user status
                self.members[me] = S_TALKING
            elif peer in self.members.keys():
                # peer is alone, create new group
                self.chat_grps[self.grp_ever] = [me, peer]
                self.grp_ever += 1
                # set users status
                self.members[me] = S_TALKING
                self.members[peer] = S_TALKING
            # ---- end of your code --- #
        return

    # implement
    def disconnect(self, me):
        """
        find myself in the group, quit, but stay in the system
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        # Remove from the groups dict
        peer_in_group, group_key = self.find_group(me)
        if peer_in_group:
            self.chat_grps[group_key].remove(me)
            # Only one person in group
            if len(self.chat_grps[group_key]) == 1:
                # Release the status for the person left
                self.members[self.chat_grps[group_key][0]] = S_ALONE
                del self.chat_grps[group_key]
            # Set user status
            self.members[me] = S_ALONE
        # ---- end of your code --- #
        return

    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        return full_list

    # implement
    def list_me(self, me):
        """
        return a list, "me" followed by other peers in my group
        """
        my_list = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        me_in_group, group_key = self.find_group(me)
        if me_in_group:
            # Deep copy
            tmp_list = self.chat_grps[group_key][:]
            tmp_list.remove(me)
            my_list = [me] + tmp_list
        # ---- end of your code --- #
        return my_list


if __name__ == "__main__":
    g = Group()
    g.join('a')
    g.join('b')
    g.join('c')
    g.join('d')
    print(g.list_all())

    g.connect('a', 'b')
    print(g.list_all())
    g.connect('c', 'a')
    print(g.list_all())
    g.leave('c')
    print(g.list_all())
    g.disconnect('b')
    print(g.list_all())
