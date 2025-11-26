import random
import math
from js import setTimeout, document

# 定数の宣言 --- (*1)
INTERVAL = 50  # ボールの移動間隔(ミリ秒)
PLAYER_W = 100  # プレイヤーのバーの幅
PLAYER_Y = 470  # プレイヤーのバーのY座標
PLAYER_MOVE = 30  # プレイヤーのバーの移動量
BALL_SPPED = 15  # ボールの移動速度
BALL_SIZE = 15  # ボールの大きさ
BLOCK_W = 50  # ブロックの幅
BLOCK_H = 20  # ブロックの高さ
COLS = 400 // BLOCK_W  # ブロックの列数
ROWS = 8  # ブロックの行数
BLOCK_COLORS = [  # ブロックの色のリスト
    "white", "red", "orange", "magenta", "pink",
    "cyan", "lime", "green", "blue"]

# ゲーム内で利用するグローバル変数 --- (*2)
info = document.getElementById("info")  # 情報表示用の要素を取得
canvas = document.getElementById("canvas")  # キャンバスを取得
context = canvas.getContext("2d")  # 2D描画コンテキストを取得
blocks = []  # ブロックの配置を保持する2次元配列
game = {"game_over": True}  # ゲームの状態を保持する辞書

def init_game():
    """ゲームの初期化"""  # --- (*3)
    global blocks, game
    # ブロックの初期配置 --- (*4)
    blocks = [[(y+1)] * COLS for y in range(ROWS)]
    # ゲームの初期化 --- (*5)
    px = (canvas.width - PLAYER_W) // 2  # プレイヤーのX座標
    game = {
        "score": 0,  # スコア
        "px": px,  # プレイヤーのX座標
        "ball_x": (px + PLAYER_W // 2),  # ボールのX座標
        "ball_y": PLAYER_Y,  # ボールのY座標
        "ball_dir": 225 + random.randint(0, 90),  # ボールの移動方向
        "game_over": False,  # ゲームオーバーかどうか
    }
    game_loop()  # ゲームループを開始

def game_loop():
    """ゲームのメインループ"""  # --- (*6)
    update_ball()  # ボールの位置を更新
    draw_screen()  # 画面を更新
    # ゲームオーバーでなければ次のループをセット
    if not game["game_over"]:
        setTimeout(game_loop, INTERVAL)

def ball_turn_angle(angele, range):
    """ボールの角度をangleだけ変化させる"""  # --- (*7)
    r = random.randint(-range, range)
    game["ball_dir"] = (game["ball_dir"] + angele + r) % 360

def update_ball():
    """ボールの位置を更新"""  # --- (*8)
    rad = game["ball_dir"] * 3.14 / 180  # 角度をラジアンに変換
    dx = int(BALL_SPPED * math.cos(rad))  # X方向の移動量
    dy = int(BALL_SPPED * math.sin(rad))  # Y方向の移動量
    bx = game["ball_x"] + dx  # ボールのX座標を更新
    by = game["ball_y"] + dy  # ボールのY座標を更新
    # プレイヤーのバーとの当たり判定 --- (*9)
    px = game["px"]  # プレイヤーのX座標
    if (by >= PLAYER_Y) and (px <= bx < (px + PLAYER_W)):
        game["ball_dir"] = 225 + random.randint(0, 90)
    # 壁に当たったか --- (*10)
    elif (bx < 0) or (bx >= canvas.width) or (by <= 0):
        ball_turn_angle(90, 10)  # ボール方向を変更
    # ブロックに当たったか？ --- (*11)
    elif check_blocks(bx, by):
        ball_turn_angle(180, 20)  # ボール方向を変更
        game["score"] += 1  # スコアを加算
        # すべてのブロックを壊したらゲームクリア --- (*12)
        if game["score"] >= COLS * ROWS:
            game_over("すごい⭐ クリアしました")
    # 穴に落ちたらゲームオーバー --- (*13)
    elif by > (canvas.height - BALL_SIZE):
        game_over("残念😢 ゲームオーバー")
    # ボール座標を記録
    game["ball_x"] = bx; game["ball_y"] = by

def check_blocks(bx, by):
    """ボールがブロックに当たったか確認"""  # --- (*14)
    block_x, block_y = bx // BLOCK_W, by // BLOCK_H
    if 0 <= block_x < COLS and 0 <= block_y < ROWS:
        if blocks[block_y][block_x] != 0:  # ブロックが存在する？
            blocks[block_y][block_x] = 0  # ブロックを消す
            return True
    return False

def game_over(msg):
    """ゲームオーバーの処理"""  # --- (*15)
    # スタートボタンを有効化
    document.getElementById("start_button").disabled = False
    # ゲームオーバーとスコアを表示
    info.innerText = f"{msg} スコア: {game['score']}"
    game["game_over"] = True
