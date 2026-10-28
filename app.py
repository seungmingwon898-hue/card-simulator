
import streamlit as st
import random

st.set_page_config(
    page_title="카드 공개 시뮬레이터",
    page_icon="🃏",
    layout="centered"
)

# 화면 디자인
st.title("🃏 카드 공개 시뮬레이터")
st.caption("버튼을 누를 때마다 카드가 한 장씩 공개됩니다.")

st.divider()

# 카드 덱 생성
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = [
    "A", "2", "3", "4", "5", "6", "7",
    "8", "9", "10", "J", "Q", "K"
]


def make_deck():
    return [
        {"suit": suit, "rank": rank}
        for suit in SUITS
        for rank in RANKS
    ]


def start_new_round():
    deck = make_deck()
    random.shuffle(deck)

    st.session_state.deck = deck
    st.session_state.opened_cards = []


# 최초 실행 시 초기화
if "deck" not in st.session_state:
    start_new_round()


# 카드 한 장 공개
def reveal_card():
    if st.session_state.deck:
        card = st.session_state.deck.pop()
        st.session_state.opened_cards.append(card)


# 새 게임 버튼
if st.button("🔄 새로 시작", use_container_width=True):
    start_new_round()
    st.rerun()


st.subheader("공개된 카드")

opened = st.session_state.opened_cards

# 처음에는 카드가 하나도 표시되지 않음
if len(opened) == 0:
    st.info("아직 공개된 카드가 없습니다. 아래 버튼을 눌러 시작하세요.")

else:
    # 공개된 카드만 화면에 표시
    columns = st.columns(4)

    for index, card in enumerate(opened):
        with columns[index % 4]:
            suit = card["suit"]
            rank = card["rank"]

            # 하트와 다이아몬드는 빨간색
            if suit in ["♥", "♦"]:
                color = "#d62828"
            else:
                color = "#222222"

            st.markdown(
                f"""
                <div style="
                    border: 2px solid #dddddd;
                    border-radius: 12px;
                    background: white;
                    padding: 18px 5px;
                    margin-bottom: 12px;
                    text-align: center;
                    min-height: 95px;
                ">
                    <div style="
                        color: {color};
                        font-size: 30px;
                        font-weight: bold;
                    ">{rank}</div>
                    <div style="
                        color: {color};
                        font-size: 27px;
                    ">{suit}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# 공개 진행 상황
st.divider()

opened_count = len(opened)
remaining_count = len(st.session_state.deck)

col1, col2 = st.columns(2)

with col1:
    st.metric("공개한 카드", f"{opened_count}장")

with col2:
    st.metric("남은 카드", f"{remaining_count}장")

st.progress(opened_count / 52)

# 한 장씩 공개하는 버튼
st.divider()

if remaining_count > 0:
    if st.button(
        "🃏 카드 한 장 공개",
        use_container_width=True,
        type="primary"
    ):
        reveal_card()
        st.rerun()
else:
    st.success("52장의 카드를 모두 공개했습니다.")

# 공개된 카드 목록
with st.expander("공개된 카드 목록 보기"):
    if opened:
        for index, card in enumerate(opened, start=1):
            st.write(
                f"{index}번째 카드: "
                f"{card['rank']}{card['suit']}"
            )
    else:
        st.write("아직 공개된 카드가 없습니다.")
