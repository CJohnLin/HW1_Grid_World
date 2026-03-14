# HW1 Grid Map API 與最佳政策推導 (Value Iteration)

這是一個利用 Python (Flask) 作為後端，HTML/CSS/JS (Vanilla) 作為前端所開發的「網格地圖與最佳路徑推導」互動式專案。

## 作業要求與主要功能 (Requirements & Features)

本專案實作了以下三項核心作業需求：

### HW1-1：網格地圖生成與環境設置 (Grid Map Generation)
*   **動態生成參數化地圖**：允許使用者輸入 $N$ 值（範圍 3~10），並動態生成大小為 $N \times N$ 的互動式網格地圖。
*   **自定義狀態位置**：提供使用者透過滑鼠點擊依序設定各類特殊狀態：
    *   **起點 (Start State)**：顯示為綠色。
    *   **終點 (Terminal/Goal State)**：顯示為紅色。
    *   **障礙物 (Obstacles)**：依照地圖大小設定 $N-2$ 個障礙物，顯示為灰色。

### HW1-2：隨機策略評估 (Policy Evaluation - Random Policy)
*   **環境與獎勵設定**：到達目標點給予分數 `+10`，每移動一步給予懲罰 `-1`。撞牆或出界時會「留在原地」並同樣獲得 `-1` 懲罰。衰減因子 (Discount Factor) $\gamma = 0.9$。
*   **疊代收斂計算**：採用完全隨機行動策略（上下左右機率均等），利用貝爾曼方程式持續反覆疊代計算每個狀態的期望價值，直到最大變異量 $\Delta < 10^{-3}$ 判定收斂為止。
*   **結果視覺化**：於前端顯示最終每個格子的狀態價值矩陣 **Value Matrix**（顯示至小數點後兩位），以及該隨機策略的行動矩陣 **Policy Matrix**。

### HW1-3：尋找最佳政策 (Value Iteration - Optimal Policy)
*   **價值疊代演算法**：實作 Value Iteration 演算法，透過最大化期望回報 ($\max_a$) 計算出每個狀態的最佳期望價值函數。
*   **推導最佳策略**：透過計算出的最佳價值矩陣，使用 $\text{argmax}_a$ 萃取出能完美避開障礙物、走向目標點最短路徑的最佳行動策略。
*   **視覺化最佳解**：於前端同步顯示演算法收斂後的 Optimal Value Matrix 與直指最佳路徑的 Optimal Policy Matrix (箭頭方向)。

## 本地端啟動方式
確認系統已安裝 Python 3，並於專案目錄執行下列指令：

```bash
# 1. 安裝相依套件 (Flask, Numpy等)
pip install -r requirements.txt

# 2. 啟動伺服器
python app.py
```
啟動後打開瀏覽器前往 [http://127.0.0.1:5000](http://127.0.0.1:5000) 即可開始使用。

## 線上展示 (Live Demo)
專案已成功部署至 Render，無需安裝即可線上體驗：
🔗 **[點擊前往 HW1 Grid World 線上版](https://hw1-grid-world.onrender.com)**

### 操作說明 (How to Use)
1. **設定網格大小**：在上方輸入框輸入 3~10 之間的數字，點擊「Generate Square」。
2. **依序點選格子**進行地圖配置：
   - **第 1 下**：設定**起點** (顯示為綠色)。
   - **第 2 下**：設定**終點** (顯示為紅色)。
   - **接下來的點擊**：設定此大小相對應數量的**障礙物** (顯示為灰色)。
3. **選擇評估模式**：
   - 點擊「**Evaluate Random Policy**」：觀看系統若採取隨機上下左右移動下的各狀態期望值（多數因撞牆/未達終點而偏低）與隨機方向。
   - 點擊「**Find Optimal Policy**」：觸發價值疊代 (Value Iteration)。系統將根據貝爾曼最佳方程式，推導出每個格子的最高期望回報值，並畫出能避開障礙物、最快抵達終點的正確箭頭路徑。

## 開發過程與 AI 協作紀錄

本專案的程式開發到線上自動化除錯測試，皆為作者與 **Antigravity (AI 助手)** 協同結對程式設計（Pair Programming）完成：
- 若想了解專案的實作過程、除錯歷史、以及最佳政策推導的設計思路與邏輯，可直接查閱根目錄下的 [`log.md`](./log.md)。
