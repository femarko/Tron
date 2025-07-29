import dotenv
import os


dotenv.load_dotenv()


def test_get_address_info(test_client, drop_create_all):
    response = test_client.post(url="https://127.0.0.1/address_info", json={"addr": os.getenv("ADDRESS")})
    json_result = response.json()
    assert response.status_code == 200
    assert isinstance(json_result["energy"], int)
    assert json_result["energy"] >= 0
    assert isinstance(json_result["bandwidth"], int)
    assert json_result["bandwidth"] >= 0
    assert isinstance(json_result["balance"], str)


def test_get_info_from_db(test_client, drop_create_all, insert_fake_data):
    response = test_client.get(url="https://127.0.0.1/get_info_from_db")
    json_result = response.json()
    assert response.status_code == 200
    assert isinstance(json_result["page"], int)
    assert json_result["page"] > 0
    assert isinstance(json_result["per_page"], int)
    assert json_result["per_page"] > 0
    assert isinstance(json_result["total"], int)
    assert json_result["total"] > 0
    assert isinstance(json_result["total_pages"], int)
    assert json_result["total_pages"] > 0
    assert isinstance(json_result["items"][0]["balance"], str)
    assert isinstance(json_result["items"][0]["energy"], int)
    assert json_result["items"][0]["energy"] >= 0
    assert isinstance(json_result["items"][0]["bandwidth"], int)
    assert json_result["items"][0]["bandwidth"] >= 0