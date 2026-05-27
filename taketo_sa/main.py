import json
import os
import sys
from datetime import datetime

# --- データの準備 ---
# 商品データ
PRODUCTS = [
    {"id": 1, "name": "リンゴ", "price": 150},
    {"id": 2, "name": "バナナ", "price": 100},
    {"id": 3, "name": "オレンジ", "price": 120},
]
ORDERS_FILE = "orders.json"


def load_orders():
    """注文履歴をファイルから読み込む"""
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_order(new_order):
    """新しい注文をファイルに保存する"""
    orders = load_orders()
    orders.append(new_order)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


# ==========================================
# 各画面の処理
# ==========================================


def show_products():
    """2. 商品一覧画面"""
    print("\n--- 商品一覧 ---")
    for p in PRODUCTS:
        print(f"ID: {p['id']} | {p['name']} - {p['price']}円")
    print("----------------")


def create_order():
    """3 & 4. 注文入力・確認画面"""
    show_products()

    # --- 商品IDの入力とエラーチェック ---
    product_id_input = input("購入したい商品のIDを入力してください: ")
    if not product_id_input.isdigit():
        print("【エラー】数字を入力してください。")
        return
    product_id = int(product_id_input)

    # 該当する商品を探す
    product = None
    for p in PRODUCTS:
        if p["id"] == product_id:
            product = p
            break

    if product is None:
        print("【エラー】その商品IDは見つかりません。")
        return

    # --- 数量の入力とエラーチェック ---
    quantity_input = input(f"「{product['name']}」の数量を入力してください: ")
    if not quantity_input.isdigit():
        print("【エラー】正しい数量（数字）を入力してください。")
        return
    quantity = int(quantity_input)
    if quantity <= 0:
        print("【エラー】数量は1以上にしてください。")
        return

    # 合計金額の計算
    total_price = product["price"] * quantity

    # --- 4. 注文確認画面 ---
    print("\n=== 注文内容の確認 ===")
    print(f"商品名: {product['name']}")
    print(f"数量  : {quantity}個")
    print(f"合計金額: {total_price}円")
    print("======================")

    confirm = input("この注文を確定しますか？ (y/n): ")
    if confirm.lower() == "y":
        # データの保存
        new_order = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "product_name": product["name"],
            "quantity": quantity,
            "total_price": total_price,
        }
        save_order(new_order)
        print("✅ 注文を確定しました！")
    else:
        print("❌ 注文をキャンセルしました。")


def show_history():
    """5. 注文履歴画面"""
    orders = load_orders()
    print("\n--- 注文履歴 ---")
    if not orders:
        print("過去の注文履歴はありません。")
    else:
        for i, o in enumerate(orders, 1):
            print(
                f"[{i}] {o['date']} | {o['product_name']} × {o['quantity']}個 = {o['total_price']}円"
            )
    print("----------------")


# ==========================================
# 1. メニュー画面（メインループ）
# ==========================================
def main():
    while True:
        print("\n=== メニュー ===")
        print("1. 商品一覧を表示")
        print("2. 商品を注文")
        print("3. 注文履歴を表示")
        print("4. 終了")
        print("================")

        choice = input("番号を選んでください (1-4): ")

        if choice == "1":
            show_products()
        elif choice == "2":
            create_order()
        elif choice == "3":
            show_history()
        elif choice == "4":
            print("アプリを終了します。ありがとうございました！")
            sys.exit()
        else:
            print("【エラー】1から4の数字を選んでください。")


if __name__ == "__main__":
    main()
