import requests
import base64


username = "test_username"
password = "test_password"
basicAuth = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")

API_GATEWAY_ENDPOINT = "http://video-to-mp3.aksaman.com"

LOGIN_ROUTE = "/auth/api/v1/login"
UPLOAD_ROUTE = "/files/api/v1/upload"
DOWNLOAD_ROUTE = "/files/api/v1/download"


# STEP: 1
def get_token():
    # step 1: login and get token
    response = requests.post(
        f"{API_GATEWAY_ENDPOINT}{LOGIN_ROUTE}",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {basicAuth}",
        },
    )

    if not response.ok:
        print("Login failed")
        print(response.text)
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
