import sys
import time

class Node:
    #Represents a node in RedBlack tree
    def __init__(self, key, value, color="RED"):
        #Initialize new node
        self.key = key
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    #This class implements Red Black tree data structure
    def __init__(self):
        #Initialize an empty red black tree
        self.NIL = Node(None, None, "BLACK")
        self.root = self.NIL

    def insert(self, key, value):
        """
        Insert a new key-value pair into the tree.
        Args:
            key: The key to insert
            value: The value associated with the key
        """
        new_node = Node(key, value)
        new_node.left = self.NIL
        new_node.right = self.NIL
        # Find the proper position for the new node

        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right
        
        # Insert the new node
        new_node.parent = y
        if y is None:
            self.root = new_node
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node
        # Fix the tree to maintain Red-Black properties
        self._insert_fixup(new_node)

    def _insert_fixup(self, k):
        """
        Fix the Red-Black Tree properties after insertion.
        Args:
            k: The newly inserted node
        """
        while k.parent and k.parent.color == "RED":
            if k.parent == k.parent.parent.left:
                y = k.parent.parent.right
                if y.color == "RED":
                    k.parent.color = "BLACK"
                    y.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self._right_rotate(k.parent.parent)
            else:
                # Mirror image of the above case
                y = k.parent.parent.left
                if y.color == "RED":
                    k.parent.color = "BLACK"
                    y.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self._left_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"

    def _left_rotate(self, x):
        """
        Perform a left rotation on the given node.
        Args:
            x: The node to rotate
        """
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        """
        Perform a right rotation on the given node.
        Args:
            x: The node to rotate
        """
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def search(self, key):
        """
        Search for a key in the tree.
        Args: key: The key to search for
        Returns the value associated with the key, or None if not found
        """
        return self._search_helper(self.root, key)

    def _search_helper(self, node, key):
        """
        This is a recursive helper method for search.
        Args:
            node: The current node in the recursion
            key: The key to search for
        Returns the value associated with the key, or None if not found
        """
        if node == self.NIL or key == node.key:
            return node.value if node != self.NIL else None
        if key < node.key:
            return self._search_helper(node.left, key)
        return self._search_helper(node.right, key)

    def delete(self, key):
        """
        This method deletes a node with the given key from the tree.
        Args:
            key: The key to delete
        Returns True if the key was found and deleted, False otherwise
        """
        z = self._find_node(self.root, key)
        if z == self.NIL:
            return False

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "BLACK":
            self._delete_fixup(x)
        return True

    def _find_node(self, node, key):
        """
        Find a node with the given key in the tree.
        Args:
            node: The current node in the recursion
            key: The key to find
        Returns the node with the given key, or self.NIL if not found
        """
        if node == self.NIL or key == node.key:
            return node
        if key < node.key:
            return self._find_node(node.left, key)
        return self._find_node(node.right, key)

    def _minimum(self, node):
        # Find the minimum node in the subtree rooted at node
        while node.left != self.NIL:
            node = node.left
        return node

    def _transplant(self, u, v):
        # Replace subtree rooted at node u with subtree rooted at node 
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_fixup(self, x):
        """
        Fix the Red-Black Tree properties after deletion.
        Args:
            x: The node to start fixing from
        """
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"

    def inorder_traversal(self):
        """
        Perform an inorder traversal of the tree.
        Returns a sorted list of (key, value) pairs in the tree
        """
        result = []
        self._inorder_helper(self.root, result)
        result.sort(key=lambda x: x[1])
        return result

    def _inorder_helper(self, node, result):
        """
        Recursive helper method for inorder traversal.
        Args:
            node: The current node in the recursion
            result: The list to store the traversal result
        """
        if node != self.NIL:
            self._inorder_helper(node.left, result)
            result.append((node.key, node.value))
            self._inorder_helper(node.right, result)
            
