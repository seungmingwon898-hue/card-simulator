
import streamlit as st
import random

st.set_page_config(
    page_title="카드 확률 시뮬레이터",
    page_icon="🃏",
    layout="centered"
)

st.title("🃏 카드 확률 시뮬레이터")
st.caption("카드를 한 장씩 공개하며 점수 변화를 확인하세요.")

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = [
    "A", "2", "3", "4", "5", "6", "7",
    "8", "9", "10", "J", "Q", "K"
]


def create_deck():
    deck = [
        {"suit": suit, "rank": rank}
        for suit in SUITS
        for rank in RANKS
    ]
    random.shuffle(deck)
    return deck


def score(cards):
    values = {
        "A": 1, "2": 2, "3": 3, "4": 4, "5": 5,
        "6": 6, "7": 7, "8": 8, "9": 9,
        "10": 0, "J": 0, "Q": 0, "K": 0
    }
    return sum(values[c["rank"]] for c in cards) % 10


def reset():
    st.session_state.deck = create_deck()
    st.session_state.player = []
    st.session_state.banker = []
    st.session_state.history = []
    st.session_state.reveal_index = 0
    st.session_state.done = False


if "deck" not in st.session_state:
    reset()


def reveal_next():
    if st.session_state.reveal_index >= 6:
        st.session_state.done = True
        return

    if not st.session_state.deck:
        st.session_state.done = True
        return

    # 공개 순서: 플레이어, 뱅커 번갈아 공개
    if st.session_state.reveal_index % 2 == 0:
        side = "player"
    else:
        side = "banker"

    card = st.session_state.deck.pop()
    st.session_state[side].append(card)
    st.session_state.history.append((side, card))
    st.session_state.reveal_index += 1

    if st.session_state.reveal_index >= 6:
        st.session_state.done = True


if st.button("🔄 새 게임", use_container_width=True):
    reset()
    st.rerun()


# 점수판
player_score = score(st.session_state.player)
banker_score = score(st.session_state.banker)

left, right = st.columns(2)

with left:
    st.subheader("🔵 플레이어")
    st.metric("현재 점수", player_score)

with right:
    st.subheader("🔴 뱅커")
    st.metric("현재 점수", banker_score)


# 카드 표시
st.divider()
left, right = st.columns(2)


def show_cards(title, cards):
    with st.container(border=True):
        st.markdown(f"### {title}")

        if not cards:
            st.caption("카드가 아직 공개되지 않았습니다.")
            return

        for card in cards:
            suit = card["suit"]
            rank = card["rank"]
            color = "#d62828" if suit in ["♥", "♦"] else "#222222"

            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:2px solid #dddddd;
                    border-radius:12px;
                    padding:12px;
                    margin:8px 0;
                    text-align:center;
                    color:{color};
                    font-size:28px;
                    font-weight:bold;
                ">{rank} {suit}</div>
                """,
                unsafe_allow_html=True
            )


with left:
    show_cards("플레이어 카드", st.session_state.player)

with right:
    show_cards("뱅커 카드", st.session_state.banker)


st.divider()

st.metric("남은 카드", len(st.session_state.deck))
st.progress(st.session_state.reveal_index / 6)

if not st.session_state.done:
    if st.button(
        "🃏 다음 카드 공개",
        type="primary",
        use_container_width=True
    ):
        reveal_next()
        st.rerun()
else:
    if player_score > banker_score:
        st.success("플레이어 점수가 더 높습니다.")
    elif banker_score > player_score:
        st.success("뱅커 점수가 더 높습니다.")
    else:
        st.info("두 점수가 같습니다.")

    st.caption("이 결과는 학습용 점수 비교이며 실제 바카라 규칙의 승패 판정은 아닙니다.")


with st.expander("공개 기록"):
    if st.session_state.history:
        for i, (side, card) in enumerate(
            st.session_state.history, start=1
        ):
            name = "플레이어" if side == "player" else "뱅커"
            st.write(f"{i}. {name}: {card['rank']}{card['suit']}")
    else:
        st.write("아직 공개된 카드가 없습니다.")
