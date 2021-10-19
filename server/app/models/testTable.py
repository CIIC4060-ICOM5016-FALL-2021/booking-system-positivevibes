# from ..main import db
#
# class testTable(db.Model):
#     __tablename__ = 'testTable'
#     testTitle = db.Column(db.String(100), primary_key=True)
#     testText = db.Column(db.String(), nullable=False)
#     testLikes = db.Column(db.String(), nullable=False, default=0)
#
#     def __init__(self, tTitle, tText, tLikes):
#         self.testTitle = tTitle
#         self.testText = tText
#         self.testLikes = tLikes