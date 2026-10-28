import random
import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle


# ==========================================
# 바카라 카드 한 장씩 공개 시뮬레이터
# ==========================================

def create_deck():
    deck = []

    # 8덱
    for _ in range(8):
        for _ in range(4):
            for rank in range(1, 14):
                value = rank if rank <= 9 else 0
                deck.append(value)

    return deck


def hand_total(cards):
    return sum(cards) % 10


def card_name(value):
    if value == 0:
        return "10/J/Q/K"
    elif value == 1:
        return "A"
    else:
        return str(value)


def card_html(value):
    return f"""
    <span style="
        display:inline-flex;
        justify-content:center;
        align-items:center;
        width:70px;
        height:95px;
        margin:5px;
        border-radius:10px;
        background:white;
        color:black;
        font-size:18px;
        font-weight:bold;
        box-shadow:0 3px 8px #0006;
    ">
        {card_name(value)}
    </span>
    """


# ==========================================
# 바카라 한 판 만들기
# ==========================================

def make_round():

    deck = create_deck()
    random.shuffle(deck)

    # 처음 4장
    p1 = deck.pop()
    b1 = deck.pop()
    p2 = deck.pop()
    b2 = deck.pop()

    player = [p1, p2]
    banker = [b1, b2]

    player_total = hand_total(player)
    banker_total = hand_total(banker)

    reveal_order = [
        ("PLAYER", p1),
        ("BANKER", b1),
        ("PLAYER", p2),
        ("BANKER", b2)
    ]

    # 자연승
    if player_total >= 8 or banker_total >= 8:
        return player, banker, reveal_order

    # ======================================
    # PLAYER 세 번째 카드
    # ======================================

    if player_total <= 5:
        p3 = deck.pop()
        player.append(p3)
        reveal_order.append(("PLAYER", p3))

    player_total = hand_total(player)

    # ======================================
    # BANKER 세 번째 카드
    # ======================================

    if banker_total <= 2:

        b3 = deck.pop()
        banker.append(b3)
        reveal_order.append(("BANKER", b3))

    elif banker_total == 3:

        if len(player) == 2 or player[2] != 8:
            b3 = deck.pop()
            banker.append(b3)
            reveal_order.append(("BANKER", b3))

    elif banker_total == 4:

        if len(player) == 2 or 2 <= player[2] <= 7:
            b3 = deck.pop()
            banker.append(b3)
            reveal_order.append(("BANKER", b3))

    elif banker_total == 5:

        if len(player) == 2 or 4 <= player[2] <= 7:
            b3 = deck.pop()
            banker.append(b3)
            reveal_order.append(("BANKER", b3))

    elif banker_total == 6:

        if len(player) == 3 and player[2] in [6, 7]:
            b3 = deck.pop()
            banker.append(b3)
            reveal_order.append(("BANKER", b3))

    return player, banker, reveal_order


# ==========================================
# 통계
# ==========================================

stats = {
    "PLAYER": 0,
    "BANKER": 0,
    "TIE": 0
}

total_games = 0

current_player = []
current_banker = []
current_order = []
reveal_index = 0
game_started = False


# ==========================================
# 버튼
# ==========================================

start_button = widgets.Button(
    description="🃏 한 판 시작",
    button_style="primary",
    layout=widgets.Layout(
        width="180px",
        height="55px"
    )
)

reveal_button = widgets.Button(
    description="🎴 카드 공개",
    button_style="warning",
    layout=widgets.Layout(
        width="180px",
        height="55px"
    )
)

reset_button = widgets.Button(
    description="🔄 초기화",
    layout=widgets.Layout(
        width="150px",
        height="55px"
    )
)

output = widgets.Output()


# ==========================================
# 테이블 표시
# ==========================================

def show_table(message=""):

    player_cards = "".join(
        card_html(c) for c in current_player
    )

    banker_cards = "".join(
        card_html(c) for c in current_banker
    )

    player_score = (
        hand_total(current_player)
        if current_player else "-"
    )

    banker_score = (
        hand_total(current_banker)
        if current_banker else "-"
    )

    html = f"""
    <div style="
        background:#126b3a;
        padding:25px;
        border-radius:20px;
        color:white;
        width:720px;
        text-align:center;
    ">

        <h2>{message}</h2>

        <div style="
            background:#0e5830;
            padding:15px;
            margin:10px;
            border-radius:15px;
        ">

            <h2>🔵 PLAYER</h2>

            <div>
                {player_cards if player_cards else "카드 대기 중"}
            </div>

            <h3>점수 : {player_score}</h3>

        </div>

        <div style="
            background:#0e5830;
            padding:15px;
            margin:10px;
            border-radius:15px;
        ">

            <h2>🔴 BANKER</h2>

            <div>
                {banker_cards if banker_cards else "카드 대기 중"}
            </div>

            <h3>점수 : {banker_score}</h3>

        </div>

    </div>
    """

    display(widgets.HTML(html))


# ==========================================
# 누적 통계
# ==========================================

def show_stats():

    print()
    print("=" * 55)
    print("📊 누적 결과")
    print("=" * 55)

    for name, emoji in [
        ("PLAYER", "🔵"),
        ("BANKER", "🔴"),
        ("TIE", "🟡")
    ]:

        count = stats[name]

        if total_games > 0:
            percent = count / total_games * 100
        else:
            percent = 0

        print(
            f"{emoji} {name:<7} : "
            f"{count:>5}회 "
            f"({percent:6.2f}%)"
        )

    print("-" * 55)
    print(f"총 판수 : {total_games:,}판")


# ==========================================
# ⭐ 최종 결과를 실제 이미지로 만들기
# ==========================================

