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
if 'counter_s' not in st.session_state:
    st.session_state.counter_s = 0  # Dead cells

# 제목
st.title("🧬 Cell Counter")

# JavaScript 키보드 감지 코드
js_code = f"""
<div id="keyboardCounter" style="padding: 30px; border: 2px solid #ddd; border-radius: 15px; background-color: #f9f9f9; min-height: 600px; outline: none;" tabindex="0">
    
    <p style="text-align: center; color: #666; margin-bottom: 30px; font-size: 16px;">
        이 영역을 클릭한 후 A (Live) 또는 S (Dead) 키를 누르세요
    </p>
    
    <div style="display: flex; justify-content: space-around; margin: 30px 0;">
        <div style="text-align: center;">
            <h3 style="color: #00b894; margin-bottom: 15px;">🟢 Live Cells (A키)</h3>
            <div id="counterA" style="font-size: 56px; font-weight: bold; color: #00b894; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); min-width: 120px;">0</div>
        </div>
        <div style="text-align: center;">
            <h3 style="color: #e74c3c; margin-bottom: 15px;">🔴 Dead Cells (S키)</h3>
            <div id="counterS" style="font-size: 56px; font-weight: bold; color: #e74c3c; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); min-width: 120px;">0</div>
        </div>
    </div>
    
    <!-- Viability 섹션 -->
    <div style="text-align: center; margin: 30px 0; padding: 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
        <h2 style="margin: 0 0 15px 0;">📊 Cell Viability</h2>
        <div id="viability" style="font-size: 48px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); margin-bottom: 10px;">0.0%</div>
        <div style="font-size: 16px; opacity: 0.9;">
            <span id="totalCells">Total: 0 cells</span>
        </div>
    </div>
    
    <!-- 리셋 버튼들 -->
    <div style="text-align: center; margin: 25px 0;">
        <button onclick="resetCounters()" style="background: #ff7979; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; margin: 8px; font-size: 14px; font-weight: bold;">🔄 전체 리셋</button>
        <button onclick="resetA()" style="background: #00b894; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; margin: 8px; font-size: 14px; font-weight: bold;">🟢 Live 리셋</button>
        <button onclick="resetS()" style="background: #e74c3c; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; margin: 8px; font-size: 14px; font-weight: bold;">🔴 Dead 리셋</button>
    </div>
</div>

<script>
let counterA = {st.session_state.counter_a};
let counterS = {st.session_state.counter_s};
let audioContext = null;

// 오디오 컨텍스트 초기화
function initAudio() {{
    try {{
        if (!audioContext) {{
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }}
        if (audioContext.state === 'suspended') {{
            audioContext.resume();
        }}
    }} catch (e) {{
        console.log('오디오 컨텍스트 초기화 실패:', e);
    }}
}}

// 소리 재생 함수
function playSound(frequency, duration = 200) {{
    try {{
        if (!audioContext) {{
            initAudio();
        }}
        
        if (audioContext && audioContext.state === 'running') {{
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = frequency;
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration / 1000);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration / 1000);
        }}
    }} catch (e) {{
        console.log('소리 재생 실패:', e);
    }}
}}

// A키 소리 (높은 톤)
function playSoundA() {{
    playSound(800, 150);
}}

// S키 소리 (개소리 - 짧은 울음소리)
function playSoundS() {{
    playDogBark();
}}

// 개소리 생성 함수
function playDogBark() {{
    try {{
        if (!audioContext) {{
            initAudio();
        }}
        
        if (audioContext && audioContext.state === 'running') {{
            // 개소리는 여러 주파수의 조합으로 만듦
            const frequencies = [150, 300, 600, 900];
            const duration = 0.3;
            
            frequencies.forEach((freq, index) => {{
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                // 노이즈 효과를 위한 주파수 변조
                oscillator.frequency.setValueAtTime(freq, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(freq * 0.7, audioContext.currentTime + duration);
                
                // 사각파로 거친 소리 만들기
                oscillator.type = index % 2 === 0 ? 'sawtooth' : 'square';
                
                // 볼륨 엔벨로프 (빠른 어택, 빠른 디케이)
                gainNode.gain.setValueAtTime(0, audioContext.currentTime);
                gainNode.gain.linearRampToValueAtTime(0.15, audioContext.currentTime + 0.02);
                gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);
                
                oscillator.start(audioContext.currentTime + index * 0.05);
                oscillator.stop(audioContext.currentTime + duration);
            }});
        }}
    }} catch (e) {{
        console.log('개소리 재생 실패:', e);
    }}
}}

function updateDisplay() {{
    document.getElementById('counterA').textContent = counterA;
    document.getElementById('counterS').textContent = counterS;
    
    // Viability 계산
    const totalCells = counterA + counterS;
    let viability = 0;
    
    if (totalCells > 0) {{
        viability = (counterA / totalCells) * 100;
    }}
    
    document.getElementById('viability').textContent = viability.toFixed(1) + '%';
    document.getElementById('totalCells').textContent = 'Total: ' + totalCells + ' cells';
    
    // Viability에 따른 색상 변경
    const viabilityContainer = document.getElementById('viability').parentElement;
    
    if (viability >= 90) {{
        viabilityContainer.style.background = 'linear-gradient(135deg, #00b894 0%, #55a3ff 100%)';
    }} else if (viability >= 70) {{
        viabilityContainer.style.background = 'linear-gradient(135deg, #fdcb6e 0%, #e17055 100%)';
    }} else if (viability >= 50) {{
        viabilityContainer.style.background = 'linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%)';
    }} else {{
        viabilityContainer.style.background = 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)';
    }}
    
    // Streamlit에 데이터 전송
    try {{
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: {{
                counter_a: counterA,
                counter_s: counterS,
                viability: viability,
                total: totalCells
            }}
        }}, '*');
    }} catch (e) {{
        console.log('데이터 전송 실패:', e);
    }}
}}

function resetCounters() {{
    counterA = 0;
    counterS = 0;
    updateDisplay();
}}

function resetA() {{
    counterA = 0;
    updateDisplay();
}}

function resetS() {{
    counterS = 0;
    updateDisplay();
}}

// 키보드 이벤트 리스너 - 수정된 부분
document.getElementById('keyboardCounter').addEventListener('keydown', function(event) {{
    // 첫 번째 키 입력 시 오디오 컨텍스트 활성화
    if (!audioContext) {{
        initAudio();
    }}
    
    if (event.key === 'a' || event.key === 'A') {{
        counterA++;
        playSoundA();
        updateDisplay();
        event.preventDefault();
    }} else if (event.key === 's' || event.key === 'S') {{
        counterS++;
        playSoundS();
        updateDisplay();
        event.preventDefault();
    }}
}});

// 클릭하면 포커스 설정
document.getElementById('keyboardCounter').addEventListener('click', function() {{
    this.focus();
}});

// 포커스 스타일 추가
document.getElementById('keyboardCounter').addEventListener('focus', function() {{
    this.style.border = '2px solid #007bff';
    this.style.boxShadow = '0 0 10px rgba(0,123,255,0.3)';
}});

document.getElementById('keyboardCounter').addEventListener('blur', function() {{
    this.style.border = '2px solid #ddd';
    this.style.boxShadow = 'none';
}});

// 초기 디스플레이 업데이트
updateDisplay();

// 페이지 로드 시 포커스 설정
setTimeout(function() {{
    document.getElementById('keyboardCounter').focus();
}}, 100);
</script>
"""

