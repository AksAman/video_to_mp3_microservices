import requests
import base64


username = "videotomp3_user"
password = "videotomp3_password"
email = "videotomp321@gmail.com"
basicAuth = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")

API_GATEWAY_ENDPOINT = "http://video-to-mp3.aksaman.com"
AUTH_ENDPOINT = "http://auth.video-to-mp3.aksaman.com"

LOGIN_ROUTE = "/auth/api/v1/login"
REGISTER_ROUTE = "/auth/api/v1/register"

UPLOAD_ROUTE = "/files/api/v1/upload"
DOWNLOAD_ROUTE = "/files/api/v1/download"


def register_user() -> bool:
    response = requests.post(
        url=f"{AUTH_ENDPOINT}{REGISTER_ROUTE}",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "email": email,
            "first_name": "videotomp3",
            "last_name": "videotomp3user",
            "username": username,
            "password": password,
            "is_admin": True,
        },
    )

    if not response.ok:
        print("Registration failed")
        print(response.text, response.status_code)
        return False

    print("Registration successful")
    return True


# STEP: 1
def get_token(retry=False):
    # step 1: login and get token
    response = requests.post(
        f"{API_GATEWAY_ENDPOINT}{LOGIN_ROUTE}",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {basicAuth}",
        },
    )

    if not response.ok:
        if response.status_code == 404 and not retry:
            print(f"User not found. Registering user {username}")
            success = register_user()
            if success:
                return get_token(retry=True)

        print("Login failed")
        print(response.text, response.status_code)
        return None

    token = response.json()["access"]
    print(f"Token: {token}")
    return token


# STEP: 2
def upload_file(token):
    files = {"file": open("test.mp4", "rb")}
    response = requests.post(
        f"{API_GATEWAY_ENDPOINT}{UPLOAD_ROUTE}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        files=files,
    )

    if not response.ok:
        print("Upload failed")
        print(response.text)
        return False

    print("Upload successful")
    print(response.json())
    return True


if __name__ == "__main__":
    token = get_token()
    if not token:
        print("Failed to get token")
        exit(1)
    success = upload_file(token)
    if not success:
        print("Failed to upload file")
        exit(1)
