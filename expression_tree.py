

from __future__ import annotations

from typing import List, Dict, Optional, Tuple, Union


import matplotlib.pyplot as plt
import networkx as nx


from adts import Queue


OP_MULTIPLY = '*'
OP_ADD = '+'
OPERATORS = [OP_ADD, OP_MULTIPLY]


class ExprTree:
    """
    A tree representing an arithmetic expression.

    This class supports operators(+ and *), variables, and integer constants.

    === Private Attributes ===
    _root: The item stored at this tree's root, or None if the tree is empty.
    _subtrees: The list of all subtrees of this expression tree.

    === Representation Invariants ===
    - If self._root is None then self._subtrees is an empty list.
      This setting of attributes represents an empty tree.

      Note: self._subtrees may be empty when self._root is not None.
      This setting of attributes represents a tree consisting of just one
      node.

    - _subtrees contains no empty trees.

    - if _root is an int or a variable (str), then _subtrees is an empty list.

    - if _root is an int it has a value between 1 and 9, inclusive.

    - if _root is a variable, it is a single character (a-z).

    - if _root is an operator ('+' or '*'), it must have at least two children.
    """
    _root: Optional[Union[str, int]]
    _subtrees: List[ExprTree]

    def __init__(self, root: Optional[Union[str, int]],
                 subtrees: List[ExprTree]) -> None:
        """Initialize a new ExprTree with the given root value
        and subtrees.

        If <root> is None, the tree is empty.
        Preconditions:
        - if <root> is None, then <subtrees> is empty.
        - if <root> is not None, then it is either an operator(+ or *),
          an int (1-9), or a variable (a-z).
        - if <root> is an operator, then subtrees has at least two children.
        - if <root> is not an operator, subtrees is an empty list.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this expression tree is empty.

        >>> t1 = ExprTree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = ExprTree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def eval(self, lookup: Dict[str, int]) -> int:
        """
        Evaluate this expression tree and return the result.

        Precondition:
        lookup contains all of the variables necessary to evaluate
        this expression tree.

        >>> exp_t = ExprTree('+', [ExprTree(3, []), \
                                   ExprTree('*', [ExprTree('x', []), \
                                                  ExprTree('y', [])]), \
                                   ExprTree('x', [])])
        >>> look_up = {}
        >>> exp_t.populate_lookup(look_up)
        >>> exp_t.eval(look_up)
        3
        >>> look_up['x'] = 7
        >>> look_up['y'] = 3
        >>> exp_t.eval(look_up)
        31
        """

        if isinstance(self._root, int):
            return self._root
        elif self._root.isalpha():
            return lookup[self._root]
        elif self._root == OP_ADD:
            i = 0
            for subtree in self._subtrees:
                i += subtree.eval(lookup)
            return i
        elif self._root == OP_MULTIPLY:
            i = 1
            for subtree in self._subtrees:
                i *= subtree.eval(lookup)
            return i
        return -1

    def __str__(self) -> str:
        """
        Return a string representation of this expression tree

        >>> exp_t = ExprTree('+', [ExprTree('a', []), \
                                   ExprTree('b', []), \
                                   ExprTree(3, [])])
        >>> str(exp_t) == '(a + b + 3)'
        True
        >>> exp_t = ExprTree(None, [])
        >>> str(exp_t) == '()'
        True
        >>> exp_t = ExprTree(5, [])
        >>> str(exp_t) == '5'
        True
        >>> exp_t = ExprTree('+', [ExprTree('*', [ExprTree(7, []), \
                                                  ExprTree('+', \
                                                           [ExprTree(6, []), \
                                                           ExprTree(6, [])] \
                                                          )]), \
                                   ExprTree(5, [])])
        >>> print(exp_t)
        ((7 * (6 + 6)) + 5)
        >>> exp_t = ExprTree('+', [ExprTree(3, []), \
                                   ExprTree('*', [ExprTree('x', []), \
                                                  ExprTree('y', [])]), \
                                   ExprTree('x', [])])
        >>> print(exp_t)
        (3 + (x * y) + x)
        """

        if self.is_empty():
            return '()'
        elif isinstance(self._root, int) or self._root not in OPERATORS:
            return str(self._root)
        return '(' + f' {self._root} '.join([
            str(subtree) for subtree in self._subtrees]) + ')'

    def __eq__(self, other: ExprTree) -> bool:
        """
        Return whether this ExprTree is equivalent to <other>.

        Two expression tree's are equivalent if their _root attributes are
        equal and their _subtrees are all equal.

        >>> t1 = ExprTree(5, [])
        >>> t1 == ExprTree(5, [])
        True
        >>> t2 = ExprTree('*', [ExprTree(5, []), ExprTree(2, [])])
        >>> t2 == ExprTree('*', [ExprTree(5, []), ExprTree(2, [])])
        True
        >>> t2 == ExprTree('*', [])
        False
        """

        return self._root == other._root and self._subtrees == other._subtrees

    def substitute(self, from_to: Dict[Union[str, int],
                                       Union[str, int]]) -> None:
        """
        Replace each value in this expression tree that is a key in <from_to>
        with the value associated with it in <from_to>.

        Precondition:
        the key-value pairs in <from_to> will result
        in this expression tree still being a valid expression tree.

        >>> exp_t = ExprTree('a', [])
        >>> exp_t.substitute({'a': 1})
        >>> print(exp_t)
        1
        >>> exp_t = ExprTree('*',[ExprTree('a', []), \
                                 ExprTree('*', [ExprTree('a', []),\
                                                ExprTree(1, [])])])
        >>> exp_t.substitute({'a': 2, '*': '+'})
        >>> print(exp_t)
        (2 + (2 + 1))
        """
        if self._root in from_to:
            self._root = from_to[self._root]
        for subtree in self._subtrees:
            subtree.substitute(from_to)

    def populate_lookup(self, lookup: Dict[str, int]) -> None:
        """
        Add entries to <lookup> so it contains a key for all variables
        appearing in this expression tree. Assign a value
        of 0 to each variable.

        >>> expr_t = ExprTree('a', [])
        >>> look_up = {}
        >>> expr_t.populate_lookup(look_up)
        >>> look_up['a'] == 0
        True
        >>> len(look_up) == 1
        True
        """

        if isinstance(self._root, str) and self._root.isalpha():
            lookup[self._root] = 0
        for subtree in self._subtrees:
            subtree.populate_lookup(lookup)

    def append(self, child: ExprTree) -> None:
        """Append child to this ExprTree's list of subtrees.

        Precondition: self is not an empty tree.

        >>> exp_t = ExprTree('+', [ExprTree('a', []), ExprTree(3, [])])
        >>> print(exp_t)
        (a + 3)
        >>> exp_t.append(ExprTree(5, []))
        >>> print(exp_t)
        (a + 3 + 5)
        """
        self._subtrees.append(child)

    def copy(self) -> ExprTree:
        """
        Return a copy of this ExprTree
        """
        if self.is_empty():
            return ExprTree(None, [])
        node = ExprTree(self._root, [])
        for c in self._subtrees:
            node._subtrees.append(c.copy())
        return node

    def visualize(self, g: nx.Graph, maps: Tuple[Dict[str, str],
                                                 Dict[int, List[str]]],
                  path: str = '', depth: int = 0) -> None:
        """
        Helper for creating a visualization of this ExprTree using networkx
        and matplotlib.

        You do not need to understand this code.
        """
        label_map, at_depth = maps
        # record all nodes at each depth and create
        # nodes (with unique names) and edges in the networkx graph g.
        if depth not in at_depth:
            at_depth[depth] = []
        node_label = path + str(depth) + str(self._root)
        at_depth[depth].append(node_label)
        label_map[node_label] = str(self._root)
        g.add_node(node_label)
        i = 0
        for c in self._subtrees:
            # recursively call visualize on each subtree
            c.visualize(g, (label_map, at_depth),
                        path + str(i), depth + 1)
            # connect self to each of its children in the graph
            g.add_edge(node_label,
                       path + str(i) + str(depth + 1) + str(c._root))
            i += 1


def construct_from_list(values: List[List[Union[str, int]]]) -> ExprTree:
    """
    Construct an expression tree from <values>.

    See the handout for a detailed explanation of how <values>
    encodes the expression tree.

    Hint: We have provided you with the helper method ExprTree.construct_child
          You will likely want to use this method.

    Precondition:
    <values> encodes a valid expression tree


    >>> example = [[5]]
    >>> exp_t = construct_from_list(example)
    >>> exp_t == ExprTree(5, [])
    True
    >>> print(exp_t)
    5
    >>> print(ExprTree(5, []))
    5
    >>> example = [['+'], [3, 'a']]
    >>> exp_t = construct_from_list(example)
    >>> subtrees = [ExprTree(3, []), ExprTree('a', [])]
    >>> exp_t == ExprTree('+', subtrees)
    True
    """

    # Assumed strict precondition
    # base case: <values> is empty
    if not values:
        return ExprTree(None, [])
    # base case: the length of <values> is 1 and the first value inside the
    # first sublist is int
    if len(values) == 1 and isinstance(values[0][0], int):
        return ExprTree(values[0][0], [])
    # Then first value should be an operator
    expr_tree = ExprTree(values[0][0], [])
    # Traverse values
    queue = Queue()  # Queue for the sublist
    tree_queue = Queue()  # Queue for the trees to have children
    tree_queue.enqueue(expr_tree)  # enqueue first operator
    for sublist in values[1:]:
        queue.enqueue(sublist)  # enqueue all sublist
    while not queue.is_empty():
        sublist = queue.dequeue()  # dequeue from queue
        current_tree = tree_queue.dequeue()  # dequeue from tree_queue
        for item in sublist:
            new_tree = ExprTree(item, [])
            if item in OPERATORS:
                # if item is an operator, children should be appended to this
                # tree later.
                tree_queue.enqueue(new_tree)
            # If it is not an operator, just append a child
            current_tree.append(new_tree)
    return expr_tree

def visualize(tree: ExprTree,
              display: bool = False,
              fname: str = "./expr_tree_sample") -> None:
    """
    Create a visualization of the given <tree> using networkx and matplotlib.

    You do not need to understand this code, but may find it helpful to use
    it in order to visually see what the expression tree looks like.

    Providing the optional argument <display> set to True will display
    the resulting image.

    The image is saved to <fname>.png (see the default value for <fname> above)
    if <display> is False.
    """
    g = nx.Graph()
    labels = {}
    at_depth = {}
    # populate g based on the tree and collect information to
    # allow us to layout the tree visualization nicely
    tree.visualize(g, (labels, at_depth))

    # set position attribute for each tree node in the visualization,
    # based on how many nodes are at the same depth
    attrs = {}
    m = max([len(at_depth[d]) for d in at_depth])
    height = max(at_depth)
    for k in at_depth:
        nodes = at_depth[k]
        n = len(nodes)
        width = (n / m)
        for i in range(len(nodes)):
            if n == 1:
                loc = 0
            else:
                loc = -width + (2 * i * width / (n - 1))
            attrs[nodes[i]] = {'pos': (loc, -k / height)}

    nx.set_node_attributes(g, attrs)

    # change * to multiplication cross - unicode char u"\u00D7"
    for k in labels:
        labels[k] = labels[k].replace('*', u"\u00D7")

    _draw_graph(g, labels, fname, display)


def _draw_graph(g: nx.Graph,
                labels: Dict[str, str],
                fname: str,
                display: bool) -> None:
    """
    Helper function for visualize.

    Use matplotlib to visualize <g> with the given <labels>.

    If <display> is False, save the image to <fname>.
    Otherwise, show the matplotlib figure.
    """
    pos = nx.get_node_attributes(g, 'pos')
    plt.figure(figsize=(8, 6))
    # plot options
    options = {
        "font_size": 32,
        "node_size": 2800,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5,
    }
    nx.draw(g, pos,
            labels=labels,
            with_labels=True, font_weight='bold', **options)
    ax = plt.gca()
    ax.margins(0.10)
    plt.axis("off")
    if display:
        plt.show()
    else:
        plt.savefig(fname + ".png", dpi=300)
    plt.close()


