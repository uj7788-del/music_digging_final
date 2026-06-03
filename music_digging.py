"""
나만의 흑인음악 취향 디깅(Digging) 대시보드 v2.2
My Black Music Taste Digging Dashboard — Objective Attributes Edition

실행 방법: streamlit run music_digging.py
의존성: pip install streamlit pillow
"""

import io
import re
import streamlit as st
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# 1. 페이지 기본 설정
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="나만의 흑인음악 취향 디깅하기",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# 2. 전역 CSS — 밝은 테마 (Light Theme)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
  /*
   * ═══════════════════════════════════════════════════════════
   * Airbnb Design System — music_digging.py
   * Canvas: #ffffff · Ink: #222222 · Rausch: #ff385c
   * Font: Pretendard (open-source substitute for Airbnb Cereal VF)
   * Shadow: single tier only
   * ═══════════════════════════════════════════════════════════
   */

  @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');

  /* ── 디자인 토큰 변수 ── */
  :root {
    --rausch:        #ff385c;
    --rausch-active: #e00b41;
    --rausch-pale:   #ffd1da;
    --ink:           #222222;
    --body-text:     #3f3f3f;
    --muted:         #6a6a6a;
    --muted-soft:    #929292;
    --hairline:      #dddddd;
    --hairline-soft: #ebebeb;
    --border-strong: #c1c1c1;
    --canvas:        #ffffff;
    --surface-soft:  #f7f7f7;
    --surface-strong:#f2f2f2;
    /* Airbnb single shadow tier */
    --shadow-float:  rgba(0,0,0,0.02) 0 0 0 1px,
                     rgba(0,0,0,0.04) 0 2px 6px 0,
                     rgba(0,0,0,0.10) 0 4px 8px 0;
    /* Rounded tokens */
    --r-xs:   4px;
    --r-sm:   8px;
    --r-md:   14px;
    --r-lg:   20px;
    --r-xl:   32px;
    --r-full: 9999px;
    /* Spacing tokens */
    --sp-xxs: 2px;  --sp-xs: 4px;  --sp-sm: 8px;
    --sp-md:  12px; --sp-base:16px;--sp-lg: 24px;
    --sp-xl:  32px; --sp-xxl:48px; --sp-section:64px;
  }

  /* ── 전체 배경 / 폰트 ── */
  html, body, [class*="css"], [class*="st-"], p, div, span, h1, h2, h3, h4, h5, h6, li, a {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', sans-serif !important;
  }
  
  /* ── 스트림릿 내부 아이콘(Material) 깨짐 방지 ── */
  i, 
  .material-icons, 
  .material-symbols-rounded, 
  .material-symbols-outlined, 
  [class*="icon"], 
  [data-testid*="stIcon"] {
    font-family: 'Material Symbols Rounded', 'Material Icons', 'Material Symbols Outlined', sans-serif !important;
  }
  
  /* span 내부에 위치한 아이콘 텍스트도 보호 */
  [data-testid*="stIcon"] *,
  .material-symbols-rounded * {
    font-family: 'Material Symbols Rounded', 'Material Icons', 'Material Symbols Outlined', sans-serif !important;
  }
  
  .stApp {
    background-color: var(--canvas);
    color: var(--ink);
  }
  .block-container { padding-top: 1.5rem; padding-bottom: var(--sp-section); }

  /* ── 사이드바 ── */
  [data-testid="stSidebar"] {
    background-color: var(--canvas);
    border-right: 1px solid var(--hairline);
  }
  [data-testid="stSidebar"] * { color: var(--ink) !important; }
  [data-testid="stSidebar"] hr { border-color: var(--hairline-soft) !important; }

  /* ── 타이틀 배너 ──
     Airbnb: 화이트 캔버스 위 Rausch 단색 워드마크 스타일
     사진이나 그라디언트 대신 여백·타이포로 승부 */
  .title-banner {
    background-color: var(--canvas);
    border-bottom: 1px solid var(--hairline);
    padding: var(--sp-lg) 0 var(--sp-xl) 0;
    margin-bottom: var(--sp-xl);
  }
  .title-eyebrow {
    font-size: 11px; font-weight: 600; letter-spacing: 0.32px;
    text-transform: uppercase; color: var(--rausch);
    margin-bottom: var(--sp-sm);
  }
  .title-main {
    font-size: 28px; font-weight: 700; line-height: 1.43;
    color: var(--ink); letter-spacing: 0;
    margin-bottom: var(--sp-sm);
  }
  .title-sub {
    font-size: 16px; font-weight: 400; line-height: 1.5;
    color: var(--muted);
  }

  /* ── 단계 뱃지 (pill tag) ── */
  .step-badge {
    display: inline-flex; align-items: center; gap: var(--sp-sm);
    background-color: var(--surface-soft);
    border: 1px solid var(--hairline);
    border-radius: var(--r-full);
    padding: 6px 16px;
    font-size: 12px; font-weight: 700; color: var(--ink);
    letter-spacing: 0; margin-bottom: var(--sp-base);
  }
  .step-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background-color: var(--rausch);
  }

  /* ── 곡 카드 ── */
  .track-card {
    background-color: var(--canvas);
    border: 1px solid var(--hairline);
    border-radius: var(--r-md);     /* 14px — property-card token */
    padding: var(--sp-lg) var(--sp-xl);
    margin-bottom: var(--sp-base);
    position: relative;
    transition: box-shadow 0.15s ease;
  }
  .track-card:hover {
    box-shadow: var(--shadow-float);
  }
  .track-number {
    position: absolute; top: var(--sp-base); right: var(--sp-xl);
    font-size: 40px; font-weight: 700; color: var(--hairline-soft);
    line-height: 1; user-select: none;
  }
  .track-title {
    font-size: 16px; font-weight: 600; line-height: 1.25;
    color: var(--ink); margin-bottom: var(--sp-xs);
  }
  .track-artist {
    font-size: 14px; font-weight: 400; line-height: 1.43;
    color: var(--muted); margin-bottom: var(--sp-md);
  }
  .track-desc {
    font-size: 14px; font-weight: 400; line-height: 1.6;
    color: var(--body-text);
    border-left: 2px solid var(--hairline);
    padding-left: var(--sp-md); margin-bottom: var(--sp-lg);
  }
  /* YouTube 링크 — Rausch pill button */
  .yt-link {
    display: inline-flex; align-items: center; gap: 6px;
    background-color: var(--rausch);
    color: #ffffff;
    border-radius: var(--r-full);
    padding: 10px 20px;
    font-size: 14px; font-weight: 500; line-height: 1.29;
    text-decoration: none;
    transition: background-color 0.15s;
  }
  .yt-link:hover { background-color: var(--rausch-active); }

  /* ── 트랙 진행 표시기 ── */
  .track-progress-wrap {
    display: flex; align-items: center; gap: var(--sp-md);
    margin-bottom: var(--sp-lg);
  }
  .track-pip {
    width: 36px; height: 36px; border-radius: var(--r-full);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 600;
    border: 1.5px solid; transition: all 0.2s;
    font-family: inherit;
  }
  .pip-done   { background-color: var(--ink);    border-color: var(--ink);         color: #ffffff; }
  .pip-active { background-color: var(--rausch); border-color: var(--rausch);      color: #ffffff; }
  .pip-locked { background-color: var(--canvas); border-color: var(--hairline);    color: var(--muted-soft); }
  .track-pip-line      { flex: 1; height: 1px; background-color: var(--hairline); }
  .track-pip-line-done { background-color: var(--ink); }

  /* ── 평가 섹션 레이블 ── */
  .eval-label {
    font-size: 12px; font-weight: 700; line-height: 1.33;
    color: var(--ink); letter-spacing: 0;
    margin-bottom: var(--sp-xs); margin-top: var(--sp-md);
  }

  /* ── 진행 표시 바 (사이드바) ── */
  .progress-wrap { margin: var(--sp-md) 0 var(--sp-lg) 0; }
  .progress-track {
    background-color: var(--surface-strong);
    border-radius: var(--r-full); height: 4px; overflow: hidden;
  }
  .progress-fill {
    height: 100%; border-radius: var(--r-full);
    background-color: var(--rausch);
    transition: width 0.4s ease;
  }
  .progress-label { font-size: 13px; font-weight: 400; color: var(--muted); margin-top: var(--sp-xs); }

  /* ── Streamlit 버튼 → Airbnb button-primary ──
     48px height · 8px radius · Rausch · weight 500 */
  .stButton > button {
    background-color: var(--rausch) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--r-sm) !important; /* 8px */
    font-family: 'Pretendard', sans-serif !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    line-height: 1.25 !important;
    padding: 14px 24px !important;
    height: 48px !important;
    transition: background-color 0.15s !important;
    box-shadow: none !important;
  }
  .stButton > button:hover {
    background-color: var(--rausch-active) !important;
    transform: none !important;
  }
  .stButton > button:disabled {
    background-color: var(--rausch-pale) !important;
    cursor: not-allowed !important;
  }

  /* ── 별점 표시 ── */
  .star-guide {
    font-size: 14px; font-weight: 500; color: var(--ink);
    margin-top: var(--sp-xs);
  }

  /* ── 완료 배너 (inline notice) ── */
  .complete-banner {
    background-color: var(--surface-soft);
    border: 1px solid var(--hairline);
    border-radius: var(--r-sm);
    padding: var(--sp-md) var(--sp-base);
    font-size: 14px; font-weight: 500;
    color: var(--ink); margin-bottom: var(--sp-base);
  }

  /* ── 전체 완료 배너 ── */
  .all-done-banner {
    background-color: var(--surface-soft);
    border: 1px solid var(--hairline);
    border-left: 3px solid var(--rausch);
    border-radius: var(--r-sm);
    padding: var(--sp-base) var(--sp-lg);
    font-size: 16px; font-weight: 500;
    color: var(--ink); margin-bottom: var(--sp-base);
  }

  /* ── 탭 (Airbnb product-tab 스타일: 언더라인 방식) ── */
  .stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid var(--hairline);
    padding: 0; gap: 0;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--muted);
    border-radius: 0;
    font-size: 16px; font-weight: 600;
    padding: 12px 16px;
    border-bottom: 2px solid transparent;
  }
  .stTabs [aria-selected="true"] {
    background: transparent !important;
    color: var(--ink) !important;
    border-bottom: 2px solid var(--ink) !important;
    box-shadow: none !important;
  }

  /* ── 속성 바 배경 ── */
  .attr-bar-bg {
    background-color: var(--surface-strong);
    border-radius: var(--r-full); height: 6px; overflow: hidden;
  }

  /* ── 사이드바 장르 설명 박스 ── */
  .sidebar-info {
    background-color: var(--surface-soft);
    border-radius: var(--r-sm);
    padding: var(--sp-md);
    margin-top: var(--sp-sm);
    border: 1px solid var(--hairline-soft);
    font-size: 13px; font-weight: 400;
    color: var(--body-text); line-height: 1.6;
  }

  /* ── 추천 카드 ── */
  .rec-card {
    background-color: var(--canvas);
    border: 1px solid var(--hairline);
    border-radius: var(--r-md);
    padding: var(--sp-base) var(--sp-lg);
    margin-bottom: var(--sp-md);
    transition: box-shadow 0.15s;
  }
  .rec-card:hover { box-shadow: var(--shadow-float); transform: translateY(-2px); }
  .rec-card-matched:hover { box-shadow: var(--shadow-float); transform: translateY(-2px); }

  .rec-card-matched {
    background-color: var(--canvas);
    border: 1px solid var(--ink);   /* 강조: ink 테두리 */
    border-radius: var(--r-md);
    padding: var(--sp-base) var(--sp-lg);
    margin-bottom: var(--sp-md);
    position: relative;
    box-shadow: var(--shadow-float);
  }
  .rec-match-badge {
    position: absolute; top: var(--sp-md); right: var(--sp-base);
    background-color: var(--ink);
    color: #ffffff;
    border-radius: var(--r-full);
    padding: 4px 10px;
    font-size: 11px; font-weight: 600; line-height: 1.18;
  }
  .rec-rank {
    font-size: 20px; font-weight: 700;
    color: var(--hairline); float: right; line-height: 1;
  }
  .rec-title {
    font-size: 16px; font-weight: 600; line-height: 1.25;
    color: var(--ink); margin-bottom: var(--sp-xxs);
  }
  .rec-artist {
    font-size: 14px; font-weight: 400; line-height: 1.43;
    color: var(--muted); margin-bottom: var(--sp-sm);
  }
  .rec-tags { display: flex; flex-wrap: wrap; gap: var(--sp-xs); margin-top: var(--sp-sm); }
  .rec-tag {
    background-color: var(--surface-soft);
    border: 1px solid var(--hairline);
    border-radius: var(--r-full);
    padding: 4px 10px;
    font-size: 11px; font-weight: 600; line-height: 1.18;
    color: var(--muted);
  }
  .rec-tag-highlight {
    background-color: var(--ink);
    border: 1px solid var(--ink);
    border-radius: var(--r-full);
    padding: 4px 10px;
    font-size: 11px; font-weight: 600; line-height: 1.18;
    color: #ffffff;
  }

  /* ── 분석 결과 헤더 ── */
  .result-header {
    background-color: var(--surface-soft);
    border: 1px solid var(--hairline);
    border-radius: var(--r-md);
    padding: var(--sp-lg) var(--sp-xl);
    margin-bottom: var(--sp-lg);
  }
  .result-title {
    font-size: 21px; font-weight: 700; line-height: 1.43;
    color: var(--ink); margin-bottom: var(--sp-xs);
  }
  .result-persona {
    font-size: 16px; font-weight: 400; line-height: 1.5;
    color: var(--body-text);
  }

  /* ── 섹션 구분선 ── */
  .section-divider {
    border: none;
    border-top: 1px solid var(--hairline-soft);
    margin: var(--sp-xxl) 0;
  }

  /* ── 믹스테이프 리포트 ── */
  .mixtape-box {
    background-color: var(--surface-soft);
    border: 1px solid var(--hairline);
    border-radius: var(--r-sm);
    padding: var(--sp-lg);
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, 'Helvetica Neue', sans-serif;
    font-size: 13px; font-weight: 400;
    color: var(--body-text); line-height: 1.9;
    white-space: pre-wrap;
  }

  /* ── 타임라인 ── */
  .timeline-wrap {
    position: relative;
    padding: var(--sp-sm) 0;
    margin-bottom: var(--sp-sm);
  }
  .timeline-wrap::before {
    content: '';
    position: absolute; left: 27px; top: 0; bottom: 0;
    width: 1px;
    background-color: var(--hairline);
  }
  .timeline-item {
    display: flex; align-items: flex-start; gap: var(--sp-lg);
    margin-bottom: var(--sp-xl); position: relative;
  }
  .timeline-node {
    flex-shrink: 0; width: 54px; height: 54px;
    border-radius: var(--r-full);
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700; line-height: 1.2;
    text-align: center; position: relative; z-index: 1;
    border: 1px solid; letter-spacing: -0.02em;
    box-shadow: var(--shadow-float);
  }
  .timeline-content {
    flex: 1; background-color: var(--canvas);
    border-radius: var(--r-md);
    padding: var(--sp-base) var(--sp-lg);
    border: 1px solid var(--hairline);
    margin-top: var(--sp-xs);
    transition: box-shadow 0.15s;
  }
  .timeline-content:hover { box-shadow: var(--shadow-float); }
  .timeline-year {
    font-size: 11px; font-weight: 600; line-height: 1.18;
    text-transform: uppercase; letter-spacing: 0.32px;
    margin-bottom: var(--sp-xs);
  }
  .timeline-title {
    font-size: 16px; font-weight: 600; line-height: 1.25;
    color: var(--ink); margin-bottom: var(--sp-xs);
  }
  .timeline-desc {
    font-size: 14px; font-weight: 400; line-height: 1.6;
    color: var(--body-text);
  }
  .timeline-artists { display: flex; flex-wrap: wrap; gap: var(--sp-xs); margin-top: var(--sp-sm); }
  .timeline-artist-tag {
    background-color: var(--surface-strong);
    border: 1px solid var(--hairline);
    border-radius: var(--r-full);
    padding: 4px 10px;
    font-size: 11px; font-weight: 600; line-height: 1.18;
    color: var(--muted);
  }

  /* ── 타임라인 헤더 ── */
  .timeline-header {
    background-color: var(--surface-soft);
    border: 1px solid var(--hairline);
    border-radius: var(--r-md);
    padding: var(--sp-base) var(--sp-xl);
    margin-bottom: var(--sp-lg);
  }
  .timeline-header-title {
    font-size: 21px; font-weight: 700; line-height: 1.43;
    color: var(--ink); margin-bottom: var(--sp-xs);
  }
  .timeline-header-sub {
    font-size: 14px; font-weight: 400; line-height: 1.43;
    color: var(--muted);
  }

  /* LP 리포트 CSS는 render_lp_report_html() 함수 내부에 인라인으로 내장됨 */
  }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 3. 하드코딩 데이터셋
#    yt_query: "아티스트명 - 곡제목" 정확히 일치 (유튜브 검색 직결)
# ══════════════════════════════════════════════════════════════

