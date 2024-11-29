function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;

}
function writeRandomNumber() {
    let randomInt = getRandomInt(120000000,3000000000);
    document.getElementById("online_num").innerHTML = "当前在线人数:"+randomInt;  // 将随机整数显示在 HTML 元素中
}
setInterval(writeRandomNumber, 33.3);