def show_result_image(result, pt, bt):

    # 결과별 설정
    if result == "PLAYER":
        title = "PLAYER"
        emoji = "🔵"
        main_color = "#1976D2"

    elif result == "BANKER":
        title = "BANKER"
        emoji = "🔴"
        main_color = "#D32F2F"

    else:
        title = "TIE"
        emoji = "🟡"
        main_color = "#F9A825"


    # 이미지 생성
    fig, ax = plt.subplots(
        figsize=(10, 5.5),
        dpi=120
    )

    # 전체 배경
    fig.patch.set_facecolor("#101820")

    ax.set_facecolor("#101820")

    # 결과 카드
    card = FancyBboxPatch(
        (0.08, 0.08),
        0.84,
        0.84,
        boxstyle="round,pad=0.025,rounding_size=0.05",
        facecolor=main_color,
        edgecolor="white",
        linewidth=4
    )

    ax.add_patch(card)


    # 위쪽 작은 글씨
    ax.text(
        0.5,
        0.82,
        "BACCARAT RESULT",
        ha="center",
        va="center",
        fontsize=17,
        color="white",
        weight="bold"
    )


    # 결과 이모지
    ax.text(
        0.5,
        0.62,
        emoji,
        ha="center",
        va="center",
        fontsize=48
    )


    # 결과
    ax.text(
        0.5,
        0.45,
        title,
        ha="center",
        va="center",
        fontsize=40,
        color="white",
        weight="bold"
    )


    # 점수
    ax.text(
        0.5,
        0.25,
        f"PLAYER  {pt}   VS   {bt}  BANKER",
        ha="center",
        va="center",
        fontsize=18,
        color="white",
        weight="bold"
    )


    # 축 제거
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    plt.tight_layout()

    # 이미지 출력
    display(fig)

    plt.close(fig)


# ==========================================
# 한 판 시작
# ==========================================

def start_game(b):

    global current_player
    global current_banker
    global current_order
    global reveal_index
    global game_started

    if game_started:
        return

    # 새 판 생성
    current_player, current_banker, current_order = make_round()

    # 실제 공개용 배열은 비워둠
    final_player = current_player
    final_banker = current_banker

    # 최종 카드 정보를 따로 저장
    current_player = []
    current_banker = []

    # 최종 카드 저장
    global hidden_player
    global hidden_banker

    hidden_player = final_player
    hidden_banker = final_banker

    reveal_index = 0
    game_started = True

    with output:

        clear_output(wait=True)

        print(f"🃏 {total_games + 1}번째 판")
        print()

        show_table(
            "🎴 카드를 한 장씩 공개하세요"
        )

        show_stats()

    start_button.disabled = True
    reveal_button.disabled = False


# ==========================================
# 카드 한 장 공개
# ==========================================

def reveal_card(b):

    global reveal_index
    global game_started
    global total_games

    if not game_started:
        return


    # ======================================
    # 아직 공개할 카드가 있는 경우
    # ======================================

    if reveal_index < len(current_order):

        side, card = current_order[reveal_index]


        if side == "PLAYER":

            current_player.append(card)

            message = (
                f"🎴 PLAYER 카드 공개 → "
                f"{card_name(card)}"
            )

        else:

            current_banker.append(card)

            message = (
                f"🎴 BANKER 카드 공개 → "
                f"{card_name(card)}"
            )


        reveal_index += 1


        with output:

            clear_output(wait=True)

            print(
                f"🃏 {total_games + 1}번째 판"
            )

            print()

            show_table(message)

            show_stats()


        # 모든 카드 공개 완료
        if reveal_index >= len(current_order):

            reveal_button.description = (
                "🏆 결과 확인"
            )

            reveal_button.button_style = (
                "success"
            )


    # ======================================
    # 모든 카드 공개 후 결과 확인
    # ======================================

    else:

        pt = hand_total(current_player)
        bt = hand_total(current_banker)


        if pt > bt:

            result = "PLAYER"

        elif bt > pt:

            result = "BANKER"

        else:

            result = "TIE"


        # 통계 기록
        stats[result] += 1
        total_games += 1

        game_started = False


        with output:

            clear_output(wait=True)

            # ⭐ 여기서 실제 이미지 생성
            show_result_image(
                result,
                pt,
                bt
            )

            print()

            show_stats()


        # 버튼 상태
        start_button.disabled = False

        reveal_button.disabled = True

        reveal_button.description = (
            "🎴 카드 공개"
        )

        reveal_button.button_style = (
            "warning"
        )


# ==========================================
# 초기화
# ==========================================

def reset_game(b):

    global current_player
    global current_banker
    global current_order
    global reveal_index
    global game_started
    global total_games

    stats["PLAYER"] = 0
    stats["BANKER"] = 0
    stats["TIE"] = 0

    total_games = 0

    current_player = []
    current_banker = []
    current_order = []

    reveal_index = 0
    game_started = False

    start_button.disabled = False

    reveal_button.disabled = True

    reveal_button.description = (
        "🎴 카드 공개"
    )

    reveal_button.button_style = (
        "warning"
    )


    with output:

        clear_output(wait=True)

        print("🔄 초기화 완료")
        print()
        print("🃏 '한 판 시작'을 눌러주세요.")


# ==========================================
# 버튼 연결
# ==========================================

start_button.on_click(start_game)

reveal_button.on_click(reveal_card)

reset_button.on_click(reset_game)


# ==========================================
# 실행
# ==========================================

display(widgets.HTML("""
<h1>🃏 바카라 시뮬레이터</h1>

<p style="font-size:17px;">
<b>한 판 시작</b>
→
<b>카드 공개</b>를 누를 때마다
한 장씩 공개
</p>
"""))


display(
    widgets.HBox([
        start_button,
        reveal_button,
        reset_button
    ])
)


display(output)


with output:

    print("🃏 '한 판 시작'을 눌러주세요.")