GENRE_DATA = {

    # ────────────────────────
    # 1. Neo-Soul
    # ────────────────────────
    "🌙 Neo-Soul": {
        "desc": "70~80년대 소울의 감성을 현대적 R&B 프로덕션으로 재해석. 따뜻한 멜로디, 깊은 보컬, 아날로그 질감.",
        "color": "#7c3aed",
        "tracks": [
            {
                "title": "On & On", "artist": "Erykah Badu", "year": 1997,
                "desc": "네오소울의 시작점. 아날로그 드럼, Badu의 독특한 보컬 톤, 재즈적 코드 진행이 장르를 정의한 곡.",
                "yt_query": "Erykah Badu - On & On",
                "vibe": ["🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎸 베이스 & 그루브 (Bass & Groove)"],
            },
            {
                "title": "Untitled (How Does It Feel)", "artist": "D'Angelo", "year": 2000,
                "desc": "빈티지 펑크와 소울의 완벽한 결합. 레이어드된 보컬 하모니와 끈적한 그루브가 압도적.",
                "yt_query": "D'Angelo - Untitled (How Does It Feel)",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🥁 리듬 & 비트 (Rhythm & Beat)"],
            },
            {
                "title": "Ex-Factor", "artist": "Lauryn Hill", "year": 1998,
                "desc": "The Miseducation 시대의 정수. 어쿠스틱 기타와 깊은 가사, 감정적 보컬 전달력이 핵심.",
                "yt_query": "Lauryn Hill - Ex-Factor",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)"],
            },
        ],
        "tracks_phase2": [
            {
                "title": "Fortunate", "artist": "Maxwell", "year": 1998,
                "desc": "부드러운 팔세토와 재즈적 화성이 완벽하게 결합된 네오소울 발라드. Maxwell의 감성적 보컬이 장르의 섬세함을 정의한다.",
                "yt_query": "Maxwell - Fortunate",
                "vibe": ["🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎹 화성 & 코드 진행 (Harmony & Chords)"],
            },
            {
                "title": "A Long Walk", "artist": "Jill Scott", "year": 2000,
                "desc": "Jill Scott 데뷔 앨범의 따뜻한 어쿠스틱 그루브. 일상의 언어로 낭만을 노래하는 네오소울의 진심이 담긴 곡.",
                "yt_query": "Jill Scott - A Long Walk",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "📜 가사 & 메시지 (Lyrics & Message)", "🎺 리얼 악기 세션 (Live Instruments)"],
            },
            {
                "title": "Video", "artist": "India.Arie", "year": 2001,
                "desc": "어쿠스틱 기타 중심의 긍정적 자존감 메시지. 인디 소울의 정수이자 진정성 있는 가사의 힘을 보여주는 명곡.",
                "yt_query": "India.Arie - Video",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎵 멜로디 (Melody)", "🎺 리얼 악기 세션 (Live Instruments)"],
            },
        ],
        "recommendations": [
            {"title": "Bag Lady", "artist": "Erykah Badu", "year": 2000, "tags": ["위로", "소울", "재즈"], 
             "match_attributes": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎺 리얼 악기 세션 (Live Instruments)", "🎹 화성 & 코드 진행 (Harmony & Chords)"]},
            {"title": "Brown Sugar", "artist": "D'Angelo", "year": 1995, "tags": ["감성", "빈티지", "로맨틱"], 
             "match_attributes": ["🎸 베이스 & 그루브 (Bass & Groove)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"]},
            {"title": "Be Here", "artist": "Raphael Saadiq", "year": 2004, "tags": ["따뜻함", "멜로디", "어덜트소울"], 
             "match_attributes": ["🎺 리얼 악기 세션 (Live Instruments)", "🎵 멜로디 (Melody)", "🎸 베이스 & 그루브 (Bass & Groove)"]},
            {"title": "New Amerykah Pt.1", "artist": "Erykah Badu", "year": 2008, "tags": ["실험적", "의식적", "사이키델릭"], 
             "match_attributes": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "📜 가사 & 메시지 (Lyrics & Message)", "🥁 리듬 & 비트 (Rhythm & Beat)"]},
            {"title": "Voodoo (Album)", "artist": "D'Angelo", "year": 2000, "tags": ["그루브", "레이어드", "완성도"], 
             "match_attributes": ["🎸 베이스 & 그루브 (Bass & Groove)", "🎺 리얼 악기 세션 (Live Instruments)", "🥁 리듬 & 비트 (Rhythm & Beat)"]},
        ],
        "timeline": [
            {"year": "1972", "era": "Proto", "title": "Al Green의 황금기", "desc": "소울의 감성과 펑크 사운드가 교차. Al Green의 음악이 네오소울 감성의 원형.", "artists": ["Al Green", "Stevie Wonder"]},
            {"year": "1994", "era": "Birth", "title": "장르의 탄생", "desc": "D'Angelo 데뷔앨범 'Brown Sugar'로 장르가 공식화되며 'Neo-Soul' 용어 확립.", "artists": ["D'Angelo", "Me'Shell NdegéOcello"]},
            {"year": "1997~1999", "era": "Golden Age", "title": "황금기 — Soulquarians의 시대", "desc": "Erykah Badu, Lauryn Hill 등 집단 Soulquarians가 네오소울의 철학적 기준을 완성.", "artists": ["Erykah Badu", "Lauryn Hill", "Common"]},
            {"year": "2000", "era": "Peak", "title": "D'Angelo 'Voodoo' — 장르의 정점", "desc": "역사상 최고작. J Dilla와의 협업으로 리듬 언어 자체를 혁신.", "artists": ["D'Angelo", "J Dilla", "Questlove"]},
        ],
    },

    # ────────────────────────
    # 2. Funk
    # ────────────────────────
    "🔥 Funk": {
        "desc": "James Brown에서 시작된 그루브 중심 사운드. 강렬한 베이스라인, 촘촘한 리듬 섹션, 반복적 훅이 특징.",
        "color": "#ea580c",
        "tracks": [
            {
                "title": "Super Freak",
                "artist": "Rick James",
                "year": 1981,
                "desc": "강렬한 신스 리프와 Rick James의 에너지가 폭발하는 클래식 펑크. MC Hammer 샘플로도 유명.",
                "yt_query": "Rick James - Super Freak",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"],
            },
            {
                "title": "Flash Light",
                "artist": "Parliament",
                "year": 1977,
                "desc": "George Clinton의 P-Funk 우주관. 무겁고 끈적한 신스 베이스와 집단 보컬이 만드는 황홀경.",
                "yt_query": "Parliament - Flash Light",
                "vibe": ["🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎺 리얼 악기 세션 (Live Instruments)"],
            },
            {
                "title": "Give Up the Funk (Tear the Roof off the Sucker)",
                "artist": "Parliament",
                "year": 1975,
                "desc": "펑크의 교과서. 반복적 리프, 콜앤리스폰스 보컬, 인펙셔스한 그루브가 완벽하게 맞물린 곡.",
                "yt_query": "Parliament - Give Up the Funk (Tear the Roof off the Sucker)",
                "vibe": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "📜 가사 & 메시지 (Lyrics & Message)"],
            },
        ],
        "tracks_phase2": [
            {
                "title": "Sex Machine", "artist": "James Brown", "year": 1970,
                "desc": "모든 펑크의 원점. '겟 업, 겟 온업'의 선언과 함께 폭발하는 가장 원초적인 그루브. JB 밴드의 유기적 앙상블이 압도적.",
                "yt_query": "James Brown - Sex Machine",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎙️ 보컬 & 음색 (Vocal & Tone)"],
            },
            {
                "title": "September", "artist": "Earth, Wind & Fire", "year": 1978,
                "desc": "'21st night of September'로 시작되는 영원한 파티 앤섬. 브라스 섹션과 디스코 그루브의 완벽한 결합.",
                "yt_query": "Earth Wind and Fire - September",
                "vibe": ["🎵 멜로디 (Melody)", "🎺 리얼 악기 세션 (Live Instruments)", "🥁 리듬 & 비트 (Rhythm & Beat)"],
            },
            {
                "title": "Everyday People", "artist": "Sly & The Family Stone", "year": 1968,
                "desc": "흑인·백인·남녀가 함께한 밴드의 평등 메시지. 단순하지만 강렬한 그루브로 시대를 초월한 울림을 남기는 곡.",
                "yt_query": "Sly and The Family Stone - Everyday People",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎸 베이스 & 그루브 (Bass & Groove)", "🎹 화성 & 코드 진행 (Harmony & Chords)"],
            },
        ],
        "recommendations": [
            {"title": "I Got You (I Feel Good)", "artist": "James Brown", "year": 1965,
             "tags": ["에너지", "파워", "클래식"], "match_attributes": ["🎺 리얼 악기 세션 (Live Instruments)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎙️ 보컬 & 음색 (Vocal & Tone)"]},
            {"title": "Jungle Boogie", "artist": "Kool & The Gang", "year": 1973,
             "tags": ["펑키", "브라스", "댄서블"], "match_attributes": ["📜 가사 & 메시지 (Lyrics & Message)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎺 리얼 악기 세션 (Live Instruments)"]},
            {"title": "That Lady", "artist": "The Isley Brothers", "year": 1973,
             "tags": ["기타", "그루브", "소울펑크"], "match_attributes": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "📜 가사 & 메시지 (Lyrics & Message)", "🥁 리듬 & 비트 (Rhythm & Beat)"]},
            {"title": "Shining Star", "artist": "Earth, Wind & Fire", "year": 1975,
             "tags": ["업리프팅", "브라스", "완성도"], "match_attributes": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "📜 가사 & 메시지 (Lyrics & Message)", "🎹 화성 & 코드 진행 (Harmony & Chords)"]},
            {"title": "Le Freak", "artist": "Chic", "year": 1978,
             "tags": ["디스코펑크", "리프", "댄스플로어"], "match_attributes": ["🥁 리듬 & 비트 (Rhythm & Beat)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "📜 가사 & 메시지 (Lyrics & Message)"]},
        ],
        "timeline": [
            {"year": "1960s", "era": "Origin",
             "title": "James Brown — 펑크의 아버지",
             "desc": "'Papa's Got a Brand New Bag'(1965)으로 비트의 1박 강조, 싱코페이션 리듬이 탄생. 모든 펑크 음악의 DNA가 여기서 시작.",
             "artists": ["James Brown", "The Famous Flames"]},
            {"year": "1967~1969", "era": "Development",
             "title": "Sly & The Family Stone의 혁신",
             "desc": "흑인과 백인, 남성과 여성이 함께한 밴드. 사이키델릭 록과 펑크의 결합으로 장르 경계를 무너뜨림.",
             "artists": ["Sly Stone", "Larry Graham"]},
            {"year": "1972~1975", "era": "P-Funk Era",
             "title": "George Clinton의 P-Funk 우주",
             "desc": "Parliament-Funkadelic 듀얼 밴드 운영. '마더십(Mothership Connection)' 컨셉으로 펑크를 문화·철학적 운동으로 확장.",
             "artists": ["George Clinton", "Bootsy Collins", "Bernie Worrell"]},
            {"year": "1976~1979", "era": "Disco Fusion",
             "title": "디스코와의 만남 — Earth, Wind & Fire",
             "desc": "펑크가 디스코의 화려함과 결합. EWF, Chic, Kool & The Gang이 댄스플로어를 지배하며 대중화에 성공.",
             "artists": ["Earth, Wind & Fire", "Chic", "Nile Rodgers"]},
            {"year": "1980s", "era": "Electro-Funk",
             "title": "신시사이저와의 결합 — Electro-Funk",
             "desc": "Prince, Rick James가 신스와 드럼머신을 흡수. 미니멀하고 섹슈얼한 펑크 사운드로 진화.",
             "artists": ["Prince", "Rick James", "Zapp"]},
            {"year": "1990s~현재", "era": "Legacy",
             "title": "힙합 샘플의 바이블",
             "desc": "NWA, De La Soul, Public Enemy 등 힙합이 펑크 비트를 샘플링하며 명맥 유지. Kendrick Lamar의 'To Pimp a Butterfly'로 현대에 부활.",
             "artists": ["Kendrick Lamar", "Bruno Mars", "Anderson .Paak"]},
        ],
    },

    # ────────────────────────
    # 3. Contemporary R&B
    # ────────────────────────
    "💜 Contemporary R&B": {
        "desc": "2000년대 이후 팝·힙합이 융합된 현대 R&B. 세련된 프로덕션, 오토튠 활용, 감성적 가사가 트레이드마크.",
        "color": "#db2777",
        "tracks": [
            {
                "title": "Climax",
                "artist": "Usher",
                "year": 2012,
                "desc": "컨템포러리 R&B와 일렉트로닉의 경계를 허문 Diplo 프로덕션. Usher의 팔세토가 절정.",
                "yt_query": "Usher - Climax",
                "vibe": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎸 베이스 & 그루브 (Bass & Groove)"],
            },
            {
                "title": "Die For You",
                "artist": "The Weeknd",
                "year": 2016,
                "desc": "80s 신스팝 미학 위에 얹힌 The Weeknd의 감성적 가사. 현대 R&B의 교과서적 트랙.",
                "yt_query": "The Weeknd - Die For You",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎵 멜로디 (Melody)", "🥁 리듬 & 비트 (Rhythm & Beat)"],
            },
            {
                "title": "Location",
                "artist": "Khalid",
                "year": 2016,
                "desc": "청춘의 감성을 담은 lo-fi R&B. 편안한 프로덕션과 Khalid의 허스키 보컬이 완벽한 조화.",
                "yt_query": "Khalid - Location",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎵 멜로디 (Melody)"],
            },
        ],
        "tracks_phase2": [
            {
                "title": "Thinkin Bout You", "artist": "Frank Ocean", "year": 2012,
                "desc": "채널 오렌지의 오프닝. 담백한 신스 위에서 Frank Ocean의 팔세토가 만들어내는 감성적 몰입감. 현대 R&B 보컬의 기준.",
                "yt_query": "Frank Ocean - Thinkin Bout You",
                "vibe": ["🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"],
            },
            {
                "title": "Good Days", "artist": "SZA", "year": 2020,
                "desc": "SZA의 뛰어난 멜로디 감각과 몽환적 프로덕션. 현대 R&B의 lo-fi 미학을 극한까지 끌어올린 신세대 R&B의 정수.",
                "yt_query": "SZA - Good Days",
                "vibe": ["🎵 멜로디 (Melody)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎙️ 보컬 & 음색 (Vocal & Tone)"],
            },
            {
                "title": "Come Through", "artist": "H.E.R.", "year": 2017,
                "desc": "기타 중심의 쿨한 R&B. H.E.R.의 복면 아이덴티티와 능숙한 기타 연주가 만드는 독특하고 세련된 매력.",
                "yt_query": "H.E.R. - Come Through",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "🎺 리얼 악기 세션 (Live Instruments)", "🎙️ 보컬 & 음색 (Vocal & Tone)"],
            },
        ],
        "recommendations": [
            {"title": "Best Part", "artist": "Daniel Caesar ft. H.E.R.", "year": 2017,
             "tags": ["로맨틱", "어쿠스틱R&B", "듀엣"], "match_attributes": ["🎵 멜로디 (Melody)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"]},
            {"title": "Superstar", "artist": "Usher", "year": 2004,
             "tags": ["클래식R&B", "스무드", "감성"], "match_attributes": ["🎸 베이스 & 그루브 (Bass & Groove)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🥁 리듬 & 비트 (Rhythm & Beat)"]},
            {"title": "Come Through", "artist": "H.E.R.", "year": 2017,
             "tags": ["기타R&B", "쿨", "세련됨"], "match_attributes": ["🥁 리듬 & 비트 (Rhythm & Beat)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"]},
            {"title": "Earned It", "artist": "The Weeknd", "year": 2015,
             "tags": ["오케스트라", "극적", "감성"], "match_attributes": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🎵 멜로디 (Melody)"]},
            {"title": "Nobody", "artist": "Khalid & Alina Barraza", "year": 2018,
             "tags": ["팝R&B", "발라드", "청춘"], "match_attributes": ["🎸 베이스 & 그루브 (Bass & Groove)", "📜 가사 & 메시지 (Lyrics & Message)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"]},
        ],
        "timeline": [
            {"year": "1994~1997", "era": "New School",
             "title": "TLC·Aaliyah — 미래형 R&B의 선구자",
             "desc": "Timbaland·Missy Elliott 프로덕션팀이 드럼패턴과 R&B 보컬을 혁신적으로 결합. Aaliyah 'One in a Million'이 컨템포러리 R&B의 문을 열었다.",
             "artists": ["Aaliyah", "TLC", "Timbaland"]},
            {"year": "2001~2004", "era": "Golden Era",
             "title": "Usher·Beyoncé — 팝R&B 전성기",
             "desc": "Usher 'Confessions', Beyoncé 'Dangerously in Love'로 R&B가 팝 메인스트림을 완전 장악.",
             "artists": ["Usher", "Beyoncé", "Alicia Keys"]},
            {"year": "2008~2011", "era": "Experimental",
             "title": "The Weeknd·Frank Ocean — 얼터너티브 R&B",
             "desc": "인디·얼터너티브 정서가 R&B에 유입. 어둡고 내성적인 가사, lo-fi 텍스처가 새로운 미학을 창조.",
             "artists": ["The Weeknd", "Frank Ocean", "Miguel"]},
            {"year": "2016~2019", "era": "Streaming Age",
             "title": "스트리밍 시대의 R&B — 장르 해방",
             "desc": "SZA 'Ctrl', Daniel Caesar 'Freudian', Khalid 'American Teen'이 장르 경계를 완전히 해체.",
             "artists": ["SZA", "Daniel Caesar", "Khalid", "H.E.R."]},
            {"year": "2020~현재", "era": "Post-Genre",
             "title": "포스트 장르 시대",
             "desc": "Brent Faiyaz, Giveon, Bryson Tiller 등 '장르 이름 없는' 아티스트들이 주류로.",
             "artists": ["Brent Faiyaz", "Giveon", "Summer Walker"]},
        ],
    },

    # ────────────────────────
    # 4. New Jack Swing
    # ────────────────────────
    "🎤 New Jack Swing": {
        "desc": "80년대 후반~90년대 초 Teddy Riley가 창시한 장르. 힙합 비트 + 소울 보컬의 완벽한 합성.",
        "color": "#0891b2",
        "tracks": [
            {
                "title": "My Prerogative",
                "artist": "Bobby Brown",
                "year": 1988,
                "desc": "뉴잭스윙의 탄생을 알린 선언적 트랙. Teddy Riley 프로덕션, 힙합 비트 위의 소울 보컬 공식 완성.",
                "yt_query": "Bobby Brown - My Prerogative",
                "vibe": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "📜 가사 & 메시지 (Lyrics & Message)", "🎵 멜로디 (Melody)"],
            },
            {
                "title": "Rump Shaker",
                "artist": "Wreckx-N-Effect",
                "year": 1992,
                "desc": "극도로 댄서블한 뉴잭스윙. 반복되는 비트 패턴과 중독성 있는 훅이 장르 정수를 보여줌.",
                "yt_query": "Wreckx-N-Effect - Rump Shaker",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "📜 가사 & 메시지 (Lyrics & Message)", "🎺 리얼 악기 세션 (Live Instruments)"],
            },
            {
                "title": "Creep",
                "artist": "TLC",
                "year": 1994,
                "desc": "여성 그룹의 관점에서 완성한 뉴잭스윙. 쿨하고 절제된 보컬과 촘촘한 비트의 균형.",
                "yt_query": "TLC - Creep",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "🎵 멜로디 (Melody)", "🎺 리얼 악기 세션 (Live Instruments)"],
            },
        ],
        "tracks_phase2": [
            {
                "title": "Poison", "artist": "Bell Biv DeVoe", "year": 1990,
                "desc": "뉴에디션 출신 BBD의 폭발적 데뷔. '독약 같은 여자'를 경고하는 중독적 훅과 강렬한 뉴잭 비트의 교과서.",
                "yt_query": "Bell Biv DeVoe - Poison",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "🥁 리듬 & 비트 (Rhythm & Beat)", "📜 가사 & 메시지 (Lyrics & Message)"],
            },
            {
                "title": "End of the Road", "artist": "Boyz II Men", "year": 1992,
                "desc": "뉴잭스윙 발라드의 최고봉. Boyz II Men의 4파트 하모니가 이별의 감정을 완벽하게 표현한 역대 최장기 빌보드 1위곡.",
                "yt_query": "Boyz II Men - End of the Road",
                "vibe": ["🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎹 화성 & 코드 진행 (Harmony & Chords)"],
            },
            {
                "title": "Remember the Time", "artist": "Michael Jackson", "year": 1992,
                "desc": "Teddy Riley 프로덕션의 완성형. 이집트 테마 뮤직비디오와 함께 뉴잭스윙을 팝 최정상으로 끌어올린 기념비적 트랙.",
                "yt_query": "Michael Jackson - Remember the Time",
                "vibe": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎸 베이스 & 그루브 (Bass & Groove)", "🎵 멜로디 (Melody)"],
            },
        ],
        "recommendations": [
            {"title": "Poison", "artist": "Bell Biv DeVoe", "year": 1990,
             "tags": ["에너지", "엣지", "뉴잭"], "match_attributes": ["📜 가사 & 메시지 (Lyrics & Message)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"]},
            {"title": "I Want Her", "artist": "Keith Sweat", "year": 1987,
             "tags": ["스무드", "로맨틱", "뉴잭"], "match_attributes": ["📜 가사 & 메시지 (Lyrics & Message)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🎙️ 보컬 & 음색 (Vocal & Tone)"]},
            {"title": "Remember the Time", "artist": "Michael Jackson", "year": 1992,
             "tags": ["팝뉴잭", "클래식", "완성도"], "match_attributes": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎸 베이스 & 그루브 (Bass & Groove)", "🎺 리얼 악기 세션 (Live Instruments)"]},
            {"title": "No Scrubs", "artist": "TLC", "year": 1999,
             "tags": ["걸파워", "팝R&B", "아이코닉"], "match_attributes": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"]},
            {"title": "Motownphilly", "artist": "Boyz II Men", "year": 1991,
             "tags": ["아카펠라", "하모니", "소울"], "match_attributes": ["🎵 멜로디 (Melody)", "📜 가사 & 메시지 (Lyrics & Message)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"]},
        ],
        "timeline": [
            {"year": "1987", "era": "Origin",
             "title": "Teddy Riley — 장르의 창시자",
             "desc": "Guy 밴드의 데뷔와 함께 드럼 머신 비트 + R&B 멜로디 공식을 처음 확립.",
             "artists": ["Teddy Riley", "Guy"]},
            {"year": "1988~1989", "era": "Breakout",
             "title": "Bobby Brown·Keith Sweat — 상업적 폭발",
             "desc": "Bobby Brown 'My Prerogative', Keith Sweat 'Make It Last Forever'가 차트를 점령.",
             "artists": ["Bobby Brown", "Keith Sweat"]},
            {"year": "1991~1992", "era": "Peak",
             "title": "Michael Jackson의 합류 — 메인스트림 정복",
             "desc": "MJ 'Dangerous' 앨범이 뉴잭스윙을 팝 최정상으로 끌어올림.",
             "artists": ["Michael Jackson", "Boyz II Men", "Jodeci"]},
            {"year": "1992~1995", "era": "Evolution",
             "title": "TLC·SWV — 여성 아티스트의 재해석",
             "desc": "TLC가 여성적 관점과 힙합 감성으로 뉴잭스윙을 재정의.",
             "artists": ["TLC", "SWV", "En Vogue"]},
            {"year": "1996~2000", "era": "Decline & Legacy",
             "title": "Timbaland 시대로의 이행",
             "desc": "Timbaland·Missy Elliott가 더 복잡한 비트 구조로 진화시키며 컨템포러리 R&B의 기반이 됨.",
             "artists": ["Timbaland", "Missy Elliott", "Ginuwine"]},
        ],
    },

    # ────────────────────────
    # 5. Quiet Storm R&B
    # ────────────────────────
    "🌊 Quiet Storm R&B": {
        "desc": "70~80년대 라디오 포맷에서 탄생한 어덜트 R&B. 느린 템포, 풍부한 오케스트레이션, 성숙한 가사.",
        "color": "#059669",
        "tracks": [
            {
                "title": "Always and Forever",
                "artist": "Heatwave",
                "year": 1977,
                "desc": "Quiet Storm의 정의. 천천히 흐르는 멜로디, 부드러운 현악, 성숙한 러브송의 교과서.",
                "yt_query": "Heatwave - Always and Forever",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🥁 리듬 & 비트 (Rhythm & Beat)"],
            },
            {
                "title": "Between the Sheets",
                "artist": "The Isley Brothers",
                "year": 1983,
                "desc": "Ron Isley의 실크 같은 보컬. 느린 그루브와 깊은 감성이 Quiet Storm의 진수를 보여줌.",
                "yt_query": "The Isley Brothers - Between the Sheets",
                "vibe": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎺 리얼 악기 세션 (Live Instruments)", "🥁 리듬 & 비트 (Rhythm & Beat)"],
            },
            {
                "title": "At Your Best (You Are Love)",
                "artist": "Aaliyah",
                "year": 1994,
                "desc": "Isley Brothers 원곡을 Aaliyah가 재해석. 10대의 목소리로 Quiet Storm 감성을 현대화한 명곡.",
                "yt_query": "Aaliyah - At Your Best (You Are Love)",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎵 멜로디 (Melody)"],
            },
        ],
        "tracks_phase2": [
            {
                "title": "Never Too Much", "artist": "Luther Vandross", "year": 1981,
                "desc": "Luther Vandross의 데뷔 앨범 타이틀곡. 부드럽고 성숙한 보컬과 댄서블한 그루브가 완벽하게 조화를 이루는 어덜트 R&B의 기준.",
                "yt_query": "Luther Vandross - Never Too Much",
                "vibe": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎸 베이스 & 그루브 (Bass & Groove)", "🎵 멜로디 (Melody)"],
            },
            {
                "title": "Sweet Love", "artist": "Anita Baker", "year": 1986,
                "desc": "재즈와 소울이 결합한 성숙한 러브송. Anita Baker의 독특한 음색과 복잡한 코드 진행이 Quiet Storm 장르의 새 기준을 세웠다.",
                "yt_query": "Anita Baker - Sweet Love",
                "vibe": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🎺 리얼 악기 세션 (Live Instruments)"],
            },
            {
                "title": "Can't Get Enough of Your Love, Babe", "artist": "Barry White", "year": 1974,
                "desc": "Barry White의 심오한 저음과 풍성한 오케스트레이션. Quiet Storm 사운드에서 가장 독특한 보컬 텍스처를 구현한 곡.",
                "yt_query": "Barry White - Can't Get Enough of Your Love Babe",
                "vibe": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎺 리얼 악기 세션 (Live Instruments)", "🎸 베이스 & 그루브 (Bass & Groove)"],
            },
        ],
        "recommendations": [
            {"title": "A Ribbon in the Sky", "artist": "Stevie Wonder", "year": 1982,
             "tags": ["낭만", "피아노", "클래식소울"], "match_attributes": ["🥁 리듬 & 비트 (Rhythm & Beat)", "🎵 멜로디 (Melody)", "🎹 화성 & 코드 진행 (Harmony & Chords)"]},
            {"title": "Never Too Much", "artist": "Luther Vandross", "year": 1981,
             "tags": ["성숙", "스무드", "로맨틱"], "match_attributes": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎸 베이스 & 그루브 (Bass & Groove)", "🎹 화성 & 코드 진행 (Harmony & Chords)"]},
            {"title": "Rock with You", "artist": "Michael Jackson", "year": 1979,
             "tags": ["부드러움", "댄서블", "팝소울"], "match_attributes": ["🥁 리듬 & 비트 (Rhythm & Beat)", "🎸 베이스 & 그루브 (Bass & Groove)", "📜 가사 & 메시지 (Lyrics & Message)"]},
            {"title": "I'll Make Love to You", "artist": "Boyz II Men", "year": 1994,
             "tags": ["로맨틱", "발라드", "아카펠라"], "match_attributes": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎺 리얼 악기 세션 (Live Instruments)", "🥁 리듬 & 비트 (Rhythm & Beat)"]},
            {"title": "Sweet Love", "artist": "Anita Baker", "year": 1986,
             "tags": ["재즈소울", "성숙", "깊이"], "match_attributes": ["📜 가사 & 메시지 (Lyrics & Message)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎸 베이스 & 그루브 (Bass & Groove)"]},
        ],
        "timeline": [
            {"year": "1976", "era": "Origin",
             "title": "WHUR-FM — Quiet Storm 탄생",
             "desc": "워싱턴 DC 라디오 DJ Melvin Lindsey가 야간 프로그램 'Quiet Storm'을 시작.",
             "artists": ["Smokey Robinson", "Marvin Gaye"]},
            {"year": "1977~1981", "era": "Definition",
             "title": "장르의 정의 — 소프트 소울의 황금기",
             "desc": "Luther Vandross, Stephanie Mills, Peabo Bryson 등이 Quiet Storm 포맷을 완성.",
             "artists": ["Luther Vandross", "Peabo Bryson", "Teddy Pendergrass"]},
            {"year": "1983~1986", "era": "Sophistication",
             "title": "재즈와의 결합 — Anita Baker·Sade",
             "desc": "Anita Baker 'Rapture', Sade 'Diamond Life'로 재즈·소울의 성숙한 융합이 완성.",
             "artists": ["Anita Baker", "Sade", "Freddie Jackson"]},
            {"year": "1990s", "era": "Mainstream",
             "title": "Barry White·Boyz II Men — 대중화",
             "desc": "Boyz II Men, Brian McKnight, R. Kelly가 Quiet Storm 감성을 팝 차트로 이동.",
             "artists": ["Boyz II Men", "Brian McKnight", "Barry White"]},
            {"year": "2000s~현재", "era": "Legacy",
             "title": "슬로우 잼의 현재",
             "desc": "John Legend, Musiq Soulchild 등이 Quiet Storm의 성숙한 감성을 현대 R&B에 이식.",
             "artists": ["John Legend", "Musiq Soulchild", "Tweet"]},
        ],
    },

    # ────────────────────────
    # 6. 60~70s Classic Soul / Motown
    # ────────────────────────
    "🎸 60~70s Classic Soul / Motown": {
        "desc": "흑인음악의 뿌리. 모타운 팩토리 사운드, 시민권 운동의 목소리, 소울·리듬앤블루스의 황금 원형.",
        "color": "#b45309",
        "tracks": [
            {
                "title": "What's Going On",
                "artist": "Marvin Gaye",
                "year": 1971,
                "desc": "흑인음악 역사상 가장 위대한 앨범 중 하나. 베트남전·인종차별에 저항하는 시대의 목소리. 재즈·소울·팝의 완벽한 결합.",
                "yt_query": "Marvin Gaye - What's Going On",
                "vibe": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🥁 리듬 & 비트 (Rhythm & Beat)", "📜 가사 & 메시지 (Lyrics & Message)"],
            },
            {
                "title": "Respect",
                "artist": "Aretha Franklin",
                "year": 1967,
                "desc": "소울의 여왕 Aretha Franklin의 아이콘적 곡. 여성 해방과 흑인 자존감의 앤섬. 강렬한 보컬 전달력의 교과서.",
                "yt_query": "Aretha Franklin - Respect",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎸 베이스 & 그루브 (Bass & Groove)", "🎹 화성 & 코드 진행 (Harmony & Chords)"],
            },
            {
                "title": "I Was Made to Love Her",
                "artist": "Stevie Wonder",
                "year": 1967,
                "desc": "10대 Stevie Wonder의 에너지가 폭발하는 Motown 클래식. 브라스와 리듬 섹션이 완벽하게 맞물리는 그루브.",
                "yt_query": "Stevie Wonder - I Was Made to Love Her",
                "vibe": ["🎵 멜로디 (Melody)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)", "📜 가사 & 메시지 (Lyrics & Message)"],
            },
        ],
        "tracks_phase2": [
            {
                "title": "(Sittin' On) The Dock of the Bay", "artist": "Otis Redding", "year": 1967,
                "desc": "Otis Redding가 비행기 사고로 세상을 떠나기 3일 전 녹음한 마지막 명곡. 멜랑꼴리하면서도 아름다운 소울의 영원한 마스터피스.",
                "yt_query": "Otis Redding - Sittin On The Dock Of The Bay",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)"],
            },
            {
                "title": "A Change Is Gonna Come", "artist": "Sam Cooke", "year": 1964,
                "desc": "시민권 운동의 영혼. Sam Cooke의 가장 감동적인 퍼포먼스와 시대를 초월한 희망의 메시지가 담긴 소울의 성경.",
                "yt_query": "Sam Cooke - A Change Is Gonna Come",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎺 리얼 악기 세션 (Live Instruments)"],
            },
            {
                "title": "Move On Up", "artist": "Curtis Mayfield", "year": 1970,
                "desc": "업리프팅한 펑크 비트 위에 담긴 흑인 사회를 향한 진취적 메시지. Curtis Mayfield의 정치적·음악적 정수를 담은 7분짜리 장대한 여정.",
                "yt_query": "Curtis Mayfield - Move On Up",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎸 베이스 & 그루브 (Bass & Groove)", "🎺 리얼 악기 세션 (Live Instruments)"],
            },
        ],
        "recommendations": [
            {"title": "Papa Was a Rollin' Stone", "artist": "The Temptations", "year": 1972,
             "tags": ["사이키델릭소울", "드라마틱", "긴장감"], "match_attributes": ["🥁 리듬 & 비트 (Rhythm & Beat)", "🎺 리얼 악기 세션 (Live Instruments)", "📜 가사 & 메시지 (Lyrics & Message)"]},
            {"title": "I Heard It Through the Grapevine", "artist": "Marvin Gaye", "year": 1968,
             "tags": ["드라마틱", "모타운", "클래식"], "match_attributes": ["🎹 화성 & 코드 진행 (Harmony & Chords)", "📜 가사 & 메시지 (Lyrics & Message)", "🎸 베이스 & 그루브 (Bass & Groove)"]},
            {"title": "Chain of Fools", "artist": "Aretha Franklin", "year": 1967,
             "tags": ["파워풀", "그루브", "소울"], "match_attributes": ["🎹 화성 & 코드 진행 (Harmony & Chords)", "🎸 베이스 & 그루브 (Bass & Groove)", "📜 가사 & 메시지 (Lyrics & Message)"]},
            {"title": "Superstition", "artist": "Stevie Wonder", "year": 1972,
             "tags": ["펑키", "클라비넷", "그루브"], "match_attributes": ["🎺 리얼 악기 세션 (Live Instruments)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎙️ 보컬 & 음색 (Vocal & Tone)"]},
            {"title": "Ain't No Mountain High Enough", "artist": "Marvin Gaye & Tammi Terrell", "year": 1967,
             "tags": ["듀엣", "감동", "클래식모타운"], "match_attributes": ["🎹 화성 & 코드 진행 (Harmony & Chords)", "📜 가사 & 메시지 (Lyrics & Message)", "🎵 멜로디 (Melody)"]},
        ],
        "timeline": [
            {"year": "1959~1961", "era": "Birth",
             "title": "Berry Gordy — 모타운 레코드 설립",
             "desc": "Detroit의 자동차 공장 노동자 Berry Gordy가 $800로 Motown을 창업. 흑인 음악을 백인 주류 시장에 팔겠다는 혁명적 비전.",
             "artists": ["Berry Gordy", "The Miracles", "Smokey Robinson"]},
            {"year": "1963~1966", "era": "Factory Sound",
             "title": "모타운 팩토리 사운드의 완성",
             "desc": "Funk Brothers 세션 밴드, Holland-Dozier-Holland 작곡팀. Supremes, Temptations, Four Tops로 전 세계 차트 정복.",
             "artists": ["The Supremes", "The Temptations", "Four Tops"]},
            {"year": "1967~1969", "era": "Soul Revolution",
             "title": "Atlantic Soul — Aretha·Otis의 시대",
             "desc": "Stax·Atlantic 레이블의 거친 소울이 Motown과 경쟁. 시민권 운동과 음악의 결합.",
             "artists": ["Aretha Franklin", "Otis Redding", "Sam Cooke"]},
            {"year": "1971~1974", "era": "Conscious Soul",
             "title": "Marvin Gaye·Stevie Wonder — 예술적 독립",
             "desc": "'What's Going On', 'Innervisions' 등 사회의식 담은 명작 탄생.",
             "artists": ["Marvin Gaye", "Stevie Wonder", "Curtis Mayfield"]},
            {"year": "1975~1979", "era": "Disco Era",
             "title": "소울에서 디스코로의 이행",
             "desc": "모타운과 소울이 디스코의 물결에 적응. 소울의 감성은 디스코 속에서 살아남음.",
             "artists": ["Commodores", "Diana Ross", "Lionel Richie"]},
            {"year": "현재", "era": "Legacy",
             "title": "모든 흑인음악의 DNA",
             "desc": "네오소울, 힙합, 컨템포러리 R&B의 모든 샘플과 감성의 원점.",
             "artists": ["Beyoncé", "Kendrick Lamar", "Leon Bridges"]},
        ],
    },

    # ────────────────────────
    # 7. 90s Hip-Hop Soul
    # ────────────────────────
    "🎧 90s Hip-Hop Soul": {
        "desc": "90년대 힙합의 날카로움과 R&B의 감성이 결합한 폭발적 장르. Mary J. Blige, Brandy, Puff Daddy가 정의한 시대.",
        "color": "#dc2626",
        "tracks": [
            {
                "title": "Real Love",
                "artist": "Mary J. Blige",
                "year": 1992,
                "desc": "힙합소울의 창시자 Mary J. Blige의 대표곡. 힙합 비트 위의 날 것 그대로의 감성. '거리의 소울'이라는 새 언어를 만들었다.",
                "yt_query": "Mary J. Blige - Real Love",
                "vibe": ["🎵 멜로디 (Melody)", "🎸 베이스 & 그루브 (Bass & Groove)", "🥁 리듬 & 비트 (Rhythm & Beat)"],
            },
            {
                "title": "Waterfalls",
                "artist": "TLC",
                "year": 1995,
                "desc": "힙합소울의 사회의식. T-Boz·Left Eye·Chilli 3인방이 에이즈·마약·폭력을 정면으로 노래. 장르가 메시지를 품은 순간.",
                "yt_query": "TLC - Waterfalls",
                "vibe": ["🎺 리얼 악기 세션 (Live Instruments)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🎙️ 보컬 & 음색 (Vocal & Tone)"],
            },
            {
                "title": "I'll Be Missing You",
                "artist": "Puff Daddy & Faith Evans",
                "year": 1997,
                "desc": "Notorious B.I.G. 추모곡. 힙합과 소울이 애도라는 감정 위에서 완벽하게 결합된 역사적 트랙.",
                "yt_query": "Puff Daddy & Faith Evans - I'll Be Missing You",
                "vibe": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🎵 멜로디 (Melody)"],
            },
        ],
        "tracks_phase2": [
            {
                "title": "One in a Million", "artist": "Aaliyah", "year": 1996,
                "desc": "Timbaland 프로덕션의 혁신. 변칙적인 드럼 패턴과 Aaliyah의 쿨한 보컬이 결합해 R&B의 미래를 제시한 세기의 명곡.",
                "yt_query": "Aaliyah - One in a Million",
                "vibe": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎙️ 보컬 & 음색 (Vocal & Tone)"],
            },
            {
                "title": "Have You Ever", "artist": "Brandy", "year": 1998,
                "desc": "Brandy의 섬세한 감성과 뛰어난 멜리스마. 90년대 힙합소울 발라드의 정점이자 보컬 기교의 살아있는 교과서.",
                "yt_query": "Brandy - Have You Ever",
                "vibe": ["🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎹 화성 & 코드 진행 (Harmony & Chords)"],
            },
            {
                "title": "If I Ruled the World", "artist": "Nas ft. Lauryn Hill", "year": 1996,
                "desc": "Nas의 철학적 가사와 Lauryn Hill의 감성적 훅이 완벽하게 결합. 힙합소울의 의식적 측면을 완성한 시대의 명곡.",
                "yt_query": "Nas ft. Lauryn Hill - If I Ruled the World",
                "vibe": ["📜 가사 & 메시지 (Lyrics & Message)", "🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)"],
            },
        ],
        "recommendations": [
            {"title": "Not Gon' Cry", "artist": "Mary J. Blige", "year": 1995,
             "tags": ["감성", "파워보컬", "힙합소울"], "match_attributes": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎸 베이스 & 그루브 (Bass & Groove)", "🎙️ 보컬 & 음색 (Vocal & Tone)"]},
            {"title": "The Boy Is Mine", "artist": "Brandy & Monica", "year": 1998,
             "tags": ["듀엣", "대결", "팝R&B"], "match_attributes": ["📜 가사 & 메시지 (Lyrics & Message)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🎙️ 보컬 & 음색 (Vocal & Tone)"]},
            {"title": "One in a Million", "artist": "Aaliyah", "year": 1996,
             "tags": ["미래적", "그루브", "쿨"], "match_attributes": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🥁 리듬 & 비트 (Rhythm & Beat)"]},
            {"title": "If I Ruled the World", "artist": "Nas ft. Lauryn Hill", "year": 1996,
             "tags": ["의식적", "힙합", "소울"], "match_attributes": ["🥁 리듬 & 비트 (Rhythm & Beat)", "🎺 리얼 악기 세션 (Live Instruments)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"]},
            {"title": "No Diggity", "artist": "Blackstreet ft. Dr. Dre", "year": 1996,
             "tags": ["그루브", "스무드", "힙합R&B"], "match_attributes": ["🎺 리얼 악기 세션 (Live Instruments)", "🎸 베이스 & 그루브 (Bass & Groove)", "🥁 리듬 & 비트 (Rhythm & Beat)"]},
        ],
        "timeline": [
            {"year": "1991~1992", "era": "Birth",
             "title": "Mary J. Blige — 힙합소울의 탄생",
             "desc": "Sean 'Puffy' Combs 프로덕션으로 'What's the 411?' 발매. '힙합 소울'이라는 카테고리 창조.",
             "artists": ["Mary J. Blige", "Sean 'Puffy' Combs"]},
            {"year": "1993~1995", "era": "Explosion",
             "title": "TLC·SWV·Xscape — 여성 그룹의 전성기",
             "desc": "힙합소울이 여성 그룹을 통해 폭발적으로 확산.",
             "artists": ["TLC", "SWV", "Xscape", "En Vogue"]},
            {"year": "1994~1997", "era": "Timbaland Revolution",
             "title": "Timbaland의 비트 혁명",
             "desc": "Aaliyah 'One in a Million'으로 Timbaland가 힙합소울의 리듬 언어를 완전히 재설계.",
             "artists": ["Timbaland", "Aaliyah", "Missy Elliott"]},
            {"year": "1997~1999", "era": "Bad Boy Era",
             "title": "Bad Boy 레이블 — 힙합소울의 글래머화",
             "desc": "Puff Daddy·Bad Boy 사운드가 힙합소울에 럭셔리와 화려함을 더함.",
             "artists": ["Faith Evans", "112", "Puff Daddy"]},
            {"year": "2000~현재", "era": "Legacy",
             "title": "힙합소울의 유산 — R&B의 표준이 되다",
             "desc": "힙합소울의 문법이 이후 모든 R&B의 기본 문법으로 편입.",
             "artists": ["Beyoncé", "Rihanna", "Destiny's Child"]},
        ],
    },

    # ────────────────────────
    # 8. Afrobeats / Dancehall
    # ────────────────────────
    "🌍 Afrobeats / Dancehall": {
        "desc": "서아프리카·카리브해의 리듬이 세계 팝 무대로. Burna Boy, WizKid, Dancehall 사운드가 만드는 글로벌 그루브.",
        "color": "#16a34a",
        "tracks": [
            {
                "title": "Come Closer",
                "artist": "WizKid ft. Drake",
                "year": 2017,
                "desc": "아프로비츠가 글로벌 팝을 정복한 순간. WizKid의 기타 기반 아프로팝과 Drake의 감성이 결합된 시대 정의적 트랙.",
                "yt_query": "WizKid ft. Drake - Come Closer",
                "vibe": ["🎹 화성 & 코드 진행 (Harmony & Chords)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎵 멜로디 (Melody)"],
            },
            {
                "title": "Essence",
                "artist": "WizKid ft. Tems",
                "year": 2020,
                "desc": "아프로비츠 역사상 가장 아름다운 트랙 중 하나. Tems의 독특한 보컬과 유기적 그루브가 완벽하게 맞물림.",
                "yt_query": "WizKid ft. Tems - Essence",
                "vibe": ["🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎹 화성 & 코드 진행 (Harmony & Chords)"],
            },
            {
                "title": "Ye",
                "artist": "Burna Boy",
                "year": 2018,
                "desc": "아프로퓨전의 교과서. 댄스홀·레게·아프로비츠가 하나로 융합되어 'Afro-Fusion'이라는 독자 언어를 완성.",
                "yt_query": "Burna Boy - Ye",
                "vibe": ["🎵 멜로디 (Melody)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎹 화성 & 코드 진행 (Harmony & Chords)"],
            },
        ],
        "tracks_phase2": [
            {
                "title": "Fall", "artist": "Davido", "year": 2017,
                "desc": "나이지리아 출신으로 빌보드 최장기 아프리카 차트 기록. Davido의 개성 넘치는 보컬과 중독적인 아프로팝 훅의 완벽한 조화.",
                "yt_query": "Davido - Fall",
                "vibe": ["🎵 멜로디 (Melody)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎹 화성 & 코드 진행 (Harmony & Chords)"],
            },
            {
                "title": "Temperature", "artist": "Sean Paul", "year": 2005,
                "desc": "댄스홀이 세계 팝 차트를 정복한 순간. Sean Paul의 패턴화된 플로우와 열기 넘치는 리듬이 만드는 순수한 파티 에너지.",
                "yt_query": "Sean Paul - Temperature",
                "vibe": ["🎸 베이스 & 그루브 (Bass & Groove)", "🥁 리듬 & 비트 (Rhythm & Beat)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"],
            },
            {
                "title": "Free Mind", "artist": "Tems", "year": 2020,
                "desc": "Tems의 독보적 음색이 처음으로 세계에 알려진 곡. 아프로소울과 얼터너티브 R&B가 결합된 독창적이고 영적인 사운드.",
                "yt_query": "Tems - Free Mind",
                "vibe": ["🎙️ 보컬 & 음색 (Vocal & Tone)", "📜 가사 & 메시지 (Lyrics & Message)", "🎵 멜로디 (Melody)"],
            },
        ],
        "recommendations": [
            {"title": "Last Last", "artist": "Burna Boy", "year": 2022,
             "tags": ["감성", "아프로퓨전", "서사"], "match_attributes": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "📜 가사 & 메시지 (Lyrics & Message)", "🥁 리듬 & 비트 (Rhythm & Beat)"]},
            {"title": "Temperature", "artist": "Sean Paul", "year": 2005,
             "tags": ["댄스홀", "댄서블", "파티"], "match_attributes": ["🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🎹 화성 & 코드 진행 (Harmony & Chords)", "🎙️ 보컬 & 음색 (Vocal & Tone)"]},
            {"title": "Soco", "artist": "WizKid", "year": 2018,
             "tags": ["아프로팝", "축제", "밝음"], "match_attributes": ["📜 가사 & 메시지 (Lyrics & Message)", "🎵 멜로디 (Melody)", "🎹 화성 & 코드 진행 (Harmony & Chords)"]},
            {"title": "Ojuelegba", "artist": "WizKid", "year": 2014,
             "tags": ["향수", "스트리트", "멜로디"], "match_attributes": ["🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)", "🎹 화성 & 코드 진행 (Harmony & Chords)"]},
            {"title": "Calm Down", "artist": "Rema", "year": 2022,
             "tags": ["아프로팝", "댄서블", "로맨틱"], "match_attributes": ["🎸 베이스 & 그루브 (Bass & Groove)", "📜 가사 & 메시지 (Lyrics & Message)", "🥁 리듬 & 비트 (Rhythm & Beat)"]},
        ],
        "timeline": [
            {"year": "1970s", "era": "Roots",
             "title": "Fela Kuti — 아프로비트(Afrobeat)의 원조",
             "desc": "나이지리아의 음악가·활동가 Fela Kuti가 재즈·펑크·요루바 전통 음악을 결합해 'Afrobeat' 창조.",
             "artists": ["Fela Kuti", "Tony Allen"]},
            {"year": "1980s", "era": "Dancehall Birth",
             "title": "자메이카 댄스홀의 탄생",
             "desc": "레게에서 파생된 댄스홀이 Kingston 클럽 문화에서 독립 장르로 성장.",
             "artists": ["Yellowman", "Shabba Ranks"]},
            {"year": "2000s", "era": "Mainstream Dancehall",
             "title": "Sean Paul·Beenie Man — 댄스홀의 글로벌화",
             "desc": "Sean Paul 'Dutty Rock'이 전 세계 차트를 석권.",
             "artists": ["Sean Paul", "Beenie Man", "Shaggy"]},
            {"year": "2010~2016", "era": "Afrobeats Rise",
             "title": "현대 Afrobeats의 탄생 — Lagos 클럽씬",
             "desc": "나이지리아 Lagos를 중심으로 WizKid, Davido, P-Square가 현대적 아프로비츠 공식 완성.",
             "artists": ["WizKid", "Davido", "P-Square"]},
            {"year": "2017~2020", "era": "Global Takeover",
             "title": "Drake·Beyoncé와의 협업 — 세계 정복",
             "desc": "WizKid-Drake 'One Dance', Beyoncé 'The Lion King: The Gift'로 아프로비츠가 서구 팝 주류에 완전 편입.",
             "artists": ["Burna Boy", "WizKid", "Tems"]},
            {"year": "2021~현재", "era": "Afrobeats Dominance",
             "title": "Burna Boy — Grammy & 세계 무대",
             "desc": "Burna Boy 그래미 수상, Tems·Ayra Starr·Rema의 부상. 아프로비츠가 글로벌 팝의 새 문법으로 자리잡음.",
             "artists": ["Burna Boy", "Tems", "Rema", "Ayra Starr"]},
        ],
    },
}

# ── 매력 요소 목록 ──
ATTRIBUTES = [
    "🎵 멜로디 (Melody)",
    "🥁 리듬 & 비트 (Rhythm & Beat)",
    "🎸 베이스 & 그루브 (Bass & Groove)",
    "🎙️ 보컬 & 음색 (Vocal & Tone)",
    "🎹 화성 & 코드 진행 (Harmony & Chords)",
    "🎺 리얼 악기 세션 (Live Instruments)",
    "🎛️ 사운드 믹싱 & 질감 (Sound Design)",
    "📜 가사 & 메시지 (Lyrics & Message)"
]

# ── 페르소나 프리셋 ──
PERSONA_MAP = [
    ({"🎸 베이스 & 그루브 (Bass & Groove)", "🥁 리듬 & 비트 (Rhythm & Beat)"}, "리듬 & 그루브 마스터 🕺\n음악의 심장인 드럼과 베이스가 만들어내는 본능적인 리듬을 사랑합니다."),
    ({"🎵 멜로디 (Melody)", "🎙️ 보컬 & 음색 (Vocal & Tone)"}, "소울풀 하모니 리스너 🎙️\n가수의 감미로운 목소리와 귀를 사로잡는 선율에 가장 먼저 반응하시네요."),
    ({"🎹 화성 & 코드 진행 (Harmony & Chords)", "🎺 리얼 악기 세션 (Live Instruments)"}, "어쿠스틱 & 재지 바이브 🎺\n복잡한 화성과 살아 숨쉬는 리얼 악기의 유기적인 연주를 즐기는 고급 취향!"),
    ({"🎛️ 사운드 믹싱 & 질감 (Sound Design)", "🥁 리듬 & 비트 (Rhythm & Beat)"}, "트렌디 사운드 디자이너 ☁️\n혁신적인 비트와 입체적인 사운드 텍스처 등 꼼꼼한 프로덕션에 감탄합니다."),
    ({"📜 가사 & 메시지 (Lyrics & Message)", "🎙️ 보컬 & 음색 (Vocal & Tone)"}, "감성 폭발 스토리텔러 📖\n가사 속에 담긴 깊은 이야기와 그것을 전달하는 보컬의 감정선에 몰입합니다."),
    ({"🎸 베이스 & 그루브 (Bass & Groove)", "🎛️ 사운드 믹싱 & 질감 (Sound Design)"}, "다크 & 딥 베이스 헌터 🦇\n무겁게 깔리는 베이스라인과 몽환적인 믹싱이 주는 특유의 공간감을 선호합니다."),
    ({"🎵 멜로디 (Melody)", "🎹 화성 & 코드 진행 (Harmony & Chords)"}, "클래식 멜로디 탐험가 🎼\n아름다운 코드 진행 위에 얹어진 우아한 멜로디 라인을 들을 때 행복을 느낍니다."),
    ({"🎺 리얼 악기 세션 (Live Instruments)", "🎙️ 보컬 & 음색 (Vocal & Tone)"}, "라이브 스테이지 매니아 🎸\n마치 공연장에 있는 듯 생동감 넘치는 악기 연주와 폭발적인 보컬을 사랑합니다.")
]

# ── 타임라인 노드 스타일 (Airbnb 토큰 기반) ──
# canvas / surface-soft / surface-strong + ink/rausch 테두리
TIMELINE_NODE_STYLES = [
    {"bg": "#222222", "border": "#222222", "text": "#ffffff"},
    {"bg": "#f7f7f7", "border": "#dddddd", "text": "#222222"},
    {"bg": "#ff385c", "border": "#ff385c", "text": "#ffffff"},
    {"bg": "#f2f2f2", "border": "#c1c1c1", "text": "#222222"},
    {"bg": "#ffffff", "border": "#222222", "text": "#222222"},
    {"bg": "#e00b41", "border": "#e00b41", "text": "#ffffff"},
]

# ── 아티스트별 대표곡 데이터 (YouTube 검색 링크 연결용) ──
ARTIST_SONGS = {
    # Neo-Soul
    "Al Green":          [("Let's Stay Together", 1972), ("Tired of Being Alone", 1971), ("I'm Still in Love with You", 1972)],
    "Stevie Wonder":     [("Superstition", 1972), ("Sir Duke", 1977), ("Isn't She Lovely", 1976)],
    "Marvin Gaye":       [("What's Going On", 1971), ("Let's Get It On", 1973), ("Sexual Healing", 1982)],
    "D'Angelo":          [("Brown Sugar", 1995), ("Untitled (How Does It Feel)", 2000), ("Really Love", 2014)],
    "Erykah Badu":       [("On & On", 1997), ("Bag Lady", 2000), ("Tyrone", 1997)],
    "Lauryn Hill":       [("Ex-Factor", 1998), ("Doo Wop (That Thing)", 1998), ("Everything Is Everything", 1998)],
    "Common":            [("The Light", 2000), ("Be", 2005), ("Come Close", 2002)],
    "Mos Def":           [("Ms. Fat Booty", 1999), ("Umi Says", 1999), ("Mathematics", 1999)],
    "Q-Tip":             [("Vivrant Thing", 1999), ("Breathe and Stop", 1999), ("Electric Relaxation", 1993)],
    "J Dilla":           [("Workinonit", 2006), ("Time: The Donut of the Heart", 2006), ("So Far to Go", 2007)],
    "Questlove":         [("You Got Me", 1999), ("The Seed (2.0)", 2002), ("Break You Off", 2002)],
    "Anderson .Paak":    [("Come Down", 2016), ("Bubblin", 2018), ("Make It Better", 2019)],
    "Frank Ocean":       [("Thinkin Bout You", 2012), ("Pyramids", 2012), ("Nights", 2016)],
    "Noname":            [("Telefone", 2016), ("Room 25", 2018), ("Song 33", 2020)],
    "Syd":               [("Body", 2017), ("All About Me", 2017), ("Fast Car", 2017)],
    "Me'Shell NdegéOcello": [("If That's Your Boyfriend", 1993), ("Faithful", 1999), ("Leviticus: Faggot", 1996)],
    "Tony! Toni! Toné!": [("Anniversary", 1993), ("Feels Good", 1990), ("If I Had No Loot", 1993)],
    "Anita Baker":       [("Sweet Love", 1986), ("Caught Up in the Rapture", 1986), ("Giving You the Best That I Got", 1988)],
    # Funk
    "James Brown":       [("I Got You (I Feel Good)", 1965), ("Papa's Got a Brand New Bag", 1965), ("Sex Machine", 1970)],
    "The Famous Flames": [("Please Please Please", 1956), ("Try Me", 1958)],
    "Sly Stone":         [("Everyday People", 1968), ("Family Affair", 1971), ("Thank You (Falettinme Be Mice Elf Agin)", 1969)],
    "Larry Graham":      [("One in a Million You", 1980), ("Thank You", 1969)],
    "George Clinton":    [("Atomic Dog", 1982), ("Flash Light", 1977), ("Give Up the Funk", 1975)],
    "Bootsy Collins":    [("Stretchin' Out", 1976), ("I'd Rather Be with You", 1976), ("Bootzilla", 1978)],
    "Bernie Worrell":    [("Flash Light", 1977), ("Aqua Boogie", 1978)],
    "Earth, Wind & Fire": [("September", 1978), ("Boogie Wonderland", 1979), ("Let's Groove", 1981)],
    "Chic":              [("Le Freak", 1978), ("Good Times", 1979), ("Dance, Dance, Dance", 1977)],
    "Nile Rodgers":      [("Le Freak", 1978), ("Get Lucky", 2013), ("Good Times", 1979)],
    "Kool & The Gang":   [("Jungle Boogie", 1973), ("Celebration", 1980), ("Get Down on It", 1981)],
    "The Isley Brothers": [("That Lady", 1973), ("Between the Sheets", 1983), ("For the Love of You", 1975)],
    "Prince":            [("Purple Rain", 1984), ("When Doves Cry", 1984), ("Kiss", 1986)],
    "Rick James":        [("Super Freak", 1981), ("Give It to Me Baby", 1981), ("Fire and Desire", 1981)],
    "Zapp":              [("More Bounce to the Ounce", 1980), ("Doo Wa Ditty", 1982)],
    "Kendrick Lamar":    [("Alright", 2015), ("HUMBLE.", 2017), ("Swimming Pools", 2012)],
    "Bruno Mars":        [("Uptown Funk", 2014), ("That's What I Like", 2016), ("Locked Out of Heaven", 2012)],
    # Contemporary R&B
    "Aaliyah":           [("Are You That Somebody", 1998), ("Try Again", 2000), ("More Than a Woman", 2001)],
    "Timbaland":         [("The Way I Are", 2007), ("Give It to Me", 2007), ("Apologize", 2007)],
    "Missy Elliott":     [("Work It", 2002), ("Get Ur Freak On", 2001), ("Lose Control", 2005)],
    "Usher":             [("Yeah!", 2004), ("Burn", 2004), ("Confessions Part II", 2004)],
    "Beyoncé":           [("Crazy in Love", 2003), ("Irreplaceable", 2006), ("Formation", 2016)],
    "Alicia Keys":       [("Fallin'", 2001), ("If I Ain't Got You", 2003), ("No One", 2007)],
    "The Weeknd":        [("Blinding Lights", 2019), ("Save Your Tears", 2020), ("Die For You", 2016)],
    "Miguel":            [("Adorn", 2012), ("Sure Thing", 2010), ("Coffee", 2015)],
    "SZA":               [("Good Days", 2020), ("Kill Bill", 2022), ("Broken Clocks", 2017)],
    "Daniel Caesar":     [("Best Part", 2017), ("Get You", 2016), ("Blessed", 2017)],
    "Khalid":            [("Location", 2016), ("Young Dumb & Broke", 2017), ("Better", 2019)],
    "H.E.R.":            [("Focus", 2016), ("Best Part", 2017), ("Come Through", 2017)],
    "Brent Faiyaz":      [("Clouded", 2020), ("Dead Man Walking", 2022), ("Wasting Time", 2021)],
    "Giveon":            [("Heartbreak Anniversary", 2020), ("Like I Want You", 2020), ("For Tonight", 2021)],
    "Summer Walker":     [("Girls Need Love", 2018), ("Playing Games", 2019), ("Come Thru", 2019)],
    # New Jack Swing
    "Teddy Riley":       [("My Prerogative", 1988), ("Rump Shaker", 1992), ("No Diggity", 1996)],
    "Bobby Brown":       [("My Prerogative", 1988), ("Don't Be Cruel", 1988), ("Every Little Step", 1989)],
    "Keith Sweat":       [("Make It Last Forever", 1987), ("I Want Her", 1987), ("Twisted", 1996)],
    "Michael Jackson":   [("Thriller", 1982), ("Billie Jean", 1982), ("Remember the Time", 1992)],
    "Boyz II Men":       [("End of the Road", 1992), ("I'll Make Love to You", 1994), ("Motownphilly", 1991)],
    "Jodeci":            [("Cry for You", 1993), ("Forever My Lady", 1991), ("Stay", 1995)],
    "TLC":               [("Waterfalls", 1994), ("No Scrubs", 1999), ("Creep", 1994)],
    "SWV":               [("Weak", 1992), ("Right Here", 1992), ("You're the One", 1996)],
    "En Vogue":          [("Hold On", 1990), ("Don't Let Go (Love)", 1996), ("Never Gonna Get It", 1992)],
    "Ginuwine":          [("Pony", 1996), ("Same Ol' G", 1999), ("In Those Jeans", 2003)],
    "Wreckx-N-Effect":   [("Rump Shaker", 1992), ("New Jack Swing", 1988)],
    "Guy":               [("Groove Me", 1988), ("I Like", 1988), ("Teddy's Jam", 1988)],
    "Bell Biv DeVoe":    [("Poison", 1990), ("Do Me!", 1990), ("BBD (I Thought It Was Me)?", 1990)],
    "Xscape":            [("Just Kickin' It", 1993), ("Understanding", 1993), ("Who Can I Run To", 1995)],
    # Quiet Storm
    "Smokey Robinson":   [("Cruisin'", 1979), ("Being with You", 1981), ("Tears of a Clown", 1967)],
    "Luther Vandross":   [("Never Too Much", 1981), ("Here and Now", 1989), ("Dance with My Father", 2003)],
    "Peabo Bryson":      [("Feel the Fire", 1977), ("A Whole New World", 1992), ("Tonight, I Celebrate My Love", 1983)],
    "Teddy Pendergrass": [("Close the Door", 1978), ("Turn Off the Lights", 1979), ("Love T.K.O.", 1980)],
    "Sade":              [("Smooth Operator", 1984), ("No Ordinary Love", 1992), ("By Your Side", 2000)],
    "Freddie Jackson":   [("Rock Me Tonight", 1985), ("You Are My Lady", 1985), ("Have You Ever Loved Somebody", 1986)],
    "Brian McKnight":    [("Back at One", 1999), ("One Last Cry", 1992), ("Never Felt This Way", 1992)],
    "Barry White":       [("Can't Get Enough of Your Love, Babe", 1974), ("You're the First, the Last, My Everything", 1974)],
    "Musiq Soulchild":   [("Just Friends (Sunny)", 2000), ("Halfcrazy", 2002), ("Love", 2000)],
    "Tweet":             [("Oops (Oh My)", 2002), ("Call Me", 2002)],
    "John Legend":       [("All of Me", 2013), ("Ordinary People", 2004), ("Green Light", 2006)],
    # Classic Soul / Motown
    "Berry Gordy":       [("Money (That's What I Want)", 1959), ("Do You Love Me", 1962)],
    "The Miracles":      [("Shop Around", 1960), ("Tears of a Clown", 1967), ("Tracks of My Tears", 1965)],
    "The Supremes":      [("Where Did Our Love Go", 1964), ("Stop! In the Name of Love", 1965), ("You Can't Hurry Love", 1966)],
    "The Temptations":   [("My Girl", 1964), ("Ain't Too Proud to Beg", 1966), ("Papa Was a Rollin' Stone", 1972)],
    "Four Tops":         [("I Can't Help Myself", 1965), ("Reach Out I'll Be There", 1966), ("Bernadette", 1967)],
    "Aretha Franklin":   [("Respect", 1967), ("Chain of Fools", 1967), ("Think", 1968)],
    "Otis Redding":      [("(Sittin' On) The Dock of the Bay", 1967), ("Try a Little Tenderness", 1966), ("I've Been Loving You Too Long", 1965)],
    "Sam Cooke":         [("A Change Is Gonna Come", 1964), ("Wonderful World", 1960), ("Chain Gang", 1960)],
    "Curtis Mayfield":   [("Move On Up", 1970), ("Superfly", 1972), ("People Get Ready", 1965)],
    "Commodores":        [("Easy", 1977), ("Brick House", 1977), ("Three Times a Lady", 1978)],
    "Diana Ross":        [("Ain't No Mountain High Enough", 1970), ("I'm Coming Out", 1980), ("Endless Love", 1981)],
    "Lionel Richie":     [("All Night Long", 1983), ("Hello", 1984), ("Say You, Say Me", 1985)],
    "Leon Bridges":      [("Coming Home", 2015), ("River", 2015), ("Bad Bad News", 2018)],
    # Hip-Hop Soul
    "Mary J. Blige":     [("Real Love", 1992), ("Be Without You", 2005), ("Not Gon' Cry", 1995)],
    "Sean 'Puffy' Combs": [("I'll Be Missing You", 1997), ("Mo Money Mo Problems", 1997)],
    "Brandy":            [("Have You Ever", 1998), ("The Boy Is Mine", 1998), ("Almost Doesn't Count", 1998)],
    "Monica":            [("Angel of Mine", 1998), ("The First Night", 1998)],
    "Nas":               [("N.Y. State of Mind", 1994), ("If I Ruled the World", 1996), ("One Love", 1994)],
    "Faith Evans":       [("I'll Be Missing You", 1997), ("Soon as I Get Home", 1995), ("Ain't Nobody", 2005)],
    "112":               [("Peaches & Cream", 2001), ("Only You", 1996), ("Dance with Me", 1998)],
    "Puff Daddy":        [("I'll Be Missing You", 1997), ("Mo Money Mo Problems", 1997), ("Been Around the World", 1997)],
    "Rihanna":           [("Umbrella", 2007), ("We Found Love", 2011), ("Diamonds", 2012)],
    "Destiny's Child":   [("Say My Name", 1999), ("Survivor", 2001), ("Bootylicious", 2001)],
    # Afrobeats / Dancehall
    "Fela Kuti":         [("Zombie", 1977), ("Lady", 1972), ("Water No Get Enemy", 1975)],
    "Tony Allen":        [("Jealousy", 2009), ("Black Voices", 2017), ("Go Back", 2020)],
    "WizKid":            [("Essence", 2020), ("Come Closer", 2017), ("Soco", 2018)],
    "Davido":            [("Fall", 2017), ("If", 2017), ("FEM", 2020)],
    "P-Square":          [("Personally", 2005), ("Do Me", 2007), ("Temptation", 2009)],
    "Burna Boy":         [("Ye", 2018), ("Last Last", 2022), ("Location", 2019)],
    "Tems":              [("Free Mind", 2020), ("Higher", 2022), ("Essence (feat. Wizkid)", 2020)],
    "Rema":              [("Calm Down", 2022), ("Dumebi", 2019), ("Iron Man", 2019)],
    "Ayra Starr":        [("Rush", 2023), ("Bloody Samaritan", 2021), ("Sability", 2021)],
    "Sean Paul":         [("Temperature", 2005), ("Get Busy", 2002), ("No Lie", 2012)],
    "Beenie Man":        [("Who Am I", 1997), ("Girls", 2004), ("Dude", 2004)],
    "Shaggy":            [("It Wasn't Me", 2000), ("Angel", 2000), ("Boombastic", 1995)],
    "Yellowman":         [("Nobody Move Nobody Get Hurt", 1982), ("Zungguzungguguzungguzeng", 1983)],
    "Shabba Ranks":      [("Mr. Loverman", 1992), ("Trailer Load a Girls", 1992), ("Twice My Age", 1992)],
    # Raphael Saadiq (Neo-Soul recommendations)
    "Raphael Saadiq":    [("Be Here", 2004), ("Never Give You Up", 2008), ("Love That Girl", 2011)],
    "Maxwell":           [("This Woman's Work", 1996), ("Fortunate", 1998), ("Pretty Wings", 2009)],
    "Heatwave":          [("Always and Forever", 1977), ("Boogie Nights", 1977)],
    "Blackstreet":       [("No Diggity", 1996), ("Before I Let You Go", 1994)],
}

# ── 태그 키워드 → 관련 추천곡 딕셔너리 ──
TAG_SONGS: dict[str, list[tuple[str, str, int]]] = {
    # ── 분위기 ──
    "그루브": [
        ("Superstition",            "Stevie Wonder",        1972),
        ("Super Freak",             "Rick James",           1981),
        ("Flash Light",             "Parliament",           1977),
        ("Sex Machine",             "James Brown",          1970),
        ("That Lady",               "The Isley Brothers",   1973),
    ],
    "감성": [
        ("Ex-Factor",               "Lauryn Hill",          1998),
        ("Ordinary People",         "John Legend",          2004),
        ("Die For You",             "The Weeknd",           2016),
        ("Best Part",               "Daniel Caesar",        2017),
        ("Pretty Wings",            "Maxwell",              2009),
    ],
    "빈티지": [
        ("Brown Sugar",             "D'Angelo",             1995),
        ("On & On",                 "Erykah Badu",          1997),
        ("Always and Forever",      "Heatwave",             1977),
        ("My Girl",                 "The Temptations",      1964),
        ("Be Here",                 "Raphael Saadiq",       2004),
    ],
    "로맨틱": [
        ("Never Too Much",          "Luther Vandross",      1981),
        ("Here and Now",            "Luther Vandross",      1989),
        ("All of Me",               "John Legend",          2013),
        ("Sweet Love",              "Anita Baker",          1986),
        ("I'll Make Love to You",   "Boyz II Men",          1994),
    ],
    "위로": [
        ("Bag Lady",                "Erykah Badu",          2000),
        ("A Change Is Gonna Come",  "Sam Cooke",            1964),
        ("Ain't No Mountain High",  "Marvin Gaye",          1967),
        ("Keep Ya Head Up",         "2Pac",                 1993),
        ("I Smile",                 "Kirk Franklin",        2011),
    ],
    "스무드": [
        ("Smooth Operator",         "Sade",                 1984),
        ("No Diggity",              "Blackstreet",          1996),
        ("Cruisin'",                "Smokey Robinson",      1979),
        ("Step in the Name of Love","R. Kelly",             2003),
        ("Fortunate",               "Maxwell",              1998),
    ],
    "쿨": [
        ("One in a Million",        "Aaliyah",              1996),
        ("Come Through",            "H.E.R.",               2017),
        ("Good Days",               "SZA",                  2020),
        ("Channel Orange",          "Frank Ocean",          2012),
        ("Clouded",                 "Brent Faiyaz",         2020),
    ],
    "세련됨": [
        ("Climax",                  "Usher",                2012),
        ("By Your Side",            "Sade",                 2000),
        ("Nights",                  "Frank Ocean",          2016),
        ("Adorn",                   "Miguel",               2012),
        ("Die For You",             "The Weeknd",           2016),
    ],
    "의식적": [
        ("What's Going On",         "Marvin Gaye",          1971),
        ("The Message",             "Grandmaster Flash",    1982),
        ("Alright",                 "Kendrick Lamar",       2015),
        ("If I Ruled the World",    "Nas",                  1996),
        ("Be",                      "Common",               2005),
    ],
    "실험적": [
        ("New Amerykah Pt.1",       "Erykah Badu",          2008),
        ("Voodoo",                  "D'Angelo",             2000),
        ("Channel Orange",          "Frank Ocean",          2012),
        ("Monodrama",               "Syd",                  2017),
        ("Telefone",                "Noname",               2016),
    ],
    "사이키델릭": [
        ("Maggot Brain",            "Funkadelic",           1971),
        ("Mind Playing Tricks on Me","Geto Boys",           1991),
        ("Purple Rain",             "Prince",               1984),
        ("New Amerykah Pt.1",       "Erykah Badu",          2008),
        ("To Pimp a Butterfly",     "Kendrick Lamar",       2015),
    ],
    "따뜻함": [
        ("Be Here",                 "Raphael Saadiq",       2004),
        ("Coming Home",             "Leon Bridges",         2015),
        ("A Ribbon in the Sky",     "Stevie Wonder",        1982),
        ("Golden",                  "Jill Scott",           2004),
        ("Umi Says",                "Mos Def",              1999),
    ],
    "낭만": [
        ("A Ribbon in the Sky",     "Stevie Wonder",        1982),
        ("Ribbon in the Sky",       "Stevie Wonder",        1982),
        ("Tonight I Celebrate My Love","Peabo Bryson",      1983),
        ("Endless Love",            "Diana Ross",           1981),
        ("I'm Still in Love with You","Al Green",           1972),
    ],
    "성숙": [
        ("Sweet Love",              "Anita Baker",          1986),
        ("Turn Off the Lights",     "Teddy Pendergrass",    1979),
        ("Never Too Much",          "Luther Vandross",      1981),
        ("Dance with My Father",    "Luther Vandross",      2003),
        ("Back at One",             "Brian McKnight",       1999),
    ],
    "깊이": [
        ("What's Going On",         "Marvin Gaye",          1971),
        ("A Change Is Gonna Come",  "Sam Cooke",            1964),
        ("Pyramid",                 "Frank Ocean",          2012),
        ("Retrograde",              "James Blake",          2013),
        ("Room 25",                 "Noname",               2018),
    ],
    "서사": [
        ("Last Last",               "Burna Boy",            2022),
        ("Ye",                      "Burna Boy",            2018),
        ("Papa Was a Rollin' Stone","The Temptations",      1972),
        ("Retrospect for Life",     "Common",               1997),
        ("Sing About Me",           "Kendrick Lamar",       2012),
    ],
    "향수": [
        ("Ojuelegba",               "WizKid",               2014),
        ("Coming Home",             "Leon Bridges",         2015),
        ("Reminisce",               "Craig Mack",           1994),
        ("Things Done Changed",     "Notorious B.I.G.",     1994),
        ("Be Careful",              "Cardi B",              2018),
    ],
    "밝음": [
        ("Soco",                    "WizKid",               2018),
        ("September",               "Earth, Wind & Fire",   1978),
        ("Shining Star",            "Earth, Wind & Fire",   1975),
        ("Boogie Wonderland",       "Earth, Wind & Fire",   1979),
        ("Celebration",             "Kool & The Gang",      1980),
    ],
    # ── 장르·스타일 ──
    "소울": [
        ("Respect",                 "Aretha Franklin",      1967),
        ("(Sittin' On) The Dock of the Bay","Otis Redding", 1967),
        ("Let's Stay Together",     "Al Green",             1972),
        ("What's Going On",         "Marvin Gaye",          1971),
        ("People Get Ready",        "Curtis Mayfield",      1965),
    ],
    "재즈": [
        ("So What",                 "Miles Davis",          1959),
        ("My Favorite Things",      "John Coltrane",        1961),
        ("Isn't She Lovely",        "Stevie Wonder",        1976),
        ("Bag Lady",                "Erykah Badu",          2000),
        ("Really Love",             "D'Angelo",             2014),
    ],
    "펑키": [
        ("Jungle Boogie",           "Kool & The Gang",      1973),
        ("Give Up the Funk",        "Parliament",           1975),
        ("Le Freak",                "Chic",                 1978),
        ("Superstition",            "Stevie Wonder",        1972),
        ("Brick House",             "Commodores",           1977),
    ],
    "소울펑크": [
        ("That Lady",               "The Isley Brothers",   1973),
        ("For the Love of You",     "The Isley Brothers",   1975),
        ("Family Affair",           "Sly & The Family Stone", 1971),
        ("Easy",                    "Commodores",           1977),
        ("Shining Star",            "Earth, Wind & Fire",   1975),
    ],
    "힙합소울": [
        ("Real Love",               "Mary J. Blige",        1992),
        ("Not Gon' Cry",            "Mary J. Blige",        1995),
        ("Waterfalls",              "TLC",                  1994),
        ("One in a Million",        "Aaliyah",              1996),
        ("No Diggity",              "Blackstreet",          1996),
    ],
    "팝R&B": [
        ("No Scrubs",               "TLC",                  1999),
        ("The Boy Is Mine",         "Brandy & Monica",      1998),
        ("Yeah!",                   "Usher",                2004),
        ("Nobody",                  "Khalid & Alina Barraza", 2018),
        ("Crazy in Love",           "Beyoncé",              2003),
    ],
    "클래식R&B": [
        ("Superstar",               "Usher",                2004),
        ("Let's Get It On",         "Marvin Gaye",          1973),
        ("Sexual Healing",          "Marvin Gaye",          1982),
        ("Rock with You",           "Michael Jackson",      1979),
        ("Weak",                    "SWV",                  1992),
    ],
    "클래식소울": [
        ("A Ribbon in the Sky",     "Stevie Wonder",        1982),
        ("My Girl",                 "The Temptations",      1964),
        ("Stop! In the Name of Love","The Supremes",        1965),
        ("I Heard It Through the Grapevine","Marvin Gaye",  1968),
        ("Chain of Fools",          "Aretha Franklin",      1967),
    ],
    "어덜트소울": [
        ("Be Here",                 "Raphael Saadiq",       2004),
        ("Golden",                  "Jill Scott",           2004),
        ("Never Too Much",          "Luther Vandross",      1981),
        ("Caught Up in the Rapture","Anita Baker",          1986),
        ("Fortunate",               "Maxwell",              1998),
    ],
    "뉴잭": [
        ("My Prerogative",          "Bobby Brown",          1988),
        ("Poison",                  "Bell Biv DeVoe",       1990),
        ("I Want Her",              "Keith Sweat",          1987),
        ("Rump Shaker",             "Wreckx-N-Effect",      1992),
        ("Do Me!",                  "Bell Biv DeVoe",       1990),
    ],
    "팝뉴잭": [
        ("Remember the Time",       "Michael Jackson",      1992),
        ("Motownphilly",            "Boyz II Men",          1991),
        ("Creep",                   "TLC",                  1994),
        ("End of the Road",         "Boyz II Men",          1992),
        ("Cry for You",             "Jodeci",               1993),
    ],
    "아프로퓨전": [
        ("Ye",                      "Burna Boy",            2018),
        ("Last Last",               "Burna Boy",            2022),
        ("Essence",                 "WizKid ft. Tems",      2020),
        ("Location",                "Burna Boy",            2019),
        ("Free Mind",               "Tems",                 2020),
    ],
    "아프로팝": [
        ("Soco",                    "WizKid",               2018),
        ("Calm Down",               "Rema",                 2022),
        ("Fall",                    "Davido",               2017),
        ("Dumebi",                  "Rema",                 2019),
        ("Rush",                    "Ayra Starr",           2023),
    ],
    "댄스홀": [
        ("Temperature",             "Sean Paul",            2005),
        ("Get Busy",                "Sean Paul",            2002),
        ("It Wasn't Me",            "Shaggy",               2000),
        ("Angel",                   "Shaggy",               2000),
        ("Who Am I",                "Beenie Man",           1997),
    ],
    "디스코펑크": [
        ("Le Freak",                "Chic",                 1978),
        ("Good Times",              "Chic",                 1979),
        ("I Will Survive",          "Gloria Gaynor",        1978),
        ("Boogie Oogie Oogie",      "A Taste of Honey",     1978),
        ("Freak Out",               "Chic",                 1978),
    ],
    "재즈소울": [
        ("Sweet Love",              "Anita Baker",          1986),
        ("Giving You the Best",     "Anita Baker",          1988),
        ("No Ordinary Love",        "Sade",                 1992),
        ("Smooth Operator",         "Sade",                 1984),
        ("Really Love",             "D'Angelo",             2014),
    ],
    "어쿠스틱R&B": [
        ("Best Part",               "Daniel Caesar",        2017),
        ("Get You",                 "Daniel Caesar",        2016),
        ("Come Through",            "H.E.R.",               2017),
        ("Location",                "Khalid",               2016),
        ("River",                   "Leon Bridges",         2015),
    ],
    # ── 사운드 특성 ──
    "에너지": [
        ("I Got You (I Feel Good)", "James Brown",          1965),
        ("Yeah!",                   "Usher",                2004),
        ("Poison",                  "Bell Biv DeVoe",       1990),
        ("Uptown Funk",             "Bruno Mars",           2014),
        ("Jungle Boogie",           "Kool & The Gang",      1973),
    ],
    "파워": [
        ("Respect",                 "Aretha Franklin",      1967),
        ("I Got You (I Feel Good)", "James Brown",          1965),
        ("HUMBLE.",                 "Kendrick Lamar",       2017),
        ("Formation",               "Beyoncé",              2016),
        ("Sex Machine",             "James Brown",          1970),
    ],
    "브라스": [
        ("Jungle Boogie",           "Kool & The Gang",      1973),
        ("Shining Star",            "Earth, Wind & Fire",   1975),
        ("September",               "Earth, Wind & Fire",   1978),
        ("Bernadette",              "Four Tops",            1967),
        ("I Can't Help Myself",     "Four Tops",            1965),
    ],
    "댄서블": [
        ("Temperature",             "Sean Paul",            2005),
        ("Le Freak",                "Chic",                 1978),
        ("September",               "Earth, Wind & Fire",   1978),
        ("Give Up the Funk",        "Parliament",           1975),
        ("Rump Shaker",             "Wreckx-N-Effect",      1992),
    ],
    "레이어드": [
        ("Voodoo",                  "D'Angelo",             2000),
        ("Donuts",                  "J Dilla",              2006),
        ("To Pimp a Butterfly",     "Kendrick Lamar",       2015),
        ("Tame Impala - Currents",  "Tame Impala",          2015),
        ("Really Love",             "D'Angelo",             2014),
    ],
    "완성도": [
        ("Voodoo (Album)",          "D'Angelo",             2000),
        ("Shining Star",            "Earth, Wind & Fire",   1975),
        ("Remember the Time",       "Michael Jackson",      1992),
        ("What's Going On",         "Marvin Gaye",          1971),
        ("Ctrl",                    "SZA",                  2017),
    ],
    "업리프팅": [
        ("Shining Star",            "Earth, Wind & Fire",   1975),
        ("September",               "Earth, Wind & Fire",   1978),
        ("Golden",                  "Jill Scott",           2004),
        ("Alright",                 "Kendrick Lamar",       2015),
        ("Boogie Wonderland",       "Earth, Wind & Fire",   1979),
    ],
    "리프": [
        ("Le Freak",                "Chic",                 1978),
        ("Super Freak",             "Rick James",           1981),
        ("Superstition",            "Stevie Wonder",        1972),
        ("Give Up the Funk",        "Parliament",           1975),
        ("Good Times",              "Chic",                 1979),
    ],
    "댄스플로어": [
        ("Le Freak",                "Chic",                 1978),
        ("Boogie Wonderland",       "Earth, Wind & Fire",   1979),
        ("Give Up the Funk",        "Parliament",           1975),
        ("Get Down on It",          "Kool & The Gang",      1981),
        ("Jungle Boogie",           "Kool & The Gang",      1973),
    ],
    "피아노": [
        ("A Ribbon in the Sky",     "Stevie Wonder",        1982),
        ("Ordinary People",         "John Legend",          2004),
        ("All of Me",               "John Legend",          2013),
        ("Isn't She Lovely",        "Stevie Wonder",        1976),
        ("Back at One",             "Brian McKnight",       1999),
    ],
    "클라비넷": [
        ("Superstition",            "Stevie Wonder",        1972),
        ("Higher Ground",           "Stevie Wonder",        1973),
        ("Living for the City",     "Stevie Wonder",        1974),
        ("Tell Me Something Good",  "Rufus",                1974),
    ],
    "오케스트라": [
        ("Earned It",               "The Weeknd",           2015),
        ("Endless Love",            "Diana Ross",           1981),
        ("My Girl",                 "The Temptations",      1964),
        ("I'll Be Missing You",     "Puff Daddy",           1997),
        ("A Change Is Gonna Come",  "Sam Cooke",            1964),
    ],
    "파워보컬": [
        ("Not Gon' Cry",            "Mary J. Blige",        1995),
        ("Respect",                 "Aretha Franklin",      1967),
        ("I Will Always Love You",  "Whitney Houston",      1992),
        ("And I Am Telling You",    "Jennifer Holliday",    1982),
        ("Chain of Fools",          "Aretha Franklin",      1967),
    ],
    "하모니": [
        ("Motownphilly",            "Boyz II Men",          1991),
        ("End of the Road",         "Boyz II Men",          1992),
        ("Stop! In the Name of Love","The Supremes",        1965),
        ("Hold On",                 "En Vogue",             1990),
        ("Forever My Lady",         "Jodeci",               1991),
    ],
    "아카펠라": [
        ("Motownphilly",            "Boyz II Men",          1991),
        ("I'll Make Love to You",   "Boyz II Men",          1994),
        ("This Is How We Do It",    "Montell Jordan",       1995),
    ],
    # ── 감정·특성 ──
    "발라드": [
        ("Never Too Much",          "Luther Vandross",      1981),
        ("End of the Road",         "Boyz II Men",          1992),
        ("Here and Now",            "Luther Vandross",      1989),
        ("I'll Be Missing You",     "Puff Daddy",           1997),
        ("Have You Ever",           "Brandy",               1998),
    ],
    "청춘": [
        ("Location",                "Khalid",               2016),
        ("Young Dumb & Broke",      "Khalid",               2017),
        ("Better",                  "Khalid",               2019),
        ("The Light",               "Common",               2000),
        ("Electric Relaxation",     "A Tribe Called Quest", 1993),
    ],
    "듀엣": [
        ("Best Part",               "Daniel Caesar ft. H.E.R.", 2017),
        ("The Boy Is Mine",         "Brandy & Monica",      1998),
        ("Endless Love",            "Diana Ross & Lionel Richie", 1981),
        ("Tonight I Celebrate",     "Peabo Bryson",         1983),
        ("Ain't No Mountain High",  "Marvin Gaye & Tammi Terrell", 1967),
    ],
    "극적": [
        ("Earned It",               "The Weeknd",           2015),
        ("Purple Rain",             "Prince",               1984),
        ("When Doves Cry",          "Prince",               1984),
        ("Close the Door",          "Teddy Pendergrass",    1978),
        ("I Will Always Love You",  "Whitney Houston",      1992),
    ],
    "드라마틱": [
        ("Papa Was a Rollin' Stone","The Temptations",      1972),
        ("I Heard It Through the Grapevine","Marvin Gaye",  1968),
        ("Strange Fruit",           "Billie Holiday",       1939),
        ("What's Going On",         "Marvin Gaye",          1971),
        ("Thriller",                "Michael Jackson",      1982),
    ],
    "감동": [
        ("Ain't No Mountain High",  "Marvin Gaye & Tammi Terrell", 1967),
        ("A Change Is Gonna Come",  "Sam Cooke",            1964),
        ("Dance with My Father",    "Luther Vandross",      2003),
        ("Golden",                  "Jill Scott",           2004),
        ("Coming Home",             "Leon Bridges",         2015),
    ],
    "파워풀": [
        ("Chain of Fools",          "Aretha Franklin",      1967),
        ("I Got You (I Feel Good)", "James Brown",          1965),
        ("HUMBLE.",                 "Kendrick Lamar",       2017),
        ("Formation",               "Beyoncé",              2016),
        ("Alright",                 "Kendrick Lamar",       2015),
    ],
    "아이코닉": [
        ("Thriller",                "Michael Jackson",      1982),
        ("Billie Jean",             "Michael Jackson",      1982),
        ("No Scrubs",               "TLC",                  1999),
        ("Respect",                 "Aretha Franklin",      1967),
        ("Crazy in Love",           "Beyoncé",              2003),
    ],
    "걸파워": [
        ("No Scrubs",               "TLC",                  1999),
        ("Survivor",                "Destiny's Child",      2001),
        ("Respect",                 "Aretha Franklin",      1967),
        ("Formation",               "Beyoncé",              2016),
        ("Not Gon' Cry",            "Mary J. Blige",        1995),
    ],
    "엣지": [
        ("Poison",                  "Bell Biv DeVoe",       1990),
        ("Super Freak",             "Rick James",           1981),
        ("Get Ur Freak On",         "Missy Elliott",        2001),
        ("Work It",                 "Missy Elliott",        2002),
        ("Rump Shaker",             "Wreckx-N-Effect",      1992),
    ],
    "미래적": [
        ("One in a Million",        "Aaliyah",              1996),
        ("Are You That Somebody",   "Aaliyah",              1998),
        ("Climax",                  "Usher",                2012),
        ("Good Days",               "SZA",                  2020),
        ("Nights",                  "Frank Ocean",          2016),
    ],
    "축제": [
        ("Soco",                    "WizKid",               2018),
        ("September",               "Earth, Wind & Fire",   1978),
        ("Celebration",             "Kool & The Gang",      1980),
        ("Boogie Wonderland",       "Earth, Wind & Fire",   1979),
        ("Fall",                    "Davido",               2017),
    ],
    "파티": [
        ("Temperature",             "Sean Paul",            2005),
        ("Get Busy",                "Sean Paul",            2002),
        ("Yeah!",                   "Usher",                2004),
        ("Jungle Boogie",           "Kool & The Gang",      1973),
        ("Le Freak",                "Chic",                 1978),
    ],
    "스트리트": [
        ("Ojuelegba",               "WizKid",               2014),
        ("N.Y. State of Mind",      "Nas",                  1994),
        ("Real Love",               "Mary J. Blige",        1992),
        ("The Message",             "Grandmaster Flash",    1982),
        ("93 'til Infinity",        "Souls of Mischief",    1993),
    ],
    "힙합": [
        ("If I Ruled the World",    "Nas",                  1996),
        ("The Light",               "Common",               2000),
        ("Electric Relaxation",     "A Tribe Called Quest", 1993),
        ("Alright",                 "Kendrick Lamar",       2015),
        ("Umi Says",                "Mos Def",              1999),
    ],
    "모타운": [
        ("I Heard It Through the Grapevine","Marvin Gaye",  1968),
        ("My Girl",                 "The Temptations",      1964),
        ("Stop! In the Name of Love","The Supremes",        1965),
        ("I Can't Help Myself",     "Four Tops",            1965),
        ("Bernadette",              "Four Tops",            1967),
    ],
    "사이키델릭소울": [
        ("Papa Was a Rollin' Stone","The Temptations",      1972),
        ("Maggot Brain",            "Funkadelic",           1971),
        ("New Amerykah Pt.1",       "Erykah Badu",          2008),
        ("Innervisions",            "Stevie Wonder",        1973),
        ("There's a Riot Goin' On", "Sly & The Family Stone", 1971),
    ],
    "클래식": [
        ("What's Going On",         "Marvin Gaye",          1971),
        ("Respect",                 "Aretha Franklin",      1967),
        ("My Girl",                 "The Temptations",      1964),
        ("I Got You (I Feel Good)", "James Brown",          1965),
        ("A Change Is Gonna Come",  "Sam Cooke",            1964),
    ],
    "긴장감": [
        ("Papa Was a Rollin' Stone","The Temptations",      1972),
        ("Thriller",                "Michael Jackson",      1982),
        ("Superfly",                "Curtis Mayfield",      1972),
        ("Straight Outta Compton",  "N.W.A",                1988),
        ("N.Y. State of Mind",      "Nas",                  1994),
    ],
    "멜로디": [
        ("Isn't She Lovely",        "Stevie Wonder",        1976),
        ("A Ribbon in the Sky",     "Stevie Wonder",        1982),
        ("Ex-Factor",               "Lauryn Hill",          1998),
        ("Best Part",               "Daniel Caesar",        2017),
        ("Essence",                 "WizKid ft. Tems",      2020),
    ],
    "부드러움": [
        ("Rock with You",           "Michael Jackson",      1979),
        ("Smooth Operator",         "Sade",                 1984),
        ("No Ordinary Love",        "Sade",                 1992),
        ("Cruisin'",                "Smokey Robinson",      1979),
        ("By Your Side",            "Sade",                 2000),
    ],
    "팝소울": [
        ("Rock with You",           "Michael Jackson",      1979),
        ("Easy",                    "Commodores",           1977),
        ("Three Times a Lady",      "Commodores",           1978),
        ("Endless Love",            "Diana Ross",           1981),
        ("I'm Coming Out",          "Diana Ross",           1980),
    ],
    "기타": [
        ("That Lady",               "The Isley Brothers",   1973),
        ("Purple Rain",             "Prince",               1984),
        ("Nothing Compares 2 U",    "Prince",               1985),
        ("Kiss",                    "Prince",               1986),
        ("Still Rock and Roll to Me","Billy Joel",          1980),
    ],
    "기타R&B": [
        ("Come Through",            "H.E.R.",               2017),
        ("Focus",                   "H.E.R.",               2016),
        ("Best Part",               "Daniel Caesar",        2017),
        ("River",                   "Leon Bridges",         2015),
        ("Adorn",                   "Miguel",               2012),
    ],
    "힙합R&B": [
        ("No Diggity",              "Blackstreet",          1996),
        ("One in a Million",        "Aaliyah",              1996),
        ("Waterfalls",              "TLC",                  1994),
        ("Real Love",               "Mary J. Blige",        1992),
        ("If I Ruled the World",    "Nas",                  1996),
    ],
}


# ══════════════════════════════════════════════════════════════
# 4. session_state 초기화
# ══════════════════════════════════════════════════════════════

def init_session(genre_key: str):
    # ── 전역 도감: 장르 변경 시에도 절대 초기화하지 않음 ──
    if "genre_collection" not in st.session_state:
        st.session_state.genre_collection = {}
    if "_master_balloons_shown" not in st.session_state:
        st.session_state._master_balloons_shown = False

    if st.session_state.get("current_genre") != genre_key:
        st.session_state.current_genre      = genre_key
        st.session_state.current_track      = 0
        st.session_state.evaluations        = {}
        st.session_state.evaluations_phase2 = {}
        st.session_state.phase              = "eval"
        st.session_state.artist_popup       = None
        st.session_state.tag_popup          = None
        st.session_state.rec_popup          = None
        st.session_state.rec_feedback              = {}
        st.session_state.like_expanded             = set()
        st.session_state.playlist_dislike_pending  = False
    # 기존 세션에서 새 키가 없을 경우 안전하게 초기화
    if "evaluations_phase2" not in st.session_state:
        st.session_state.evaluations_phase2 = {}
    if "rec_feedback" not in st.session_state:
        st.session_state.rec_feedback = {}
    if "like_expanded" not in st.session_state:
        st.session_state.like_expanded = set()
    if "playlist_dislike_pending" not in st.session_state:
        st.session_state.playlist_dislike_pending = False

def get_eval(idx: int, store_key: str = "evaluations") -> dict:
    return st.session_state[store_key].get(idx, {"score": 3, "attributes": [], "note": ""})

def save_eval(idx: int, score: int, attributes: list, note: str, store_key: str = "evaluations"):
    st.session_state[store_key][idx] = {"score": score, "attributes": attributes, "note": note}


# ══════════════════════════════════════════════════════════════
# 5. 분석 로직
# ══════════════════════════════════════════════════════════════

def calc_attribute_scores(evaluations: dict) -> dict:
    attr_scores = {a: 0.0 for a in ATTRIBUTES}
    for ev in evaluations.values():
        for attr in ev["attributes"]:
            if attr in attr_scores:
                attr_scores[attr] += ev["score"]
    return attr_scores

def get_persona(attr_scores: dict) -> str:
    sorted_attrs = sorted(attr_scores.items(), key=lambda x: x[1], reverse=True)
    top_two   = {a for a, s in sorted_attrs[:2] if s > 0}
    top_three = {a for a, s in sorted_attrs[:3] if s > 0}
    for key_set, text in PERSONA_MAP:
        if len(key_set) == 3 and key_set <= top_three:
            return text
    for key_set, text in PERSONA_MAP:
        if key_set <= top_two or key_set == top_two:
            return text
    return f"🎵 자유로운 리스너 — {', '.join(top_two)} 중심의 개성 있는 음악 취향" if top_two \
           else "🎵 탐색 중인 리스너 — 다양한 장르를 자유롭게 유영 중"

def rank_recommendations_dynamic(
    recommendations: list,
    evaluations: dict,
    tracks: list,
    attr_scores: dict,
) -> tuple[list, dict, list]:
    """
    고득점(4~5점) 트랙의 vibe 속성을 추출하여 추천 정렬에 반영.

    로직:
    ① 점수 4점 이상인 트랙의 vibe 속성을 수집, 점수만큼 가중치 부여
    ② 사용자가 직접 선택한 매력 요소(attr_scores)와 합산 → combined_scores
    ③ combined_scores 상위 2 속성과 각 추천곡의 match_attributes 교집합을
       match_score로 환산, 내림차순 정렬

    반환
    -----
    ranked_recs  : 정렬된 추천 리스트 (match_score, high_vibe_match 키 포함)
    combined     : 합산 속성 점수 dict
    high_tracks  : 고득점(>=4) 트랙 정보 리스트 (제목, 아티스트, 점수, vibe)
    """
    # ① 고득점 트랙 vibe 수집
    high_vibe: dict[str, float] = {}
    high_tracks_info = []
    for idx, ev in evaluations.items():
        if ev["score"] >= 4 and idx < len(tracks):
            t = tracks[idx]
            high_tracks_info.append({
                "title":  t["title"],
                "artist": t["artist"],
                "score":  ev["score"],
                "vibe":   t.get("vibe", []),
            })
            for attr in t.get("vibe", []):
                high_vibe[attr] = high_vibe.get(attr, 0) + ev["score"]  # 점수 가중

    # ② attr_scores(사용자 선택 기반) + high_vibe(고득점 트랙 기반) 합산
    combined = {a: attr_scores.get(a, 0) + high_vibe.get(a, 0) for a in ATTRIBUTES}

    # ③ 상위 2 속성 추출 후 match_attributes 교집합 스코어링
    top_attrs = {a for a, s in sorted(combined.items(), key=lambda x: x[1], reverse=True)[:2] if s > 0}

    scored = []
    for rec in recommendations:
        ma = set(rec.get("match_attributes", []))
        overlap = len(top_attrs & ma)
        # 고득점 트랙 vibe와도 직접 비교해 추가 보너스
        vibe_bonus = sum(1 for ht in high_tracks_info
                         if any(v in ma for v in ht["vibe"]) and ht["score"] >= 4)
        scored.append({**rec, "match_score": overlap, "vibe_bonus": vibe_bonus})

    # 1차: match_score, 2차: vibe_bonus 내림차순
    scored.sort(key=lambda x: (x["match_score"], x["vibe_bonus"]), reverse=True)
    return scored, combined, high_tracks_info

def generate_mixtape_report(genre_key, evaluations, attr_scores, persona, ranked_recs, active_tracks=None) -> str:
    """
    TXT 다운로드용 클린 텍스트 리포트 (ASCII 아트 없는 가독성 버전).
    HTML 렌더링은 render_lp_report_html() 함수가 담당.
    """
    tracks = active_tracks if active_tracks is not None else GENRE_DATA[genre_key]["tracks"]
    now    = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
    lines  = [
        "나만의 흑인음악 디깅 리포트",
        "=" * 40,
        f"디깅 날짜  : {now}",
        f"선택 장르  : {genre_key}",
        f"나의 페르소나 : {persona}",
        "",
        "[ 음악 속성 분석 ]",
    ]
    max_s = max(attr_scores.values()) if max(attr_scores.values()) > 0 else 1
    for attr in ATTRIBUTES:
        s   = attr_scores.get(attr, 0)
        pct = int(s / max_s * 100) if max_s > 0 else 0
        lines.append(f"  {attr} : {s:.0f}pts ({pct}%)")

    lines += ["", "[ 오늘의 디깅 트랙 ]"]
    for idx, track in enumerate(tracks):
        ev    = evaluations.get(idx, {})
        score = ev.get("score", "-")
        attrs = ev.get("attributes", [])
        note  = ev.get("note", "").strip() or "(노트 없음)"
        stars = "★" * int(score) + "☆" * (5 - int(score)) if isinstance(score, int) else "-"
        lines += [
            f"  {idx+1}. {track['title']} — {track['artist']} ({track['year']})",
            f"     점수  : {stars} ({score}/5)",
            f"     매력  : {', '.join(attrs) if attrs else '선택 없음'}",
            f"     노트  : {note}",
            "",
        ]

    lines += ["[ 추천 플레이리스트 TOP 5 ]"]
    for i, rec in enumerate(ranked_recs[:5], 1):
        match = " [MATCH]" if rec.get("match_score", 0) > 0 else ""
        lines.append(f"  {i}. {rec['title']} — {rec['artist']} ({rec['year']}){match}")
        lines.append(f"     태그: {' / '.join(rec['tags'])}")
        lines.append("")

    lines += [
        "=" * 40,
        "Produced by 흑인음악 디깅 대시보드",
        "Keep Digging, Keep Growing.",
    ]
    return "\n".join(lines)


def render_receipt_html(
    genre_key:   str,
    persona:     str,
    evaluations: dict,
    all_tracks:  list,
    attr_scores: dict,
    avg:         float,
    is_phase2:   bool,
) -> str:
    """감성 영수증(Receiptify) 스타일 HTML 생성"""
    now_dt   = datetime.now()
    date_str = now_dt.strftime("%Y-%m-%d")
    time_str = now_dt.strftime("%H:%M")
    order_no = now_dt.strftime("%Y%m%d%H%M")

    # 페르소나 → 대표 키워드 + 세부 설명 분리
    _persona_raw = persona.strip()
    if "\n" in _persona_raw:
        # 형식: "키워드 이모지\n세부 설명 문장"
        _pk, _pd = _persona_raw.split("\n", 1)
        persona_keyword = _pk.strip()
        persona_detail  = _pd.strip()
    elif " — " in _persona_raw:
        # 형식: "🎵 자유로운 리스너 — 속성1, 속성2 중심의..."
        _pk, _pd = _persona_raw.split(" — ", 1)
        persona_keyword = _pk.strip()
        persona_detail  = _pd.strip()
    else:
        persona_keyword = _persona_raw
        persona_detail  = ""
    # 대표 키워드: 이모지+이름만 (괄호 앞까지), 18자 제한
    persona_keyword = persona_keyword.split("(")[0].strip()
    if len(persona_keyword) > 18:
        persona_keyword = persona_keyword[:17] + "…"
    # 세부 설명: 36자 제한
    if len(persona_detail) > 36:
        persona_detail = persona_detail[:35] + "…"

    genre_disp = genre_key if len(genre_key) <= 28 else genre_key[:27] + "…"
    track_cnt  = len(all_tracks)
    depth_text = "· DEEP ANALYSIS ·" if is_phase2 else ""

    # ── Track List rows ──
    track_rows = ""
    for i, t in enumerate(all_tracks):
        ev     = evaluations.get(i, {})
        score  = ev.get("score", 0)
        stars  = "★" * score + "☆" * (5 - score)
        title  = t["title"][:23]
        artist = t["artist"][:22]
        tag    = " · <span style='font-size:9px;color:#e65100;'>2차</span>" if (is_phase2 and i >= 3) else ""
        # 한 줄 디깅 노트 (입력된 경우에만 표시)
        raw_note = ev.get("note", "").strip()
        note_html = ""
        if raw_note:
            note_disp = raw_note if len(raw_note) <= 36 else raw_note[:35] + "…"
            note_html = (
                f"<br><span style='font-size:9px;color:#555;font-style:italic;'>"
                f"&ldquo;{note_disp}&rdquo;</span>"
            )
        track_rows += (
            f"<tr>"
            f"<td style='width:20px;padding:4px 0;font-size:11px;color:#999;vertical-align:top;'>{i+1:02d}</td>"
            f"<td style='padding:4px 5px;font-size:12px;vertical-align:top;line-height:1.55;'>"
            f"<b>{title}</b>{tag}<br>"
            f"<span style='font-size:10px;color:#666;'>{artist}</span>"
            f"{note_html}"
            f"</td>"
            f"<td style='padding:4px 0;font-size:12px;text-align:right;white-space:nowrap;'>{stars}</td>"
            f"</tr>"
        )

    # ── Nutrition Facts rows ──
    ATTR_SHORT = {
        "🎵 멜로디 (Melody)":                    "MELODY",
        "🥁 리듬 & 비트 (Rhythm & Beat)":         "RHYTHM",
        "🎸 베이스 & 그루브 (Bass & Groove)":      "BASS/GROOVE",
        "🎙️ 보컬 & 음색 (Vocal & Tone)":          "VOCAL",
        "🎹 화성 & 코드 진행 (Harmony & Chords)":  "HARMONY",
        "🎺 리얼 악기 세션 (Live Instruments)":    "LIVE INSTR.",
        "🎛️ 사운드 믹싱 & 질감 (Sound Design)":   "SOUND DESIGN",
        "📜 가사 & 메시지 (Lyrics & Message)":     "LYRICS/MSG",
    }
    sorted_a = sorted(attr_scores.items(), key=lambda x: x[1], reverse=True)
    max_s    = max((s for _, s in sorted_a), default=1) or 1
    nutrition_rows = ""
    for attr, s_val in sorted_a:
        pct   = int(s_val / max_s * 100) if max_s > 0 else 0
        short = ATTR_SHORT.get(attr, attr[:12])
        bar_f = round(pct / 100 * 12)
        bar   = "█" * bar_f + "░" * (12 - bar_f)
        nutrition_rows += (
            f"<tr>"
            f"<td style='padding:2px 0;font-size:11px;white-space:nowrap;width:110px;'>{short}</td>"
            f"<td style='padding:2px 5px;font-size:11px;color:#444;letter-spacing:-0.5px;'>{bar}</td>"
            f"<td style='padding:2px 0;font-size:11px;text-align:right;width:36px;'>{pct}%</td>"
            f"</tr>"
        )

    # ── Barcode spans ──
    bp = [3,1,2,1,3,2,1,1,3,1,2,3,1,2,1,1,3,2,1,2,1,1,3,2,1,3,1,1,2,1,3,1,2,2,1,3]
    barcode = "".join(
        f'<span style="display:inline-block;width:{w}px;height:46px;background:#111111;'
        f'margin-right:{"2" if w >= 2 else "1"}px;vertical-align:middle;"></span>'
        for w in bp
    )

    # ── Stars ──
    avg_stars = "★" * round(avg) + "☆" * (5 - round(avg))

    return f"""
<div style="
  font-family:'Pretendard',-apple-system,BlinkMacSystemFont,system-ui,'Helvetica Neue',sans-serif;
  background:#fdfdfd;
  color:#111111;
  max-width:460px;
  margin:12px auto 40px auto;
  padding:34px 30px 28px 30px;
  box-shadow:
    0 1px 2px rgba(0,0,0,0.12),
    0 4px 16px rgba(0,0,0,0.09),
    0 16px 48px rgba(0,0,0,0.06),
    4px 0 8px rgba(0,0,0,0.04),
    -4px 0 8px rgba(0,0,0,0.04);
">

  <div style="text-align:center;margin-bottom:20px;">
    <div style="font-size:9px;letter-spacing:5px;color:#aaa;margin-bottom:8px;">★ &nbsp; ★ &nbsp; ★</div>
    <div style="font-size:22px;font-weight:bold;letter-spacing:7px;line-height:1.3;">DIGGING</div>
    <div style="font-size:22px;font-weight:bold;letter-spacing:7px;line-height:1.3;">RECEIPT</div>
    <div style="font-size:9px;letter-spacing:2px;color:#999;margin-top:8px;">
      나만의 흑인음악 취향 디깅하기
    </div>
  </div>

  <div style="border-bottom:1px dashed #111;margin:0 0 14px 0;"></div>

  <div style="font-size:11px;line-height:2.1;margin-bottom:4px;">
    <div>ORDER NO&nbsp;: #{order_no}</div>
    <div>DATE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {date_str} &nbsp; {time_str}</div>
    <div>GENRE&nbsp;&nbsp;&nbsp;&nbsp;: {genre_disp}</div>
    <div>CUSTOMER : {persona_keyword}</div>
    {'<div style="padding-left:80px;font-size:9px;color:#666;line-height:1.5;margin-top:-4px;">' + persona_detail + '</div>' if persona_detail else ''}
    <div>TRACKS&nbsp;&nbsp;&nbsp;: {track_cnt} TRACKS &nbsp;{depth_text}</div>
  </div>

  <div style="border-bottom:1px dashed #111;margin:14px 0;"></div>

  <div style="font-size:12px;font-weight:bold;letter-spacing:3px;margin-bottom:10px;">
    TRACK LIST
  </div>
  <table style="width:100%;border-collapse:collapse;">
    {track_rows}
  </table>

  <div style="border-bottom:1px dashed #111;margin:14px 0;"></div>

  <div style="font-size:12px;font-weight:bold;letter-spacing:3px;margin-bottom:3px;">
    NUTRITION FACTS
  </div>
  <div style="font-size:9px;color:#888;letter-spacing:1px;margin-bottom:8px;">
    SERVING: 8 MUSIC ATTRIBUTES &nbsp;·&nbsp; SORTED BY SCORE
  </div>
  <div style="border-bottom:3px solid #111;margin-bottom:5px;"></div>
  <table style="width:100%;border-collapse:collapse;">
    {nutrition_rows}
  </table>
  <div style="border-bottom:1px solid #111;margin-top:5px;"></div>

  <div style="border-bottom:1px dashed #111;margin:14px 0;"></div>

  <div style="text-align:center;padding:8px 0 14px 0;">
    <div style="font-size:10px;letter-spacing:5px;color:#888;margin-bottom:10px;">
      — TOTAL SCORE —
    </div>
    <div style="font-size:30px;letter-spacing:3px;">{avg_stars}</div>
    <div style="font-size:26px;font-weight:bold;letter-spacing:4px;margin-top:6px;">
      {avg:.1f} / 5.0
    </div>
  </div>

  <div style="border-bottom:1px dashed #111;margin:0 0 18px 0;"></div>

  <div style="text-align:center;">
    <div>{barcode}</div>
    <div style="font-size:10px;letter-spacing:5px;color:#888;margin-top:10px;">
      THANK YOU FOR DIGGING
    </div>
    <div style="font-size:9px;letter-spacing:2px;color:#bbb;margin-top:4px;">
      KEEP DIGGING &nbsp;·&nbsp; KEEP GROWING
    </div>
  </div>

</div>"""


# ══════════════════════════════════════════════════════════════
# 5-b. 포토카드 렌더링 & PNG 생성
# ══════════════════════════════════════════════════════════════

def _hex_to_rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def _adjust_hex(h: str, delta: float) -> str:
    r, g, b = _hex_to_rgb(h)
    if delta >= 0:
        r = min(255, int(r + (255 - r) * delta))
        g = min(255, int(g + (255 - g) * delta))
        b = min(255, int(b + (255 - b) * delta))
    else:
        f = 1 + delta
        r, g, b = max(0, int(r * f)), max(0, int(g * f)), max(0, int(b * f))
    return f"#{r:02x}{g:02x}{b:02x}"


def render_photo_card_html(
    genre_key:   str,
    genre_color: str,
    persona:     str,
    attr_scores: dict,
    evaluations: dict,
    all_tracks:  list,
    avg:         float,
    is_phase2:   bool,
    safe_genre:  str = "card",
) -> str:
    """포켓몬 TCG 스타일 트레이딩 카드 HTML 생성"""
    # ── 색상 ──
    base       = _hex_to_rgb(genre_color)
    light_hex  = _adjust_hex(genre_color, +0.38)
    dark_hex   = _adjust_hex(genre_color, -0.52)
    gold       = (255, 215, 0)
    border_rgb = tuple(int(c * 0.28 + g * 0.72) for c, g in zip(base, gold))
    border_hex = f"#{border_rgb[0]:02x}{border_rgb[1]:02x}{border_rgb[2]:02x}"
    body_bg    = _adjust_hex(genre_color, -0.70)

    # ── 장르 메타 ──
    GENRE_META = {
        "🌙 Neo-Soul":                       ("001","Rare Holo",  "◆◆",   "🌙"),
        "🔥 Funk":                            ("002","Ultra Rare", "◆◆◆",  "🔥"),
        "💜 Contemporary R&B":               ("003","Rare",       "◆",    "💜"),
        "🎤 New Jack Swing":                  ("004","Uncommon",   "◈◈",   "🎤"),
        "🌊 Quiet Storm R&B":                 ("005","Rare Holo",  "◆◆",   "🌊"),
        "🎸 60~70s Classic Soul / Motown":   ("006","Secret Rare","★◆★",  "🎸"),
        "🎧 90s Hip-Hop Soul":               ("007","Ultra Rare", "◆◆◆",  "🎧"),
        "🌍 Afrobeats / Dancehall":          ("008","Common",     "◇",    "🌍"),
    }
    card_no, rarity_name, rarity_sym, genre_emoji = GENRE_META.get(
        genre_key, ("000", "Rare", "◆", "🎵"))
    genre_short = genre_key.split(" ", 1)[-1].split("/")[0].strip()[:16]

    # 장르별 구슬 아이템 이모지 매핑
    GENRE_ITEM = {
        "🌙 Neo-Soul":                       "📼",
        "🔥 Funk":                            "🪩",
        "💜 Contemporary R&B":               "🎧",
        "🎤 New Jack Swing":                  "📻",
        "🌊 Quiet Storm R&B":                 "🎙️",
        "🎸 60~70s Classic Soul / Motown":   "📀",
        "🎧 90s Hip-Hop Soul":               "🎛️",
        "🌍 Afrobeats / Dancehall":          "🪘",
    }
    item_emoji = GENRE_ITEM.get(genre_key, "🎵")

    # ── 장르별 캐릭터 SVG (치비 스타일 인물 일러스트) ──
    _C = {
        "🌙 Neo-Soul": (
            '<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">'
            # 아프로 헤어
            '<ellipse cx="50" cy="26" rx="26" ry="23" fill="#5b21b6" opacity="0.85"/>'
            '<circle cx="50" cy="28" r="20" fill="#8b5cf6"/>'
            '<circle cx="36" cy="18" r="6" fill="#a78bfa" opacity="0.9"/>'
            '<circle cx="64" cy="16" r="6" fill="#a78bfa" opacity="0.9"/>'
            '<circle cx="50" cy="10" r="6" fill="#c4b5fd"/>'
            # 얼굴
            '<circle cx="50" cy="37" r="15" fill="#c8956c"/>'
            # 눈 감은 채 노래
            '<path d="M43 35 Q45 33 47 35" stroke="#3d1f0f" stroke-width="1.5" fill="none"/>'
            '<path d="M53 35 Q55 33 57 35" stroke="#3d1f0f" stroke-width="1.5" fill="none"/>'
            '<ellipse cx="50" cy="42" rx="4" ry="3" fill="#8b3a2a"/>'
            # 목
            '<rect x="46" y="51" width="8" height="7" rx="2" fill="#c8956c"/>'
            # 드레스
            '<path d="M33 58 L50 55 L67 58 L72 115 L28 115 Z" fill="#7c3aed" opacity="0.9"/>'
            '<rect x="37" y="72" width="26" height="3" rx="1" fill="#4c1d95" opacity="0.6"/>'
            # 팔
            '<line x1="33" y1="65" x2="18" y2="82" stroke="#c8956c" stroke-width="6" stroke-linecap="round"/>'
            '<line x1="67" y1="63" x2="80" y2="52" stroke="#c8956c" stroke-width="6" stroke-linecap="round"/>'
            # 마이크
            '<circle cx="84" cy="47" r="7" fill="#9ca3af"/>'
            '<circle cx="84" cy="47" r="4" fill="#6b7280"/>'
            '<rect x="82" y="52" width="4" height="10" rx="2" fill="#9ca3af"/>'
            # 음표
            '<text x="10" y="52" font-size="13" fill="rgba(196,181,253,0.85)" font-family="serif">♪</text>'
            '<text x="74" y="78" font-size="10" fill="rgba(196,181,253,0.65)" font-family="serif">♫</text>'
            '<circle cx="42" cy="88" r="2" fill="rgba(255,255,200,0.5)"/>'
            '<circle cx="57" cy="96" r="1.5" fill="rgba(255,255,200,0.45)"/>'
            '</svg>'
        ),
        "🔥 Funk": (
            '<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">'
            # 빅 아프로
            '<circle cx="50" cy="20" r="24" fill="#c2410c" opacity="0.85"/>'
            '<circle cx="50" cy="20" r="20" fill="#ea580c"/>'
            '<circle cx="36" cy="12" r="7" fill="#f97316" opacity="0.8"/>'
            '<circle cx="64" cy="11" r="7" fill="#f97316" opacity="0.8"/>'
            '<circle cx="50" cy="5"  r="6" fill="#fb923c"/>'
            # 얼굴
            '<circle cx="50" cy="30" r="14" fill="#b87452"/>'
            # 선글라스
            '<rect x="38" y="26" width="10" height="7" rx="3" fill="#1e293b"/>'
            '<rect x="52" y="26" width="10" height="7" rx="3" fill="#1e293b"/>'
            '<line x1="48" y1="29" x2="52" y2="29" stroke="#475569" stroke-width="1.5"/>'
            # 큰 웃음
            '<path d="M43 37 Q50 43 57 37" stroke="#1c1917" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
            # 몸 — 댄스 포즈
            '<rect x="43" y="43" width="14" height="6" rx="3" fill="#b87452"/>'
            '<path d="M34 49 L50 46 L66 49 L63 80 L37 80 Z" fill="#dc2626" opacity="0.9"/>'
            '<text x="43" y="68" font-size="11" fill="rgba(255,200,0,0.85)">★</text>'
            # 다리 스플릿
            '<line x1="44" y1="80" x2="18" y2="102" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>'
            '<line x1="56" y1="80" x2="82" y2="102" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>'
            '<ellipse cx="16" cy="104" rx="8" ry="4" fill="#78350f"/>'
            '<ellipse cx="84" cy="104" rx="8" ry="4" fill="#78350f"/>'
            # 팔
            '<line x1="34" y1="54" x2="14" y2="42" stroke="#b87452" stroke-width="6" stroke-linecap="round"/>'
            '<line x1="66" y1="54" x2="82" y2="44" stroke="#b87452" stroke-width="6" stroke-linecap="round"/>'
            '<text x="4"  y="36" font-size="10" fill="rgba(255,200,50,0.9)">✦</text>'
            '<text x="84" y="32" font-size="9"  fill="rgba(255,200,50,0.8)">✦</text>'
            '<text x="10" y="72" font-size="10" fill="rgba(255,100,50,0.8)" font-family="serif">♪</text>'
            '</svg>'
        ),
        "💜 Contemporary R&B": (
            '<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">'
            # 페이드 헤어컷
            '<ellipse cx="50" cy="20" rx="17" ry="14" fill="#1e1b4b"/>'
            '<circle cx="50" cy="23" r="13" fill="#312e81"/>'
            # 얼굴
            '<circle cx="50" cy="34" r="15" fill="#a07850"/>'
            # 쿨한 눈
            '<rect x="41" y="30" width="8" height="3" rx="1.5" fill="#1e1b4b"/>'
            '<rect x="51" y="30" width="8" height="3" rx="1.5" fill="#1e1b4b"/>'
            '<path d="M44 39 Q50 43 56 39" stroke="#6b3f1f" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
            # 헤드폰
            '<path d="M34 27 Q35 14 50 13 Q65 14 66 27" stroke="#7c3aed" stroke-width="4.5" fill="none"/>'
            '<rect x="29" y="25" width="9" height="11" rx="4.5" fill="#7c3aed"/>'
            '<rect x="62" y="25" width="9" height="11" rx="4.5" fill="#7c3aed"/>'
            '<rect x="31" y="27" width="5" height="7" rx="2.5" fill="#a78bfa"/>'
            '<rect x="64" y="27" width="5" height="7" rx="2.5" fill="#a78bfa"/>'
            # 목
            '<rect x="46" y="48" width="8" height="6" rx="2" fill="#a07850"/>'
            # 후디
            '<path d="M28 54 L50 50 L72 54 L70 115 L30 115 Z" fill="#4c1d95" opacity="0.9"/>'
            '<line x1="50" y1="54" x2="50" y2="84" stroke="#7c3aed" stroke-width="1.5"/>'
            '<rect x="37" y="79" width="26" height="15" rx="5" fill="#3b0764" opacity="0.7"/>'
            # 팔
            '<line x1="28" y1="64" x2="38" y2="81" stroke="#a07850" stroke-width="6" stroke-linecap="round"/>'
            '<line x1="72" y1="64" x2="62" y2="81" stroke="#a07850" stroke-width="6" stroke-linecap="round"/>'
            # 사운드웨이브
            '<path d="M10 58 Q13 53 16 58 Q19 63 22 58" stroke="rgba(167,139,250,0.75)" stroke-width="2" fill="none"/>'
            '<path d="M78 58 Q81 53 84 58 Q87 63 90 58" stroke="rgba(167,139,250,0.75)" stroke-width="2" fill="none"/>'
            '<text x="8" y="46" font-size="10" fill="rgba(167,139,250,0.7)" font-family="serif">♫</text>'
            '</svg>'
        ),
        "🎤 New Jack Swing": (
            '<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">'
            # 플랫탑 헤어
            '<rect x="31" y="7" width="38" height="14" rx="2" fill="#164e63"/>'
            '<rect x="32" y="9" width="36" height="12" rx="2" fill="#0e7490"/>'
            '<ellipse cx="50" cy="21" rx="18" ry="10" fill="#0e7490"/>'
            # 얼굴
            '<circle cx="50" cy="32" r="15" fill="#8B6A4A"/>'
            '<circle cx="43" cy="29" r="3.5" fill="#1a1a1a"/>'
            '<circle cx="57" cy="29" r="3.5" fill="#1a1a1a"/>'
            '<circle cx="44" cy="28" r="1.2" fill="white"/>'
            '<circle cx="58" cy="28" r="1.2" fill="white"/>'
            '<path d="M42 38 Q50 45 58 38" stroke="#1a1a1a" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
            # 목 체인
            '<path d="M43 46 Q50 51 57 46" stroke="#fbbf24" stroke-width="2" fill="none"/>'
            # 90s 재킷
            '<path d="M27 49 L50 46 L73 49 L76 115 L24 115 Z" fill="#0891b2" opacity="0.9"/>'
            '<path d="M50 49 L40 59 L34 49" fill="#164e63"/>'
            '<path d="M50 49 L60 59 L66 49" fill="#164e63"/>'
            # 붐박스
            '<rect x="63" y="51" width="30" height="18" rx="3" fill="#1e293b"/>'
            '<circle cx="70" cy="60" r="5.5" fill="#334155"/>'
            '<circle cx="70" cy="60" r="3"   fill="#475569"/>'
            '<circle cx="82" cy="60" r="5.5" fill="#334155"/>'
            '<circle cx="82" cy="60" r="3"   fill="#475569"/>'
            '<rect x="74" y="56" width="4" height="3" rx="1" fill="#0ea5e9"/>'
            # 팔
            '<line x1="73" y1="57" x2="70" y2="55" stroke="#8B6A4A" stroke-width="6" stroke-linecap="round"/>'
            '<line x1="27" y1="57" x2="13" y2="70" stroke="#8B6A4A" stroke-width="6" stroke-linecap="round"/>'
            # 사운드웨이브
            '<path d="M93 55 Q96 60 93 65" stroke="rgba(14,165,233,0.8)" stroke-width="2" fill="none"/>'
            '<path d="M96 52 Q100 60 96 68" stroke="rgba(14,165,233,0.55)" stroke-width="1.5" fill="none"/>'
            '</svg>'
        ),
        "🌊 Quiet Storm R&B": (
            '<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">'
            # 우아한 업도 헤어
            '<ellipse cx="50" cy="17" rx="17" ry="14" fill="#064e3b"/>'
            '<circle cx="50" cy="19" r="12" fill="#059669"/>'
            '<circle cx="50" cy="11" r="9" fill="#10b981"/>'
            '<circle cx="56" cy="8" r="3.5" fill="#fbbf24"/>'
            '<circle cx="56" cy="8" r="2" fill="#f59e0b"/>'
            # 얼굴
            '<circle cx="50" cy="33" r="14" fill="#f5d5a8"/>'
            '<ellipse cx="44" cy="30" rx="4" ry="2.5" fill="#1a1a1a"/>'
            '<ellipse cx="56" cy="30" rx="4" ry="2.5" fill="#1a1a1a"/>'
            '<line x1="40" y1="28" x2="38" y2="26" stroke="#1a1a1a" stroke-width="1"/>'
            '<line x1="60" y1="28" x2="62" y2="26" stroke="#1a1a1a" stroke-width="1"/>'
            '<path d="M44 38 Q50 43 56 38 Q53 41 50 42 Q47 41 44 38" fill="#be185d"/>'
            # 목걸이
            '<path d="M40 47 Q50 51 60 47" stroke="#f0fdf4" stroke-width="1.5" stroke-dasharray="3,2" fill="none"/>'
            # 드레스
            '<path d="M32 54 L50 50 L68 54 L65 115 L35 115 Z" fill="#065f46" opacity="0.9"/>'
            '<path d="M32 59 Q45 70 40 85 L35 115" fill="#047857" opacity="0.5"/>'
            # 빈티지 마이크 스탠드
            '<circle cx="78" cy="59" r="6.5" fill="#9ca3af"/>'
            '<circle cx="78" cy="59" r="4"   fill="#6b7280"/>'
            '<rect x="76" y="64" width="4" height="28" fill="#9ca3af"/>'
            '<ellipse cx="78" cy="93" rx="8" ry="3" fill="#6b7280"/>'
            # 팔
            '<line x1="68" y1="64" x2="76" y2="61" stroke="#f5d5a8" stroke-width="5" stroke-linecap="round"/>'
            '<line x1="32" y1="61" x2="20" y2="74" stroke="#f5d5a8" stroke-width="5" stroke-linecap="round"/>'
            '<text x="6"  y="48" font-size="13" fill="rgba(167,243,208,0.85)" font-family="serif">♩</text>'
            '<text x="85" y="44" font-size="10" fill="rgba(167,243,208,0.65)" font-family="serif">♪</text>'
            '</svg>'
        ),
        "🎸 60~70s Classic Soul / Motown": (
            '<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">'
            # 숏 헤어 모타운
            '<ellipse cx="50" cy="19" rx="16" ry="14" fill="#78350f"/>'
            '<ellipse cx="50" cy="21" rx="13" ry="10" fill="#92400e"/>'
            # 얼굴
            '<circle cx="50" cy="33" r="14" fill="#7a4a2f"/>'
            '<ellipse cx="44" cy="30" rx="4" ry="2.5" fill="#1c1917"/>'
            '<ellipse cx="56" cy="30" rx="4" ry="2.5" fill="#1c1917"/>'
            '<circle cx="45" cy="29" r="1.2" fill="white"/>'
            '<circle cx="57" cy="29" r="1.2" fill="white"/>'
            '<path d="M43 38 Q50 43 57 38" stroke="#1c1917" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
            # 정장 슈트
            '<path d="M40 46 L50 43 L60 46 L58 54 L42 54 Z" fill="#f8fafc"/>'
            '<path d="M26 54 L50 50 L74 54 L72 115 L28 115 Z" fill="#b45309" opacity="0.9"/>'
            '<path d="M50 50 L40 61 L35 54" fill="#92400e"/>'
            '<path d="M50 50 L60 61 L65 54" fill="#92400e"/>'
            '<path d="M48 50 L52 50 L53 67 L50 71 L47 67 Z" fill="#dc2626"/>'
            # 들어올린 주먹 (Black Power)
            '<circle cx="17" cy="44" r="8" fill="#7a4a2f"/>'
            '<rect x="13" y="39" width="8" height="9" rx="3" fill="#7a4a2f"/>'
            '<line x1="26" y1="62" x2="17" y2="49" stroke="#7a4a2f" stroke-width="7" stroke-linecap="round"/>'
            # 오른팔
            '<line x1="74" y1="64" x2="83" y2="77" stroke="#7a4a2f" stroke-width="6" stroke-linecap="round"/>'
            # 트로피
            '<text x="78" y="81" font-size="15" fill="rgba(251,191,36,0.95)">🏆</text>'
            '<text x="4"  y="36" font-size="11" fill="rgba(251,191,36,0.9)">✦</text>'
            '<text x="83" y="50" font-size="10" fill="rgba(251,191,36,0.8)">★</text>'
            '</svg>'
        ),
        "🎧 90s Hip-Hop Soul": (
            '<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">'
            # 뒤로 쓴 야구 모자
            '<ellipse cx="50" cy="17" rx="19" ry="10" fill="#1e1b4b"/>'
            '<rect x="31" y="13" width="38" height="9" rx="4" fill="#312e81"/>'
            '<rect x="38" y="22" width="24" height="4" rx="2" fill="#1e293b"/>'
            '<rect x="47" y="13" width="8" height="5" rx="1" fill="#dc2626"/>'
            # 얼굴
            '<circle cx="50" cy="33" r="14" fill="#8b5e3c"/>'
            '<path d="M42 30 Q45 28 48 30" stroke="#2d1810" stroke-width="2" fill="none"/>'
            '<path d="M52 30 Q55 28 58 30" stroke="#2d1810" stroke-width="2" fill="none"/>'
            '<path d="M45 38 Q51 42 55 38" stroke="#2d1810" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
            # 목
            '<rect x="46" y="46" width="8" height="6" rx="2" fill="#8b5e3c"/>'
            # 오버사이즈 후디
            '<path d="M24 52 L50 48 L76 52 L80 115 L20 115 Z" fill="#7f1d1d" opacity="0.9"/>'
            '<rect x="34" y="78" width="32" height="18" rx="5" fill="#991b1b" opacity="0.7"/>'
            # 목걸이 체인
            '<path d="M40 50 Q50 54 60 50" stroke="#fbbf24" stroke-width="2.5" fill="none"/>'
            # 왼팔 + 턴테이블
            '<line x1="24" y1="62" x2="13" y2="72" stroke="#8b5e3c" stroke-width="7" stroke-linecap="round"/>'
            '<rect x="2"  y="70" width="22" height="15" rx="3" fill="#1e293b"/>'
            '<circle cx="13" cy="77" r="5.5" fill="#374151"/>'
            '<circle cx="13" cy="77" r="2.5" fill="#111827"/>'
            '<rect x="19" y="73" width="3.5" height="4" rx="1" fill="#fbbf24"/>'
            # 오른팔 들어올림
            '<line x1="76" y1="60" x2="86" y2="50" stroke="#8b5e3c" stroke-width="7" stroke-linecap="round"/>'
            '<text x="82" y="67" font-size="12" fill="rgba(252,165,165,0.8)" font-family="serif">♫</text>'
            '<text x="0"  y="62" font-size="9"  fill="rgba(252,165,165,0.7)" font-family="serif">♪</text>'
            '</svg>'
        ),
        "🌍 Afrobeats / Dancehall": (
            '<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">'
            # 땋은 머리
            '<ellipse cx="50" cy="19" rx="18" ry="16" fill="#14532d"/>'
            '<line x1="36" y1="9"  x2="33" y2="34" stroke="#166534" stroke-width="3.5" stroke-linecap="round"/>'
            '<line x1="42" y1="6"  x2="39" y2="34" stroke="#15803d" stroke-width="3.5" stroke-linecap="round"/>'
            '<line x1="50" y1="5"  x2="50" y2="34" stroke="#16a34a" stroke-width="3.5" stroke-linecap="round"/>'
            '<line x1="58" y1="6"  x2="61" y2="34" stroke="#15803d" stroke-width="3.5" stroke-linecap="round"/>'
            '<line x1="64" y1="9"  x2="67" y2="34" stroke="#166534" stroke-width="3.5" stroke-linecap="round"/>'
            # 헤어 비즈
            '<circle cx="35" cy="28" r="3" fill="#fbbf24"/>'
            '<circle cx="65" cy="26" r="3" fill="#ef4444"/>'
            '<circle cx="50" cy="30" r="2.5" fill="#3b82f6"/>'
            # 얼굴
            '<circle cx="50" cy="36" r="14" fill="#6b3d1c"/>'
            '<circle cx="43" cy="33" r="4.5" fill="white"/>'
            '<circle cx="57" cy="33" r="4.5" fill="white"/>'
            '<circle cx="44" cy="33" r="2.5" fill="#1a1a1a"/>'
            '<circle cx="58" cy="33" r="2.5" fill="#1a1a1a"/>'
            '<circle cx="45" cy="32" r="1"   fill="white"/>'
            '<circle cx="59" cy="32" r="1"   fill="white"/>'
            '<path d="M41 41 Q50 48 59 41" stroke="#1a1a1a" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
            # 목
            '<rect x="46" y="49" width="8" height="6" rx="2" fill="#6b3d1c"/>'
            # 아프리카 프린트 의상
            '<path d="M27 55 L50 51 L73 55 L76 115 L24 115 Z" fill="#15803d" opacity="0.9"/>'
            '<rect x="30" y="60" width="40" height="6" fill="#fbbf24" opacity="0.65"/>'
            '<rect x="30" y="70" width="40" height="3" fill="#ef4444" opacity="0.55"/>'
            '<rect x="30" y="77" width="40" height="5" fill="#fbbf24" opacity="0.65"/>'
            # 춤 포즈 — 팔 활짝
            '<line x1="27" y1="60" x2="6"  y2="52" stroke="#6b3d1c" stroke-width="7" stroke-linecap="round"/>'
            '<line x1="73" y1="60" x2="94" y2="52" stroke="#6b3d1c" stroke-width="7" stroke-linecap="round"/>'
            # 북
            '<ellipse cx="6"  cy="55" rx="7" ry="4.5" fill="#92400e"/>'
            '<ellipse cx="94" cy="55" rx="7" ry="4.5" fill="#92400e"/>'
            # 별 + 에너지
            '<text x="4"  y="37" font-size="12" fill="rgba(251,191,36,0.95)">★</text>'
            '<text x="86" y="40" font-size="12" fill="rgba(239,68,68,0.95)">★</text>'
            '<text x="44" y="7"  font-size="10" fill="rgba(59,130,246,0.85)">✦</text>'
            '<text x="10" y="77" font-size="9"  fill="rgba(251,191,36,0.8)" font-family="serif">♫</text>'
            '<text x="80" y="74" font-size="9"  fill="rgba(239,68,68,0.8)" font-family="serif">♪</text>'
            '</svg>'
        ),
    }
    char_svg = _C.get(genre_key, _C.get("🌙 Neo-Soul", ""))

    # ── 데이터 ──
    sorted_a = sorted(attr_scores.items(), key=lambda x: x[1], reverse=True)
    max_s    = max((s for _, s in sorted_a), default=1) or 1

    ATTR_SHORT = {
        "🎵 멜로디 (Melody)":                    "MELODY",
        "🥁 리듬 & 비트 (Rhythm & Beat)":         "RHYTHM & BEAT",
        "🎸 베이스 & 그루브 (Bass & Groove)":      "BASS & GROOVE",
        "🎙️ 보컬 & 음색 (Vocal & Tone)":          "VOCAL & TONE",
        "🎹 화성 & 코드 진행 (Harmony & Chords)":  "HARMONY",
        "🎺 리얼 악기 세션 (Live Instruments)":    "LIVE INSTR.",
        "🎛️ 사운드 믹싱 & 질감 (Sound Design)":   "SOUND DESIGN",
        "📜 가사 & 메시지 (Lyrics & Message)":     "LYRICS & MSG",
    }
    SKILL_ICON = {
        "MELODY":"🎵","RHYTHM & BEAT":"⚡","BASS & GROOVE":"🔊",
        "VOCAL & TONE":"🎙","HARMONY":"🎹","LIVE INSTR.":"🎺",
        "SOUND DESIGN":"🎛","LYRICS & MSG":"📜",
    }
    SKILL_DESC = {
        "MELODY":        "선율의 파동이 상대방의 마음을 꿰뚫는다",
        "RHYTHM & BEAT": "강렬한 비트로 전장 전체를 뒤흔든다",
        "BASS & GROOVE": "무거운 베이스가 지면을 폭발시킨다",
        "VOCAL & TONE":  "폭발적인 보컬이 상대를 완전히 압도한다",
        "HARMONY":       "복잡한 화음의 미로에 상대를 가둔다",
        "LIVE INSTR.":   "라이브 에너지로 공간 전체를 지배한다",
        "SOUND DESIGN":  "입체적인 사운드가 현실을 장악한다",
        "LYRICS & MSG":  "가사의 힘이 상대의 의지를 꺾는다",
    }
    top1_key  = ATTR_SHORT.get(sorted_a[0][0], "ATTR") if sorted_a else "ATTR"
    top2_key  = ATTR_SHORT.get(sorted_a[1][0], "ATTR") if len(sorted_a) > 1 else "ATTR"
    dmg1      = max(20, min(90, round(sorted_a[0][1] / max_s * 80))) if sorted_a else 40
    dmg2      = max(15, min(70, round(sorted_a[1][1] / max_s * 60))) if len(sorted_a) > 1 else 25
    s1_icon   = SKILL_ICON.get(top1_key, "⚡")
    s2_icon   = SKILL_ICON.get(top2_key, "🔥")
    s1_desc   = SKILL_DESC.get(top1_key, "강력한 기술로 상대를 공격한다")
    s2_desc   = SKILL_DESC.get(top2_key, "특수 능력으로 상대를 압도한다")

    hp_val    = max(40, min(130, round(avg * 20) * 5))
    avg_stars = "★" * round(avg) + "☆" * (5 - round(avg))

    best_idx   = max(evaluations, key=lambda k: evaluations[k].get("score", 0), default=0)
    best_t     = all_tracks[best_idx] if best_idx < len(all_tracks) else None
    best_score = evaluations.get(best_idx, {}).get("score", 0)
    best_title  = best_t["title"]  if best_t else "—"
    best_artist = best_t["artist"] if best_t else "—"
    best_stars  = "★" * best_score + "☆" * (5 - best_score)

    # 페르소나: " — " 또는 "\n" 기준으로 이름/서브 분리
    _p_raw = persona.split("\n")[0].strip()
    if " — " in _p_raw:
        _sp    = _p_raw.split(" — ", 1)
        p_name = _sp[0].strip()
        # 속성 이름만 추출 (첫 괄호 이전까지) — "🎛️ 사운드 믹싱 & 질감 (Sound Design)..." → "🎛️ 사운드 믹싱 & 질감"
        _raw_sub = _sp[1].strip()
        p_sub = _raw_sub.split("(")[0].strip()[:22]
    else:
        p_name = _p_raw
        p_sub  = ""
    p_sub_html = f'<div class="psub">{p_sub}</div>' if p_sub else ""
    phase_badge  = (
        '<span style="background:rgba(255,100,50,0.35);border:1px solid rgba(255,120,60,0.7);'
        'border-radius:6px;padding:1px 5px;font-size:8px;margin-left:5px;color:#ffaa88;">'
        'DEEP</span>'
    ) if is_phase2 else ""

    # ── 일러스트 박스 메쉬 그라디언트 ──
    illu_bg = (
        f"radial-gradient(ellipse at 22% 25%, {_adjust_hex(genre_color,+0.52)}cc 0%, transparent 46%),"
        f"radial-gradient(ellipse at 78% 75%, {_adjust_hex(genre_color,-0.38)}cc 0%, transparent 46%),"
        f"radial-gradient(ellipse at 75% 20%, rgba(255,255,255,0.20) 0%, transparent 38%),"
        f"radial-gradient(ellipse at 25% 80%, rgba(0,0,0,0.28) 0%, transparent 38%),"
        f"linear-gradient(138deg, {light_hex} 0%, {genre_color} 50%, {dark_hex} 100%)"
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{
  background:transparent;
  display:flex;flex-direction:column;align-items:center;
  padding:0;margin:0;
  font-family:'Pretendard',-apple-system,BlinkMacSystemFont,sans-serif;
}}
.outer{{
  background:radial-gradient(ellipse at 50% 40%,{_adjust_hex(genre_color,-0.38)} 0%,#080810 80%);
  border-radius:16px;padding:14px 13px;display:inline-flex;
}}
.cw{{
  filter:drop-shadow(0 0 28px {genre_color}55) drop-shadow(0 10px 30px rgba(0,0,0,0.7));
  transition:transform .25s ease;cursor:pointer;
}}
.cw:hover{{transform:translateY(-5px) rotate(0.6deg) scale(1.01);}}
.card{{
  width:355px;
  background:linear-gradient(152deg,{light_hex} 0%,{genre_color} 44%,{dark_hex} 100%);
  border:5px solid {border_hex};
  border-radius:18px;padding:8px;position:relative;overflow:hidden;
}}
/* 홀로그램 포일 */
.card::before{{
  content:'';position:absolute;inset:0;border-radius:14px;
  background:linear-gradient(
    122deg,
    transparent 6%,rgba(255,255,255,0.035) 16%,
    rgba(255,100,80,0.08) 24%,rgba(255,230,80,0.08) 31%,
    rgba(80,230,110,0.08) 38%,rgba(80,155,255,0.08) 45%,
    rgba(170,80,255,0.08) 52%,rgba(255,80,160,0.08) 59%,
    rgba(255,255,255,0.035) 68%,transparent 80%
  );
  pointer-events:none;z-index:20;
}}
/* 스펙큘러 광택 */
.card::after{{
  content:'';position:absolute;inset:0;border-radius:14px;
  background:linear-gradient(
    46deg,transparent 30%,
    rgba(255,255,255,0.11) 44%,rgba(255,255,255,0.07) 53%,
    transparent 65%
  );
  pointer-events:none;z-index:21;
}}
.inner{{
  border:2px solid rgba(255,255,255,0.28);border-radius:12px;
  padding:10px 11px 8px;position:relative;z-index:1;
  display:flex;flex-direction:column;gap:7px;
}}
/* 헤더 */
.hdr{{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;}}
.pname{{font-size:17px;font-weight:900;color:#fff;line-height:1.2;
  text-shadow:1px 2px 5px rgba(0,0,0,0.55),0 0 14px rgba(255,255,255,0.18);}}
.hp-line{{font-size:9px;color:rgba(255,255,255,0.52);margin-top:3px;letter-spacing:.4px;}}
.tbadge{{
  background:rgba(0,0,0,0.28);border:1.5px solid rgba(255,255,255,0.32);
  border-radius:20px;padding:4px 9px;font-size:11px;font-weight:700;
  color:#fff;text-align:center;white-space:nowrap;
}}
.tbadge .em{{font-size:15px;display:block;line-height:1.3;}}
/* 일러스트 박스 */
.ibox{{
  width:100%;height:210px;
  border:2.5px solid rgba(255,255,255,0.32);border-radius:10px;
  overflow:hidden;position:relative;
  background:{illu_bg};
}}
.ibox::before{{
  content:'';position:absolute;inset:0;
  background:
    repeating-linear-gradient(0deg,transparent,transparent 27px,rgba(255,255,255,0.03) 27px,rgba(255,255,255,0.03) 28px),
    repeating-linear-gradient(90deg,transparent,transparent 27px,rgba(255,255,255,0.03) 27px,rgba(255,255,255,0.03) 28px);
}}
/* ── 캐릭터 부유 애니메이션 ── */
@keyframes levitate{{
  0%,100%{{transform:translateY(0px) scale(1);}}
  50%{{transform:translateY(-8px) scale(1.02);}}
}}
/* 캐릭터 래퍼 */
.char-wrap{{
  position:absolute;inset:0;
  display:flex;align-items:center;justify-content:center;
  animation:levitate 3.8s ease-in-out infinite;
}}
.char-wrap svg{{
  height:190px;width:auto;
  filter:
    drop-shadow(0 0 18px {genre_color}cc)
    drop-shadow(0 8px 16px rgba(0,0,0,0.65))
    drop-shadow(0 0 40px {genre_color}66);
}}
.ino{{position:absolute;bottom:5px;right:8px;font-size:9px;color:rgba(255,255,255,0.30);
  font-weight:600;letter-spacing:1px;}}
/* 레어리티 */
.rrow{{
  display:flex;justify-content:space-between;align-items:center;
  border-bottom:1px solid rgba(255,255,255,0.14);padding-bottom:5px;
}}
.rname{{font-size:9px;font-weight:700;color:{border_hex};letter-spacing:1.5px;
  text-shadow:0 0 8px {border_hex}88;}}
.rsym{{font-size:13px;color:{border_hex};text-shadow:0 0 10px {border_hex};}}
/* 스킬 */
.sk{{
  background:rgba(0,0,0,0.22);border:1px solid rgba(255,255,255,0.10);
  border-radius:8px;padding:7px 10px;
}}
.sk-title{{font-size:8px;font-weight:700;color:rgba(255,255,255,0.40);
  letter-spacing:2px;margin-bottom:5px;}}
.sr{{display:flex;justify-content:space-between;align-items:flex-start;padding:3px 0;}}
.sr+.sr{{border-top:1px solid rgba(255,255,255,0.09);margin-top:3px;padding-top:6px;}}
.sn{{font-size:12px;font-weight:800;color:#fff;
  text-shadow:0 1px 3px rgba(0,0,0,0.5);}}
.sd{{font-size:9px;color:rgba(255,255,255,0.46);margin-top:2px;}}
.dmg{{font-size:18px;font-weight:900;color:#ffe066;white-space:nowrap;padding-left:6px;
  text-shadow:0 0 10px rgba(255,224,102,0.65),1px 1px 0 rgba(0,0,0,0.5);align-self:center;}}
.dmu{{font-size:9px;font-weight:600;color:rgba(255,220,80,0.65);}}
/* 플레이버 */
.flv{{
  background:rgba(0,0,0,0.18);border-left:2.5px solid rgba(255,255,255,0.28);
  border-radius:0 6px 6px 0;padding:6px 9px;
  font-size:10px;color:rgba(255,255,255,0.78);font-style:italic;line-height:1.55;
}}
/* 풋터 */
.ftr{{
  display:flex;justify-content:space-between;align-items:center;
  border-top:1px solid rgba(255,255,255,0.14);padding-top:6px;
  font-size:8px;color:rgba(255,255,255,0.38);letter-spacing:.3px;
}}
.ftr-s{{color:rgba(255,255,255,0.62);font-weight:600;}}
.psub{{font-size:10px;color:rgba(255,255,255,0.58);margin-top:3px;
  font-style:italic;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:190px;}}
</style>
</head>
<body>
<div class="outer">
<div class="cw">
  <div class="card">
    <div class="inner">

      <div class="hdr">
        <div>
          <div class="pname">{p_name}{phase_badge}</div>
          {p_sub_html}
          <div class="hp-line">HP {hp_val} &nbsp;·&nbsp; {avg_stars}</div>
        </div>
        <div class="tbadge">
          <span class="em">{genre_emoji}</span>
          <span>{genre_short}</span>
        </div>
      </div>

      <div class="ibox">
        <div class="char-wrap">
          {char_svg}
        </div>
        <div class="ino">No.{card_no}</div>
      </div>

      <div class="rrow">
        <span class="rname">{rarity_name}</span>
        <span class="rsym">{rarity_sym}</span>
      </div>

      <div class="sk">
        <div class="sk-title">⚔ SPECIAL ABILITIES</div>
        <div class="sr">
          <div>
            <div class="sn">{s1_icon} {top1_key}</div>
            <div class="sd">{s1_desc}</div>
          </div>
          <div class="dmg">{dmg1}<span class="dmu"> DMG</span></div>
        </div>
        <div class="sr">
          <div>
            <div class="sn">{s2_icon} {top2_key}</div>
            <div class="sd">{s2_desc}</div>
          </div>
          <div class="dmg">{dmg2}<span class="dmu"> DMG</span></div>
        </div>
      </div>

      <div class="flv">
        🎵 나의 최애 트랙: &ldquo;{best_title}&rdquo;<br>
        {best_artist} &nbsp;·&nbsp; {best_stars}
      </div>

      <div class="ftr">
        <span class="ftr-s">{avg:.1f} / 5.0</span>
        <span>Illus. BLACK MUSIC DIGGING</span>
        <span>{card_no} / 008</span>
      </div>

    </div>
  </div>
</div>
</div>
</div>

<button id="dl-btn" onclick="downloadCard()" style="
  display:block;width:381px;margin:28px 0 4px;
  padding:14px 20px;
  background:linear-gradient(135deg,#ff385c,#c8002a);
  color:#fff;border:none;border-radius:12px;
  font-size:15px;font-weight:700;cursor:pointer;
  font-family:'Pretendard',sans-serif;letter-spacing:0.2px;
  transition:opacity .15s;
" onmouseover="this.style.opacity='.82'"
   onmouseout="this.style.opacity='1'">
  📸 내 음악 DNA 포토카드 저장하기
</button>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
function downloadCard() {{
  var btn = document.getElementById('dl-btn');
  if (typeof html2canvas === 'undefined') {{
    btn.textContent = '⏳ 로딩 중... 다시 클릭해주세요'; return;
  }}
  btn.textContent = '⏳ 이미지 생성 중...';
  btn.disabled = true;
  html2canvas(document.querySelector('.outer'), {{
    scale: 2,
    useCORS: true,
    allowTaint: true,
    backgroundColor: '#080810',
    logging: false
  }}).then(function(canvas) {{
    var a = document.createElement('a');
    a.href = canvas.toDataURL('image/jpeg', 0.95);
    a.download = 'digging_card_{safe_genre}.jpg';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    btn.textContent = '✅ 저장 완료!';
    setTimeout(function() {{
      btn.textContent = '📸 내 음악 DNA 포토카드 저장하기';
      btn.disabled = false;
    }}, 2000);
  }}).catch(function() {{
    btn.textContent = '❌ 다시 시도해주세요';
    btn.disabled = false;
  }});
}}
</script>
</body>
</html>"""


def render_master_card_html(collection: dict) -> str:
    """8개 장르 완료 보상 — 얼티밋 마스터 카드 (무지개 홀로그램)"""
    total_attrs: dict = {}
    for gd in collection.values():
        for attr, score in gd.get("attr_scores", {}).items():
            total_attrs[attr] = total_attrs.get(attr, 0) + score

    ATTR_SHORT = {
        "🎵 멜로디 (Melody)":"MELODY",
        "🥁 리듬 & 비트 (Rhythm & Beat)":"RHYTHM & BEAT",
        "🎸 베이스 & 그루브 (Bass & Groove)":"BASS & GROOVE",
        "🎙️ 보컬 & 음색 (Vocal & Tone)":"VOCAL & TONE",
        "🎹 화성 & 코드 진행 (Harmony & Chords)":"HARMONY",
        "🎺 리얼 악기 세션 (Live Instruments)":"LIVE INSTR.",
        "🎛️ 사운드 믹싱 & 질감 (Sound Design)":"SOUND DESIGN",
        "📜 가사 & 메시지 (Lyrics & Message)":"LYRICS & MSG",
    }
    SKILL_ICON = {
        "MELODY":"🎵","RHYTHM & BEAT":"⚡","BASS & GROOVE":"🔊",
        "VOCAL & TONE":"🎙","HARMONY":"🎹","LIVE INSTR.":"🎺",
        "SOUND DESIGN":"🎛","LYRICS & MSG":"📜",
    }
    SKILL_DESC = {
        "MELODY":"8개 장르를 가로지르는 선율의 절대 지배자",
        "RHYTHM & BEAT":"우주를 흔드는 리듬의 궁극 마스터",
        "BASS & GROOVE":"대지를 진동시키는 그루브의 신",
        "VOCAL & TONE":"영혼을 관통하는 보컬의 절대자",
        "HARMONY":"모든 화음을 초월한 화성의 주인",
        "LIVE INSTR.":"라이브 에너지의 완전한 지배자",
        "SOUND DESIGN":"사운드 공간을 창조하는 마에스트로",
        "LYRICS & MSG":"가사로 세상을 바꾸는 시인",
    }
    sorted_a = sorted(total_attrs.items(), key=lambda x: x[1], reverse=True)
    top1 = ATTR_SHORT.get(sorted_a[0][0], "ATTR") if sorted_a else "ATTR"
    top2 = ATTR_SHORT.get(sorted_a[1][0], "ATTR") if len(sorted_a) > 1 else "ATTR"
    s1_icon = SKILL_ICON.get(top1, "⚡")
    s2_icon = SKILL_ICON.get(top2, "🔥")
    s1_desc = SKILL_DESC.get(top1, "궁극의 능력")
    s2_desc = SKILL_DESC.get(top2, "전설의 기술")
    mx   = max(sorted_a[0][1], 1) if sorted_a else 1
    dmg1 = min(999, round(sorted_a[0][1] / mx * 200)) if sorted_a else 100
    dmg2 = min(999, round(sorted_a[1][1] / mx * 160)) if len(sorted_a) > 1 else 80
    n_deep = sum(1 for v in collection.values() if v.get("is_phase2"))

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:transparent;display:flex;flex-direction:column;align-items:center;
  padding:0;margin:0;font-family:'Pretendard',-apple-system,sans-serif;}}
@keyframes rainbowFlow{{
  0%{{background-position:0% 50%;}} 50%{{background-position:100% 50%;}} 100%{{background-position:0% 50%;}}
}}
@keyframes pulseGlow{{
  0%,100%{{box-shadow:0 0 32px rgba(255,215,0,.7),0 0 64px rgba(255,0,128,.35),0 0 100px rgba(0,200,255,.2);}}
  50%{{box-shadow:0 0 64px rgba(255,215,0,1),0 0 100px rgba(0,200,255,.5),0 0 150px rgba(255,0,128,.4);}}
}}
@keyframes levitate{{
  0%,100%{{transform:translateY(0) scale(1);}} 50%{{transform:translateY(-10px) scale(1.04);}}
}}
@keyframes crownPulse{{
  0%,100%{{filter:drop-shadow(0 0 14px #ffd700) drop-shadow(0 0 28px #ff8800);}}
  50%{{filter:drop-shadow(0 0 28px #fff) drop-shadow(0 0 50px #ffd700);}}
}}
@keyframes twinkle{{
  0%,100%{{opacity:0;transform:scale(.5);}} 50%{{opacity:1;transform:scale(1.8);}}
}}
.rainbow-wrap{{
  background:linear-gradient(90deg,#ff0040,#ff8800,#ffee00,#00ff88,#00aaff,#8844ff,#ff0040);
  background-size:400% 100%;
  animation:rainbowFlow 2.5s linear infinite, pulseGlow 2.8s ease-in-out infinite;
  border-radius:24px;padding:6px;
}}
.card{{
  width:355px;
  background:linear-gradient(152deg,#1a0040 0%,#060012 50%,#000820 100%);
  border-radius:20px;padding:8px;position:relative;overflow:hidden;
}}
.card::before{{
  content:'';position:absolute;inset:0;border-radius:16px;
  background:linear-gradient(122deg,
    transparent 6%,rgba(255,255,255,.05) 16%,
    rgba(255,60,60,.12) 24%,rgba(255,200,60,.12) 31%,
    rgba(60,230,120,.12) 38%,rgba(60,160,255,.12) 45%,
    rgba(180,60,255,.12) 52%,rgba(255,60,180,.12) 59%,
    rgba(255,255,255,.05) 68%,transparent 80%);
  pointer-events:none;z-index:20;
}}
.inner{{
  border:2px solid rgba(255,215,0,.3);border-radius:14px;
  padding:10px 11px 8px;position:relative;z-index:1;
  display:flex;flex-direction:column;gap:7px;
}}
.hdr{{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;}}
.pname{{
  font-size:14px;font-weight:900;
  background:linear-gradient(90deg,#ffd700,#ff8800,#ffee44,#00ffaa,#00aaff,#ff88cc,#ffd700);
  background-size:300%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:rainbowFlow 2s linear infinite;line-height:1.25;
}}
.hp-line{{font-size:9px;color:rgba(255,215,0,.6);margin-top:3px;}}
.tbadge{{
  background:rgba(255,215,0,.12);border:1.5px solid rgba(255,215,0,.55);
  border-radius:20px;padding:4px 9px;font-size:10px;font-weight:700;
  color:#ffd700;text-align:center;white-space:nowrap;flex-shrink:0;
}}
.tbadge .em{{font-size:15px;display:block;line-height:1.3;}}
.ibox{{
  width:100%;height:210px;
  border:2px solid rgba(255,215,0,.35);border-radius:10px;
  overflow:hidden;position:relative;
  background:
    radial-gradient(ellipse at 50% 50%,rgba(255,215,0,.18) 0%,transparent 55%),
    radial-gradient(ellipse at 20% 25%,rgba(255,0,128,.12) 0%,transparent 45%),
    radial-gradient(ellipse at 80% 75%,rgba(0,200,255,.12) 0%,transparent 45%),
    linear-gradient(145deg,#1a0040,#000820);
}}
.stars{{position:absolute;inset:0;pointer-events:none;}}
.star{{position:absolute;border-radius:50%;background:#ffd700;opacity:0;
  animation:twinkle 2s ease-in-out infinite;}}
.orb-wrap{{
  position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  animation:levitate 3.5s ease-in-out infinite;
}}
.orb{{
  width:138px;height:138px;border-radius:50%;
  background:radial-gradient(circle at 32% 32%,#fffbe0,#ffd700 28%,#ff8800 56%,#b8600a 80%,#4a1a00);
  display:flex;align-items:center;justify-content:center;
  animation:crownPulse 2.2s ease-in-out infinite;position:relative;
}}
.orb::before{{
  content:'';position:absolute;inset:-14px;border-radius:50%;
  background:radial-gradient(ellipse,rgba(255,215,0,.45) 0%,transparent 68%);
  animation:levitate 2.4s ease-in-out infinite reverse;
}}
.crown{{font-size:66px;line-height:1;position:relative;z-index:1;}}
.ino{{position:absolute;bottom:5px;right:8px;font-size:9px;
  color:rgba(255,215,0,.45);font-weight:600;letter-spacing:1px;}}
.rrow{{
  display:flex;justify-content:space-between;align-items:center;
  border-bottom:1px solid rgba(255,215,0,.2);padding-bottom:5px;
}}
.rname{{
  font-size:9px;font-weight:700;letter-spacing:1.2px;
  background:linear-gradient(90deg,#ffd700,#ff8800,#ffd700);
  background-size:200%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:rainbowFlow 2s linear infinite;
}}
.rsym{{font-size:12px;color:#ffd700;text-shadow:0 0 10px #ffd700;}}
.sk{{
  background:rgba(255,215,0,.06);border:1px solid rgba(255,215,0,.18);
  border-radius:8px;padding:7px 10px;
}}
.sk-title{{font-size:8px;font-weight:700;color:rgba(255,215,0,.5);
  letter-spacing:2px;margin-bottom:5px;}}
.sr{{display:flex;justify-content:space-between;align-items:flex-start;padding:3px 0;}}
.sr+.sr{{border-top:1px solid rgba(255,215,0,.12);margin-top:3px;padding-top:6px;}}
.sn{{font-size:12px;font-weight:800;color:#fff;}}
.sd{{font-size:9px;color:rgba(255,255,255,.44);margin-top:2px;}}
.dmg{{
  font-size:18px;font-weight:900;white-space:nowrap;padding-left:6px;align-self:center;
  background:linear-gradient(90deg,#ffd700,#ff8800);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}}
.dmu{{font-size:9px;font-weight:600;color:rgba(255,215,0,.65);}}
.flv{{
  background:rgba(255,215,0,.06);border-left:2.5px solid rgba(255,215,0,.5);
  border-radius:0 6px 6px 0;padding:6px 9px;
  font-size:10px;color:rgba(255,255,255,.76);font-style:italic;line-height:1.55;
}}
.ftr{{
  display:flex;justify-content:space-between;align-items:center;
  border-top:1px solid rgba(255,215,0,.15);padding-top:6px;
  font-size:8px;color:rgba(255,215,0,.45);letter-spacing:.3px;
}}
.ftr-s{{color:rgba(255,215,0,.8);font-weight:700;}}
</style>
</head>
<body>
<div class="rainbow-wrap">
<div class="card">
  <div class="inner">
    <div class="hdr">
      <div>
        <div class="pname">👑 ULTIMATE MASTER MIX</div>
        <div class="hp-line">HP MAX &nbsp;·&nbsp; ★★★★★ &nbsp;·&nbsp; 8/8 GENRES</div>
      </div>
      <div class="tbadge"><span class="em">🌈</span><span>ALL GENRES</span></div>
    </div>

    <div class="ibox">
      <div class="stars">
        <div class="star" style="width:4px;height:4px;left:8%;top:12%;animation-delay:0s;"></div>
        <div class="star" style="width:3px;height:3px;left:88%;top:8%;animation-delay:.4s;"></div>
        <div class="star" style="width:5px;height:5px;left:22%;top:78%;animation-delay:.8s;"></div>
        <div class="star" style="width:3px;height:3px;left:78%;top:72%;animation-delay:1.2s;"></div>
        <div class="star" style="width:4px;height:4px;left:50%;top:15%;animation-delay:1.6s;"></div>
        <div class="star" style="width:3px;height:3px;left:12%;top:50%;animation-delay:.2s;"></div>
        <div class="star" style="width:4px;height:4px;left:92%;top:45%;animation-delay:.6s;"></div>
        <div class="star" style="width:3px;height:3px;left:62%;top:88%;animation-delay:1s;"></div>
        <div class="star" style="width:5px;height:5px;left:35%;top:30%;animation-delay:1.4s;"></div>
        <div class="star" style="width:3px;height:3px;left:72%;top:28%;animation-delay:1.8s;"></div>
      </div>
      <div class="orb-wrap">
        <div class="orb"><span class="crown">👑</span></div>
      </div>
      <div class="ino">ULTIMATE / 008</div>
    </div>

    <div class="rrow">
      <span class="rname">✦ SECRET ULTIMATE RARE ✦</span>
      <span class="rsym">★◆★◆★</span>
    </div>

    <div class="sk">
      <div class="sk-title">⚔ ULTIMATE ABILITIES — 8 GENRES COMBINED</div>
      <div class="sr">
        <div>
          <div class="sn">{s1_icon} {top1}</div>
          <div class="sd">{s1_desc}</div>
        </div>
        <div class="dmg">{dmg1}<span class="dmu"> DMG</span></div>
      </div>
      <div class="sr">
        <div>
          <div class="sn">{s2_icon} {top2}</div>
          <div class="sd">{s2_desc}</div>
        </div>
        <div class="dmg">{dmg2}<span class="dmu"> DMG</span></div>
      </div>
    </div>

    <div class="flv">
      🎖 ALL 8 GENRES MASTERED<br>
      당신은 흑인음악의 진정한 디거입니다. 전설이 되었습니다.
    </div>

    <div class="ftr">
      <span class="ftr-s">MASTER COLLECTOR</span>
      <span>Illus. BLACK MUSIC DIGGING</span>
      <span>ULT / 008</span>
    </div>
  </div>
</div>
</div>

<button id="dl-btn" onclick="downloadMaster()" style="
  display:block;width:381px;margin:14px 0 4px;padding:14px 20px;
  background:linear-gradient(90deg,#ff0040,#ff8800,#ffee00,#00ff88,#00aaff,#8844ff,#ff0040);
  background-size:300% 100%;animation:rainbowFlow 2.5s linear infinite;
  color:#fff;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;
  font-family:'Pretendard',sans-serif;text-shadow:0 1px 4px rgba(0,0,0,.6);
" onmouseover="this.style.opacity='.82'" onmouseout="this.style.opacity='1'">
  👑 나의 얼티밋 마스터 카드 저장하기
</button>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
function downloadMaster() {{
  var btn = document.getElementById('dl-btn');
  if (typeof html2canvas === 'undefined') {{ btn.textContent='⏳ 로딩 중...'; return; }}
  btn.textContent='⏳ 생성 중...'; btn.disabled=true;
  html2canvas(document.querySelector('.rainbow-wrap'), {{
    scale:2, useCORS:true, allowTaint:true, backgroundColor:'#080010', logging:false
  }}).then(function(canvas) {{
    var a = document.createElement('a');
    a.href = canvas.toDataURL('image/jpeg', 0.95);
    a.download = 'ultimate_master_card.jpg';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    btn.textContent='✅ 저장 완료!';
    setTimeout(function(){{ btn.textContent='👑 나의 얼티밋 마스터 카드 저장하기'; btn.disabled=false; }}, 2000);
  }}).catch(function(){{ btn.textContent='❌ 다시 시도'; btn.disabled=false; }});
}}
</script>
</body>
</html>"""


def generate_photo_card_png(
    genre_key:   str,
    genre_color: str,
    persona:     str,
    attr_scores: dict,
    evaluations: dict,
    all_tracks:  list,
    avg:         float,
    is_phase2:   bool,
) -> bytes:
    """HTML 카드를 브라우저로 캡처 → JPEG 반환 (html2image 우선, Pillow 폴백)"""

    # ── 방법 1: html2image → 미리보기와 동일한 결과 ──
    # ① stdout/stderr 완전 차단 → Streamlit 통신 보호
    # ② 500×720 뷰포트로 여유 캡처 후 PIL 자동 크롭 → 잘림·공백 제거
    try:
        import sys as _sys, os as _os, io as _io2, tempfile as _tmp
        from html2image import Html2Image
        from PIL import Image as _PILImg, ImageChops as _IC

        _html = render_photo_card_html(
            genre_key=genre_key, genre_color=genre_color,
            persona=persona, attr_scores=attr_scores,
            evaluations=evaluations, all_tracks=all_tracks,
            avg=avg, is_phase2=is_phase2,
        )

        # html2image 로그를 Streamlit이 절대 볼 수 없게 차단
        class _Null:
            def write(self, *a): pass
            def flush(self): pass

        _so, _se = _sys.stdout, _sys.stderr
        _sys.stdout = _sys.stderr = _Null()
        _result = b""
        try:
            with _tmp.TemporaryDirectory() as _td:
                _hti = Html2Image(
                    output_path=_td,
                    custom_flags=[
                        "--no-sandbox", "--disable-gpu",
                        "--log-level=3", "--disable-logging",
                        "--disable-extensions",
                    ],
                )
                # 500×720으로 여유 있게 캡처
                _hti.screenshot(html_str=_html, save_as="card.png", size=(500, 720))
                _p = _os.path.join(_td, "card.png")
                if _os.path.exists(_p) and _os.path.getsize(_p) > 500:
                    _img = _PILImg.open(_p).convert("RGB")
                    # 흰 여백 자동 제거 (ImageChops.difference 방식)
                    _bg  = _PILImg.new("RGB", _img.size, (255, 255, 255))
                    _box = _IC.difference(_img, _bg).getbbox()
                    if _box:
                        _pad = 6  # 드롭쉐도우 6px 살리기
                        _img = _img.crop((
                            max(0,           _box[0] - _pad),
                            max(0,           _box[1] - _pad),
                            min(_img.width,  _box[2] + _pad),
                            min(_img.height, _box[3] + _pad),
                        ))
                    _buf = _io2.BytesIO()
                    _img.save(_buf, format="JPEG", quality=95)
                    _buf.seek(0)
                    _result = _buf.getvalue()
        finally:
            _sys.stdout, _sys.stderr = _so, _se  # 반드시 복원

        if _result:
            return _result

    except BaseException:
        pass

    # ── 방법 2: Pillow 폴백 (html2image 미설치 시 단순 카드) ──
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return b""

    # ── 순수 RGB 캔버스 (RGBA 합성 없음 → 파일 손상 방지) ──
    W, H = 420, 580

    # ── 색상 계산 ──
    base    = _hex_to_rgb(genre_color)
    top_c   = tuple(min(255, int(c + (255-c)*0.38)) for c in base)
    bot_c   = tuple(max(0,   int(c * 0.28))          for c in base)
    gold    = (255, 215, 0)
    bdr_c   = tuple(int(c*0.25 + g*0.75) for c, g in zip(base, gold))

    # ── 그라디언트 배경 (RGB only) ──
    img  = Image.new("RGB", (W, H), bot_c)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t  = y / H
        px = tuple(int(a*(1-t) + b*t) for a, b in zip(top_c, bot_c))
        draw.line([(0, y), (W, y)], fill=px)

    # ── 테두리 (금색 + 내부 흰 이중선) ──
    draw.rectangle([0,   0,   W-1, H-1],   outline=bdr_c,         width=5)
    draw.rectangle([6,   6,   W-7, H-7],   outline=(255,255,255), width=1)
    draw.rectangle([9,   9,   W-10, H-10], outline=(255,255,255), width=1)

    # ── 폰트 로드 ──
    def _fnt(sz, bold=False):
        paths = (["C:/Windows/Fonts/malgunbd.ttf","C:/Windows/Fonts/arialbd.ttf",
                   "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"]
                  if bold else
                  ["C:/Windows/Fonts/malgun.ttf","C:/Windows/Fonts/arial.ttf",
                   "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"])
        for p in paths:
            try: return ImageFont.truetype(p, sz)
            except: pass
        try: return ImageFont.load_default(size=sz)
        except: return ImageFont.load_default()

    # ── 이모지 제거 헬퍼 ──
    _EM = re.compile(r"[\U00010000-\U0010ffff]|‍", flags=re.UNICODE)
    def _cl(t): return _EM.sub("", t).strip()

    # ── 텍스트 폭 계산 (Pillow 버전 호환) ──
    def _tw(txt, fnt):
        try:    return draw.textbbox((0,0), txt, font=fnt)[2]
        except: pass
        try:    return draw.textsize(txt, font=fnt)[0]
        except: return len(txt) * (fnt.size if hasattr(fnt,"size") else 10)

    # ── 텍스트 그리기 헬퍼 ──
    W_  = (255, 255, 255)
    DIM = (200, 200, 200)
    YLW = (255, 220, 55)
    FNT = (150, 150, 150)
    PAD = 16

    def _tl(txt, x, y, sz=20, bold=False, col=None):
        draw.text((x, y), txt, font=_fnt(sz, bold), fill=col or W_)

    def _tr(txt, x, y, sz=20, bold=False, col=None):
        f  = _fnt(sz, bold)
        tw = _tw(txt, f)
        draw.text((x - tw, y), txt, font=f, fill=col or W_)

    def _tc(txt, y, sz=20, bold=False, col=None):
        f  = _fnt(sz, bold)
        tw = _tw(txt, f)
        draw.text(((W - tw) // 2, y), txt, font=f, fill=col or W_)

    def _hline(y):
        draw.line([(PAD+4, y), (W-PAD-4, y)], fill=(100, 100, 100), width=1)

    # ── 데이터 ──
    GENRE_META = {
        "🌙 Neo-Soul":                       ("001","Rare Holo","◆◆"),
        "🔥 Funk":                            ("002","Ultra Rare","◆◆◆"),
        "💜 Contemporary R&B":               ("003","Rare","◆"),
        "🎤 New Jack Swing":                  ("004","Uncommon","◈◈"),
        "🌊 Quiet Storm R&B":                 ("005","Rare Holo","◆◆"),
        "🎸 60~70s Classic Soul / Motown":   ("006","Secret Rare","★◆★"),
        "🎧 90s Hip-Hop Soul":               ("007","Ultra Rare","◆◆◆"),
        "🌍 Afrobeats / Dancehall":          ("008","Common","◇"),
    }
    card_no, rarity_name, rarity_sym = GENRE_META.get(genre_key, ("000","Rare","◆"))
    genre_disp = _cl(genre_key.split(" ",1)[-1].split("/")[0].strip())

    ATTR_SHORT = {
        "🎵 멜로디 (Melody)":"MELODY","🥁 리듬 & 비트 (Rhythm & Beat)":"RHYTHM & BEAT",
        "🎸 베이스 & 그루브 (Bass & Groove)":"BASS & GROOVE",
        "🎙️ 보컬 & 음색 (Vocal & Tone)":"VOCAL & TONE",
        "🎹 화성 & 코드 진행 (Harmony & Chords)":"HARMONY",
        "🎺 리얼 악기 세션 (Live Instruments)":"LIVE INSTR.",
        "🎛️ 사운드 믹싱 & 질감 (Sound Design)":"SOUND DESIGN",
        "📜 가사 & 메시지 (Lyrics & Message)":"LYRICS & MSG",
    }
    sorted_a = sorted(attr_scores.items(), key=lambda x: x[1], reverse=True)
    max_s    = max((s for _,s in sorted_a), default=1) or 1
    top1 = ATTR_SHORT.get(sorted_a[0][0],"ATTR") if sorted_a else "ATTR"
    top2 = ATTR_SHORT.get(sorted_a[1][0],"ATTR") if len(sorted_a)>1 else "ATTR"
    dmg1 = max(20, min(90, round(sorted_a[0][1]/max_s*80))) if sorted_a else 40
    dmg2 = max(15, min(70, round(sorted_a[1][1]/max_s*60))) if len(sorted_a)>1 else 25

    best_idx = max(evaluations, key=lambda k: evaluations[k].get("score",0), default=0)
    best_t   = all_tracks[best_idx] if best_idx < len(all_tracks) else None
    b_score  = evaluations.get(best_idx,{}).get("score",0)
    b_title  = best_t["title"][:22]      if best_t else "—"
    b_artist = _cl(best_t["artist"])[:20] if best_t else "—"
    b_stars  = "★"*b_score + "☆"*(5-b_score)
    avg_stars= "★"*round(avg) + "☆"*(5-round(avg))
    hp_val   = max(40, min(130, round(avg*20)*5))
    p_clean  = _cl(persona.split("\n")[0].strip())
    if " — " in p_clean:
        p_clean = p_clean.split(" — ")[0].strip()
    p_clean = p_clean[:16]

    # ── 레이아웃 렌더링 ──
    # 상단 바
    _tc("2026 MY DIGGING RECORD", 14, 13, col=DIM)
    _hline(32)

    # 헤더
    _tl(p_clean,            PAD,       46, 22, bold=True)
    _tr(f"HP {hp_val}",     W-PAD,     46, 17, col=YLW)
    _tl(genre_disp.upper(), PAD,       70, 15, col=DIM)
    _tr(f"{rarity_name} {rarity_sym}", W-PAD, 70, 13, col=bdr_c)
    _hline(84)

    # 일러스트 박스
    draw.rectangle([PAD, 90, W-PAD, 230], outline=(180,180,180), width=1)
    # 박스 배경 (어둡게)
    box_fill = tuple(max(0, int(c*0.45)) for c in base)
    draw.rectangle([PAD+1, 91, W-PAD-1, 229], fill=box_fill)
    # 박스 안 동심원 패턴
    cx_, cy_ = W//2, 160
    for r, alpha in [(80,40),(60,55),(40,70),(20,90)]:
        shade = tuple(min(255, int(c + (255-c)*(alpha/100))) for c in base)
        draw.ellipse([cx_-r, cy_-r, cx_+r, cy_+r], outline=shade, width=2)
    _tc(genre_disp.upper(), 148, 18, bold=True)
    _tr(f"No.{card_no}",    W-PAD-4, 220, 11, col=FNT)
    _hline(236)

    # 레어리티
    _tl(rarity_name, PAD, 248, 13, col=bdr_c)
    _tr(rarity_sym,  W-PAD, 248, 14, col=bdr_c)
    _hline(262)

    # 스킬
    _tc("SPECIAL ABILITIES", 274, 12, col=DIM)
    _hline(286)
    _tl(top1,            PAD,   302, 17, bold=True)
    _tr(f"{dmg1} DMG",   W-PAD, 302, 17, bold=True, col=YLW)
    _hline(316)
    _tl(top2,            PAD,   332, 17, bold=True)
    _tr(f"{dmg2} DMG",   W-PAD, 332, 17, bold=True, col=YLW)
    _hline(346)

    # 최애 트랙
    _tl(f'"{b_title}"',          PAD, 360, 16, bold=True)
    _tl(f"{b_artist}  {b_stars}", PAD, 380, 14, col=DIM)
    _hline(398)

    # 총점
    _tc(avg_stars,          416, 22)
    _tc(f"{avg:.1f} / 5.0", 444, 20, bold=True)
    _hline(466)

    # 풋터
    _tl(f"Illus. BLACK MUSIC DIGGING", PAD, 478, 11, col=FNT)
    _tr(f"{card_no}/008",               W-PAD, 478, 11, col=FNT)
    if is_phase2:
        _tc("DEEP ANALYSIS EDITION", 496, 10, col=FNT)

    # ── JPEG 저장 (Windows PNG 레지스트리 오류 우회) ──
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    buf.seek(0)
    return buf.getvalue()


def render_master_gold_card_html(collection: dict) -> str:
    """8개 장르 완료 보상 — SECRET ULTIMATE RARE 카드 HTML"""
    # ── 합산 속성 ──
    total_attrs: dict = {}
    for gd in collection.values():
        for attr, score in gd.get("attr_scores", {}).items():
            total_attrs[attr] = total_attrs.get(attr, 0) + score

    ATTR_SHORT = {
        "🎵 멜로디 (Melody)":"MELODY",
        "🥁 리듬 & 비트 (Rhythm & Beat)":"RHYTHM & BEAT",
        "🎸 베이스 & 그루브 (Bass & Groove)":"BASS & GROOVE",
        "🎙️ 보컬 & 음색 (Vocal & Tone)":"VOCAL & TONE",
        "🎹 화성 & 코드 진행 (Harmony & Chords)":"HARMONY",
        "🎺 리얼 악기 세션 (Live Instruments)":"LIVE INSTR.",
        "🎛️ 사운드 믹싱 & 질감 (Sound Design)":"SOUND DESIGN",
        "📜 가사 & 메시지 (Lyrics & Message)":"LYRICS & MSG",
    }
    SKILL_ICON = {
        "MELODY":"🎵","RHYTHM & BEAT":"⚡","BASS & GROOVE":"🔊",
        "VOCAL & TONE":"🎙","HARMONY":"🎹","LIVE INSTR.":"🎺",
        "SOUND DESIGN":"🎛","LYRICS & MSG":"📜",
    }
    SKILL_DESC_M = {
        "MELODY":"8개 장르를 가로지르는 선율의 절대 지배자",
        "RHYTHM & BEAT":"우주를 흔드는 리듬의 궁극 마스터",
        "BASS & GROOVE":"대지를 진동시키는 그루브의 신",
        "VOCAL & TONE":"영혼을 관통하는 보컬의 절대자",
        "HARMONY":"모든 화음을 초월한 화성의 주인",
        "LIVE INSTR.":"라이브 에너지의 완전한 지배자",
        "SOUND DESIGN":"사운드 공간을 창조하는 마에스트로",
        "LYRICS & MSG":"가사로 세상을 바꾸는 전설의 시인",
    }
    sorted_a = sorted(total_attrs.items(), key=lambda x: x[1], reverse=True)
    mx       = max(sorted_a[0][1], 1) if sorted_a else 1
    top1_key = ATTR_SHORT.get(sorted_a[0][0], "ATTR") if sorted_a else "ATTR"
    top2_key = ATTR_SHORT.get(sorted_a[1][0], "ATTR") if len(sorted_a) > 1 else "ATTR"
    dmg1     = min(999, round(sorted_a[0][1] / mx * 200)) if sorted_a else 100
    dmg2     = min(999, round(sorted_a[1][1] / mx * 160)) if len(sorted_a) > 1 else 80
    s1_icon  = SKILL_ICON.get(top1_key, "⚡")
    s2_icon  = SKILL_ICON.get(top2_key, "🔥")
    s1_desc  = SKILL_DESC_M.get(top1_key, "궁극의 능력")
    s2_desc  = SKILL_DESC_M.get(top2_key, "전설의 기술")
    n_deep   = sum(1 for v in collection.values() if v.get("is_phase2"))

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{
  background:transparent;
  display:flex;flex-direction:column;align-items:center;
  padding:0;margin:0;
  font-family:'Pretendard',-apple-system,BlinkMacSystemFont,sans-serif;
}}

/* ── 레인보우 테두리 래퍼 ── */
.rainbow-wrap{{
  background:linear-gradient(135deg,#ff0040,#ff7700,#ffee00,#00ff88,#00aaff,#8844ff,#ff0040);
  border-radius:26px;
  padding:5px;
  filter:drop-shadow(0 0 32px rgba(255,100,0,.55)) drop-shadow(0 12px 40px rgba(0,0,0,.75));
}}

/* ── 카드 본체 ── */
.card{{
  width:355px;
  background:linear-gradient(150deg,#2c0055 0%,#160030 45%,#06000f 100%);
  border-radius:22px;
  padding:0;
  position:relative;
  overflow:hidden;
}}

/* 홀로그램 포일 shimmer */
.card::before{{
  content:'';position:absolute;inset:0;border-radius:22px;
  background:linear-gradient(
    118deg,
    transparent 8%,rgba(255,255,255,0.03) 18%,
    rgba(255,80,80,0.06) 26%,rgba(255,200,50,0.06) 33%,
    rgba(80,230,120,0.06) 40%,rgba(80,160,255,0.06) 47%,
    rgba(180,60,255,0.06) 54%,rgba(255,60,180,0.06) 61%,
    rgba(255,255,255,0.03) 70%,transparent 82%
  );
  pointer-events:none;z-index:20;
}}

/* ── 내부 패딩 ── */
.inner{{
  padding:16px 14px 14px;
  display:flex;flex-direction:column;gap:10px;
  position:relative;z-index:1;
}}

/* ── 헤더 ── */
.hdr{{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;}}
.card-title{{
  font-size:19px;font-weight:900;color:#fff;line-height:1.2;
  letter-spacing:.3px;
  text-shadow:0 0 20px rgba(255,200,0,.6),1px 2px 4px rgba(0,0,0,.7);
  display:flex;align-items:center;gap:6px;
}}
.hp-line{{font-size:10px;color:rgba(255,255,255,0.52);margin-top:5px;letter-spacing:.5px;}}

/* ALL GENRES 배지 */
.badge-wrap{{
  background:linear-gradient(135deg,#ff0040,#ff7700,#ffee00,#00ff88,#00aaff,#8844ff);
  border-radius:18px;padding:3px;flex-shrink:0;
}}
.badge-inner{{
  background:#16002e;border-radius:16px;
  padding:6px 11px;text-align:center;min-width:76px;
}}
.badge-em{{font-size:17px;display:block;line-height:1.3;}}
.badge-txt{{font-size:9px;font-weight:700;color:#fff;letter-spacing:1.5px;}}

/* ── 일러스트 박스 ── */
.ibox{{
  width:100%;height:220px;
  background:linear-gradient(150deg,#1e0040 0%,#090018 100%);
  border-radius:14px;
  position:relative;overflow:hidden;
  border:1px solid rgba(255,255,255,0.08);
}}

/* 황금 글로우 원 */
.gold-orb{{
  position:absolute;top:50%;left:50%;
  transform:translate(-50%,-52%);
  width:162px;height:162px;border-radius:50%;
  background:radial-gradient(circle at 36% 34%,#fff9a0 0%,#ffe040 18%,#ffb300 45%,#c97800 72%,#7a4400 100%);
  box-shadow:0 0 50px rgba(255,180,0,.65),0 0 100px rgba(255,140,0,.35);
  display:flex;align-items:center;justify-content:center;
  font-size:86px;line-height:1;
}}

/* 배경 빛줄기 */
.ibox::before{{
  content:'';position:absolute;inset:0;
  background:
    radial-gradient(ellipse at 50% 52%,rgba(255,180,0,.18) 0%,transparent 65%),
    radial-gradient(ellipse at 20% 20%,rgba(120,0,255,.10) 0%,transparent 50%),
    radial-gradient(ellipse at 80% 80%,rgba(0,100,255,.08) 0%,transparent 50%);
}}
.ino{{position:absolute;bottom:8px;right:10px;font-size:9px;
  color:rgba(255,200,100,0.40);font-weight:600;letter-spacing:2px;}}

/* ── 레어리티 행 ── */
.rrow{{
  display:flex;justify-content:space-between;align-items:center;
  padding:5px 2px;
  border-top:1px solid rgba(255,215,0,.18);
  border-bottom:1px solid rgba(255,215,0,.18);
}}
.rname{{
  font-size:10px;font-weight:700;color:#FFD700;letter-spacing:1.5px;
  text-shadow:0 0 10px rgba(255,215,0,.6);
}}
.rsym{{font-size:15px;color:#FFD700;text-shadow:0 0 12px rgba(255,215,0,.7);}}

/* ── 스킬 박스 ── */
.sk{{
  background:rgba(0,0,0,0.32);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:10px;padding:10px 12px;
}}
.sk-title{{
  font-size:8px;font-weight:700;color:rgba(255,255,255,0.38);
  letter-spacing:2.5px;margin-bottom:8px;
}}
.sr{{display:flex;justify-content:space-between;align-items:center;padding:5px 0;}}
.sr+.sr{{border-top:1px solid rgba(255,255,255,0.07);}}
.sn{{font-size:14px;font-weight:800;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.5);}}
.sd{{font-size:9px;color:rgba(255,255,255,0.42);margin-top:3px;}}
.dmg-box{{
  background:#FFB300;border-radius:7px;
  padding:5px 9px;min-width:54px;text-align:center;flex-shrink:0;
}}
.dmg-val{{font-size:22px;font-weight:900;color:#000;line-height:1;}}
.dmg-unit{{font-size:8px;font-weight:700;color:rgba(0,0,0,.55);}}

/* ── 플레이버 텍스트 ── */
.flv{{
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:8px;padding:10px 12px;
  font-size:11px;color:rgba(255,255,255,0.72);line-height:1.75;
}}

/* ── 풋터 ── */
.ftr{{
  display:flex;justify-content:space-between;align-items:center;
  border-top:1px solid rgba(255,255,255,0.10);padding-top:7px;
  font-size:9px;color:rgba(255,255,255,0.35);
}}
.ftr-l{{color:#FFD700;font-weight:700;font-size:10px;letter-spacing:.5px;}}
.ftr-r{{color:rgba(255,215,0,0.55);font-weight:600;}}
</style>
</head>
<body>
<div class="rainbow-wrap">
<div class="card">
  <div class="inner">

    <!-- 헤더 -->
    <div class="hdr">
      <div>
        <div class="card-title">🎮 ULTIMATE MASTER MIX</div>
        <div class="hp-line">HP MAX &nbsp;·&nbsp; ★★★★★ &nbsp;·&nbsp; 8/8 GENRES</div>
      </div>
      <div class="badge-wrap">
        <div class="badge-inner">
          <span class="badge-em">🌈</span>
          <span class="badge-txt">ALL GENRES</span>
        </div>
      </div>
    </div>

    <!-- 일러스트 -->
    <div class="ibox">
      <div class="gold-orb">👑</div>
      <div class="ino">ULTIMATE / 008</div>
    </div>

    <!-- 레어리티 -->
    <div class="rrow">
      <span class="rname">✦ SECRET ULTIMATE RARE ✦</span>
      <span class="rsym">★◆★◆★</span>
    </div>

    <!-- 스킬 -->
    <div class="sk">
      <div class="sk-title">✺ ULTIMATE ABILITIES — 8 GENRES COMBINED</div>
      <div class="sr">
        <div>
          <div class="sn">{s1_icon} {top1_key}</div>
          <div class="sd">{s1_desc}</div>
        </div>
        <div class="dmg-box">
          <div class="dmg-val">{dmg1}</div>
          <div class="dmg-unit">DMG</div>
        </div>
      </div>
      <div class="sr">
        <div>
          <div class="sn">{s2_icon} {top2_key}</div>
          <div class="sd">{s2_desc}</div>
        </div>
        <div class="dmg-box">
          <div class="dmg-val">{dmg2}</div>
          <div class="dmg-unit">DMG</div>
        </div>
      </div>
    </div>

    <!-- 플레이버 -->
    <div class="flv">
      ♪ ALL 8 GENRES MASTERED<br>
      당신은 흑인음악의 진정한 디깅입니다. 전설이 되었습니다.
    </div>

    <!-- 풋터 -->
    <div class="ftr">
      <span class="ftr-l">MASTER COLLECTOR</span>
      <span>Illus. BLACK MUSIC DIGGING</span>
      <span class="ftr-r">ULT / 008</span>
    </div>

  </div>
</div>
</div>

<!-- 통상 포토카드와 동일한 381px 폭 고정 -->
<div style="width:381px;height:0;overflow:hidden;"></div>

</body>
</html>"""


def generate_master_gold_card_png(collection: dict) -> bytes:
    """8개 장르 완료 보상 — 골드 레어 카드 PNG (html2image 우선, PIL 폴백)"""

    # ── 방법 1: html2image ──
    try:
        import sys as _sys, os as _os, io as _io2, tempfile as _tmp
        from html2image import Html2Image
        from PIL import Image as _PILImg, ImageChops as _IC

        _html = render_master_gold_card_html(collection)

        class _Null:
            def write(self, *a): pass
            def flush(self): pass

        _so, _se = _sys.stdout, _sys.stderr
        _sys.stdout = _sys.stderr = _Null()
        _result = b""
        try:
            with _tmp.TemporaryDirectory() as _td:
                _hti = Html2Image(
                    output_path=_td,
                    custom_flags=[
                        "--no-sandbox", "--disable-gpu",
                        "--log-level=3", "--disable-logging",
                        "--disable-extensions",
                    ],
                )
                # 일반 포토카드와 1픽셀 오차 없이 동일한 캡처 설정
                _hti.screenshot(html_str=_html, save_as="master.png", size=(500, 720))
                _p = _os.path.join(_td, "master.png")
                if _os.path.exists(_p) and _os.path.getsize(_p) > 500:
                    _img = _PILImg.open(_p).convert("RGB")
                    # 흰 여백 자동 제거 (일반 카드와 동일)
                    _bg  = _PILImg.new("RGB", _img.size, (255, 255, 255))
                    _box = _IC.difference(_img, _bg).getbbox()
                    if _box:
                        _pad = 6  # 드롭쉐도우 6px 살리기
                        _img = _img.crop((
                            max(0,           _box[0] - _pad),
                            max(0,           _box[1] - _pad),
                            min(_img.width,  _box[2] + _pad),
                            min(_img.height, _box[3] + _pad),
                        ))
                    _buf = _io2.BytesIO()
                    _img.save(_buf, format="JPEG", quality=95)
                    _buf.seek(0)
                    _result = _buf.getvalue()
        finally:
            _sys.stdout, _sys.stderr = _so, _se

        if _result:
            return _result

    except BaseException:
        pass

    # ── 방법 2: Pillow 폴백 ──
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return b""

    # ── 포토카드 동일 레이아웃 (금색 테마) ──
    # 색상
    GOLD        = (255, 215,   0)
    GOLD_DARK   = (120,  90,   0)
    GOLD_LIGHT  = (255, 240, 130)
    WHITE       = (255, 255, 255)
    DARK_BG     = ( 10,   5,   0)
    MID_BG      = ( 50,  28,   0)
    AMBER       = (201, 146,  42)
    DIM_GOLD    = (160, 120,  40)
    CREAM       = (255, 248, 200)
    BORDER      = (255, 215,   0)

    # 카드 크기 (포토카드와 동일)
    W, H  = 381, 580
    PAD   = 18
    INNER = 10   # inner padding

    # ── 전체 배경 (어두운 호박색 그라디언트) ──
    img  = Image.new("RGB", (W, H), DARK_BG)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t   = y / H
        col = tuple(int(a*(1-t) + b*t) for a, b in zip(MID_BG, DARK_BG))
        draw.line([(0, y), (W, y)], fill=col)

    # 대각선 shimmer
    for i, xo in enumerate(range(-H, W+H, 60)):
        a = 12 + (i % 3) * 5
        sh = tuple(int(c * a / 100) for c in GOLD_LIGHT)
        draw.polygon([(xo,0),(xo+H,H),(xo+H+20,H),(xo+20,0)], fill=sh)

    # ── 카드 테두리 (금색 이중) ──
    draw.rectangle([0, 0, W-1, H-1], outline=GOLD,      width=6)
    draw.rectangle([7, 7, W-8, H-8], outline=GOLD_DARK, width=2)

    # ── 폰트 ──
    def _fnt(sz, bold=False):
        fonts = (["C:/Windows/Fonts/malgunbd.ttf","C:/Windows/Fonts/arialbd.ttf",
                  "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"] if bold else
                 ["C:/Windows/Fonts/malgun.ttf","C:/Windows/Fonts/arial.ttf",
                  "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"])
        for p in fonts:
            try: return ImageFont.truetype(p, sz)
            except: pass
        try: return ImageFont.load_default(size=sz)
        except: return ImageFont.load_default()

    def _tw(t, f):
        try: return draw.textbbox((0,0),t,font=f)[2]
        except:
            try: return draw.textsize(t,font=f)[0]
            except: return len(t)*(f.size if hasattr(f,"size") else 10)

    def _tl(t, x, y, sz=16, bold=False, col=None):
        draw.text((x,y), t, font=_fnt(sz,bold), fill=col or WHITE)
    def _tr(t, x, y, sz=16, bold=False, col=None):
        f=_fnt(sz,bold); draw.text((x-_tw(t,f),y), t, font=f, fill=col or WHITE)
    def _tc(t, y, sz=16, bold=False, col=None):
        f=_fnt(sz,bold); draw.text(((W-_tw(t,f))//2,y), t, font=f, fill=col or WHITE)
    def _hline(y, col=None, w=1):
        draw.line([(PAD,y),(W-PAD,y)], fill=col or GOLD_DARK, width=w)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 헤더 (포토카드 동일 구조)
    y0 = 14
    _tl("마스터 컬렉터", PAD+2, y0,    sz=18, bold=True, col=CREAM)
    _tl("8개 장르를 완전 정복한 전설", PAD+2, y0+22, sz=11, col=GOLD_LIGHT)
    _tl("HP 999  ★★★★★", PAD+2, y0+37, sz=10, col=DIM_GOLD)
    # 우측 배지
    bx, by, bw, bh = W-PAD-56, y0, 56, 48
    draw.rounded_rectangle([bx,by,bx+bw,by+bh], radius=14, fill=(0,0,0,0))
    draw.rounded_rectangle([bx,by,bx+bw,by+bh], radius=14,
                            outline=GOLD, width=2)
    _tc("MASTER", by+26, sz=9, bold=True, col=GOLD)
    _hline(y0+56, col=GOLD, w=2)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 일러스트 박스
    IY, IH = y0+62, 185
    draw.rectangle([PAD, IY, W-PAD, IY+IH], outline=GOLD, width=2)
    # 일러스트 박스 배경 그라디언트
    for dy in range(IH):
        t2   = dy / IH
        ibg  = tuple(int(a*(1-t2)+b*t2) for a,b in zip((80,50,0),(5,3,0)))
        draw.line([(PAD+1, IY+dy),(W-PAD-1, IY+dy)], fill=ibg)
    # 동심원 후광
    cx, cy2 = W//2, IY + IH//2
    for r, br in [(70,0.15),(52,0.22),(34,0.33),(18,0.50)]:
        sh = tuple(int(g*br) for g in GOLD)
        draw.ellipse([cx-r,cy2-r,cx+r,cy2+r], outline=sh, width=2)
    # 왕관 그리기 (PIL)
    cw = 50
    # 왕관 뾰족이 3개
    crown_poly = [
        (cx-cw,  cy2+18),
        (cx-cw,  cy2-8),
        (cx-cw+14, cy2-22),
        (cx,     cy2-10),
        (cx+cw-14,cy2-22),
        (cx+cw,  cy2-8),
        (cx+cw,  cy2+18),
    ]
    draw.polygon(crown_poly, fill=GOLD)
    draw.polygon(crown_poly, outline=GOLD_DARK, width=2)
    # 왕관 기저
    draw.rounded_rectangle([cx-cw, cy2+10, cx+cw, cy2+20], radius=3, fill=AMBER)
    # 보석
    draw.ellipse([cx-5,  cy2-20, cx+5,  cy2-10], fill=(220,50,50))
    draw.ellipse([cx-cw+8, cy2-12, cx-cw+18, cy2-3], fill=(50,100,220))
    draw.ellipse([cx+cw-18,cy2-12, cx+cw-8, cy2-3],  fill=(50,180,80))
    # 별 반짝
    for sx,sy_ in [(PAD+12,IY+12),(W-PAD-22,IY+12),(PAD+12,IY+IH-22),(W-PAD-22,IY+IH-22)]:
        _tl("★", sx, sy_, sz=11, bold=True, col=(255,230,80))
    # No. 표기
    _tr("No.000", W-PAD-4, IY+IH-14, sz=9, col=(180,150,40))
    _hline(IY+IH+4, col=GOLD, w=1)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 레어리티 행
    ry = IY + IH + 10
    _tl("GOLD  ★  ULTRA RARE", PAD+2, ry, sz=9, bold=True, col=GOLD)
    _tr("★★★", W-PAD, ry, sz=13, col=GOLD)
    _hline(ry+18, col=GOLD_DARK, w=1)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 합산 속성 스킬
    total_attrs: dict = {}
    for gd in collection.values():
        for attr, score in gd.get("attr_scores", {}).items():
            total_attrs[attr] = total_attrs.get(attr, 0) + score

    ATTR_SHORT = {
        "🎵 멜로디 (Melody)":"MELODY","🥁 리듬 & 비트 (Rhythm & Beat)":"RHYTHM & BEAT",
        "🎸 베이스 & 그루브 (Bass & Groove)":"BASS & GROOVE",
        "🎙️ 보컬 & 음색 (Vocal & Tone)":"VOCAL & TONE",
        "🎹 화성 & 코드 진행 (Harmony & Chords)":"HARMONY",
        "🎺 리얼 악기 세션 (Live Instruments)":"LIVE INSTR.",
        "🎛️ 사운드 믹싱 & 질감 (Sound Design)":"SOUND DESIGN",
        "📜 가사 & 메시지 (Lyrics & Message)":"LYRICS & MSG",
    }
    SKILL_DESC_M = {
        "MELODY":"8개 장르를 가로지르는 선율의 절대 지배자",
        "RHYTHM & BEAT":"우주를 흔드는 리듬의 궁극 마스터",
        "BASS & GROOVE":"대지를 진동시키는 그루브의 신",
        "VOCAL & TONE":"영혼을 관통하는 보컬의 절대자",
        "HARMONY":"모든 화음을 초월한 화성의 주인",
        "LIVE INSTR.":"라이브 에너지의 완전한 지배자",
        "SOUND DESIGN":"사운드 공간을 창조하는 마에스트로",
        "LYRICS & MSG":"가사로 세상을 바꾸는 전설의 시인",
    }
    sorted_a = sorted(total_attrs.items(), key=lambda x: x[1], reverse=True)
    mx       = max(sorted_a[0][1], 1) if sorted_a else 1
    top1_k   = ATTR_SHORT.get(sorted_a[0][0],"ATTR") if sorted_a else "ATTR"
    top2_k   = ATTR_SHORT.get(sorted_a[1][0],"ATTR") if len(sorted_a)>1 else "ATTR"
    dmg1     = min(999, round(sorted_a[0][1]/mx*200)) if sorted_a else 100
    dmg2     = min(999, round(sorted_a[1][1]/mx*160)) if len(sorted_a)>1 else 80
    s1_desc  = SKILL_DESC_M.get(top1_k,"궁극의 능력")
    s2_desc  = SKILL_DESC_M.get(top2_k,"전설의 기술")

    sy = ry + 24
    # 스킬 박스 배경
    draw.rounded_rectangle([PAD, sy, W-PAD, sy+78], radius=6,
                            fill=(20,12,0), outline=(80,60,0), width=1)
    _tl("SPECIAL ABILITIES", PAD+8, sy+5, sz=8, bold=True, col=DIM_GOLD)
    # 스킬 1
    _tl(top1_k, PAD+8, sy+18, sz=13, bold=True, col=WHITE)
    _tl(s1_desc[:28], PAD+8, sy+32, sz=9, col=GOLD_LIGHT)
    _tr(f"{dmg1} DMG", W-PAD-6, sy+18, sz=14, bold=True, col=GOLD)
    # 구분선
    draw.line([(PAD+4, sy+46),(W-PAD-4, sy+46)], fill=(60,45,0), width=1)
    # 스킬 2
    _tl(top2_k, PAD+8, sy+52, sz=13, bold=True, col=WHITE)
    _tl(s2_desc[:28], PAD+8, sy+66, sz=9, col=GOLD_LIGHT)
    _tr(f"{dmg2} DMG", W-PAD-6, sy+52, sz=14, bold=True, col=GOLD)
    _hline(sy+82, col=GOLD_DARK, w=1)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 플레이버 텍스트 (포토카드의 최애 트랙 자리)
    fy = sy + 88
    draw.rounded_rectangle([PAD, fy, W-PAD, fy+30], radius=4,
                            fill=(15,8,0), outline=(70,52,0), width=1)
    _tl("♛ 8개 장르 완전 정복 달성", PAD+8, fy+5,  sz=11, bold=True, col=CREAM)
    _tl("Neo-Soul · Funk · R&B · NJS · QS · Soul · Hip-Hop · Afro",
        PAD+8, fy+18, sz=8, col=DIM_GOLD)
    _hline(fy+34, col=GOLD, w=1)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 풋터
    n_deep = sum(1 for v in collection.values() if v.get("is_phase2"))
    fty = fy + 40
    _tl(f"ALL 8 / 8", PAD+2, fty, sz=9, bold=True, col=GOLD)
    _tc("Illus. BLACK MUSIC DIGGING", fty, sz=8, col=DIM_GOLD)
    _tr(f"000 / 008", W-PAD, fty, sz=9, col=GOLD)

    # ── JPEG 저장 ──
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=96)
    buf.seek(0)
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════
# 6. 타임라인 렌더링
# ══════════════════════════════════════════════════════════════

def render_timeline(genre_key: str, genre_color: str):
    """
    장르 역사 타임라인 렌더링.
    아티스트 태그를 st.button으로 교체 → 클릭 시 대표곡 카드 표시.
    """
    tl = GENRE_DATA[genre_key].get("timeline", [])
    if not tl:
        st.info("타임라인 데이터 준비 중입니다.")
        return

    # 헤더
    st.markdown(f"""
<div class="timeline-header">
  <div class="timeline-header-title">📜 {genre_key} — 장르 역사 타임라인</div>
  <div class="timeline-header-sub">
    이 장르가 어떻게 태동하고, 발전하고, 세상을 바꿨는지 핵심 역사를 따라가보세요.<br>
    <span style="color:#ff385c;font-weight:500;">🎤 아티스트 이름을 클릭하면 대표곡을 확인할 수 있어요!</span>
  </div>
</div>
""", unsafe_allow_html=True)

    for i, item in enumerate(tl):
        s = TIMELINE_NODE_STYLES[i % len(TIMELINE_NODE_STYLES)]

        # ── 타임라인 아이템 본문 (HTML) ──
        st.markdown(f"""
<div style="display:flex;align-items:flex-start;gap:18px;margin-bottom:8px;">
  <div style="flex-shrink:0;width:54px;height:54px;border-radius:9999px;
              display:flex;align-items:center;justify-content:center;
              font-size:10px;font-weight:700;line-height:1.2;text-align:center;
              border:1px solid;letter-spacing:-0.02em;
              background:{s['bg']};border-color:{s['border']};color:{s['text']};
              box-shadow:rgba(0,0,0,0.02) 0 0 0 1px,rgba(0,0,0,0.04) 0 2px 6px;">
    {item['year']}
  </div>
  <div style="flex:1;background:#ffffff;border-radius:14px;
              padding:14px 18px;border:1px solid #dddddd;margin-top:4px;">
    <div style="font-size:11px;font-weight:600;text-transform:uppercase;
                letter-spacing:0.32px;margin-bottom:4px;color:{s['border']};">
      {item.get('era', '').upper()} ERA
    </div>
    <div style="font-size:16px;font-weight:600;color:#222222;margin-bottom:6px;line-height:1.3;">
      {item['title']}
    </div>
    <div style="font-size:14px;color:#3f3f3f;line-height:1.6;">
      {item['desc']}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        # ── 아티스트 버튼 (Streamlit native) ──
        artists = item.get("artists", [])
        if artists:
            # 왼쪽 72px 여백(노드 너비+갭) 맞추기
            _, btn_area = st.columns([0.09, 0.91])
            with btn_area:
                btn_cols = st.columns(min(len(artists), 4))
                for j, artist in enumerate(artists):
                    with btn_cols[j % 4]:
                        # 현재 선택된 아티스트면 버튼 라벨에 표시
                        is_active = (
                            st.session_state.get("artist_popup") == (artist, i)
                        )
                        label = f"✦ {artist}" if is_active else artist
                        if st.button(
                            label,
                            key=f"artist_{genre_key}_{i}_{j}",
                            use_container_width=True,
                        ):
                            if is_active:
                                # 같은 버튼 재클릭 → 닫기
                                st.session_state.artist_popup = None
                            else:
                                st.session_state.artist_popup = (artist, i)
                            st.rerun()

        # ── 대표곡 카드: 이 아이템의 아티스트가 선택됐을 때만 표시 ──
        popup = st.session_state.get("artist_popup")
        if popup:
            popup_artist, popup_item_idx = popup
            if popup_item_idx == i and popup_artist in artists:
                songs = ARTIST_SONGS.get(popup_artist, [])
                _, card_area = st.columns([0.09, 0.91])
                with card_area:
                    with st.container(border=True):
                        st.markdown(
                            f"**🎵 {popup_artist} 대표곡**  "
                            f"<span style='font-size:12px;color:#929292;'>"
                            f"클릭하면 YouTube에서 검색됩니다</span>",
                            unsafe_allow_html=True,
                        )
                        if songs:
                            for title, year in songs:
                                yt_q = f"{popup_artist} {title}".replace(" ", "+").replace("'", "%27")
                                st.markdown(
                                    f"- [{title} *({year})*]"
                                    f"(https://www.youtube.com/results?search_query={yt_q})"
                                )
                        else:
                            st.caption("대표곡 정보가 준비 중입니다.")

        # 아이템 간 구분선 (마지막 제외)
        if i < len(tl) - 1:
            st.markdown(
                '<div style="width:2px;height:20px;background:#dddddd;'
                'margin:0 0 4px 26px;"></div>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════
# ── 결과 화면 전환 직후 맨 위 스크롤 (사이드바보다 먼저 실행) ──
if st.session_state.get("_scroll_to_top"):
    st.session_state._scroll_to_top = False
    import streamlit.components.v1 as _cst
    _cst.html("""<script>
    (function(){
        var _s = function(){
            [
                window.parent.document.querySelector('section.main'),
                window.parent.document.querySelector('[data-testid="stMain"]'),
                window.parent.document.querySelector('.main'),
                window.parent.document.body,
                window.parent.document.documentElement
            ].forEach(function(e){ if(e){ e.scrollTop=0; e.scrollLeft=0; } });
            window.parent.scrollTo(0,0);
        };
        _s();
        [30,80,180,350,600].forEach(function(t){ setTimeout(_s,t); });
    })();
    </script>""", height=0)

# 7. 사이드바
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🎧 장르 선택")
    st.markdown('<div style="font-size:0.8rem;color:#9ca3af;margin-bottom:10px;">디깅할 서브 장르를 골라보세요 (총 8개)</div>',
                unsafe_allow_html=True)

    selected_genre = st.selectbox("서브 장르", list(GENRE_DATA.keys()),
                                   label_visibility="collapsed", key="genre_select")
    gdata = GENRE_DATA[selected_genre]

    st.markdown("---")

    # 세션 초기화 (장르 변경 시)
    init_session(selected_genre)

    if st.session_state.phase in ("eval_phase2", "result_phase2"):
        # Phase 2: evaluations 딕셔너리에서 인덱스 3~5(2단계 트랙)만 카운트
        completed = sum(1 for k in st.session_state.evaluations if k >= 3)
        phase_label = "2단계"
    else:
        completed = len(st.session_state.evaluations)
        phase_label = "평가"
    prog_pct  = int(completed / 3 * 100)
    st.markdown("### 📈 진행 상황")
    st.markdown(f"""
<div class="progress-wrap">
  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
    <span style="font-size:0.78rem;color:#6b7280;">{phase_label} 완료</span>
    <span style="font-size:0.78rem;color:#7c3aed;font-weight:700;">{completed}/3곡</span>
  </div>
  <div class="progress-track">
    <div class="progress-fill" style="width:{prog_pct}%;"></div>
  </div>
  <div class="progress-label">
    {"✅ 분석 준비 완료!" if completed == 3 else f"{3-completed}곡 더 평가하면 결과를 볼 수 있어요"}
  </div>
</div>
""", unsafe_allow_html=True)

    # ── 🎴 나의 디깅 도감 ──
    # 결과 화면 진입 직후 도감을 즉시 반영 (사이드바가 결과 섹션보다 먼저 그려지므로 여기서 선갱신)
    if st.session_state.get("phase") in ("result", "result_phase2"):
        _is_p2 = (st.session_state.phase == "result_phase2")
        _all_ev = st.session_state.get("evaluations", {})
        _ev_pre = _all_ev if _is_p2 else {k: v for k, v in _all_ev.items() if k < 3}
        _pre_attr    = calc_attribute_scores(_ev_pre)
        _pre_persona = get_persona(_pre_attr)
        st.session_state.genre_collection[selected_genre] = {
            "attr_scores": _pre_attr,
            "persona":     _pre_persona,
            "is_phase2":   _is_p2,
        }

    st.markdown("---")
    st.markdown("### 🎴 나의 디깅 도감")
    _gc       = st.session_state.get("genre_collection", {})
    _n_done   = len(_gc)
    _coll_pct = int(_n_done / 8 * 100)
    _bar_color = "#ffd700" if _n_done == 8 else "#7c3aed"
    st.markdown(f"""
<div class="progress-wrap">
  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
    <span style="font-size:0.78rem;color:#6b7280;">장르 수집</span>
    <span style="font-size:0.78rem;font-weight:700;color:{_bar_color};">{_n_done}/8</span>
  </div>
  <div class="progress-track">
    <div style="height:100%;border-radius:9999px;width:{_coll_pct}%;
                background:{_bar_color};transition:width .4s ease;"></div>
  </div>
</div>
""", unsafe_allow_html=True)
    for _gk in GENRE_DATA.keys():
        _done   = _gk in _gc
        _deep   = " 🔬" if _done and _gc[_gk].get("is_phase2") else ""
        _icon   = "✅" if _done else "⬜"
        _gname  = _gk[:22]
        st.markdown(
            f'<div style="font-size:0.75rem;padding:1px 0;color:{"#222" if _done else "#aaa"};">'
            f'{_icon} {_gname}{_deep}</div>',
            unsafe_allow_html=True,
        )
    if _n_done == 8:
        st.markdown(
            '<div style="font-size:0.75rem;font-weight:700;color:#ffd700;'
            'margin-top:6px;text-align:center;">👑 마스터 컬렉터 달성!</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    if st.button("🔄 처음부터 다시 시작", use_container_width=True):
        # genre_collection은 초기화하지 않음 — 도감 데이터 영구 유지
        st.session_state.current_genre               = None
        st.session_state.current_track               = 0
        st.session_state.evaluations                 = {}
        st.session_state.evaluations_phase2          = {}
        st.session_state.phase                       = "eval"
        st.session_state.rec_feedback                = {}
        st.session_state.like_expanded               = set()
        st.session_state.playlist_dislike_pending    = False
        st.rerun()

    st.markdown("""
<div style="font-size:0.72rem;color:#9ca3af;margin-top:20px;line-height:1.9;">
ℹ️ 3곡 평가 완료 시<br>레이더 차트·고득점 기반<br>유사곡 추천·믹스테이프<br>리포트가 생성됩니다.<br><br>
📜 장르 역사 타임라인은<br>결과 화면 하단에서 확인<br>할 수 있습니다.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 7-b. 얼티밋 마스터 카드 (8개 장르 완료 시 최상단 표시)
# ══════════════════════════════════════════════════════════════

_master_collection = st.session_state.get("genre_collection", {})
if len(_master_collection) == 8:
    import streamlit.components.v1 as _comp_master
    st.markdown("""
<div style="background:linear-gradient(135deg,#1a0040,#000820);
            border:2px solid rgba(255,215,0,.45);border-radius:14px;
            padding:16px 24px;margin-bottom:10px;text-align:center;">
  <div style="font-size:22px;font-weight:900;
              background:linear-gradient(90deg,#ffd700,#ff8800,#ffee44,#00ffaa,#ffd700);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;margin-bottom:6px;">
    👑 ALL 8 GENRES MASTERED — ULTIMATE COLLECTOR
  </div>
  <div style="font-size:13px;color:rgba(255,215,0,.7);">
    8개 장르를 모두 디깅했습니다. 당신은 흑인음악의 전설입니다.
  </div>
</div>
""", unsafe_allow_html=True)
    _comp_master.html(render_master_card_html(_master_collection), height=700, scrolling=False)

# ══════════════════════════════════════════════════════════════
# 8. 타이틀 배너
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div class="title-banner">
  <div class="title-eyebrow">🎵 Music Taste Explorer</div>
  <div class="title-main">나만의 흑인음악 취향 디깅하기</div>
  <div class="title-sub">
    '음악 디깅(Digging)'이란 과거 힙합 프로듀서들이 먼지 쌓인 LP판 상자를 파헤치며 숨은 명곡을 찾던 문화에서 유래한 말로,
    알고리즘이 떠먹여 주는 유행가 대신 나만의 보석 같은 음악을 적극적으로 찾아 나서는 과정을 뜻합니다.
    이곳에서는 단 3곡의 청취 평가만으로 당신의 음악 DNA를 분석해 드립니다.
    내가 멜로디에 끌리는지, 그루브에 반응하는지 지금 바로 확인해 보세요.<br><br>
    흑인음악 특유의 바이브를 좋아하지만 낯선 장르 앞에서 어디서부터 음악을 들어야 할지 막막하셨다면,
    이 공간이 완벽한 가이드가 되어 드릴 것입니다.
    네오소울부터 펑크까지 친절한 장르 가이드를 따라 숨겨진 명곡들을 평가하다 보면,
    어느새 진짜 내 취향에 꼭 맞는 '인생곡'들을 발견하게 될 것입니다.
    지금 바로 나만의 음악 보물찾기를 시작하고, 8개의 디깅 도감을 완벽하게 채워보세요!
  </div>
</div>
""", unsafe_allow_html=True)

# 세션 재확인
init_session(selected_genre)
genre_color = gdata["color"]

# phase에 따라 활성 트랙 결정
# evaluations 딕셔너리는 항상 하나: phase1 → indices 0-2, phase2 → indices 3-5 (누적)
_tracks_p1  = gdata["tracks"]
_tracks_p2  = gdata.get("tracks_phase2", [])
_tracks_all = _tracks_p1 + _tracks_p2  # 6곡 합산 (result_phase2에서 사용)

_cur_phase = st.session_state.phase
if _cur_phase == "eval_phase2":
    tracks = _tracks_p2          # 평가 UI는 phase2 3곡만 표시
elif _cur_phase == "result_phase2":
    tracks = _tracks_all         # 결과 화면은 6곡 합산
else:
    tracks = _tracks_p1          # phase1 기본

# phase 자동 전환
if len(st.session_state.evaluations) == 3 and st.session_state.phase == "eval":
    st.session_state.phase = "result"
    st.session_state._scroll_to_top = True
if len(st.session_state.evaluations) >= 6 and st.session_state.phase == "eval_phase2":
    st.session_state.phase = "result_phase2"
    st.session_state._scroll_to_top = True
    tracks = _tracks_all


# ══════════════════════════════════════════════════════════════
# 9. EVAL 단계 — 메인 탭 (음악 평가 | 장르 타임라인)
# ══════════════════════════════════════════════════════════════

if st.session_state.phase in ("eval", "eval_phase2"):
    is_phase2  = (st.session_state.phase == "eval_phase2")
    # phase1/phase2 모두 동일한 evaluations 딕셔너리 사용
    # phase1: 인덱스 0-2, phase2: 인덱스 3-5로 누적 저장
    eval_store = "evaluations"
    pkey       = "p2" if is_phase2 else "p1"  # 위젯 key 충돌 방지

    # Phase 2 진입 배너
    if is_phase2:
        st.markdown("""
<div style="background:#fff8e1;border:1px solid #ffc107;border-left:4px solid #ff9800;
            border-radius:8px;padding:14px 20px;margin-bottom:20px;">
  <span style="font-size:15px;font-weight:700;color:#e65100;">🔬 2단계 심층 테스트</span>
  <span style="font-size:14px;color:#5d4037;margin-left:10px;">더 정확한 취향 분석을 위해 새로운 3곡을 평가해 주세요.</span>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # 장르 소개 카드 (평가 시작 전, phase1에서만 표시)
    # ══════════════════════════════════════════
    genre_intro = {
        "🌙 Neo-Soul": {
            "period": "1994 – 현재",
            "origin": "미국 (뉴욕 · LA)",
            "key_artists": "Erykah Badu, D'Angelo, Lauryn Hill, Maxwell",
            "sound": "어쿠스틱 악기 기반의 따뜻한 질감, 재즈·훵크를 흡수한 코드 진행, 내면의 감정을 담은 보컬",
            "vibe": "빈티지 감성 · 의식적 가사 · 아날로그 온기",
            "icon": "🌙",
        },
        "🔥 Funk": {
            "period": "1960s – 현재",
            "origin": "미국 (뉴올리언스 · 오하이오)",
            "key_artists": "James Brown, Parliament, Sly & The Family Stone, Prince",
            "sound": "강렬한 베이스라인과 1박 강조 리듬, 브라스 섹션, 반복적인 그루브 훅",
            "vibe": "댄서블 에너지 · 몸이 먼저 반응하는 비트 · 집단적 황홀경",
            "icon": "🔥",
        },
        "💜 Contemporary R&B": {
            "period": "2000s – 현재",
            "origin": "미국 (전역)",
            "key_artists": "Usher, The Weeknd, SZA, Frank Ocean, Khalid",
            "sound": "일렉트로닉·힙합이 융합된 세련된 프로덕션, 팔세토 보컬, 감성적 가사",
            "vibe": "모던 감성 · 자정의 무드 · 도시적 낭만",
            "icon": "💜",
        },
        "🎤 New Jack Swing": {
            "period": "1987 – 1996",
            "origin": "미국 (뉴욕)",
            "key_artists": "Bobby Brown, Teddy Riley, TLC, Michael Jackson",
            "sound": "드럼 머신 비트 위의 소울 보컬, 힙합 리듬과 R&B 멜로디의 결합",
            "vibe": "90년대 파티 에너지 · 섹시한 그루브 · 팝 친화적",
            "icon": "🎤",
        },
        "🌊 Quiet Storm R&B": {
            "period": "1976 – 현재",
            "origin": "미국 (워싱턴 DC)",
            "key_artists": "Luther Vandross, Anita Baker, Sade, Boyz II Men",
            "sound": "느린 템포, 풍성한 현악 오케스트레이션, 성숙하고 감미로운 보컬",
            "vibe": "성숙한 낭만 · 깊은 밤의 감성 · 어덜트 소울",
            "icon": "🌊",
        },
        "🎸 60~70s Classic Soul / Motown": {
            "period": "1959 – 1979",
            "origin": "미국 (디트로이트 · 멤피스)",
            "key_artists": "Marvin Gaye, Aretha Franklin, Stevie Wonder, The Temptations",
            "sound": "라이브 세션 밴드의 유기적 사운드, 콜앤리스폰스 창법, 브라스와 현악의 조화",
            "vibe": "시민권 운동의 영혼 · 따뜻한 진정성 · 흑인음악의 뿌리",
            "icon": "🎸",
        },
        "🎧 90s Hip-Hop Soul": {
            "period": "1991 – 2000",
            "origin": "미국 (뉴욕 · 애틀란타)",
            "key_artists": "Mary J. Blige, TLC, Aaliyah, Puff Daddy",
            "sound": "힙합 드럼 비트 위에 얹힌 생생한 R&B 보컬, 샘플링과 소울의 결합",
            "vibe": "거리의 감성 · 날 것의 감정 · 90년대 뉴욕 에너지",
            "icon": "🎧",
        },
        "🌍 Afrobeats / Dancehall": {
            "period": "2000s – 현재",
            "origin": "나이지리아 (라고스) · 자메이카 (킹스턴)",
            "key_artists": "WizKid, Burna Boy, Tems, Sean Paul",
            "sound": "서아프리카 타악기 리듬과 현대 팝 프로덕션의 융합, 춤을 부르는 그루브",
            "vibe": "글로벌 파티 에너지 · 낙천적 활력 · 문화적 자부심",
            "icon": "🌍",
        },
    }

    intro = genre_intro.get(selected_genre) if not is_phase2 else None
    if intro:
        st.markdown(f"""
<div style="background-color:#f7f7f7;border:1px solid #dddddd;border-radius:14px;
            padding:24px 28px;margin-bottom:24px;">
  <div style="font-size:11px;font-weight:700;letter-spacing:0.25em;text-transform:uppercase;
              color:#929292;margin-bottom:10px;">GENRE GUIDE</div>
  <div style="font-size:22px;font-weight:700;color:#222222;margin-bottom:6px;">
    {intro['icon']} {selected_genre.split(' ', 1)[-1]}
  </div>
  <div style="font-size:14px;color:#6a6a6a;line-height:1.7;margin-bottom:18px;">
    {gdata['desc']}
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px 24px;margin-bottom:16px;">
    <div>
      <div style="font-size:11px;font-weight:600;color:#929292;margin-bottom:3px;">활동 시기</div>
      <div style="font-size:14px;color:#222222;">{intro['period']}</div>
    </div>
    <div>
      <div style="font-size:11px;font-weight:600;color:#929292;margin-bottom:3px;">대표 아티스트</div>
      <div style="font-size:14px;color:#222222;">{intro['key_artists']}</div>
    </div>
  </div>
  <div style="border-top:1px solid #dddddd;padding-top:14px;margin-top:4px;">
    <div style="font-size:11px;font-weight:600;color:#929292;margin-bottom:6px;">사운드 특징</div>
    <div style="font-size:14px;color:#3f3f3f;line-height:1.7;margin-bottom:12px;">{intro['sound']}</div>
    <div style="display:inline-flex;gap:8px;flex-wrap:wrap;">
      {''.join(f'<span style="background-color:#222222;color:#ffffff;border-radius:9999px;padding:4px 12px;font-size:12px;font-weight:500;">{v.strip()}</span>' for v in intro['vibe'].split('·'))}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    step_label = "STEP 01 — 2단계 심층 평가" if is_phase2 else "STEP 01 — 음악 청취 &amp; 다차원 평가"
    st.markdown(f"""
<div class="step-badge">
  <div class="step-dot"></div>
  {step_label}
</div>
""", unsafe_allow_html=True)

    # ── 상단 트랙 진행 표시기 ──
    cur = st.session_state.current_track
    cur_evals = st.session_state[eval_store]
    # phase2: 인덱스 3-5 범위 표시, phase1: 0-2
    pip_start = 3 if is_phase2 else 0
    pip_html = '<div class="track-progress-wrap">'
    for i in range(pip_start, pip_start + 3):
        disp = i - pip_start + 1
        if i in cur_evals:
            cls = "pip-done"; label = "✓"
        elif i == cur:
            cls = "pip-active"; label = str(disp)
        else:
            cls = "pip-locked"; label = str(disp)
        pip_html += f'<div class="track-pip {cls}">{label}</div>'
        if i < pip_start + 2:
            line_cls = "track-pip-line-done" if i in cur_evals else "track-pip-line"
            pip_html += f'<div class="track-pip-line {line_cls}"></div>'
    pip_html += '</div>'
    st.markdown(pip_html, unsafe_allow_html=True)

    # ── 현재 트랙 정보 ──
    # tracks는 eval_phase2 시 tracks_phase2만 담겨 있으므로, phase2에서는 cur-3으로 인덱싱
    track_disp_idx = cur - 3 if is_phase2 else cur
    track = tracks[track_disp_idx]
    yt_q  = track["yt_query"].replace(" ", "+").replace("'", "%27").replace("&", "%26")

    st.markdown(f"""
<div class="track-card">
  <div class="track-number">0{cur+1}</div>
  <div class="track-title">🎵 {track['title']}</div>
  <div class="track-artist">👤 {track['artist']} · {track['year']}</div>
  <div class="track-desc">{track['desc']}</div>
  <a class="yt-link"
     href="https://www.youtube.com/results?search_query={yt_q}"
     target="_blank">▶ YouTube에서 "{track['artist']} - {track['title']}" 검색 ↗</a>
</div>
""", unsafe_allow_html=True)

    # 이미 저장된 값 불러오기 (cur = 3~5도 evaluations에서 그대로 읽음)
    prev = get_eval(cur, eval_store)

    # ── 총점 슬라이더 ──
    st.markdown('<div class="eval-label">⭐ 총점 (1~5점)</div>', unsafe_allow_html=True)
    score = st.slider("총점", 1, 5, value=prev["score"],
                      key=f"score_{selected_genre}_{cur}_{pkey}",
                      label_visibility="collapsed")
    st.markdown(f'<div class="star-guide">{"★"*score}{"☆"*(5-score)} &nbsp; {score}점</div>',
                unsafe_allow_html=True)

    # ── 매력 요소 체크박스 ──
    st.markdown('<div class="eval-label">✨ 좋았던 매력 요소 (복수 선택 가능)</div>',
                unsafe_allow_html=True)
    # 8개 속성을 4개씩 2줄(그리드)로 배치
    attr_cols_row1 = st.columns(4)
    attr_cols_row2 = st.columns(4)
    selected_attrs = []

    for ai, attr in enumerate(ATTRIBUTES):
        # 인덱스 0~3은 첫 번째 줄, 4~7은 두 번째 줄
        col = attr_cols_row1[ai] if ai < 4 else attr_cols_row2[ai - 4]
        with col:
            if st.checkbox(attr, value=(attr in prev["attributes"]),
                           key=f"attr_{selected_genre}_{cur}_{attr}_{pkey}"):
                selected_attrs.append(attr)

    # ── 한 줄 디깅 노트 ──
    st.markdown('<div class="eval-label">📝 한 줄 디깅 노트</div>', unsafe_allow_html=True)
    note = st.text_input("디깅 노트", value=prev["note"],
                         placeholder="이 곡을 들으며 느낀 감상평이나 매력 포인트를 자유롭게 적어보세요...",
                         key=f"note_{selected_genre}_{cur}_{pkey}",
                         label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 버튼 영역 ──
    already_saved = cur in st.session_state[eval_store]
    last_track    = 5 if is_phase2 else 2   # phase2: 5번 인덱스가 마지막
    first_track   = 3 if is_phase2 else 0   # phase2: 3번 인덱스가 첫 곡

    if cur < last_track:
        # ── Track 1,2 (phase2: 4,5번째): 평가 저장 후 다음 트랙으로 ──
        bcol1, bcol2, _ = st.columns([1.4, 1.4, 2])
        with bcol1:
            btn_label = "💾 수정 저장" if already_saved else "✅ 평가 완료"
            if st.button(btn_label, key=f"save_{selected_genre}_{cur}_{pkey}", use_container_width=True):
                save_eval(cur, score, selected_attrs, note, eval_store)
                st.rerun()

        # "다음 트랙" 버튼 — 저장된 경우에만 활성화
        with bcol2:
            next_disabled = cur not in st.session_state[eval_store]
            next_label    = "➡️ 다음 곡으로" if is_phase2 else f"➡️ Track {cur+2}로 이동"
            if st.button(
                next_label,
                key=f"next_{selected_genre}_{cur}_{pkey}",
                disabled=next_disabled,
                use_container_width=True,
            ):
                st.session_state.current_track = cur + 1
                st.rerun()

        if next_disabled:
            st.caption("💡 먼저 **평가 완료** 버튼을 눌러 저장해주세요.")

    else:
        # ── 마지막 트랙: 평가 완료 & 결과 보기 ──
        next_phase     = "result_phase2" if is_phase2 else "result"
        complete_count = 6 if is_phase2 else 3
        bcol1, _ = st.columns([1.6, 2])
        with bcol1:
            btn_label = "💾 수정 저장" if already_saved else "🎉 평가 완료 & 결과 보기"
            if st.button(btn_label, key=f"save_{selected_genre}_{cur}_{pkey}", use_container_width=True):
                save_eval(cur, score, selected_attrs, note, eval_store)
                if len(st.session_state[eval_store]) >= complete_count:
                    st.session_state.phase = next_phase
                    st.session_state._scroll_to_top = True
                st.rerun()

    # 이전 트랙으로 돌아가기 (phase 내 첫 트랙이 아닐 때만)
    if cur > first_track:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"← Track {cur}으로 돌아가기",
                     key=f"prev_{selected_genre}_{cur}_{pkey}"):
            st.session_state.current_track = cur - 1
            st.rerun()

    # 이미 저장된 트랙 요약 배너
    if already_saved:
        saved = st.session_state[eval_store][cur]
        st.markdown(f"""
<div class="complete-banner">
  ✅ 저장됨 — {saved['score']}점 · {', '.join(saved['attributes']) if saved['attributes'] else '속성 미선택'}
  {f' · 📝 {saved["note"][:30]}{"..." if len(saved["note"])>30 else ""}' if saved.get('note') else ''}
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 10. RESULT 단계 — 분석 결과 화면
# ══════════════════════════════════════════════════════════════

elif st.session_state.phase in ("result", "result_phase2"):
    is_phase2_result = (st.session_state.phase == "result_phase2")
    _all_evals = st.session_state.get("evaluations", {})
    # result_phase2: 6곡 전체 합산 분석 / result: phase1 3곡만 분석
    evaluations = _all_evals if is_phase2_result else {k: v for k, v in _all_evals.items() if k < 3}

    attr_scores = calc_attribute_scores(evaluations)
    persona     = get_persona(attr_scores)

    # ── 전역 도감에 저장 (장르 변경 후에도 유지) ──
    st.session_state.genre_collection[selected_genre] = {
        "attr_scores": attr_scores,
        "persona":     persona,
        "is_phase2":   is_phase2_result,
    }
    # 8개 장르 최초 완성 시 폭죽 🎆
    if (len(st.session_state.genre_collection) == 8
            and not st.session_state._master_balloons_shown):
        st.balloons()
        st.session_state._master_balloons_shown = True

    # 고득점 기반 유사곡 추천 정렬
    # tracks는 외부 스코프에서 result_phase2 시 _tracks_all(6곡)로 설정되어 있음
    ranked_recs, combined_scores, high_tracks_info = rank_recommendations_dynamic(
        gdata["recommendations"], evaluations, tracks, attr_scores
    )

    # 완료 배너 — phase2 여부에 따라 텍스트 분기
    if is_phase2_result:
        st.markdown("""
<div style="background:#e8f5e9;border:1px solid #4caf50;border-left:4px solid #2e7d32;
            border-radius:8px;padding:14px 20px;margin-bottom:12px;">
  <div style="font-size:15px;font-weight:700;color:#1b5e20;margin-bottom:4px;">🔬 2단계 심층 분석 완료!</div>
  <div style="font-size:13px;color:#2e7d32;">1차 3곡 + 2차 3곡, 총 6곡의 데이터를 종합한 심층 분석 결과입니다.</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<div class="all-done-banner">
  🎉 2단계 심층 테스트 완료! 총 6곡의 데이터를 종합한 당신의 진짜 음악 DNA 주파수를 확인하세요.
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="all-done-banner">
  🎉 3곡 평가 완료! 당신의 음악 DNA 분석 결과를 확인해보세요.
</div>
""", unsafe_allow_html=True)

    back_phase = "eval_phase2" if is_phase2_result else "eval"
    bc1, bc2, _ = st.columns([1.2, 1.4, 3])
    with bc1:
        if st.button("← 평가 수정하기"):
            st.session_state.phase = back_phase
            st.rerun()
    if is_phase2_result:
        with bc2:
            if st.button("← 1단계 결과 보기"):
                st.session_state.phase = "result"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 결과 헤더 — 곡 수와 평균 점수를 evaluations 실제 데이터로 계산
    _eval_count  = len(evaluations) if evaluations else 1
    avg          = sum(e["score"] for e in evaluations.values()) / _eval_count
    track_label  = f"{_eval_count}곡 (심층 분석 완료 🔬)" if is_phase2_result else f"{_eval_count}곡"
    st.markdown(f"""
<div class="result-header">
  <div class="result-title">🎭 {persona}</div>
  <div class="result-persona">
    선택 장르: <strong>{selected_genre}</strong> &nbsp;|&nbsp;
    평균 점수: <strong>{'★'*round(avg)}{'☆'*(5-round(avg))} ({avg:.1f}/5)</strong>
    &nbsp;|&nbsp; 총 평가 트랙: <strong>{track_label}</strong>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── STEP 02: 감성 영수증 (Receiptify) ──
    st.markdown("""
<div class="step-badge">
  <div class="step-dot"></div>
  STEP 02 — 나의 음악 취향 감성 영수증
</div>
""", unsafe_allow_html=True)

    st.markdown(
        render_receipt_html(
            genre_key   = selected_genre,
            persona     = persona,
            evaluations = evaluations,
            all_tracks  = tracks,
            attr_scores = attr_scores,
            avg         = avg,
            is_phase2   = is_phase2_result,
        ),
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # STEP 03 ① — 맞춤 추천 플레이리스트
    # ══════════════════════════════════════════════
    st.markdown("""
<div class="step-badge">
  <div class="step-dot"></div>
  STEP 03 — 맞춤 추천 플레이리스트
</div>
""", unsafe_allow_html=True)

    # 추천 근거 문구
    top_combined = [a for a, s in sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:2] if s > 0]
    if high_tracks_info:
        high_track_names = ", ".join(f'"{ht["title"]}"({ht["score"]}점)' for ht in high_tracks_info)
        basis_text = (
            f'{high_track_names}과 유사한 곡 · '
            f'선호 속성 <strong>{" · ".join(top_combined)}</strong> 반영'
        )
    else:
        basis_text = f'선호 속성 <strong>{" · ".join(top_combined)}</strong> 기반 정렬'

    st.markdown(
        f'<div style="font-size:13px;font-weight:400;color:#6a6a6a;'
        f'margin-bottom:20px;line-height:1.6;">{basis_text}</div>',
        unsafe_allow_html=True,
    )

    # ── 추천 카드 — Streamlit 네이티브 2열 그리드 ──
    rank_labels = ["🥇", "🥈", "🥉", "4위", "5위"]
    card_cols = st.columns(2)

    # 클릭된 추천곡 상태 초기화
    if "rec_popup" not in st.session_state:
        st.session_state.rec_popup = None

    for rank, rec in enumerate(ranked_recs[:5], 1):
        ms       = rec.get("match_score", 0)
        vb       = rec.get("vibe_bonus", 0)
        is_best  = ms == 2 or (ms == 1 and vb > 0)
        is_match = ms > 0 or vb > 0

        # 매치 라벨
        if is_best:
            match_label = "🎯 BEST MATCH"
        elif is_match:
            match_label = "✓ MATCH"
        else:
            match_label = ""

        with card_cols[(rank - 1) % 2]:
            with st.container(border=True):
                # 순위 + 매치 라벨
                top_l, top_r = st.columns([3, 2])
                with top_l:
                    st.caption(rank_labels[rank - 1])
                with top_r:
                    if match_label:
                        st.caption(f"**{match_label}**")

                # 곡명 + 아티스트
                st.markdown(f"**{rec['title']}**")
                st.caption(f"👤 {rec['artist']}  ·  {rec['year']}")

                # ── 태그 버튼 (클릭 → 유사곡 표시) ──
                tag_btn_cols = st.columns(len(rec["tags"]))
                for ti, tag in enumerate(rec["tags"]):
                    tag_key = f"tag_{selected_genre}_{rank}_{ti}"
                    is_tag_open = st.session_state.get("tag_popup") == tag_key
                    btn_label_t = f"✦ {tag}" if is_tag_open else f"# {tag}"
                    with tag_btn_cols[ti]:
                        if st.button(btn_label_t, key=tag_key, use_container_width=True):
                            st.session_state.tag_popup = None if is_tag_open else tag_key
                            # YouTube 팝업은 닫기
                            st.session_state.rec_popup = None
                            st.rerun()

                # ── 태그 관련 유사곡 표시 ──
                active_tag_key = st.session_state.get("tag_popup", "")
                if active_tag_key and active_tag_key.startswith(f"tag_{selected_genre}_{rank}_"):
                    clicked_ti  = int(active_tag_key.split("_")[-1])
                    clicked_tag = rec["tags"][clicked_ti]
                    tag_songs   = TAG_SONGS.get(clicked_tag, [])
                    st.markdown(f"**#{clicked_tag} 유사곡**")
                    if tag_songs:
                        for s_title, s_artist, s_year in tag_songs:
                            yt_q = f"{s_artist} {s_title}".replace(" ", "+").replace("'", "%27").replace("&", "%26")
                            st.markdown(
                                f"- [{s_title} — {s_artist} ({s_year})]"
                                f"(https://www.youtube.com/results?search_query={yt_q})"
                            )
                    else:
                        st.caption("관련 곡 정보를 준비 중입니다.")

                # ── YouTube 바로듣기 버튼 ──
                rec_key = f"rec_{selected_genre}_{rank}"
                is_open = st.session_state.rec_popup == rec_key
                btn_yt  = "🔗 링크 닫기" if is_open else "▶ YouTube에서 듣기"
                if st.button(btn_yt, key=f"btn_{rec_key}", use_container_width=True):
                    st.session_state.rec_popup  = None if is_open else rec_key
                    st.session_state.tag_popup  = None
                    st.rerun()
                if is_open:
                    yt_q   = f"{rec['artist']} {rec['title']}".replace(" ", "+").replace("'", "%27").replace("&", "%26")
                    yt_url = f"https://www.youtube.com/results?search_query={yt_q}"
                    st.markdown(f"👉 [**{rec['title']}** — YouTube 검색]({yt_url})")

                # ── 👍 좋아요 버튼 (phase1 결과에서만, 카드별) ──
                if not is_phase2_result:
                    st.markdown(
                        '<div style="border-top:1px solid #ebebeb;margin:10px 0 8px 0;"></div>',
                        unsafe_allow_html=True,
                    )
                    feedback_now = st.session_state.rec_feedback.get(rank)
                    like_label   = "👍 좋아요 ✓" if feedback_now == "like" else "👍 좋아요"
                    if st.button(like_label, key=f"like_{selected_genre}_{rank}", use_container_width=True):
                        st.session_state.rec_feedback[rank] = "like"
                        likes = st.session_state.get("like_expanded", set())
                        likes.add(rank)
                        st.session_state.like_expanded            = likes
                        st.session_state.playlist_dislike_pending = False
                        st.session_state.tag_popup  = None
                        st.session_state.rec_popup  = None
                        st.rerun()

            # ── 👍 Deep Dive: TAG_SONGS 기반 유사곡 (카드 외부, 같은 컬럼) ──
            if not is_phase2_result and rank in st.session_state.get("like_expanded", set()):
                deep_songs: list = []
                for tag in rec["tags"]:
                    for s in TAG_SONGS.get(tag, []):
                        if s not in deep_songs:
                            deep_songs.append(s)
                    if len(deep_songs) >= 3:
                        break
                song_items = ""
                for s_title, s_artist, s_year in deep_songs[:3]:
                    yt_q = (
                        f"{s_artist} {s_title}"
                        .replace(" ", "+").replace("'", "%27").replace("&", "%26")
                    )
                    song_items += (
                        f'<div style="padding:4px 0;font-size:13px;">'
                        f'🎵 <a href="https://www.youtube.com/results?search_query={yt_q}" '
                        f'target="_blank" style="color:#222;text-decoration:none;">'
                        f'<strong>{s_title}</strong></a>'
                        f' — {s_artist} ({s_year})</div>'
                    )
                st.markdown(
                    f'<div style="background:#f0fff4;border:1px solid #86efac;'
                    f'border-radius:10px;padding:14px 16px;margin-top:4px;">'
                    f'<div style="font-size:13px;font-weight:700;color:#166534;margin-bottom:8px;">'
                    f'🎉 이 곡을 좋아하는 사람들이 즐겨 듣는 추천 트랙</div>'
                    f'{song_items}</div>',
                    unsafe_allow_html=True,
                )

    # ── 전체 플레이리스트 붐따 (phase1 결과에서만) ──
    if not is_phase2_result:
        st.markdown("<br>", unsafe_allow_html=True)

        if not st.session_state.playlist_dislike_pending:
            # 전체 붐따 트리거 버튼
            st.markdown(
                '<div style="text-align:center;margin:4px 0 8px 0;">'
                '<span style="font-size:12px;color:#929292;">'
                '추천 결과가 전체적으로 마음에 안 드시나요?'
                '</span></div>',
                unsafe_allow_html=True,
            )
            _, center_col, _ = st.columns([2, 3, 2])
            with center_col:
                if st.button(
                    "👎 추천 결과가 아쉬워요",
                    key=f"playlist_dislike_{selected_genre}",
                    use_container_width=True,
                ):
                    st.session_state.playlist_dislike_pending = True
                    st.rerun()
        else:
            # ── 확인 패널 ──
            st.markdown(
                """
<div style="
  background:#fff8e1;
  border:2px solid #ffc107;
  border-radius:14px;
  padding:24px 28px;
  margin:8px 0 20px 0;
  text-align:center;
">
  <div style="font-size:32px;margin-bottom:8px;">🔬</div>
  <div style="font-size:17px;font-weight:700;color:#111;margin-bottom:8px;">
    더 정확한 분석이 필요하신가요?
  </div>
  <div style="font-size:14px;color:#555;line-height:1.7;margin-bottom:20px;">
    2단계 심층 테스트에서는 새로운 3곡을 추가로 평가해서<br>
    1차 결과와 합산한 <strong>더 정밀한 취향 분석</strong>을 제공합니다.
  </div>
</div>
""",
                unsafe_allow_html=True,
            )
            confirm_l, confirm_r = st.columns(2)
            with confirm_l:
                if st.button(
                    "← 돌아가기",
                    key=f"playlist_dislike_cancel_{selected_genre}",
                    use_container_width=True,
                ):
                    st.session_state.playlist_dislike_pending = False
                    st.rerun()
            with confirm_r:
                if st.button(
                    "🚀 2단계 심층 테스트 시작",
                    key=f"playlist_dislike_confirm_{selected_genre}",
                    use_container_width=True,
                ):
                    st.toast("2단계 심층 테스트를 시작합니다! 🔬")
                    st.session_state.phase                    = "eval_phase2"
                    st.session_state.current_track            = 3
                    st.session_state.playlist_dislike_pending = False
                    st.session_state.rec_feedback             = {}
                    st.session_state.like_expanded            = set()
                    st.rerun()

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # STEP 04 — 포토카드 수집
    # ══════════════════════════════════════════════
    st.markdown("""
<div class="step-badge">
  <div class="step-dot"></div>
  STEP 04 — 나의 음악 DNA 포토카드
</div>
""", unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:13px;color:#6a6a6a;margin-bottom:4px;text-align:center;">'
        '장르별로 수집하고 SNS에 공유해보세요 ✨'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── HTML 카드 미리보기 + JS 다운로드 버튼 일체형 ──
    # Python 서버 처리 없이 브라우저에서 직접 캡처 → 미리보기와 완전 동일
    import streamlit.components.v1 as _components
    _safe_genre = re.sub(r"[^\w가-힣]", "_", selected_genre).strip("_")
    _components.html(
        render_photo_card_html(
            genre_key   = selected_genre,
            genre_color = genre_color,
            persona     = persona,
            attr_scores = attr_scores,
            evaluations = evaluations,
            all_tracks  = tracks,
            avg         = avg,
            is_phase2   = is_phase2_result,
            safe_genre  = _safe_genre,
        ),
        height=686,
        scrolling=False,
    )

    # 하단 타임라인
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("""
<div class="step-badge">
  <div class="step-dot"></div>
  BONUS — 장르 역사 타임라인
</div>
""", unsafe_allow_html=True)
    render_timeline(selected_genre, genre_color)

    st.markdown("""
<div style="background-color:#f7f7f7;border:1px solid #dddddd;border-radius:8px;
            padding:24px;text-align:center;margin-top:24px;">
  <div style="font-size:14px;font-weight:400;color:#6a6a6a;line-height:1.6;">
    다른 장르도 디깅해보세요 — 사이드바에서 장르를 변경하면 새로운 음악 탐험을 시작합니다.<br>
    <span style="color:#222222;font-weight:500;">총 8개 장르 · 각 장르마다 다른 레이더 차트 · 추천 리스트 · 역사 타임라인</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 11. HISTORY_ONLY 단계
# ══════════════════════════════════════════════════════════════

elif st.session_state.phase == "history_only":
    if st.button("← 분석 결과로 돌아가기"):
        st.session_state.phase = "result"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    render_timeline(selected_genre, genre_color)
