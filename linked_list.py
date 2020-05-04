class Node():
    def __init__(self, info):
        self.info = info
        self.next = None

class LinkedList():
    def __init__(self, root):
        self.root = root

    def display(self):
        current = self.root
        while (current):
            print(current.info)
            current = current.next
       
    def add_to_end(self, nd):
        current = self.root
        while (current.next):
            current = current.next
        current.next = nd
 
    def add_to_beg(self, nd):
        old_root = self.root
        self.root = nd
        nd.next = old_root
        
    def remove_from_beg(self): #fifo
        #remove the first element
        if (self.root == None):
            print("empty linked list")
            return None
        result = self.root
        self.root = self.root.next
        return result

    def remove_specific_info(self, info):
        #remove the node containing the info
        if (self.root == None):
            print("empty linked list")
            return
        if (self.root.info == info):
            self.root = self.root.next
            print("removed from the beginning")
            return
        current = self.root
        while (current and current.next):
            if (current.next.info == info):
                current.next = current.next.next
                print("removed ", info)
                return
            current = current.next
        print("can't find the info in the linked list")    
        

link_list = LinkedList(Node(5))
link_list.add_to_beg(Node(3))
link_list.add_to_beg(Node(1))
link_list.add_to_beg(Node(-1))
link_list.add_to_beg(Node(-3))

link_list.display()   

link_list.remove_from_beg()
link_list.display()
