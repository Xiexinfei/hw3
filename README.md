# hw3

有四個RPC function，
（橘燈）gesture：在PC輸入讓mbed偵測手勢，決定要用哪個角度
angle：（此command由pyserial傳送）將mbed傳來的角度存起來（因為confirm角度後會reset mbed）
（藍燈）tilt：在PC端輸入讓mbed偵測角度，
resewee：（此command由pyserial傳送）當confirm角度貨超過角度達到一定次數，reset mbed回到RPC loop

螢幕上顯示：
gesture  mode時：MODE = 0，tilt ange : 0/1/2(20/50/70 degree)(根據手勢決定)
tilt mode時：MODE = 1，＿th over!（第幾次超過所選角度）current angle : ＿（現在的角度）

輸入/gesture/run 後進入偵側手勢模式，此function會開一個thread來偵測手勢，主程式會將手勢對應的角度印到uLCD上，並且在interruptin(button)按下之後，回傳現在所選的角度給PC，
PC此時會將此角度存起來，接著reset mbed（以resewee function來reset），再將其角度傳回mbed（以angle function來抓角度），reset mbed後PC可選擇輸入gesture或tilt，
選擇gesture可再偵測一次手勢，選擇角度，選擇tilt則是開始偵測角度，tilt function首先會先重連網路（因為剛剛reset mbed）
接著initialize現在的加速度（led1亮）再開始偵測角度（led2亮）超過所選角度PC會回傳訊息，達一定次數後，再次以resewee reset mbed

（主要是在main.cpp和mqtt_client.py中作修改）