class MinHeap:
    #Implements minHeap data structure
    def __init__(self):
        #Initialise an empty min heap
        self.heap = []

    def insert(self, item):
        """
        Insert a new item into the heap.
        Args:
            item: The item to be inserted
        """
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def extract_min(self):
        #Remove and return the minimum element from the heap.
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return min_val

    def _sift_up(self, i):
        # Restore the heap property by moving an element up the heap.
        #Args: i: The index of the element to sift up
        parent = (i - 1) // 2
        if i > 0 and self.heap[i] < self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            self._sift_up(parent)

    def _sift_down(self, i):
        #Restore the heap property by moving an element down the heap.
        #i: The index of the element to sift down
        min_index = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(self.heap) and self.heap[left] < self.heap[min_index]:
            min_index = left
        if right < len(self.heap) and self.heap[right] < self.heap[min_index]:
            min_index = right
        if i != min_index:
            self.heap[i], self.heap[min_index] = self.heap[min_index], self.heap[i]
            self._sift_down(min_index)

    def __len__(self):
        #Return the number of elements in the heap.
        return len(self.heap)

class MaxHeap:
    # Implements a max heap data structure.
    def __init__(self):
        #Initialise an empty max heap
        self.heap = []

    def parent(self, i):
        # Return the parent index of a given index.
        return (i - 1) // 2

    def left_child(self, i):
        # Return the left child index of a given index.
        return 2 * i + 1

    def right_child(self, i):
        # Return the right child index of a given index.
        return 2 * i + 2

    def swap(self, i, j):
        #Swap two elements in the heap.
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, item):
        # Insert a new item into the heap.
        # Args: item: The item to be inserted
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self):
        """
        Remove and return the maximum element from the heap.
        Returns the maximum element, or None if the heap is empty
        """
        if not self.heap:
            return None
        max_element = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._sift_down(0)  # Corrected method call
        return max_element

    def _sift_up(self, i):
        # Restore the heap property by moving an element up the heap.
        parent = self.parent(i)
        if i > 0 and self._compare(self.heap[i], self.heap[parent]) > 0:
            self.swap(i, parent)
            self._sift_up(parent)

    def _sift_down(self, i):
        # Restore the heap property by moving an element down the heap.
        max_index = i
        left = self.left_child(i)
        right = self.right_child(i)
        if left < len(self.heap) and self._compare(self.heap[left], self.heap[max_index]) > 0:
            max_index = left
        if right < len(self.heap) and self._compare(self.heap[right], self.heap[max_index]) > 0:
            max_index = right
        if i != max_index:
            self.swap(i, max_index)
            self._sift_down(max_index)

    def _compare(self, a, b):
        """
        Compare two elements in the heap.
        Args:
            a, b: The elements to compare
        Returns a positive value if a > b, negative if a < b, and 0 if equal
        """
        if a[0] != b[0]:  # Compare priorities
            return a[0] - b[0]
        return b[1] - a[1]  # If priorities are equal, compare timestamps (earlier timestamp has higher priority)

    def remove(self, value, key_index=0):
        #Remove a specific value from the heap.
            for i, item in enumerate(self.heap):
                if item[key_index] == value:
                    last_item = self.heap.pop()
                    if i < len(self.heap):
                        self.heap[i] = last_item
                        self._sift_up(i)
                        self._sift_down(i)
                    return True
            return False

    def __len__(self):
        # Return the number of elements in the heap.
        return len(self.heap)


