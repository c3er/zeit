"""A directory browser using Ttk Treeview.

Based on the demo found in Tk 8.5 library/demos/browse
"""
import os
import glob
import tkinter
from tkinter import ttk

class AutoScrollbar(ttk.Scrollbar):
    '''A scrollbar that hides it self if it's not needed.
    Only works if you use the grid geometry manager.
    '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        super().set(lo, hi)
        
    def pack(self, **kw):
        raise tkinter.TclError("Can not use pack with this widget")
    
    def place(self, **kw):
        raise tkinter.TclError("Can not use place with this widget")

# Treeview related #############################################################
def populate_tree(tree, node):
    if tree.set(node, "type") != 'directory':
        return

    path = tree.set(node, "fullpath")
    tree.delete(*tree.get_children(node))

    parent = tree.parent(node)
    special_dirs = [] if parent else glob.glob('.') + glob.glob('..')

    for p in special_dirs + os.listdir(path):
        ptype = None
        p = os.path.join(path, p).replace('\\', '/')
        
        if os.path.isdir(p):
            ptype = "directory"
        elif os.path.isfile(p):
            ptype = "file"

        fname = os.path.split(p)[1]
        id = tree.insert(node, "end", text = fname, values = [p, ptype])

        if ptype == 'directory':
            if fname not in ('.', '..'):
                tree.insert(id, 0, text = "dummy")
                tree.item(id, text = fname)
        elif ptype == 'file':
            size = os.stat(p).st_size
            tree.set(id, "size", "%d bytes" % size)


def populate_roots(tree):
    dir = os.path.abspath('.').replace('\\', '/')
    node = tree.insert('', 'end', text = dir, values = [dir, "directory"])
    populate_tree(tree, node)
################################################################################

# Handlers #####################################################################
def update_tree(event):
    tree = event.widget
    populate_tree(tree, tree.focus())

def change_dir(event):
    tree = event.widget
    node = tree.focus()
    
    if tree.parent(node):
        path = os.path.abspath(tree.set(node, "fullpath"))
        if os.path.isdir(path):
            os.chdir(path)
            tree.delete(tree.get_children(''))
            populate_roots(tree)
################################################################################

def main():
    root = tkinter.Tk()
    
    vsb = AutoScrollbar(orient = "vertical")
    hsb = AutoScrollbar(orient = "horizontal")
    
    tree = ttk.Treeview(
        columns = ("fullpath", "type", "size"),
        displaycolumns = "size",
        yscrollcommand = vsb.set,
        xscrollcommand = hsb.set
    )
    
    vsb.configure(command = tree.yview)
    hsb.configure(command = tree.xview)
    
    tree.heading("#0", text = "Directory Structure", anchor = 'w')
    tree.heading("size", text = "File Size", anchor = 'w')
    tree.column("size", stretch = 0, width = 100)
    
    populate_roots(tree)
    tree.bind('<<TreeviewOpen>>', update_tree)
    tree.bind('<Double-Button-1>', change_dir)
    
    # Arrange the tree and its scrollbars in the toplevel
    tree.grid(column = 0, row = 0, sticky = 'nswe')
    vsb.grid(column = 1, row = 0, sticky = 'ns')
    hsb.grid(column = 0, row = 1, sticky = 'ew')
    root.grid_columnconfigure(0, weight = 1)
    root.grid_rowconfigure(0, weight = 1)
    
    root.mainloop()
    
if __name__ == '__main__':
    main()
