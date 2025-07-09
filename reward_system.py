"""
Design a coupon and voucher managment.

Requirements were:
Admin will create coupons with rules(like match age>18 and cart_value>1000);
Coupons will have (averall uses limit / per ser limit ), expiry date , active/inactive etc.


Vouchers will be of type
Unassigned : anyone can use but only one uses
"PreAssigned": Voucher attached to user id


Was asked to design api too:
User will see list of coupons available and Vouchers;
Admin can delete/ create , activate or disable coupons etc.
"""
from datetime import datetime
from typing import List, Dict, Optional 

# Coupon Class
class Coupon:
    def __init__(
        self, 
        code: str, 
        discount: float, 
        usage_limit: int, 
        expiry_date: datetime, 
        is_active: bool
    ):
        self.code = code
        self.discount = discount
        self.expiry_date = expiry_date
        self.usage_limit = usage_limit
        self.usage_count = 0  # Total times the coupon is used
        self.is_active = is_active

    def is_valid(self):
        return self.is_active and self.usage_count < self.usage_limit and datetime.now() < self.expiry_date
    
    def apply(self, cart_value):
        if self.is_valid():
            self.usage_count += 1
            return cart_value - (cart_value * self.discount / 100)
        return None


class Voucher:
    def __init__(self, code, discount, expiry_date, voucher_type, user_id=None):
        self.code = code
        self.discount = discount
        self.expiry_date = expiry_date
        self.voucher_type = voucher_type
        self.user_id = user_id
        self.is_redeemed = False
    
    def is_valid(self, user_id):
        
        if self.is_redeemed or datetime.now() > self.expiry_date:
            return False
        if self.voucher_type == "PreAssigned" and self.user_id != user_id:
            return False
        return True
    
    def redeem(self, user_id, cart_value):
        if self.is_valid(user_id):
            self.is_redeemed = True
            return cart_value - self.discount
        return None
    

coupon = Coupon("SAVE10", 10, 5, datetime(2025, 2, 14), True)
cart_value = 1000
new_price = coupon.apply(cart_value)
if new_price:
    print(f"Coupon Applied! New Price: {new_price}")
else:
    print("Coupon Invalid or Expired!")

# Creating a pre-assigned voucher
preassigned_voucher = Voucher("VIP50", 50, datetime(2025, 2, 14), "PreAssigned", "user123")

# Trying to redeem with correct user
new_price = preassigned_voucher.redeem("user123", 500)
if new_price:
    print(f"Voucher Applied! New Price: {new_price}")
else:
    print("Voucher Invalid or Already Redeemed!")

# Trying to redeem with wrong user
new_price = preassigned_voucher.redeem("user999", 500)
print("Wrong User Voucher:", "Applied" if new_price else "Failed")