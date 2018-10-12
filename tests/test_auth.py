from tests import Base


class TestAuth(Base):
    """
    This class handles testing authentication.
    """

    def test_user_redirect(self):
        """
        Tests: '/google/redirect' endpoint
        """
        res = self.client.get("/google/redirect?type=register")
        self.assertTrue(200 <= res.status_code < 300)

        res = self.client.get("/google/redirect?type=login")
        self.assertTrue(200 <= res.status_code < 300)

        res = self.client.get("/google/redirect")
        self.assertTrue(res.status_code >= 400)
