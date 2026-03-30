import streamlit as st
import requests

##백앤드 코드
# 1. API를 이용해서 실시간 환율 정보 가져오기
def get_exchange_rate(base, target):
  # 무료 환율 API 주소(base변수에 따라서 기준 통화가 바뀜)
  url = f"https://open.er-api.com/v6/latest/{base}"

  # 환율 주소를 인터넷으로 요청해서 데이터 받아오기
  response = requests.get(url)
  data = response.json() #파이썬이 읽기 쉽게 변환

  # 알고 싶은 통화(target 변수)의 데이터가 있는지 확인
  if target in data["rates"]:
    rate = data["rates"][target] # 현재 환율
    # result = amount * rate # 변경된 금액
    return rate
  else:
    return None
# 콜백함수와 세션 설정
if "amount_top" not in st.session_state:
  st.session_state.amount_top=1.0
  st.session_state.amount_bot=1.0
  st.session_state.curr_top="USD"
  st.session_state.curr_bot="KRW"

# 계산기용 세션 설정
if "cal_formula" not in st.session_state:
  st.session_state.cal_formula = ""
  
  # 매달러 1.0 기준 원화 계산
  rate = get_exchange_rate("USD", "KRW")
  if rate:
    st.session_state.amount_bot = 1.0 * rate
    
def cal_bottom():
  rate = get_exchange_rate(st.session_state.curr_top, st.session_state.curr_bot)
  if rate:
    st.session_state.amount_bot = st.session_state.amount_top*rate

def cal_top():
  rate = get_exchange_rate(st.session_state.curr_bot, st.session_state.curr_top)
  if rate:
    st.session_state.amount_top = st.session_state.amount_bot*rate

def currency_change():
  cal_bottom()

# 계산기 기능 함수 만들기
def click_button(val):
  if val == "=":
    try:
      # 수식 계산
      result_value = eval(st.session_state.cal_formula.replace('x','*').replace('%','/'))
      st.session_state.cal_formula = str(result_value)
    except:
      st.session_state.cal_formula = "Error"
  elif val =='C':
    st.session_state.cal_formula = ""
  else:
    st.session_state.cal_formula += str(result_value)

# 2. 웹페이지 화면 구성
st.title("실시간 환율 계산기")

# 자주 사용하는 통화 기호 리스트
currency_list = ["KRW","USD","TWD","EUR","JPY","GBP"]

# 화면을 좌,우(2단)으로 나누기
col1, col2 = st.columns(2)

with col1:
  # 내가 가진 돈(기본값 USD)로 설정
  st.selectbox("기준통화", currency_list, key="curr_top", on_change=currency_change)

with col2:
  # 환전할 금액 열 추가
  st.number_input("", min_value=1.0, key="amount_top", on_change=cal_bottom)

col3, col4 = st.columns(2)

with col3:
  # 목표 통화 설정
  st.selectbox("목표통화", currency_list, key="curr_bot", on_change=currency_change)
    
with col4:
  st.number_input("", key="amount_bot", on_change=cal_top)

# 계산기 UI 만들기
st.subheader("계산기")

# 숫자 입력할 textbox(기호때문에 text로 받음, number로 받으면 오류)
st.text_input("수식입력", value=st.session_state.cal_formula)

# 계산기 button 만들기
button = [
  '7','8','9','%',
  '4','5','6','x',
  '1','2','3','-',
  '0','.','=','+'
]

cols = st.columns(4)
for i, btn in enumerate(button):
  with cols[i%4]:
    if st.button(btn, use_container_width=True):
      click_button(btn)
      
#st.info(f"환전결과:{base_amount:,.2f}{base_currency} → {result:,.2f}{target_currency}")
#st.error("환율 정보를 가져오는데 실패했습니다.")
# 환전 할 금액 입력
# amount = st.number_input("환전할 금액을 입력하세요", min_value=1.0, value=100.0)
