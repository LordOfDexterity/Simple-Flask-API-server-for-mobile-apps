# from app import db
#
#
# # If you change model fields, you need to recreate the whole table.
# # Call "drop" method
# # https://your_url:port/ModelName/drop
#
#
# # class Sample(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     sample_column = db.Column(db.String(80), unique=True, nullable=False)
# #
# #     def __init__(self, **columns):
# #         self.sample_column = columns.get('sample_column')
# #
# #     def __repr__(self):
# #         return '<Shop %r>' % self.shop_name
#
#
# class Shop(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     shop_name = db.Column(db.String(80), unique=True, nullable=False)
#     shop_phone = db.Column(db.Integer, unique=True, nullable=False)
#     shop_pan_number = db.Column(db.String(80), unique=True, nullable=True)
#     shop_address = db.Column(db.String(120), unique=False, nullable=True)
#
#     def __init__(self, **columns):
#         self.shop_name = columns.get('shop_name')
#         self.shop_phone = columns.get('shop_phone')
#         self.shop_address = columns.get('shop_address')
#         self.shop_pan_number = columns.get('shop_pan_number')
#
#     def __repr__(self):
#         return '<Shop %r>' % self.shop_name
#
#     @staticmethod
#     def unique_columns():
#         return ['shop_name', 'shop_phone', 'shop_pan_number']
#
#     @staticmethod
#     def required_columns():
#         return ['shop_name', 'shop_phone']
#
#     @staticmethod
#     def is_valid(**columns):
#         valid_name = len(columns.get('shop_name', '')) <= 80
#         valid_phone = columns.get('shop_phone', '').isdigit()
#         valid_pan_number = len(columns.get('shop_pan_number', '')) <= 80
#         valid_address = len(columns.get('shop_address', '')) <= 120
#         if valid_name and valid_phone and valid_pan_number and valid_address:
#             return True
#         else:
#             return False