class GatorTicketMaster:
    
    def __init__(self):
        """Initialize the GatorTicketMaster system with empty data structures."""
        self.available_seats = MinHeap()
        self.waitlist = MaxHeap()
        self.reservations = RedBlackTree()
        self.last_seat_number = 0

    def initialize(self, seat_count):
        """
        Initialize the system with a given number of seats.
        Args:
            seat_count (int): Number of seats to initialize
        Returns: str: Confirmation message
        """
        if seat_count <= 0:
            return "Invalid input. Please provide a valid number of seats."
        for i in range(1, seat_count + 1):
            self.available_seats.insert(i)
        self.last_seat_number = seat_count
        return f"{seat_count} Seats are made available for reservation"

    def available(self):
        """
        Report the number of available seats and waitlist size.
        Returns:  str: Status message
        """
        available_count = len(self.available_seats)
        waitlist_count = len(self.waitlist)
        return f"Total Seats Available : {available_count}, Waitlist : {waitlist_count}"
    
    def reserve(self, user_id, user_priority):
        """
        Reserve a seat for a user or add them to the waitlist.
        Args:
            user_id : User ID
            user_priority : User priority
        Returns: str: Confirmation message
        """
        if not self.available_seats.heap:
            self.waitlist.insert((user_priority, time.time(), user_id))
            return f"User {user_id} is added to the waiting list"
        else:
            seat_id = self.available_seats.extract_min()
            self.reservations.insert(user_id, seat_id)
            return f"User {user_id} reserved seat {seat_id}"
    
    def cancel(self, seat_id, user_id):
        """
        Cancel a users reservation and reassign the seat if possible.
        Args:
            seat_id : Seat ID to cancel
            user_id : User ID cancelling the reservation
        Returns: str: Confirmation message
        """
        if not self.reservations.search(user_id):
            return f"User {user_id} has no reservation to cancel"
    
        reserved_seat = self.reservations.search(user_id)
        if reserved_seat != seat_id:
            return f"User {user_id} has no reservation for seat {seat_id}"
    
        self.reservations.delete(user_id)
    
        if self.waitlist.heap:
            next_user = self.waitlist.extract_max()
            self.reservations.insert(next_user[2], seat_id)
            return f"User {user_id} canceled their reservation\nUser {next_user[2]} reserved seat {seat_id}"
        else:
            self.available_seats.insert(seat_id)
            return f"User {user_id} canceled their reservation"

    def exit_waitlist(self, user_id):
        """
        Remove a user from the waitlist.
        Args:
            user_id: User ID to remove from waitlist
        Returns: str: Confirmation message
        """
        if self.waitlist.remove(user_id, key_index=2):
            return f"User {user_id} is removed from the waiting list"
        return f"User {user_id} is not in waitlist"

    def update_priority(self, user_id, user_priority):
        """
        Update a user's priority in the waitlist.
        Args:
            user_id : User ID to update
            user_priority : New priority
        Returns: str: Confirmation message
        """
        for i, item in enumerate(self.waitlist.heap):
            if item[2] == user_id:
                # Create a new tuple with updated priority but same timestamp and user_id
                updated_item = (user_priority, item[1], user_id)
                # Replace the old item with the updated one
                self.waitlist.heap[i] = updated_item
                # Restore the heap property
                self.waitlist._sift_up(i)
                self.waitlist._sift_down(i)
                return f"User {user_id} priority has been updated to {user_priority}"
        return f"User {user_id} priority is not updated"

    def add_seats(self, count):
        """
        Add new seats and assign them to waitlisted users if possible.
        Args:
            count : Number of seats to add
        Returns: str: Confirmation message
        """
        if count <= 0:
            return "Invalid input. Please provide a valid number of seats."
        
        new_seats = list(range(self.last_seat_number + 1, self.last_seat_number + count + 1))
        self.last_seat_number += count
        
        result = [f"Additional {count} Seats are made available for reservation"]
        
        if self.waitlist.heap:
            # Sort waitlist by priority (highest first), then by timestamp (earliest first)
            waitlist_users = sorted(self.waitlist.heap, key=lambda x: (-x[0], x[1]))
            
            while new_seats and waitlist_users:
                seat_id = min(new_seats)
                new_seats.remove(seat_id)
                user = waitlist_users.pop(0)
                self.reservations.insert(user[2], seat_id)
                result.append(f"User {user[2]} reserved seat {seat_id}")
                self.waitlist.remove(user[2], key_index=2)  # Remove user from the original waitlist
        
        # If there are still seats left, make them available
        for seat in new_seats:
            self.available_seats.insert(seat)
        
        return "\n".join(result)

    def print_reservations(self):
        """
        Get a list of all current reservations.
        Returns: list: List of reservation strings
        """
        reservations = self.reservations.inorder_traversal()
        return [f"[seat {seat}, user {user}]" for user, seat in reservations]

    def release_seats(self, user_id1, user_id2):
        """
        Release seats for a range of user IDs and reassign them if possible.
        Args:
            user_id1 : Start of user ID range
            user_id2 : End of user ID range
        Returns:
            str: Confirmation message
        """
        if user_id1 > user_id2:
            return "Invalid input. Please provide a valid range of users."
        
        released_seats = []
        released_users = []
        result = [f"Reservations of the Users in the range [{user_id1}, {user_id2}] are released"]
        
        for user_id in range(user_id1, user_id2 + 1):
            seat = self.reservations.search(user_id)
            if seat:
                self.reservations.delete(user_id)
                released_seats.append(seat)
                released_users.append(user_id)
            else:
                # Check if the user is in the waitlist
                for i, item in enumerate(self.waitlist.heap):
                    if item[2] == user_id:
                        self.waitlist.heap.pop(i)
                        break
        
        released_seats.sort()
        
        # If waitlist is not empty, assign seats to waitlisted users
        if self.waitlist.heap:
            # Sort waitlist by priority (highest first), then by timestamp (earliest first)
            waitlist_users = sorted(self.waitlist.heap, key=lambda x: (-x[0], x[1]))
            
            while released_seats and waitlist_users:
                lowest_seat = released_seats.pop(0)  # Get and remove the lowest seat
                highest_priority_user = waitlist_users.pop(0)  # Get and remove the highest priority user
                self.reservations.insert(highest_priority_user[2], lowest_seat)
                result.append(f"User {highest_priority_user[2]} reserved seat {lowest_seat}")
                self.waitlist.remove(highest_priority_user[2], key_index=2)  # Remove user from the original waitlist
        
        # If there are still seats left or waitlist was empty, make them available
        for seat in released_seats:
            self.available_seats.insert(seat)
        
        return "\n".join(result)

