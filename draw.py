def draw_screen():
    """画面を更新"""
    context.clearRect(0, 0, canvas.width, canvas.height)  # 画面をクリア
    # 背景画像を描画 --- (*1)
    back_image = document.getElementById("back_image")
    context.drawImage(back_image, 0, 0, canvas.width, canvas.height)
    # ブロックを描画 --- (*2)
    for y in range(ROWS):
        for x in range(COLS):
            if blocks[y][x] == 0:  # ブロックが存在しない場合
                continue
            # ブロックの位置とサイズを計算
            bx, by = x * BLOCK_W, y * BLOCK_H
            bw, bh = BLOCK_W - 1, BLOCK_H - 1
            base_color = BLOCK_COLORS[blocks[y][x]]
            # 上から下への線形グラデーション --- (*3)
            grad = context.createLinearGradient(bx, by, bx, by + bh)
            grad.addColorStop(0, "white")             # ハイライト
            grad.addColorStop(0.2, base_color)        # 本来の色
            grad.addColorStop(1, "rgba(0,0,0,0.6)")   # 影の濃淡
            context.fillStyle = grad
            context.fillRect(bx, by, bw, bh)
    # プレイヤーのバーを描画 --- (*4)
    bar_image = document.getElementById("bar_image")
    context.drawImage(bar_image, game["px"], PLAYER_Y, PLAYER_W, 40) 
    # ボールを描画 --- (*5)
    context.fillStyle = "white"  # ボールの色を設定
    context.strokeStyle = "black"  # ボールの周囲の色を設定
    context.beginPath()  # 新しいパスを開始
    context.arc(game["ball_x"], game["ball_y"],
                BALL_SIZE // 2, 0, 2 * math.pi)  # 円を描く
    context.fill()  # 円を塗りつぶす
    context.stroke()  # 円の周囲を描く
    # スコアを表示
    if not game["game_over"]:
        info.innerText = f"ブロック崩し スコア: {game['score']}点"
