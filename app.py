# -*- coding: utf-8 -*-
"""
Streamlit 앱: 평면도형의 기초와 성질

설명: 초등학교 4~6학년을 위한 인터랙티브 학습 앱
- 탭1: 도형 탐험 (삼각형, 사각형(직사각형/평행사변형), 원)
- 탭2: 사각형의 족보 (포함 관계 시각화 + 설명)
- 탭3: 퀴즈 (도형 이름 맞추기, OX 퀴즈)

사용법:
    pip install -r requirements.txt
    streamlit run app.py

작성자: GitHub Copilot (도움말용)
"""

import math
import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --------------------------------------------------
# 페이지 설정 및 공통 스타일
# --------------------------------------------------
st.set_page_config(page_title="평면도형 탐험", layout="wide")

# 제목과 간단한 안내 (친절한 말투 / 이모지 포함)
st.title("🌟 평면도형의 기초와 성질 탐험")
st.markdown(
    """
안녕하세요! 반가워요 😊

여러 가지 도형을 직접 만져보면서 모양과 성질을 배워봐요. 슬라이더를 움직하면 도형이 실시간으로 변해요.
쉬운 말로 친절하게 설명해 줄게요. 시작해볼까요?
"""
)

# 공통 축 범위 (scale 고정하여 도형이 찌그러지지 않도록 함)
AX_RANGE = 6  # 축 범위: -AX_RANGE .. AX_RANGE


# --------------------------------------------------
# 유틸리티 함수들
# --------------------------------------------------

def plot_shape(fig):
    """Plotly Figure에 축 비율과 레이아웃을 고정해주는 공통 설정"""
    fig.update_xaxes(range=[-AX_RANGE, AX_RANGE], zeroline=False, showgrid=False)
    fig.update_yaxes(range=[-AX_RANGE, AX_RANGE], zeroline=False, showgrid=False, scaleanchor="x")
    fig.update_layout(width=600, height=600, margin=dict(l=10, r=10, t=10, b=10))
    return fig


def draw_triangle(base, alpha_deg, beta_deg):
    """
    기하 계산을 이용해 삼각형 좌표를 계산
    - base: 밑변 길이 (AB)
    - alpha_deg: A에서의 각도(도)
    - beta_deg: B에서의 각도(도)
    반환: [(x1,y1),(x2,y2),(x3,y3)]
    """
    # 각도를 라디안으로 변환
    alpha = math.radians(alpha_deg)
    beta = math.radians(beta_deg)
    gamma = math.radians(180 - alpha_deg - beta_deg)

    # 삼각형이 성립하지 않으면 None 반환
    if gamma <= 0:
        return None

    # 법칙: a/sin(A) = b/sin(B) = c/sin(C) = 2R
    c = base
    s = c / math.sin(gamma)
    # a: BC (opp A), b: AC (opp B)
    a = s * math.sin(alpha)
    b = s * math.sin(beta)

    # 좌표: A=(0,0), B=(c,0), C는 A로부터 길이 b, 각도 alpha
    A = (0.0, 0.0)
    B = (c, 0.0)
    C = (b * math.cos(alpha), b * math.sin(alpha))
    return [A, B, C]


def draw_parallelogram(width, height, angle_deg):
    """
    평행사변형(또는 직사각형/마름모로 변형 가능)의 좌표 계산
    - width: 밑변 길이
    - height: 높이 (수직 거리)
    - angle_deg: 밑 변과 옆 변의 기울기 각도 (도) — 0이면 직사각형
    """
    angle = math.radians(angle_deg)
    A = (0.0, 0.0)
    B = (width, 0.0)
    # 평행이동 벡터: (dx, height)
    dx = height / math.tan(angle) if abs(math.tan(angle)) > 1e-6 else 0.0
    D = (dx, height)
    C = (width + dx, height)
    return [A, B, C, D]


def draw_rectangle(width, height):
    """직사각형 좌표 계산"""
    A = (0.0, 0.0)
    B = (width, 0.0)
    C = (width, height)
    D = (0.0, height)
    return [A, B, C, D]


def draw_circle(radius, num_points=80):
    """원 좌표를 폴리라인으로 반환"""
    thetas = np.linspace(0, 2 * math.pi, num_points)
    xs = radius * np.cos(thetas)
    ys = radius * np.sin(thetas)
    return xs, ys


