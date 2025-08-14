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
    st.session_state.counter_a = 0  # Live cells
if 'counter_f' not in st.session_state:
    st.session_state.counter_f = 0  # Dead cells

# 제목
st.title("🧬 Cell Counter & Viability Calculator")

# JavaScript 키보드 감지 코드
js_code = """
<div id="keyboardCounter" style="padding: 20px; border: 2px solid #ddd; border-radius: 10px; background-color: #f9f9f9;">
    <h3 style="text-align: center; color: #333;">Cell Counter</h3>
    <p style="text-align: center; color: #666; margin-bottom: 20px;">
        이 영역을 클릭한 후 A (Live) 또는 F (Dead) 키를 누르세요
    </p>
    
    <div style="display: flex; justify-content: space-around; margin: 20px 0;">
        <div style="text-align: center;">
            <h4>🟢 Live Cells (A키)</h4>
            <div id="counterA" style="font-size: 48px; font-weight: bold; color: #00b894; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">0</div>
        </div>
        <div style="text-align: center;">
            <h4>🔴 Dead Cells (F키)</h4>
            <div id="counterF" style="font-size: 48px; font-weight: bold; color: #e74c3c; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">0</div>
        </div>
    </div>
    
    <!-- Viability 섹션 추가 -->
    <div style="text-align: center; margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
        <h3 style="margin: 0 0 10px 0;">📊 Cell Viability</h3>
        <div id="viability" style="font-size: 36px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">0.0%</div>
        <div style="font-size: 14px; margin-top: 5px; opacity: 0.9;">
            <span id="totalCells">Total: 0 cells</span>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 20px;">
        <button onclick="resetCounters()" style="background: #ff7979; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">전체 리셋</button>
        <button onclick="resetA()" style="background: #00b894; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">Live 리셋</button>
        <button onclick="resetF()" style="background: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">Dead 리셋</button>
    </div>
    
    <div style="text-align: center; margin: 15px 0;">
        <button onclick="playSoundA()" style="background: #fd79a8; color: white; padding: 8px 16px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 12px;">🔊 Live 소리</button>
        <button onclick="playSoundF()" style="background: #fdcb6e; color: white; padding: 8px 16px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 12px;">🔊 Dead 소리</button>
    </div>
    
    <p style="text-align: center; color: #888; margin-top: 20px; font-size: 14px;">
        💡 팁: 이 박스를 클릭한 후 키보드를 사용하세요<br>
        🔊 A키: Live cell (높은음) | F키: Dead cell (낮은음)
    </p>
</div>

<script>
let counterA = 0;
let counterF = 0;
let audioContext = null;

// 오디오 컨텍스트 초기화
function initAudio() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
}

// 소리 재생 함수
function playSound(frequency, duration = 200) {
    if (!audioContext) {
        initAudio();
    }
    
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = frequency;
    oscillator.type = 'sine';
    
    // 볼륨 조절 (페이드 아웃 효과)
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration / 1000);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + duration / 1000);
}

// A키 소리 (높은 톤)
function playSoundA() {
    playSound(800, 150); // 800Hz, 150ms
}

// F키 소리 (낮은 톤)
function playSoundF() {
    playSound(400, 150); // 400Hz, 150ms
}

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
    
    // Viability 계산 (Live / (Live + Dead) * 100)
    const totalCells = counterA + counterF;
    let viability = 0;
    
    if (totalCells > 0) {
        viability = (counterA / totalCells) * 100;
    }
    
    // Viability 표시 업데이트
    document.getElementById('viability').textContent = viability.toFixed(1) + '%';
    document.getElementById('totalCells').textContent = 'Total: ' + totalCells + ' cells';
    
    // Viability에 따른 색상 변경
    const viabilityElement = document.getElementById('viability');
    const viabilityContainer = viabilityElement.parentElement;
    
    if (viability >= 90) {
        viabilityContainer.style.background = 'linear-gradient(135deg, #00b894 0%, #55a3ff 100%)'; // 매우 좋음 - 녹색/파랑
    } else if (viability >= 70) {
        viabilityContainer.style.background = 'linear-gradient(135deg, #fdcb6e 0%, #e17055 100%)'; // 좋음 - 노랑/주황
    } else if (viability >= 50) {
        viabilityContainer.style.background = 'linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%)'; // 보통 - 분홍/노랑
    } else {
        viabilityContainer.style.background = 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)'; // 나쁨 - 빨강
    }
    
    // Streamlit에 데이터 전송
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: {
            counter_a: counterA,
            counter_f: counterF,
            viability: viability,
            total: totalCells
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
    // 첫 번째 키 입력 시 오디오 컨텍스트 활성화
    if (!audioContext) {
        initAudio();
    }
    
    if (event.key === 'a' || event.key === 'A') {
        counterA++;
        playSoundA(); // A키 소리
        updateDisplay();
        event.preventDefault();
    } else if (event.key === 'f' || event.key === 'F') {
        counterF++;
        playSoundF(); // F키 소리
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

# 실시간 통계 표시
total_cells = st.session_state.counter_a + st.session_state.counter_f
if total_cells > 0:
    viability = (st.session_state.counter_a / total_cells) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🟢 Live Cells", st.session_state.counter_a)
    with col2:
        st.metric("🔴 Dead Cells", st.session_state.counter_f)  
    with col3:
        st.metric("📊 Viability", f"{viability:.1f}%")
        
    # 생존율에 따른 상태 메시지
    if viability >= 90:
        st.success(f"🎉 Excellent viability! ({viability:.1f}%)")
    elif viability >= 70:
        st.info(f"👍 Good viability ({viability:.1f}%)")
    elif viability >= 50:
        st.warning(f"⚠️ Moderate viability ({viability:.1f}%)")
    else:
        st.error(f"❌ Low viability ({viability:.1f}%)")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🟢 Live Cells", 0)
    with col2:
        st.metric("🔴 Dead Cells", 0)
    with col3:
        st.metric("📊 Viability", "0.0%")

# 간단한 상태 표시만 유지

# 사용법 안내
with st.expander("📖 사용법"):
    st.markdown("""
    ### 키보드 셀 카운터 사용법
    
    1. **위의 회색 박스를 클릭**하여 활성화하세요
    2. **A키**를 누르면 Live Cell 카운터가 증가합니다 🟢
    3. **F키**를 누르면 Dead Cell 카운터가 증가합니다 🔴
    4. **Viability**가 실시간으로 계산됩니다: Live / (Live + Dead) × 100
    
    ### 🧬 Cell Viability 해석
    - **90% 이상**: 🎉 Excellent (매우 우수)
    - **70-89%**: 👍 Good (양호)  
    - **50-69%**: ⚠️ Moderate (보통)
    - **50% 미만**: ❌ Low (낮음)
    
    ### 💡 팁
    - 박스가 파란색 테두리로 둘러싸이면 활성화된 상태입니다
    - Viability 색상이 결과에 따라 자동으로 변경됩니다
    - 각 셀 타입별로 다른 소리가 재생됩니다
    - 리셋 버튼으로 개별 또는 전체 카운터를 초기화할 수 있습니다
    """)

# 정보 표시
st.markdown("---")
st.info("🔢 현재 상태 - A키 카운터: {} | F키 카운터: {}".format(
    st.session_state.counter_a, 
    st.session_state.counter_f
))
