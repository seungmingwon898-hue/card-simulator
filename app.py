
import random
import streamlit as st

st.set_page_config(page_title="바카라 카드 시뮬레이터", page_icon="🃏", layout="centered")

if "round_data" not in st.session_state:
    st.session_state.round_data = None
if "revealed" not in st.session_state:
    st.session_state.revealed = 0
if "history" not in st.session_state:
    st.session_state.history = []

def card_name(card):
    rank, suit = card
    suits = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}
    ranks = {"A": "A", "J": "J", "Q": "Q", "K": "K"}
    return f"{suits[suit]} {ranks.get(rank, rank)}"

def card_value(card):
    rank = card[0]
    if rank in ("10", "J", "Q", "K"):
        return 0
    if rank == "A":
        return 1
    return int(rank)

def total(cards):
    return sum(card_value(c) for c in cards) % 10

def new_round():
    deck = [(r, s) for s in "SHDC"
            for r in ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]]
    random.shuffle(deck)

    player = [deck.pop(), deck.pop()]
    banker = [deck.pop(), deck.pop()]

    if total(player) < 6:
        player.append(deck.pop())

    if total(banker) < 6:
        banker.append(deck.pop())

    st.session_state.round_data = {
        "player": player,
        "banker": banker,
    }
    st.session_state.revealed = 0

def show_cards(label, cards, start, revealed):
    st.subheader(label)
    cols = st.columns(len(cards))
    for i, card in enumerate(cards):
        with cols[i]:
            if start + i < revealed:
                color = "#d62828" if card[1] in ("H", "D") else "#222222"
                st.markdown(
                    f"""<div style="background:white;color:{color};
                    border-radius:12px;padding:18px 5px;text-align:center;
                    font-size:25px;border:2px solid #ddd;">
                    {card_name(card)}</div>""",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """<div style="background:#174a38;color:white;
                    border-radius:12px;padding:18px 5px;text-align:center;
                    font-size:25px;border:2px solid #ddd;">🂠</div>""",
                    unsafe_allow_html=True
                )

st.markdown(
    "<h1 style='text-align:center;color:#d4af37'>🃏 BACCARAT</h1>"
    "<p style='text-align:center'>카드를 한 장씩 공개하는 시뮬레이터</p>",
    unsafe_allow_html=True
)

st.markdown("---")

if st.button("🎴 새 게임 시작", use_container_width=True):
    new_round()

data = st.session_state.round_data

if data:
    player = data["player"]
    banker = data["banker"]
    all_cards = player + banker

    show_cards("PLAYER", player, 0, st.session_state.revealed)
    show_cards("BANKER", banker, len(player), st.session_state.revealed)

    st.write(f"공개된 카드: {st.session_state.revealed} / {len(all_cards)}")

    if st.session_state.revealed < len(all_cards):
        if st.button("🂠 다음 카드 공개", use_container_width=True):
            st.session_state.revealed += 1
            st.rerun()
    else:
        p_total = total(player)
        b_total = total(banker)

        st.markdown("---")
        st.subheader("🏆 최종 결과")

        col1, col2 = st.columns(2)
        col1.metric("PLAYER 점수", p_total)
        col2.metric("BANKER 점수", b_total)

        if p_total > b_total:
            result = "PLAYER 승리"
        elif b_total > p_total:
            result = "BANKER 승리"
        else:
            result = "무승부"

        st.success(f"🎉 {result}")

        if st.button("결과 기록하기", use_container_width=True):
            if not st.session_state.history or st.session_state.history[-1] != result:
                st.session_state.history.append(result)

if st.session_state.history:
    st.markdown("---")
    st.subheader("📊 기록")
    st.write(f"총 기록 수: {len(st.session_state.history)}")
    st.write(f"PLAYER 승리: {st.session_state.history.count('PLAYER 승리')}")
    st.write(f"BANKER 승리: {st.session_state.history.count('BANKER 승리')}")
    st.write(f"무승부: {st.session_state.history.count('무승부')}")
