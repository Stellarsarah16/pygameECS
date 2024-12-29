class Item:
    def __init__(self, id, amount):
        self.item_id = id
        self.amount = amount

    def copy(self, new_amount=None):
        if new_amount is None:
            new_amount = self.amount
        return Item(self.item_id, new_amount)
    
    