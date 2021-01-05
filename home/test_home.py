from .views import index


def test_index(rf):
    request = rf.get("/")
    response = index(request)
    assert response.status_code == 200
    assert b"conduit" in response.content
    assert b"How to build webapps that scale" in response.content
    assert b"emberjs" in response.content