# JavaScript 컴포넌트 표시
component_value = components.html(js_code, height=700)

# 카운터 값 업데이트
if component_value and isinstance(component_value, dict):
    if 'counter_a' in component_value:
        st.session_state.counter_a = component_value['counter_a']
    if 'counter_s' in component_value:
        st.session_state.counter_s = component_value['counter_s']

# 사용법 안내
with st.expander("📖 사용법"):
    st.markdown("""
    ### 키보드 셀 카운터 사용법
    
    1. **위의 회색 박스를 클릭**하여 활성화하세요
    2. **A키**를 누르면 Live Cell 카운터가 증가합니다 🟢
    3. **S키**를 누르면 Dead Cell 카운터가 증가합니다 🔴
    4. **Viability**가 실시간으로 계산됩니다: Live / (Live + Dead) × 100
           
    ### 💡 팁
    - 박스가 파란색 테두리로 둘러싸이면 활성화된 상태입니다
    - Viability 색상이 결과에 따라 자동으로 변경됩니다
    - 각 셀 타입별로 다른 소리가 재생됩니다
    - 리셋 버튼으로 개별 또는 전체 카운터를 초기화할 수 있습니다
    """)

# 정보 표시
st.markdown("---")
st.info("SMC 이식외과 - Live: {} cells, Dead: {} cells".format(
    st.session_state.counter_a, 
    st.session_state.counter_s
))
