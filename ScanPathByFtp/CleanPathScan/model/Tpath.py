from CleanPathScan import db

class Tpath(db.Model):
    __tablename__ = 'TPath'
    id = db.Column(db.Integer,primary_key=True)
    scode = db.Column(db.String(50))
    pcode = db.Column(db.String(50))
    path = db.Column(db.String(500))
    isFolder = db.Column(db.Integer)
    size = db.Column(db.BigInteger)
    batch = db.Column(db.String(50))
    phoneSign = db.Column(db.String(50))

    def __init__(self,scode,pcode,path,isFolder,size,batch,phoneSign):
        self.scode  = scode
        self.pcode = pcode
        self.path = path
        self.isFolder = isFolder
        self.size = size
        self.batch = batch
        self.phoneSign = phoneSign

    def __repr__(self):
        return '<path %r>' % self.path