"""MySQL dialect tests."""
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from sqlalchemygrate.migrations import migrate

from .conftest import Address, Person, Base


@pytest.fixture
def engine1():
    """Source engine."""
    engine = create_engine('sqlite:///')
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def session1(engine1):
    """Source session."""
    return sessionmaker(bind=engine1)()


@pytest.fixture(scope='session')
def mysql_connection_with_database(run_services, mysql_socket, mysql_database_name):
    """The connection string to the local mysql instance."""
    if run_services:
        return 'mysql://root@localhost/{0}?unix_socket={1}&charset=utf8'.format(
            mysql_database_name, mysql_socket)


@pytest.fixture(params=['sqlite', 'mysql'])
def engine2(request):
    """Target engine."""
    if request.param == 'mysql':
        connection_string = request.getfuncargvalue('mysql_connection_with_database')
        request.getfuncargvalue('mysql_database')
    else:
        connection_string = 'sqlite:///'
    engine = create_engine(connection_string)
    if request.param == 'sqlite':
        engine.execute('PRAGMA foreign_keys = ON')
    return engine


@pytest.fixture
def session2(engine2):
    """Target session."""
    return sessionmaker(bind=engine2)()


@pytest.mark.parametrize('disable_foreign_keys', [True, False])
def test_disable_foreign_keys(engine1, engine2, session1, session2, disable_foreign_keys):
    """Test disable foreign key checks."""
    session1.add(Address(person=Person(name='Person'), post_code='12323'))
    session1.commit()
    session1.execute('PRAGMA foreign_keys = OFF')
    session1.execute('delete from person')
    session1.commit()

    if disable_foreign_keys:
        migrate(engine1, engine2, metadata=Base.metadata, disable_foreign_keys=disable_foreign_keys)
        address = session2.query(Address).one()
        assert address.post_code == '12323'
        assert address.person is None
        assert not session2.query(Person).count()
    else:
        with pytest.raises(IntegrityError):
            migrate(engine1, engine2, metadata=Base.metadata, disable_foreign_keys=disable_foreign_keys)
