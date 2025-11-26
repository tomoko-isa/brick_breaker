def start_button_on_click(event):
    """ゲーム開始ボタンがクリックされたときの処理"""  # --- (*1)
    # スタートボタンを無効化
    document.getElementById("start_button").disabled = True
    init_game()  # ゲームを初期化

def player_move(dx):
    """プレイヤーのバーを移動"""  # -- (*2)
    if game["game_over"]:
        return  # ゲームオーバーなら何もしない
    px = game["px"] + dx  # プレイヤーのバーを移動
    if 0 <= px <= canvas.width - PLAYER_W:
        game["px"] = px
    draw_screen()  # 画面を更新

def right_button_on_click(event):
    """右ボタンがクリックされたときの処理"""  # --- (*3)
    player_move(PLAYER_MOVE)

def left_button_on_click(event):
    """左ボタンがクリックされたときの処理"""  # --- (*4)
    player_move(-1 * PLAYER_MOVE)

def key_down(event):
    """キーが押されたときの処理"""  # --- (*5)
    if event.key == "ArrowLeft":  # ←キー
        left_button_on_click(event)
    elif event.key == "ArrowRight":  # →キー
        right_button_on_click(event)

# キーイベントを登録 --- (*6)
document.addEventListener("keydown", key_down)
