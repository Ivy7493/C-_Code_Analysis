class Node {
private:
    int key;
    Node* next;
    /* Other members of Node Class */
 
    // Now class  LinkedList can
    // access private members of Node
    friend class LinkedList;
};