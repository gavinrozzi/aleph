from aleph.core import db


class Cache(db.Model):
    """Store OCR computation results."""
    __tablename__ = 'cache'

    id = db.Column(db.BigInteger, primary_key=True)
    key = db.Column(db.Unicode, index=True)
    value = db.Column(db.Unicode)

    @classmethod
    def get_cache(cls, key):
        q = db.session.query(cls.value)
        q = q.filter_by(key=key)
        cobj = q.first()
        value = cobj.value if cobj is not None else None
        return value

    @classmethod
    def set_cache(cls, key, value):
        q = db.session.query(cls)
        q = q.filter_by(key=key)
        cobj = q.first()
        if cobj is None:
            cobj = cls()
            cobj.key = key
        cobj.value = value
        db.session.add(cobj)
