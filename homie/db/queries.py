from sqlmodel import select

from homie.db.models import PostalCode
from homie.db.session import db_session

    
@db_session
def get_or_create_postal_code(code: str, district: str | None = None, session=None) -> PostalCode:
    postal_code = session.exec(select(PostalCode).where(PostalCode.code == code)).first()
    if postal_code is None:
        postal_code = PostalCode(code=code, district=district)
        session.add(postal_code)
        session.commit()
        postal_code.refresh()
    return postal_code