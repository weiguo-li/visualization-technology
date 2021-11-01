from collections import defaultdict
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime as dt
import numpy as np
import matplotlib.cm as cm


class Tree:
    def __init__(self, node="", *children):
        self.node = node
        self.width = len(node)
        if children:
            self.children = children
        else:
            self.children = []

    def __str__(self):
        return "%s" % (self.node)

    def __repr__(self):
        return "%s" % (self.node)

    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            return self.children[key]
        if isinstance(key, str):
            for child in self.children:
                if child.node == key: return child

    def __iter__(self):
        return self.children.__iter__()

    def __len__(self):
        return len(self.children)

    def addChild(self, nodeName):
        self.children.append(nodeName)


class DrawTree(object):
    def __init__(self, tree, parent=None, depth=0, number=1):
        self.x = -1.
        self.y = depth
        self.tree = tree
        self.children = [DrawTree(c, self, depth + 1, i + 1)
                         for i, c
                         in enumerate(tree.children)]
        self.parent = parent
        self.thread = None
        self.mod = 0
        self.ancestor = self
        self.change = self.shift = 0
        self._lmost_sibling = None
        # this is the number of the node in its group of siblings 1..n
        self.number = number

    def left(self):
        return self.thread or len(self.children) and self.children[0]

    def right(self):
        return self.thread or len(self.children) and self.children[-1]

    def lbrother(self):
        n = None
        if self.parent:
            for node in self.parent.children:
                if node == self:
                    return n
                else:
                    n = node
        return n

    def get_lmost_sibling(self):
        if not self._lmost_sibling and self.parent and self != \
                self.parent.children[0]:
            self._lmost_sibling = self.parent.children[0]
        return self._lmost_sibling

    lmost_sibling = property(get_lmost_sibling)

    def __str__(self):
        return "%s: x=%s mod=%s" % (self.tree, self.x, self.mod)

    def __repr__(self):
        return self.__str__()


def buchheim(tree):
    dt = firstwalk(DrawTree(tree))
    min = second_walk(dt)
    if min < 0:
        third_walk(dt, -min)
    return dt


def third_walk(tree, n):
    tree.x += n
    for c in tree.children:
        third_walk(c, n)


def firstwalk(v, distance=1.):
    if len(v.children) == 0:
        if v.lmost_sibling:
            v.x = v.lbrother().x + distance
        else:
            v.x = 0.
    else:
        default_ancestor = v.children[0]
        for w in v.children:
            firstwalk(w)
            default_ancestor = apportion(w, default_ancestor, distance)
        # print "finished v =", v.tree, "children"
        execute_shifts(v)

        midpoint = (v.children[0].x + v.children[-1].x) / 2

        ell = v.children[0]
        arr = v.children[-1]
        w = v.lbrother()
        if w:
            v.x = w.x + distance
            v.mod = v.x - midpoint
        else:
            v.x = midpoint
    return v


def apportion(v, default_ancestor, distance):
    w = v.lbrother()
    if w is not None:
        # in buchheim notation:
        # i == inner; o == outer; r == right; l == left; r = +; l = -
        vir = vor = v
        vil = w
        vol = v.lmost_sibling
        sir = sor = v.mod
        sil = vil.mod
        sol = vol.mod
        while vil.right() and vir.left():
            vil = vil.right()
            vir = vir.left()
            vol = vol.left()
            vor = vor.right()
            vor.ancestor = v
            shift = (vil.x + sil) - (vir.x + sir) + distance
            if shift > 0:
                move_subtree(ancestor(vil, v, default_ancestor), v, shift)
                sir = sir + shift
                sor = sor + shift
            sil += vil.mod
            sir += vir.mod
            sol += vol.mod
            sor += vor.mod
        if vil.right() and not vor.right():
            vor.thread = vil.right()
            vor.mod += sil - sor
        else:
            if vir.left() and not vol.left():
                vol.thread = vir.left()
                vol.mod += sir - sol
            default_ancestor = v
    return default_ancestor


def move_subtree(wl, wr, shift):
    subtrees = wr.number - wl.number
    # print wl.tree, "is conflicted with", wr.tree, 'moving', subtrees, 'shift', shift
    # print wl, wr, wr.number, wl.number, shift, subtrees, shift/subtrees
    wr.change -= shift / subtrees
    wr.shift += shift
    wl.change += shift / subtrees
    wr.x += shift
    wr.mod += shift


def execute_shifts(v):
    shift = change = 0
    for w in v.children[::-1]:
        # print "shift:", w, shift, w.change
        w.x += shift
        w.mod += shift
        change += w.change
        shift += w.shift + change


def ancestor(vil, v, default_ancestor):
    # the relevant text is at the bottom of page 7 of
    # "Improving Walker's Algorithm to Run in Linear Time" by Buchheim et al, (2002)
    # http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.16.8757&rep=rep1&type=pdf
    if vil.ancestor in v.parent.children:
        return vil.ancestor
    else:
        return default_ancestor


def second_walk(v, m=0, depth=0, min=None):
    v.x += m
    v.y = depth
    if min is None or v.x < min:
        min = v.x
    for w in v.children:
        min = second_walk(w, m + v.mod, depth + 1, min)
    return min


edges = {'root': ['bigleft', 'm1', 'm2', 'm3', 'm4', 'bigright'],
         'bigleft': ['l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7','l8','l9','l10','l11'],
         'l7': ['ll1'],
         'm3': ['m31'],
         'bigright': ['brr'],
         'brr': ['br1', 'br2', 'br3', 'br4', 'br5', 'br6', 'br7','br8','br9','br10','br11']
         }


def generateTree(edgeDic):
    allNodes = {}
    for k, v in edgeDic.items():
        if k in allNodes:
            n = allNodes[k]
        else:
            n = Tree(k, )
            allNodes[k] = n
        for s in v:
            if s in allNodes:
                cn = allNodes[s]
            else:
                cn = Tree(s, )
                allNodes[s] = cn
            allNodes[k].addChild(cn)
    return allNodes


treeDic = generateTree(edges)
tree = treeDic['root']
d = buchheim(tree)


def width(apex, xm=0):
    if not apex.children:
        return xm
    for child in apex.children:
        if child.x > xm:
            xm = child.x
            # print xm
        xm = width(child, xm)
    return xm


def angleCo(x, y, xm):
    angle = 2 * np.pi * x / (xm + 1)
    nx, ny = y * np.sin(angle), y * np.cos(angle)
    return nx, ny


max_x = width(d)


def drawt(root, circle):
    x = root.x
    y = root.y
    if circle == True:
        x, y = angleCo(x, y, max_x)
    plt.scatter(x, y, facecolor='gray', lw=0, s=100, alpha=.3)
    plt.text(x, y, root.tree, fontsize=10)
    for child in root.children:
        drawt(child, circle)


def drawconn(root, circle):
    rootx = root.x
    rooty = root.y
    if circle == True:
        rootx, rooty = angleCo(rootx, rooty, max_x)
    for child in root.children:
        childx = child.x
        childy = child.y
        if circle == True:
            childx, childy = angleCo(childx, childy, max_x)
        plt.plot([rootx, childx], [rooty, childy], linestyle='-', linewidth=1, color='grey', alpha=0.7)
        drawconn(child, circle)


fig = plt.figure(figsize=(10, 5), facecolor='white')
#
ax1 = fig.add_subplot(121)
drawt(d, False)
drawconn(d, False)
#
ax1 = fig.add_subplot(122)
drawt(d, True)
drawconn(d, True)
#
plt.tight_layout()
plt.show()