# --------------------------------------------------
# 탭 구성: 도형 탐험 / 사각형의 족보 / 퀴즈
# --------------------------------------------------

tabs = st.tabs(["도형 탐험 🔍", "사각형의 족보 🧩", "퀴즈 ✅"])

# ------------------ 탭1: 도형 탐험 ------------------
with tabs[0]:
    st.header("도형을 직접 만져봐요! 🤗")

    # 좌우 레이아웃: 왼쪽 컨트롤, 오른쪽 그래프
    left, right = st.columns([1, 1])

    with left:
        st.subheader("도형 선택")
        shape = st.selectbox("도형을 골라주세요:", ["삼각형", "사각형(직사각형/평행사변형)", "원"])
        st.markdown("---")

        # 삼각형 옵션
        if shape == "삼각형":
            st.markdown("**밑변과 두 각도를 조절해요** (삼각형이 성립하도록 조절하세요)")
            base = st.slider("밑변 길이 (AB)", 0.5, 8.0, 4.0, step=0.1)
            alpha = st.slider("A 꼭짓점 각도 (°)", 5, 170, 50)
            beta = st.slider("B 꼭짓점 각도 (°)", 5, 170, 60)

        # 사각형 옵션
        elif shape == "사각형(직사각형/평행사변형)":
            st.markdown("**직사각형 또는 평행사변형을 선택하고 크기를 조절해요**")
            quad_type = st.radio("종류", ["직사각형", "평행사변형", "마름모(모두 같은 변)"])
            width = st.slider("밑변 길이", 0.5, 8.0, 4.0, step=0.1)
            height = st.slider("높이", 0.5, 6.0, 2.5, step=0.1)
            angle = st.slider("기울기 각도 (°) - 평행사변형일 때", 0, 80, 20)

        # 원 옵션
        else:
            st.markdown("**반지름을 조절해요**")
            radius = st.slider("반지름", 0.5, 5.0, 2.0, step=0.1)

    with right:
        # Plotly figure 생성
        fig = go.Figure()

        if shape == "삼각형":
            coords = draw_triangle(base, alpha, beta)
            if coords is None:
                st.warning("삼각형이 성립하지 않아요. 각도를 조절해 주세요. 😅")
            else:
                xs = [p[0] for p in coords] + [coords[0][0]]
                ys = [p[1] for p in coords] + [coords[0][1]]
                fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", fill="toself", name="triangle",
                                         marker=dict(size=8, color="royalblue"), line=dict(color="royalblue", width=3)))

                # 각 변의 길이 계산
                def dist(p, q):
                    return math.hypot(p[0] - q[0], p[1] - q[1])

                A, B, C = coords
                AB = dist(A, B)
                BC = dist(B, C)
                CA = dist(C, A)

                # 정보 표시
                st.markdown("### 삼각형 정보")
                st.write(f"- 변의 길이: AB = {AB:.2f}, BC = {BC:.2f}, CA = {CA:.2f}")
                # 성질 설명 (쉬운 말)
                st.info("이등변/정삼각형 등을 확인하려면 변의 길이를 비교해보세요. 예: 두 변이 같으면 이등변삼각형이에요 🟦")

        elif shape == "사각형(직사각형/평행사변형)":
            # 마름모는 모든 변이 같도록 height를 조정
            if quad_type == "직사각형":
                pts = draw_rectangle(width, height)
                color = "seagreen"
            elif quad_type == "마름모(모두 같은 변)":
                # 마름모를 만들려면 width를 한 변 길이로 보고 높이는 사각형의 높이로 변환
                # 간단 구현: 마름모를 대각선 기반으로 대칭 생성
                side = width
                # 정사영 높이를 height로 맞추려면 기울기로 변환
                # angle = arctan(height / (side/2)) 를 사용
                angle_for_rhombus = math.degrees(math.atan2(height, side / 2 if side!=0 else 1))
                pts = draw_parallelogram(side, height, angle_for_rhombus)
                color = "orange"
            else:
                pts = draw_parallelogram(width, height, angle)
                color = "purple"

            xs = [p[0] for p in pts] + [pts[0][0]]
            ys = [p[1] for p in pts] + [pts[0][1]]
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", fill="toself",
                                     marker=dict(size=8, color=color), line=dict(color=color, width=3)))

            st.markdown("### 사각형 정보")
            if quad_type == "직사각형":
                st.write(f"- 직사각형: 가로 {width:.2f}, 세로 {height:.2f}")
                st.success("직사각형은 네 각이 모두 직각이에요. 모든 대각선 길이는 같지 않을 수도 있어요.")
            elif quad_type == "마름모(모두 같은 변)":
                st.write(f"- 마름모(대략): 한 변 길이 ≈ {width:.2f}")
                st.success("마름모는 네 변의 길이가 모두 같아요. 대각선은 서로 수직이에요.")
            else:
                st.write(f"- 평행사변형: 밑변 {width:.2f}, 높이 {height:.2f}, 기울기 {angle}°")
                st.info("평행사변형은 마주보는 변이 서로 평행해요. 기울기를 0으로 하면 직사각형이에요.")

        else:  # 원
            xs, ys = draw_circle(radius)
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="crimson", width=3)))
            # 중심 표시
            fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=8, color="crimson")))
            st.markdown("### 원 정보")
            st.write(f"- 반지름: {radius:.2f}")
            st.info("원의 중심에서 반지름만큼 떨어진 점들이 모두 원 위에 있어요. 지름은 반지름의 2배예요.")

        # 공통 레이아웃 적용
        fig = plot_shape(fig)
        st.plotly_chart(fig, use_container_width=True)

