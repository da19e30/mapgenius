import os
import time
import json
import requests

BASE_URL = "http://localhost:8000/api/v1"

def print_result(step, success, message=""):
    status = "OK" if success else "FAIL"
    print(f"[{status}] {step}: {message}")

def main():
    # Generate unique email to avoid conflict
    unique_id = int(time.time())
    # 1. Register user
    register_data = {
        "username": f"testuser{unique_id}",
        "email": f"testuser{unique_id}@example.com",
        "password": "TestPass123!"
    }
    try:
        r = requests.post(f"{BASE_URL}/users/register", json=register_data)
        if r.status_code not in (200, 201):
            print_result("Register", False, f"Status {r.status_code}, {r.text}")
            return
        print_result("Register", True)
    except Exception as e:
        print_result("Register", False, str(e))
        return

    # 2. Login
    try:
        r = requests.post(f"{BASE_URL}/users/login", json={"email": register_data["email"], "password": register_data["password"]})
        if r.status_code != 200:
            print_result("Login", False, f"Status {r.status_code}, {r.text}")
            return
        token = r.json().get("access_token")
        if not token:
            print_result("Login", False, "No token returned")
            return
        headers = {"Authorization": f"Bearer {token}"}
        print_result("Login", True)
    except Exception as e:
        print_result("Login", False, str(e))
        return

    # 3. Get current user
    try:
        r = requests.get(f"{BASE_URL}/users/me", headers=headers)
        if r.status_code != 200:
            print_result("Get Me", False, f"Status {r.status_code}, {r.text}")
            return
        print_result("Get Me", True)
    except Exception as e:
        print_result("Get Me", False, str(e))
        return

    # 4. Create a simple PNG invoice file (1x1 pixel)
    import base64
    png_data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO6XKOcAAAAASUVORK5CYII="
    )
    invoice_path = os.path.join(os.getcwd(), "sample_invoice.png")
    with open(invoice_path, "wb") as f:
        f.write(png_data)

    # 5. Upload invoice
    try:
        with open(invoice_path, "rb") as f:
            files = {"file": ("sample_invoice.png", f, "image/png")}
            r = requests.post(f"{BASE_URL}/invoices/upload", headers=headers, files=files)
        if r.status_code != 200:
            print_result("Upload Invoice", False, f"Status {r.status_code}, {r.text}")
            return
        upload_resp = r.json()
        invoice_id = upload_resp.get("invoice_id")
        if not invoice_id:
            print_result("Upload Invoice", False, "No invoice_id returned")
            return
        print_result("Upload Invoice", True, f"ID {invoice_id}")
    except Exception as e:
        print_result("Upload Invoice", False, str(e))
        return

    # 6. List invoices
    try:
        r = requests.get(f"{BASE_URL}/invoices/list", headers=headers)
        if r.status_code != 200:
            print_result("List Invoices", False, f"Status {r.status_code}, {r.text}")
        else:
            print_result("List Invoices", True, f"Count {len(r.json())}")
    except Exception as e:
        print_result("List Invoices", False, str(e))

    # 7. Get specific invoice
    try:
        r = requests.get(f"{BASE_URL}/invoices/{invoice_id}", headers=headers)
        if r.status_code != 200:
            print_result("Get Invoice", False, f"Status {r.status_code}, {r.text}")
        else:
            print_result("Get Invoice", True)
    except Exception as e:
        print_result("Get Invoice", False, str(e))

    # 8. AI insights
    try:
        r = requests.get(f"{BASE_URL}/ai/insights", headers=headers)
        if r.status_code == 200:
            print_result("AI Insights", True)
        else:
            print_result("AI Insights", False, f"Status {r.status_code}, {r.text}")
    except Exception as e:
        print_result("AI Insights", False, str(e))

    # 9. AI predict
    try:
        r = requests.get(f"{BASE_URL}/ai/predict", headers=headers)
        if r.status_code == 200:
            print_result("AI Predict", True)
        else:
            print_result("AI Predict", False, f"Status {r.status_code}, {r.text}")
    except Exception as e:
        print_result("AI Predict", False, str(e))

    # 10. Financial data list
    try:
        r = requests.get(f"{BASE_URL}/financial-data/list", headers=headers)
        if r.status_code == 200:
            print_result("Financial Data List", True, f"Count {len(r.json())}")
        else:
            print_result("Financial Data List", False, f"Status {r.status_code}, {r.text}")
    except Exception as e:
        print_result("Financial Data List", False, str(e))

    # Cleanup sample file
    os.remove(invoice_path)

if __name__ == "__main__":
    main()
