# HW1 Grid Map API 與最佳政策推導 (Value Iteration)

這是一個利用 Python (Flask) 作為後端，HTML/CSS/JS (Vanilla) 作為前端所開發的「網格地圖與最佳路徑推導」互動式專案。

## 主要功能

本專案實作了以下兩項核心作業需求：
1. **網格地圖開發 (Grid Map Generation)**：
    * 允許用戶輸入 $N$ 值（範圍 3~10），並生成動態大小為 $N \times N$ 的互動式網格地圖。
    * 提供使用者依序點擊設定：起點（綠格）、終點（紅格），以及 $N-2$ 個障礙物（灰格）。
2. **策略評估與推導最佳政策**：
    * **Evaluate Random Policy (隨機策略評估)**：顯示每個格子若是「隨機採取上下左右行動」的期望 Value 回報與該隨機 Policy（撞牆/出界會留在原地並扣分）。
    * **Find Optimal Policy (價值疊代算法 - Value Iteration)**：根據馬可夫決策過程 (MDP)，後端利用貝爾曼最佳方程式，以 $\gamma = 0.9$ 收斂逼出一條能**完美避開障礙物並走向目標 (Goal) 的最短最佳路線**。

## 本地端啟動方式
確認系統已安裝 Python 3，並於專案目錄執行下列指令：

```bash
# 1. 安裝相依套件 (Flask, Numpy等)
pip install -r requirements.txt

# 2. 啟動伺服器
python app.py
```
啟動後打開瀏覽器前往 [http://127.0.0.1:5000](http://127.0.0.1:5000) 即可開始使用。

## 部署與線上版
本專案已包含支援 `Render` 與 `Heroku` 部署環境之設定檔：
- `requirements.txt`：聲明執行環境套件。
- `Procfile`：宣告 `web: gunicorn app:app` 作為正式伺服器進入點。

## 開發過程與 AI 協作紀錄

本專案的程式開發到線上自動化除錯測試，皆為作者與 **Antigravity (AI 助手)** 協同結對程式設計（Pair Programming）完成：
- 若想了解專案的實作過程、除錯歷史、以及最佳政策推導的設計思路與邏輯，可直接查閱根目錄下的 [`log.md`](./log.md)。
