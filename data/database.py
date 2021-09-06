import traceback





class Database:
    def __init__(self):
        self.connected = False


    def connect(self):
        try:
            print("Connecting to database.")
            #num = 1/0
            self.connected = True
        except Exception as e:
            print(f"Error caught: {e}")
            print(traceback.format_exc())
            self.connected = False

    def insert(self):
        print("Inserting new item.")

    def delete(self, item):
        print("Deleting item.")

    def save(self):
        print("Saving all data.")

    def _close_connection(self):
        print("Closing connection.")

