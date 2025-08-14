import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="키보드 카운터",
    page_icon="🔢",
    layout="centered"
)

# 세션 상태 초기화
if 'counter_a' not in st.session_state:
    st.session_state.counter_a = 0
if 'counter_f' not in st.session_state:
    st.session_state.counter_f = 0

# 제목
st.title("🔢 키보드 카운터")
st.markdown("---")

# JavaScript 키보드 감지 코드
js_code = """
<div id="keyboardCounter" style="padding: 20px; border: 2px solid #ddd; border-radius: 10px; background-color: #f9f9f9;">
    <h3 style="text-align: center; color: #333;">키보드 입력 감지 영역</h3>
    <p style="text-align: center; color: #666; margin-bottom: 20px;">
        이 영역을 클릭한 후 A 또는 F 키를 누르세요
    </p>
    
    <div style="display: flex; justify-content: space-around; margin: 20px 0;">
        <div style="text-align: center;">
            <h4>카운터 1 (A키)</h4>
            <div id="counterA" style="font-size: 48px; font-weight: bold; color: #ff6b6b; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">0</div>
        </div>
        <div style="text-align: center;">
            <h4>카운터 2 (F키)</h4>
            <div id="counterF" style="font-size: 48px; font-weight: bold; color: #4ecdc4; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">0</div>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 20px;">
        <button onclick="resetCounters()" style="background: #ff7979; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">전체 리셋</button>
        <button onclick="resetA()" style="background: #74b9ff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">카운터 1 리셋</button>
        <button onclick="resetF()" style="background: #00b894; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">카운터 2 리셋</button>
    </div>
    
    <p style="text-align: center; color: #888; margin-top: 20px; font-size: 14px;">
        💡 팁: 이 박스를 클릭한 후 키보드를 사용하세요
    </p>
</div>

<script>
let counterA = 0;
let counterF = 0;

// Streamlit 세션 상태에서 초기값 가져오기
if (window.parent && window.parent.document) {
    const streamlitData = window.parent.document.querySelector('[data-testid="stApp"]');
    if (streamlitData) {
        counterA = """ + str(st.session_state.counter_a) + """;
        counterF = """ + str(st.session_state.counter_f) + """;
    }
}

function updateDisplay() {
    document.getElementById('counterA').textContent = counterA;
    document.getElementById('counterF').textContent = counterF;
    
    // Streamlit에 데이터 전송
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: {
            counter_a: counterA,
            counter_f: counterF
        }
    }, '*');
}

function resetCounters() {
    counterA = 0;
    counterF = 0;
    updateDisplay();
}

function resetA() {
    counterA = 0;
    updateDisplay();
}

function resetF() {
    counterF = 0;
    updateDisplay();
}

// 키보드 이벤트 리스너
document.getElementById('keyboardCounter').addEventListener('keydown', function(event) {
    if (event.key === 'a' || event.key === 'A') {
        counterA++;
        updateDisplay();
        event.preventDefault();
    } else if (event.key === 'f' || event.key === 'F') {
        counterF++;
        updateDisplay();
        event.preventDefault();
    }
});

// 클릭하면 포커스 설정
document.getElementById('keyboardCounter').addEventListener('click', function() {
    this.focus();
});

// 포커스 가능하게 만들기
document.getElementById('keyboardCounter').setAttribute('tabindex', '0');

// 초기 디스플레이 업데이트
updateDisplay();

// 페이지 로드 시 포커스 설정
window.addEventListener('load', function() {
    document.getElementById('keyboardCounter').focus();
});
</script>
"""

# JavaScript 컴포넌트 표시
component_value = components.html(js_code, height=400)

# 카운터 값 업데이트 (JavaScript에서 받은 데이터)
if component_value and isinstance(component_value, dict):
    if 'counter_a' in component_value:
        st.session_state.counter_a = component_value['counter_a']
    if 'counter_f' in component_value:
        st.session_state.counter_f = component_value['counter_f']

# 현재 상태 표시 (백업용)
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="카운터 1 (A키)", 
        value=st.session_state.counter_a,
        help="A 키를 누르면 증가합니다"
    )
    if st.button("카운터 1 리셋", key="reset_a"):
        st.session_state.counter_a = 0
        st.rerun()

with col2:
    st.metric(
        label="카운터 2 (F키)", 
        value=st.session_state.counter_f,
        help="F 키를 누르면 증가합니다"
    )
    if st.button("카운터 2 리셋", key="reset_f"):
        st.session_state.counter_f = 0
        st.rerun()

# 전체 리셋 버튼
if st.button("🔄 전체 리셋", type="primary"):
    st.session_state.counter_a = 0
    st.session_state.counter_f = 0
    st.rerun()

# 사용법 안내
st.markdown("---")
with st.expander("📖 사용법"):
    st.markdown("""
    ### 키보드 카운터 사용법
    
    1. **위의 회색 박스를 클릭**하여 활성화하세요
    2. **A키**를 누르면 카운터 1이 증가합니다
    3. **F키**를 누르면 카운터 2가 증가합니다
    4. 각각의 리셋 버튼으로 카운터를 초기화할 수 있습니다
    
    ### 💡 팁
    - 박스가 파란색 테두리로 둘러싸이면 활성화된 상태입니다
    - 다른 곳을 클릭하면 비활성화되므로 다시 박스를 클릭하세요
    - 카운터는 실시간으로 업데이트됩니다
    """)

# 정보 표시
st.markdown("---")
st.info("🔢 현재 상태 - A키 카운터: {} | F키 카운터: {}".format(
    st.session_state.counter_a, 
    st.session_state.counter_f
))