# ------------------ 탭2: 사각형의 족보 ------------------
with tabs[1]:
    st.header("사각형의 족보를 살펴봐요 🧭")
    st.markdown("사다리꼴 → 평행사변형 → 직사각형/마름모 → 정사각형의 포함 관계를 그림과 버튼으로 배워봐요.")

    # 그림: 간단한 계층 다이어그램을 그립니다 (plotly annotations 사용)
    fig2 = go.Figure()
    # 네모 박스 위치 지정 (x, y 중앙)
    nodes = {
        "사다리꼴": (0, 2),
        "평행사변형": (0, 1),
        "직사각형": (-1, 0),
        "마름모": (1, 0),
        "정사각형": (0, -1),
    }

    # 박스와 텍스트 추가
    for name, (x, y) in nodes.items():
        fig2.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[name], textposition="middle center",
                                  marker=dict(size=160, color="lightblue", opacity=0.6), showlegend=False, hoverinfo='none'))

    # 화살표 (선) 연결
    fig2.add_shape(type="line", x0=0, y0=1.6, x1=0, y1=1.1, line=dict(color="black"))  # 사다리->평행
    fig2.add_shape(type="line", x0=0, y0=0.6, x1=-0.9, y1=0.15, line=dict(color="black"))  # 평행->직사
    fig2.add_shape(type="line", x0=0, y0=0.6, x1=0.9, y1=0.15, line=dict(color="black"))  # 평행->마름
    fig2.add_shape(type="line", x0=-0.4, y0=-0.2, x1=-0.05, y1=-0.8, line=dict(color="black"))
    fig2.add_shape(type="line", x0=0.4, y0=-0.2, x1=0.05, y1=-0.8, line=dict(color="black"))

    fig2 = plot_shape(fig2)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.write("아래 버튼을 눌러서 왜 포함관계가 성립하는지 친절히 설명을 볼 수 있어요.")

    # 버튼형 인터랙션 (각 항목 클릭 시 설명 표시)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("사다리꼴 설명 🟩"):
            st.success("사다리꼴은 한 쌍의 마주보는 변만 평행해요. 모든 평행사변형은 사다리꼴이 될 수 있어요.")
    with col2:
        if st.button("평행사변형 설명 🔷"):
            st.success("평행사변형은 마주보는 두 쌍의 변이 모두 평행해요. 이 성질 때문에 조금 더 규칙적인 모양이에요.")
    with col3:
        if st.button("직사각형/마름모 설명 🔶"):
            st.success("직사각형은 네 각이 모두 90°인 평행사변형이에요. 마름모는 네 변의 길이가 모두 같은 평행사변형이에요.")

    if st.button("정사각형 설명 ✨"):
        st.success("정사각형은 네 변의 길이가 모두 같고, 네 각이 모두 직각인 도형이에요. 그래서 직사각형이면서 마름모이기도 해요!")

