import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import open_db
from app.domain.merchants import create_merchant, create_user
from app.domain.products import upsert_product, stock_qty
from app.lib.dates import reset_clock

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    open_db(":memory:")
    reset_clock()

def test_pos_products_and_checkout():
    m_id = create_merchant({'name': 'Fashion Hub', 'phone': '01900000003'})
    u_id = create_user(m_id, {
        'name': 'Tamim Ahmed',
        'email': 'owner@demo.bd',
        'role': 'agency_owner',
        'password': 'password123'
    })

    # Initial product
    p_id = upsert_product(m_id, {
        'name': 'Cotton Polo Shirt',
        'sku': 'POLO-01',
        'selling_price': 150000, # ৳1500
        'purchase_price': 70000, # ৳700
        'stock_qty': 50,
    }, {'source': 'manual', 'actor': f'user:{u_id}'})

    # 1. Login
    login_res = client.post("/api/auth/login", json={'email': 'owner@demo.bd', 'password': 'password123'})
    assert login_res.status_code == 200

    # 2. Fetch active POS products
    res = client.get("/api/pos/products")
    assert res.status_code == 200
    data = res.json()
    assert "products" in data
    assert len(data["products"]) == 1
    assert data["products"][0]["name"] == "Cotton Polo Shirt"
    assert data["products"][0]["selling_price_bdt"] == 1500.0

    # 3. Complete in-store POS checkout
    payload = {
        "items": [
            {
                "product_id": p_id,
                "qty": 2,
                "unit_price": 1500.0
            }
        ],
        "customer_name": "Rahim Khan (In-Store)",
        "customer_phone": "01811223344",
        "discount": 100.0,
        "payment_method": "cash",
        "tendered": 3000.0,
        "note": "POS Counter 1 Sale"
    }

    checkout_res = client.post("/api/pos/checkout", json=payload)
    assert checkout_res.status_code == 200
    receipt = checkout_res.json()

    assert receipt["success"] is True
    assert "receipt_no" in receipt
    assert receipt["receipt_no"].startswith("POS-")
    assert receipt["customer_name"] == "Rahim Khan (In-Store)"
    assert receipt["items_count"] == 2
    assert receipt["subtotal"] == 3000.0
    assert receipt["discount"] == 100.0
    assert receipt["total"] == 2900.0
    assert receipt["tendered"] == 3000.0
    assert receipt["change"] == 100.0

    # 4. Verify real-time stock deduction
    assert stock_qty(p_id) == 48

    # 5. Verify order in POS orders history
    history_res = client.get("/api/pos/orders")
    assert history_res.status_code == 200
    history = history_res.json()
    assert len(history["orders"]) == 1
    assert history["orders"][0]["external_id"] == receipt["receipt_no"]
    assert history["orders"][0]["customer_name"] == "Rahim Khan (In-Store)"
    assert history["summary"]["today_orders_count"] == 1
    assert history["summary"]["today_revenue_bdt"] == 2900.0

def test_pos_pull_website_with_image_option():
    m_id = create_merchant({'name': 'Digital Retail Hub', 'phone': '01900000004'})
    u_id = create_user(m_id, {
        'name': 'Kashem Ali',
        'email': 'kashem@retail.bd',
        'role': 'agency_owner',
        'password': 'password123'
    })

    # 1. Login
    login_res = client.post("/api/auth/login", json={'email': 'kashem@retail.bd', 'password': 'password123'})
    assert login_res.status_code == 200

    # 2. Pull website inventory with import_images=True
    pull_res = client.post("/api/pos/pull-website", json={
        'platform': 'wordpress',
        'store_url': 'https://demo-woocommerce.local',
        'import_images': True,
    })
    assert pull_res.status_code == 200
    pull_data = pull_res.json()
    assert pull_data["ok"] is True
    assert pull_data["pulled_count"] > 0

    # 3. Verify POS products now have image_url
    pos_res = client.get("/api/pos/products")
    assert pos_res.status_code == 200
    prods = pos_res.json()["products"]
    assert len(prods) > 0
    # Verify products have an image URL
    prods_with_img = [p for p in prods if p.get("image_url")]
    assert len(prods_with_img) > 0
    assert prods_with_img[0]["image_url"].startswith("http")

    # 4. Update product image directly in POS
    target_pid = prods[0]["id"]
    new_img_url = "https://images.unsplash.com/photo-custom?w=400"
    patch_img_res = client.patch(f"/api/pos/products/{target_pid}/image", json={
        "image_url": new_img_url
    })
    assert patch_img_res.status_code == 200
    assert patch_img_res.json()["image_url"] == new_img_url

    # Check updated image in POS products list
    pos_res_after = client.get("/api/pos/products").json()["products"]
    updated_prod = next(p for p in pos_res_after if p["id"] == target_pid)
    assert updated_prod["image_url"] == new_img_url

    # 5. Pull website inventory with import_images=False (image option disabled)
    m2_id = create_merchant({'name': 'No Image Store', 'phone': '01900000005'})
    create_user(m2_id, {
        'name': 'Staff User',
        'email': 'staff@retail.bd',
        'role': 'agency_owner',
        'password': 'password123'
    })
    client.post("/api/auth/login", json={'email': 'staff@retail.bd', 'password': 'password123'})

    pull_no_img = client.post("/api/pos/pull-website", json={
        'platform': 'shopify',
        'store_url': 'https://demo-shopify.local',
        'import_images': False,
    })
    assert pull_no_img.status_code == 200
    no_img_prods = client.get("/api/pos/products").json()["products"]
    # All products pulled with import_images=False should have None as image_url
    for p in no_img_prods:
        assert p.get("image_url") is None