def process_input(input_file, output_file):
    """
    Process commands from an input file and write results to an output file.
    Args:
        input_file (str): Path to the input file containing commands
        output_file (str): Path to the output file for writing results
    """
    gator_tm = GatorTicketMaster()  # Create an instance of GatorTicketMaster
    with open(input_file, 'r') as f, open(output_file, 'w') as out:
        for line in f:
            # Parse the command and its arguments
            command = line.strip().split('(')
            func_name = command[0]
            args = command[1].rstrip(')').split(',') if len(command) > 1 else []
            # Execute the appropriate method based on the command
            if func_name == 'Initialize':
                result = gator_tm.initialize(int(args[0]))
            elif func_name == 'Available':
                result = gator_tm.available()
            elif func_name == 'Reserve':
                result = gator_tm.reserve(int(args[0]), int(args[1]))
            elif func_name == 'Cancel':
                result = gator_tm.cancel(int(args[0]), int(args[1]))
            elif func_name == 'PrintReservations':
                result = gator_tm.print_reservations()
            elif func_name == 'AddSeats':
                result = gator_tm.add_seats(int(args[0]))
            elif func_name == 'UpdatePriority':
                result = gator_tm.update_priority(int(args[0]), int(args[1]))
            elif func_name == 'ExitWaitlist':
                result = gator_tm.exit_waitlist(int(args[0]))
            elif func_name == 'ReleaseSeats':
                result = gator_tm.release_seats(int(args[0]), int(args[1]))
            elif func_name == 'Quit':
                out.write("Program Terminated!!\n")
                break
            else:
                result = "Unknown command"
            # Write the result to the output file
            if isinstance(result, list):
                out.write('\n'.join(result) + '\n')
            else:
                out.write(str(result) + '\n')

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python gatorTicketMaster.py <input_file>")
        sys.exit(1)
    # Get the input file name from command-line arguments
    input_file = sys.argv[1]
    # Generate the output file name based on the input file name
    output_file = input_file.split('.')[0] + "_output_file.txt"
     # Process the input file and generate the output
    process_input(input_file, output_file)