# ------------------ 탭3: 퀴즈 ------------------
with tabs[2]:
    st.header("퀴즈로 배운 내용을 확인해봐요! 🎯")
    st.markdown("도형을 보고 이름을 맞히거나, 성질에 대한 OX 퀴즈를 풀어보세요.")

    # 세션 상태로 점수 추적 (중복 카운트 방지 플래그 포함)
    if 'score' not in st.session_state:
        st.session_state['score'] = 0
    if 'total' not in st.session_state:
        st.session_state['total'] = 0


    # 퀴즈 1: 그림 보고 이름 맞추기 (삼각형/사각형/원)
    st.subheader("문제 1: 도형 이름 맞추기")
    quiz_fig = go.Figure()
    # 간단히 랜덤으로 하나 보여주기
    quiz_choice = st.radio("보기", ["삼각형", "사각형", "원"], index=0, horizontal=True)

    # 실제 그림 표시 (동일한 그리기 함수 사용)
    if quiz_choice == "삼각형":
        c = draw_triangle(4.0, 50, 60)
        xs = [p[0] for p in c] + [c[0][0]]
        ys = [p[1] for p in c] + [c[0][1]]
        quiz_fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='royalblue', width=4)))
    elif quiz_choice == "사각형":
        pts = draw_rectangle(3.5, 2.0)
        xs = [p[0] for p in pts] + [pts[0][0]]
        ys = [p[1] for p in pts] + [pts[0][1]]
        quiz_fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='seagreen', width=4)))
    else:
        xs, ys = draw_circle(2.0)
        quiz_fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='crimson', width=4)))

    quiz_fig = plot_shape(quiz_fig)
    st.plotly_chart(quiz_fig, use_container_width=True)

    answer = st.selectbox("이 도형의 이름은 무엇일까요?", ["선택하세요", "삼각형", "사각형", "원"])
    if st.button("정답 확인 🔎"):
        # 중복 카운트 방지
        if not st.session_state.get('answered_name', False):
            st.session_state['total'] += 1
            st.session_state['answered_name'] = True
            if answer == quiz_choice:
                st.session_state['score'] += 1
                st.success("참 잘했어요! 🎉 정답이에요!")
            else:
                st.error("아쉽네요 😢 정답은 '%s'예요. 힌트: 모서리 개수를 세어보세요!" % quiz_choice)
        else:
            st.info("이미 제출했어요 — 다음 문제로 넘어가요! 🌟")

    st.markdown("---")

    # 퀴즈 2: OX 문제
    st.subheader("문제 2: 성질 OX 퀴즈")
    ox_qs = [
        ("정사각형은 항상 직사각형이다.", True, "정사각형은 네 각이 모두 직각이므로 직사각형이에요."),
        ("모든 평행사변형은 사다리꼴이다.", True, "사다리꼴은 한 쌍만 평행해도 되므로, 평행사변형은 사다리꼴의 일종이에요."),
        ("모든 마름모는 직사각형이다.", False, "마름모는 네 변의 길이가 같지만 각이 직각일 필요는 없어요.")
    ]

    for i, (q, correct, hint) in enumerate(ox_qs, 1):
        st.write(f"Q{i}. {q}")
        choice = st.radio(f"선택 {i}", ["O", "X"], key=f"ox{i}")
        if st.button(f"제출 {i}", key=f"submit{i}"):
            # 중복 카운트 방지
            answered_key = f"answered_{i}"
            if not st.session_state.get(answered_key, False):
                st.session_state['total'] += 1
                st.session_state[answered_key] = True
                picked = True if choice == "O" else False
                if picked == correct:
                    st.session_state['score'] += 1
                    st.success("정답이에요! 잘 이해했어요 🎉")
                    st.caption(hint)
                else:
                    st.error("틀렸어요. 힌트를 줄게요: " + hint)
            else:
                st.info("이미 제출했어요 — 다른 문제를 풀어봐요! ✨")

    st.markdown("---")
    # 점수 표시
    st.info(f"현재 점수: {st.session_state['score']} / {st.session_state['total']}")
    st.info("퀴즈를 통해 배운 내용을 다시 확인해보세요. 더 풀고 싶다면 도형 탐험 탭으로 돌아가세요! 😄")


# --------------------------------------------------
# 파일 끝: 간단한 실행 안내
# --------------------------------------------------
st.markdown("---")
st.caption("앱 제작: 평면도형 학습용 예제 (Streamlit + Plotly). 문의/개선 요청은 프로젝트 리포지터리에 남겨주세요.")
