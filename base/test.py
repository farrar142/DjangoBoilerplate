import json
from typing import Any
from django.test import testcases
from django.test import client
from django.contrib.auth import get_user_model


class Client(client.Client):
    def post(
        self,
        path,
        data=None,
        format=None,
        content_type='application/json',
        **extra,
    ):
        if content_type == 'application/json':
            data = json.dumps(data)
        return super(client.Client, self).post(
            path, data, content_type, **extra
        )

    def patch(
        self,
        path,
        data=None,
        content_type='application/json',
        **extra,
    ):
        if content_type == 'application/json':
            data = json.dumps(data)
        return super(client.Client, self).patch(
            path,
            data,
            content_type,
            **extra,
        )

    def delete(
        self,
        path,
        data=None,
        content_type='application/json',
        **extra,
    ):
        if content_type == 'application/json':
            data = json.dumps(data)
        return super(client.Client, self).delete(
            path,
            data,
            content_type,
            **extra,
        )


class TestCase(testcases.TestCase):
    client_class = Client
    user: Any

    def setUp(self) -> None:
        super().setUp()
        User = get_user_model()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@contoso.net'
        )


class TestSetUpTestCase(TestCase):
    def test_test_case(self):
        self.assertEqual(True, True)
        resp = self.client.get("/api/test")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), "true")
        self.assertNotEqual(resp.json(), "false")
